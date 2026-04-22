import paramiko

HOST = "172.18.14.8"
USER = "chat"
PASSWORD = "chat886"


def run_cmd(client, cmd, timeout=30):
    print(f">>> {cmd[:200]}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    exit_code = stdout.channel.recv_exit_status()
    combined = out + err
    print(combined.strip()[:2000])
    return exit_code, combined


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=30)
    print("Connected!")

    try:
        run_cmd(client, "ps aux | grep 'pip3 install' | grep -v grep | wc -l")
        run_cmd(client, "tail -20 ~/pip_install.log")
        run_cmd(client, "python3 -c 'import fastapi; print(fastapi.__version__)' 2>&1")
        run_cmd(client, "python3 -c 'import sqlalchemy; print(sqlalchemy.__version__)' 2>&1")
        run_cmd(client, "python3 -c 'import alembic; print(alembic.__version__)' 2>&1")
    finally:
        client.close()


if __name__ == "__main__":
    main()
