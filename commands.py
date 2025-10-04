from logger import log_command
from vfs import VirtualFileSystem

vfs_instance = None

def set_vfs(vfs_path):
    global vfs_instance
    vfs_instance = VirtualFileSystem(vfs_path)

def execute_command(command, args, log_file):
    log_command(log_file, command, args)

    if command == "exit":
        print("Exiting the emulator.")
        return False
    elif command == "ls":
        print(f"[LS] Arguments: {args}")
    elif command == "cd":
        print(f"[CD] Arguments: {args}")
    elif command == "vfs-info":
        if vfs_instance:
            print(vfs_instance.info())
        else:
            print("No VFS loaded.")
    else:
        print(f"Unknown command: {command}")
        print("Exiting the emulator.")
        return False
    return True
