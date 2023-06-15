import ctypes
import subprocess
import sys


def run_as_admin(command):
    if sys.platform != 'win32':
        raise OSError('This function is only available on Windows.')

    try:
        # Check if the script is already running as administrator
        return ctypes.windll.shell32.IsUserAnAdmin()

    except AttributeError:
        raise OSError('Failed to check administrator privileges.')

    if not ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1):
        raise OSError('Failed to elevate privileges.')


def execute_command_as_admin(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f'Command execution failed: {e}')
        sys.exit(1)


# Command to be executed with administrator privileges
command_to_execute = "slmgr -rearm"

# Prompting for administrator privileges if not already running as administrator
if not run_as_admin(command_to_execute):
    run_as_admin(sys.argv)

# Execute the command with administrator privileges
execute_command_as_admin(command_to_execute)