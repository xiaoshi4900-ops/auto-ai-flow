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
    print(f"Connecting to {HOST}...")
    client.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=30)
    print("Connected!")

    try:
        print("\n=== Fix pg_hba.conf ===")
        sudo_cmd(client, "bash -c 'cat /etc/postgresql/*/main/pg_hba.conf | head -20'")

        print("\n=== Reset pg_hba.conf to allow local peer auth ===")
        sudo_cmd(client, "bash -c \"sed -i 's/host all all 0.0.0.0\\/0 md5/host all all 0.0.0.0\\/0 md5/' /etc/postgresql/*/main/pg_hba.conf\"")
        sudo_cmd(client, "bash -c \"sed -i 's/^local   all             all                                     md5/local   all             all                                     peer/' /etc/postgresql/*/main/pg_hba.conf\"")
        sudo_cmd(client, "bash -c \"sed -i 's/^local   all             all                                     scram-sha-256/local   all             all                                     peer/' /etc/postgresql/*/main/pg_hba.conf\"")

        print("\n=== Restart PostgreSQL ===")
        sudo_cmd(client, "systemctl restart postgresql")
        time.sleep(3)

        print("\n=== Verify pg_hba.conf ===")
        sudo_cmd(client, "bash -c 'cat /etc/postgresql/*/main/pg_hba.conf | grep -v \"^#\" | grep -v \"^$\"'")

        print("\n=== Create DB and user ===")
        sudo_cmd(client, "-u postgres psql -c \"CREATE USER auto_ai_flow WITH PASSWORD 'aiflow2026';\" 2>/dev/null; echo USER_DONE")
        sudo_cmd(client, "-u postgres psql -c \"CREATE DATABASE auto_ai_flow OWNER auto_ai_flow ENCODING 'UTF8';\" 2>/dev/null; echo DB_DONE")
        sudo_cmd(client, "-u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE auto_ai_flow TO auto_ai_flow;\"")
        sudo_cmd(client, "-u postgres psql -c \"ALTER DATABASE auto_ai_flow OWNER TO auto_ai_flow;\"")
        sudo_cmd(client, "-u postgres psql -l | grep auto_ai_flow")

        print("\n=== Grant schema permissions ===")
        sudo_cmd(client, "-u postgres psql -d auto_ai_flow -c \"GRANT ALL ON SCHEMA public TO auto_ai_flow;\"")
        sudo_cmd(client, "-u postgres psql -d auto_ai_flow -c \"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO auto_ai_flow;\"")
        sudo_cmd(client, "-u postgres psql -d auto_ai_flow -c \"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO auto_ai_flow;\"")

        print("\n=== Test connection ===")
        run_cmd(client, "PGPASSWORD=aiflow2026 psql -h 127.0.0.1 -U auto_ai_flow -d auto_ai_flow -c 'SELECT 1;' 2>&1")

        print("\n=== DONE ===")

    finally:
        client.close()


if __name__ == "__main__":
    main()
