import paramiko
import os
import stat
import time

HOST = "172.18.14.8"
USER = "chat"
PASSWORD = "chat886"
REMOTE_FRONTEND = "/home/chat/AutoAiFlow/frontend"


def run_cmd(client, cmd, timeout=300):
    print(f"\n>>> {cmd[:200]}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    exit_code = stdout.channel.recv_exit_status()
    combined = out + err
    print(combined.strip()[:3000])
    return exit_code, combined


def upload_dir(sftp, local_dir, remote_dir):
    try:
        sftp.stat(remote_dir)
    except FileNotFoundError:
        sftp.mkdir(remote_dir)

    for item in os.listdir(local_dir):
        lp = os.path.join(local_dir, item)
        rp = f"{remote_dir}/{item}"
        if os.path.isfile(lp):
            try:
                sftp.put(lp, rp)
                print(f"  + {rp}")
            except Exception as e:
                print(f"  SKIP {rp}: {e}")
        elif os.path.isdir(lp):
            if item in ('node_modules', '.git', '__pycache__', '.vscode'):
                continue
            upload_dir(sftp, lp, rp)


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=30)
    print("Connected!")
    sftp = client.open_sftp()

    try:
        print("\n=== Upload frontend dist ===")
        local_dist = r"c:\workspace\AutoAiFlow\frontend\dist"
        run_cmd(client, f"rm -rf {REMOTE_FRONTEND}")
        run_cmd(client, f"mkdir -p {REMOTE_FRONTEND}")
        upload_dir(sftp, local_dist, f"{REMOTE_FRONTEND}/dist")
        print("Frontend dist uploaded!")

        print("\n=== Install nginx ===")
        e, _ = run_cmd(client, "which nginx 2>/dev/null")
        if e != 0:
            run_cmd(client, f"echo '{PASSWORD}' | sudo -S apt-get update -qq && echo '{PASSWORD}' | sudo -S apt-get install -y nginx 2>&1 | tail -5", timeout=300)

        print("\n=== Configure nginx ===")
        nginx_conf = """server {
    listen 80;
    server_name _;

    root /home/chat/AutoAiFlow/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000;
    }
}"""
        with sftp.file("/tmp/aiflow_nginx.conf", "w") as f:
            f.write(nginx_conf)
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S cp /tmp/aiflow_nginx.conf /etc/nginx/sites-available/aiflow 2>&1")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S ln -sf /etc/nginx/sites-available/aiflow /etc/nginx/sites-enabled/aiflow 2>&1")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S rm -f /etc/nginx/sites-enabled/default 2>&1")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S nginx -t 2>&1")
        run_cmd(client, f"echo '{PASSWORD}' | sudo -S systemctl restart nginx 2>&1")

        print("\n=== Verify nginx ===")
        time.sleep(2)
        run_cmd(client, "curl -sf http://localhost/ | head -5 2>&1")

        print("\n=== ALL DONE ===")

    finally:
        sftp.close()
        client.close()


if __name__ == "__main__":
    main()
