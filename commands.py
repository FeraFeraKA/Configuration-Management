from logger import log_command

def execute_command(command, args, log_file):
    log_command(log_file, command, args)

    if command == "exit":
        print("Exiting the emulator.")
        return False
    elif command == "ls":
        print(f"[LS] Arguments: {args}")
    elif command == "cd":
        print(f"[CD] Arguments: {args}")
    else:
        print(f"Unknown command: {command}")
        return False
    return True
