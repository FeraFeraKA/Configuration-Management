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

    elif command == "vfs-info":
        if vfs_instance:
            print(vfs_instance.info())
        else:
            print("No VFS loaded.")

    elif command == "ls":
        if vfs_instance:
            print(vfs_instance.ls())
        else:
            print("No VFS loaded.")

    elif command == "cd":
        if vfs_instance:
            if args:
                print(vfs_instance.cd(args[0]))
            else:
                print("Usage: cd <dirname>")
        else:
            print("No VFS loaded.")

    elif command == "head":
        if vfs_instance:
            if args:
                n = int(args[1]) if len(args) > 1 else 5
                print(vfs_instance.head(args[0], n))
            else:
                print("Usage: head <filename> [n]")
        else:
            print("No VFS loaded.")

    elif command == "wc":
        if vfs_instance:
            if args:
                print(vfs_instance.wc(args[0]))
            else:
                print("Usage: wc <filename>")
        else:
            print("No VFS loaded.")

    elif command == "tree":
        if vfs_instance:
            print(vfs_instance.tree())
        else:
            print("No VFS loaded.")

    elif command == "mv":
        if len(args) < 2:
            print("Usage: mv <src> <dest>")
        else:
            print(vfs_instance.mv(args[0], args[1]))

    else:
        print(f"Unknown command: {command}")
        return False

    return True
