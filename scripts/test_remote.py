import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('172.18.14.8', port=22, username='chat', password='chat886', timeout=10)

cmd = "PGPASSWORD=aiflow2026 psql -h 127.0.0.1 -U auto_ai_flow -d auto_ai_flow -c 'SELECT current_database(), current_user, version();'"
stdin, stdout, stderr = client.exec_command(cmd, timeout=30)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("STDOUT:", out)
print("STDERR:", err)
print("EXIT:", stdout.channel.recv_exit_status())

cmd2 = "redis-cli ping"
stdin, stdout, stderr = client.exec_command(cmd2, timeout=10)
out2 = stdout.read().decode('utf-8', errors='replace')
print("Redis:", out2)

client.close()
