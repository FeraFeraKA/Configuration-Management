import shlex
from commands import execute_command

def repl(vfs_name, log_file):
    print(f"Shell emulator for {vfs_name}. Type 'exit' to quit.")
    while True:
        try:
            command_line = input(f"{vfs_name}> ")
            tokens = shlex.split(command_line)
            if not tokens:
                continue
            command, *args = tokens
            if not execute_command(command, args, log_file):
                break
        except Exception as e:
            print(f"Error: {e}")
