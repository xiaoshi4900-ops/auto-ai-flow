import paramiko

HOST = "172.18.14.8"
USER = "chat"
PASSWORD = "chat886"


def run_cmd(client, cmd, timeout=30):
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
        print("\n=== Check nginx error log ===")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S tail -20 /var/log/nginx/error.log 2>&1")

        print("\n=== Check file permissions ===")
        run_cmd(client, "ls -la /home/chat/AutoAiFlow/frontend/dist/ | head -10")
        run_cmd(client, "namei -l /home/chat/AutoAiFlow/frontend/dist/index.html 2>&1 | head -10")

        print("\n=== Fix permissions ===")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S chmod -R 755 /home/chat/AutoAiFlow/frontend/dist 2>&1")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S chmod 755 /home/chat 2>&1")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S chmod 755 /home/chat/AutoAiFlow 2>&1")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S chmod 755 /home/chat/AutoAiFlow/frontend 2>&1")

        print("\n=== Test again ===")
        run_cmd(client, "curl -sf http://localhost/ | head -5 2>&1")
        run_cmd(client, "curl -sf http://localhost/api/v1/skills 2>&1 | head -3")

        print("\n=== DONE ===")

    finally:
        client.close()


if __name__ == "__main__":
    main()
