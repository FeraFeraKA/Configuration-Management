import json
import hashlib

class VirtualFileSystem:
    def __init__(self, path):
        self.path = path
        self.name = None
        self.data = None
        self.sha256 = None
        self.cwd = []
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read()
                self.data = json.loads(content)
                self.sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
                self.name = self.data.get("name", "UnnamedVFS")
        except Exception as e:
            print(f"Error loading VFS: {e}")
            self.data = {"folders": [], "files": []}
            self.name = "ErrorVFS"
            self.sha256 = "N/A"

    def info(self):
        return f"VFS Name: {self.name}\nSHA-256: {self.sha256}"

    def _get_current_dir(self):
        node = self.data
        for folder in self.cwd:
            found = None
            for f in node.get("folders", []):
                if f["name"] == folder:
                    found = f
                    break
            if not found:
                raise FileNotFoundError(f"Folder not found: {folder}")
            node = found
        return node

    def ls(self):
        node = self._get_current_dir()
        items = []
        for f in node.get("folders", []):
            items.append(f"[DIR] {f['name']}")
        for file in node.get("files", []):
            items.append(f"[FILE] {file['name']}")
        return "\n".join(items) if items else "(empty)"

    def cd(self, dirname):
        if dirname == "..":
            if self.cwd:
                self.cwd.pop()
            return f"Moved to {'/' if not self.cwd else '/' + '/'.join(self.cwd)}"
        node = self._get_current_dir()
        for f in node.get("folders", []):
            if f["name"] == dirname:
                self.cwd.append(dirname)
                return f"Moved to /{'/'.join(self.cwd)}"
        return f"No such directory: {dirname}"

    def head(self, filename, n=5):
        node = self._get_current_dir()
        for file in node.get("files", []):
            if file["name"] == filename and file["type"] == "text":
                lines = file["content"].splitlines()
                return "\n".join(lines[:n])
        return f"No such text file: {filename}"

    def wc(self, filename):
        node = self._get_current_dir()
        for file in node.get("files", []):
            if file["name"] == filename and file["type"] == "text":
                content = file["content"]
                lines = content.splitlines()
                words = content.split()
                chars = len(content)
                return f"Lines: {len(lines)}, Words: {len(words)}, Chars: {chars}"
        return f"No such text file: {filename}"

    def tree(self, node=None, prefix=""):
        top_level = False
        if node is None:
            node = self.data
            top_level = True

        lines = []

        for f in node.get("folders", []) or []:
            if not isinstance(f, dict):
                continue
            lines.append(f"{prefix}{f.get('name', '<no-name>')}/")
            child_lines = self.tree(f, prefix + "  ")
            if isinstance(child_lines, str):
                child_lines = child_lines.splitlines()
            lines.extend(child_lines)

        for file in node.get("files", []) or []:
            if not isinstance(file, dict):
                continue
            lines.append(f"{prefix}{file.get('name', '<no-name>')}")

        if top_level:
            return "\n".join(lines)
        return lines


