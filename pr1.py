import shlex

def repl():
    vfs_name = "VFS"
    print(f"Shell emulator for {vfs_name}. Type 'exit' to quit.")

    while True:
        try:
            command_line = input(f"{vfs_name}> ")

            tokens = shlex.split(command_line)
            if not tokens:
                continue

            command, *args = tokens

            if command == "exit":
                print("Exiting the emulator.")
                break
            elif command == "ls":
                print(f"[LS] Arguments: {args}")
            elif command == "cd":
                print(f"[CD] Arguments: {args}")
            else:
                print(f"Unknown command: {command}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()
