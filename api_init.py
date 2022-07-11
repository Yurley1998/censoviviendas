import subprocess
cmd = ["uvicorn", "app:app"]
subprocess.Popen(cmd, close_fds=True)
