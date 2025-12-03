import os
import subprocess

def run_command(user_input):
    """VULN: PY005 - Command injection via os.system"""
    os.system("ls " + user_input)

def execute_shell(filename):
    """VULN: PY005 - Shell command with user input"""
    os.system(f"cat {filename}")

def backup_file(path):
    """VULN: PY005 - subprocess with shell=True"""
    subprocess.call("cp " + path + " /backup/", shell=True)
