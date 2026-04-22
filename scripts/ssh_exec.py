import paramiko
import sys
import os

HOST = '172.18.14.8'
PORT = 22
USER = 'chat'
PASSWORD = 'chat886'

def get_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=10)
    return client

def ssh_exec(command, timeout=120):
    client = get_client()
    try:
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        exit_code = stdout.channel.recv_exit_status()
        if out:
            print(out)
        if err:
            print(err, file=sys.stderr)
        return exit_code
    finally:
        client.close()

def ssh_exec_sudo(command, timeout=120):
    full_cmd = f"echo '{PASSWORD}' | sudo -S bash -c '{command}'"
    return ssh_exec(full_cmd, timeout)

def ssh_upload_script(local_path, remote_path):
    client = get_client()
    try:
        sftp = client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
    finally:
        client.close()

if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else 'exec'
    if action == 'exec':
        cmd = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'echo hello'
        sys.exit(ssh_exec(cmd))
    elif action == 'sudo':
        cmd = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'echo hello'
        sys.exit(ssh_exec_sudo(cmd))
    elif action == 'upload':
        local = sys.argv[2]
        remote = sys.argv[3]
        ssh_upload_script(local, remote)
        print(f"Uploaded {local} -> {remote}")
