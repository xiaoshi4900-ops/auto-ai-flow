import paramiko
import time

HOST = "172.18.14.8"
USER = "chat"
PASSWORD = "chat886"
REMOTE_BACKEND = "/home/chat/AutoAiFlow/backend"


def run_cmd(client, cmd, timeout=300):
    print(f"\n>>> {cmd[:200]}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    exit_code = stdout.channel.recv_exit_status()
    combined = out + err
    print(combined.strip()[:3000])
    return exit_code, combined


def sudo_cmd(client, cmd, timeout=120):
    full = f"echo '{PASSWORD}' | sudo -S {cmd} 2>&1"
    return run_cmd(client, full, timeout)


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {HOST}...")
    client.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=30)
    print("Connected!")

    try:
        print("\n=== Install Python deps (background) ===")
        run_cmd(client, "nohup pip3 install --user fastapi 'uvicorn[standard]' sqlalchemy 'psycopg[binary]' alembic pydantic pydantic-settings 'python-jose[cryptography]' 'passlib[bcrypt]' python-multipart 'celery[redis]' redis httpx langchain langchain-openai langchain-community > ~/pip_install.log 2>&1 & echo $!")

        print("\n=== Waiting for pip install to complete ===")
        for i in range(60):
            time.sleep(10)
            e, out = run_cmd(client, "ps aux | grep 'pip3 install' | grep -v grep | wc -l", timeout=30)
            if "0" in out.strip():
                print("pip install completed!")
                break
            print(f"  Still running... ({(i+1)*10}s)")

        run_cmd(client, "tail -10 ~/pip_install.log")

        print("\n=== Upload backend code ===")
        import os
        sftp = client.open_sftp()
        run_cmd(client, f"rm -rf {REMOTE_BACKEND}")
        run_cmd(client, f"mkdir -p {REMOTE_BACKEND}")

        local_backend = r"c:\workspace\AutoAiFlow\backend"

        def upload_dir(ld, rd):
            try:
                sftp.stat(rd)
            except FileNotFoundError:
                sftp.mkdir(rd)
            for item in os.listdir(ld):
                lp = os.path.join(ld, item)
                rp = f"{rd}/{item}"
                if os.path.isfile(lp):
                    if item.endswith(('.pyc', '.pyo')) or '__pycache__' in lp:
                        continue
                    try:
                        sftp.put(lp, rp)
                    except Exception as e:
                        print(f"  SKIP {rp}: {e}")
                elif os.path.isdir(lp):
                    if item in ('__pycache__', '.git', 'node_modules', '.venv', 'dist', '.ruff_cache', '.eggs', 'auto_ai_flow_backend.egg-info'):
                        continue
                    upload_dir(lp, rp)

        upload_dir(local_backend, REMOTE_BACKEND)
        print("Upload complete")

        env_content = """APP_NAME=AutoAiFlow
APP_ENV=dev
APP_DEBUG=true
DATABASE_URL=postgresql+psycopg://auto_ai_flow:aiflow2026@127.0.0.1:5432/auto_ai_flow
REDIS_URL=redis://127.0.0.1:6379/0
JWT_SECRET=dev-secret-change-in-production-2026
JWT_EXPIRE_MINUTES=120
JWT_REFRESH_EXPIRE_DAYS=7
DEFAULT_TIMEOUT_SEC=300
OPENAI_API_KEY=
"""
        with sftp.file(f"{REMOTE_BACKEND}/.env", "w") as f:
            f.write(env_content)
        print("  + .env uploaded")
        sftp.close()

        print("\n=== Alembic migration ===")
        e, out = run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic upgrade head 2>&1")
        if e != 0:
            print("Migration failed, trying autogenerate...")
            run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic revision --autogenerate -m 'initial' 2>&1")
            run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic upgrade head 2>&1")
        run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic current 2>&1")

        print("\n=== Seed data ===")
        run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -c 'from app.db.seed import seed_all; seed_all()' 2>&1")

        print("\n=== Start backend ===")
        run_cmd(client, "pkill -f 'uvicorn app.main' 2>/dev/null; echo killed")
        time.sleep(1)
        run_cmd(client, f"cd {REMOTE_BACKEND} && nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > ~/backend.log 2>&1 & echo started")
        time.sleep(5)
        run_cmd(client, "curl -sf http://localhost:8000/healthz 2>/dev/null || (echo 'Backend not ready, logs:'; tail -30 ~/backend.log)")

        print("\n=== Start Celery worker ===")
        run_cmd(client, "pkill -f 'celery.*app.tasks' 2>/dev/null; echo killed")
        time.sleep(1)
        run_cmd(client, f"cd {REMOTE_BACKEND} && nohup python3 -m celery -A app.tasks.celery_app:celery_app worker --loglevel=info --concurrency=2 > ~/worker.log 2>&1 & echo started")

        print("\n=== ALL DONE ===")

    finally:
        client.close()


if __name__ == "__main__":
    main()
