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


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=30)
    print("Connected!")

    try:
        print("\n=== Force upgrade pydantic and reinstall langchain ===")
        run_cmd(client, "pip3 install --user --force-reinstall pydantic==2.6.3 pydantic-core==2.16.3 pydantic-settings==2.2.1 2>&1 | tail -5", timeout=300)
        run_cmd(client, "pip3 install --user --force-reinstall langchain>=0.1.0 langchain-core>=0.1.0 langchain-openai>=0.0.8 langchain-community>=0.0.20 2>&1 | tail -5", timeout=600)

        print("\n=== Verify all deps ===")
        run_cmd(client, "python3 -c 'import pydantic; print(\"pydantic\", pydantic.__version__)'")
        run_cmd(client, "python3 -c 'import fastapi; print(\"fastapi\", fastapi.__version__)'")
        run_cmd(client, "python3 -c 'import alembic; print(\"alembic\", alembic.__version__)'")
        run_cmd(client, "python3 -c 'import celery; print(\"celery\", celery.__version__)'")
        run_cmd(client, "python3 -c 'import langchain_core; print(\"langchain_core\", langchain_core.__version__)'")
        run_cmd(client, "python3 -c 'import langchain_openai; print(\"langchain_openai ok\")'")

        print("\n=== DONE ===")

    finally:
        client.close()


if __name__ == "__main__":
    main()
