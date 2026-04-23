import paramiko
import time
import os
import sys

HOST = "172.18.14.8"
USER = "chat"
PASSWORD = "chat886"
REMOTE_BACKEND = "/home/chat/AutoAiFlow/backend"

STEP = sys.argv[1] if len(sys.argv) > 1 else "all"


def run_cmd(client: paramiko.SSHClient, cmd: str, timeout: int = 300) -> tuple[int, str]:
    print(f"\n>>> {cmd[:200]}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    exit_code = stdout.channel.recv_exit_status()
    combined = out + err
    print(combined.strip()[:3000])
    return exit_code, combined


def sudo_cmd(client: paramiko.SSHClient, cmd: str, timeout: int = 120) -> tuple[int, str]:
    full = f"echo '{PASSWORD}' | sudo -S {cmd} 2>&1"
    return run_cmd(client, full, timeout)


def get_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {HOST}...")
    client.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=30)
    print("Connected!")
    return client


def step_check(client):
    print("\n=== Check environment ===")
    run_cmd(client, "cat /etc/os-release | head -2")
    run_cmd(client, "pg_isready")
    run_cmd(client, "redis-cli ping")
    run_cmd(client, "python3 --version")
    run_cmd(client, "node --version")


def step_pg_config(client):
    print("\n=== Configure PostgreSQL ===")
    sudo_cmd(client, "sed -i \"s/#listen_addresses = 'localhost'/listen_addresses = '*' /\" /etc/postgresql/*/main/postgresql.conf")
    sudo_cmd(client, "bash -c 'echo \"host all all 0.0.0.0/0 md5\" >> /etc/postgresql/*/main/pg_hba.conf'")
    sudo_cmd(client, "systemctl restart postgresql")
    time.sleep(3)
    run_cmd(client, "pg_isready")


def step_create_db(client):
    print("\n=== Create DB and user ===")
    sudo_cmd(client, "-u postgres psql -c \"CREATE USER auto_ai_flow WITH PASSWORD 'aiflow2026';\" 2>/dev/null; echo USER_DONE")
    sudo_cmd(client, "-u postgres psql -c \"CREATE DATABASE auto_ai_flow OWNER auto_ai_flow ENCODING 'UTF8';\" 2>/dev/null; echo DB_DONE")
    sudo_cmd(client, "-u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE auto_ai_flow TO auto_ai_flow;\"")
    sudo_cmd(client, "-u postgres psql -c \"ALTER DATABASE auto_ai_flow OWNER TO auto_ai_flow;\"")
    sudo_cmd(client, "-u postgres psql -l | grep auto_ai_flow")


def step_install_deps(client):
    print("\n=== Install Python deps ===")
    run_cmd(client, "pip3 install --user fastapi 'uvicorn[standard]' sqlalchemy 'psycopg[binary]' alembic pydantic pydantic-settings 'python-jose[cryptography]' 'passlib[bcrypt]' python-multipart 'celery[redis]' redis httpx openai 2>&1 | tail -5", timeout=600)


def step_upload(client):
    print("\n=== Upload backend code ===")
    sftp = client.open_sftp()
    run_cmd(client, f"rm -rf {REMOTE_BACKEND}")
    run_cmd(client, f"mkdir -p {REMOTE_BACKEND}")

    local_backend = r"c:\workspace\AutoAiFlow\backend"

    def upload_dir(ld: str, rd: str):
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


def step_migrate(client):
    print("\n=== Alembic migration ===")
    e, out = run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic upgrade head 2>&1")
    if e != 0:
        print("Migration failed, trying autogenerate...")
        run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic revision --autogenerate -m 'initial' 2>&1")
        run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic upgrade head 2>&1")
    run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic current 2>&1")


def step_seed(client):
    print("\n=== Seed data ===")
    run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -c 'from app.db.seed import seed_all; seed_all()' 2>&1")


def step_start_backend(client):
    print("\n=== Start backend ===")
    run_cmd(client, "pkill -f 'uvicorn app.main' 2>/dev/null; echo killed")
    time.sleep(1)
    run_cmd(client, f"cd {REMOTE_BACKEND} && nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > ~/backend.log 2>&1 & echo started")
    time.sleep(5)
    run_cmd(client, "curl -sf http://localhost:8000/healthz 2>/dev/null || (echo 'Backend not ready, logs:'; tail -30 ~/backend.log)")


def step_start_worker(client):
    print("\n=== Start Celery worker ===")
    run_cmd(client, "pkill -f 'celery.*app.tasks' 2>/dev/null; echo killed")
    time.sleep(1)
    run_cmd(client, f"cd {REMOTE_BACKEND} && nohup python3 -m celery -A app.tasks.celery_app:celery_app worker --loglevel=info --concurrency=2 > ~/worker.log 2>&1 & echo started")


STEPS = {
    "check": step_check,
    "pg_config": step_pg_config,
    "create_db": step_create_db,
    "install_deps": step_install_deps,
    "upload": step_upload,
    "migrate": step_migrate,
    "seed": step_seed,
    "start_backend": step_start_backend,
    "start_worker": step_start_worker,
}

STEP_ORDER = ["check", "pg_config", "create_db", "install_deps", "upload", "migrate", "seed", "start_backend", "start_worker"]


def main():
    client = get_client()
    try:
        if STEP == "all":
            for name in STEP_ORDER:
                STEPS[name](client)
        elif STEP in STEPS:
            STEPS[STEP](client)
        else:
            print(f"Unknown step: {STEP}. Available: {', '.join(STEP_ORDER)}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
