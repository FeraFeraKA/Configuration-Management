import shlex
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem


def log_command(log_file, command, args):
    try:
        try:
            tree = ET.parse(log_file)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("log")
            tree = ET.ElementTree(root)

        entry = ET.SubElement(root, "entry")
        entry.set("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        entry.set("command", command)
        entry.set("args", str(args))

        indent(root)
        tree.write(log_file, encoding="utf-8", xml_declaration=True)

    except Exception as e:
        print(f"Logging error: {e}")


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



def run_script(path, vfs_name, log_file):
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                print(f"{vfs_name}> {line}")
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

    if args.script:
        success = run_script(args.script, args.vfs, args.log)
        if not success:
            exit(0)

    repl(args.vfs, args.log)
