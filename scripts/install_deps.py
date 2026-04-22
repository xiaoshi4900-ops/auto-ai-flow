import paramiko
import time

HOST = "172.18.14.8"
USER = "chat"
PASSWORD = "chat886"


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
    client.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=30)
    print("Connected!")

    try:
        print("\n=== Kill stuck pip processes ===")
        run_cmd(client, "pkill -f 'pip3 install' 2>/dev/null; echo killed")
        time.sleep(2)

        print("\n=== Install core deps first (no langchain) ===")
        run_cmd(client, "pip3 install --user fastapi==0.110.0 'uvicorn[standard]==0.29.0' sqlalchemy==2.0.29 'psycopg[binary]==3.1.18' alembic==1.13.1 pydantic==2.6.3 pydantic-settings==2.2.1 'python-jose[cryptography]==3.3.0' 'passlib[bcrypt]==1.7.4' python-multipart==0.0.9 'celery[redis]==5.3.6' redis==5.0.1 httpx==0.27.0 2>&1 | tail -5", timeout=600)

        print("\n=== Verify core deps ===")
        run_cmd(client, "python3 -c 'import fastapi; print(\"fastapi\", fastapi.__version__)'")
        run_cmd(client, "python3 -c 'import alembic; print(\"alembic\", alembic.__version__)'")
        run_cmd(client, "python3 -c 'import celery; print(\"celery\", celery.__version__)'")
        run_cmd(client, "python3 -c 'import psycopg; print(\"psycopg\", psycopg.__version__)'")

        print("\n=== Install langchain separately ===")
        run_cmd(client, "pip3 install --user langchain==0.1.13 langchain-openai==0.0.8 langchain-community==0.0.20 2>&1 | tail -5", timeout=600)

        print("\n=== Verify langchain ===")
        run_cmd(client, "python3 -c 'import langchain; print(\"langchain\", langchain.__version__)'")

        print("\n=== DONE ===")

    finally:
        client.close()


if __name__ == "__main__":
    main()
