import paramiko

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


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=30)
    print("Connected!")

    try:
        print("\n=== Check alembic versions ===")
        run_cmd(client, f"ls -la {REMOTE_BACKEND}/alembic/versions/")

        print("\n=== Generate initial migration ===")
        e, out = run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic revision --autogenerate -m 'initial' 2>&1")
        if e != 0:
            print("Autogenerate failed, trying direct table creation...")
            run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -c \"from app.db.base import Base; from app.db.models import *; from app.db.session import engine; Base.metadata.create_all(engine); print('Tables created!')\" 2>&1")
        else:
            print("\n=== Apply migration ===")
            run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic upgrade head 2>&1")
            run_cmd(client, f"cd {REMOTE_BACKEND} && PYTHONPATH=. python3 -m alembic current 2>&1")

        print("\n=== Verify tables ===")
        run_cmd(client, "PGPASSWORD=aiflow2026 psql -h 127.0.0.1 -U auto_ai_flow -d auto_ai_flow -c '\\dt' 2>&1")

        print("\n=== DONE ===")

    finally:
        client.close()


if __name__ == "__main__":
    main()
