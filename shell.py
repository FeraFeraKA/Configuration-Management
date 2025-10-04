import argparse
import shlex
from repl import repl
from commands import execute_command

def run_script(path, vfs_name, log_file):
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                print(f"{vfs_name}> {line}")  # emulate user input
                tokens = shlex.split(line)
                if not tokens:
                    continue
                command, *args = tokens
                if not execute_command(command, args, log_file):
                    return False
        return True
    except Exception as e:
        print(f"Error while running script: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shell emulator config")
    parser.add_argument("--vfs", type=str, help="Path to virtual filesystem", default="VFS")
    parser.add_argument("--log", type=str, help="Path to log file", default="log.xml")
    parser.add_argument("--script", type=str, help="Path to startup script")
    args = parser.parse_args()

    print("Startup configuration:")
    print(f"  VFS path: {args.vfs}")
    print(f"  Log file: {args.log}")
    if args.script:
        print(f"  Startup script: {args.script}")
        success = run_script(args.script, args.vfs, args.log)
        if not success:
            exit(0)

    repl(args.vfs, args.log)
