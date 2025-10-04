import xml.etree.ElementTree as ET
from datetime import datetime

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
