import json
import hashlib

class VirtualFileSystem:
    def __init__(self, path):
        self.path = path
        self.name = None
        self.data = None
        self.sha256 = None
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
            self.data = {}
            self.name = "ErrorVFS"
            self.sha256 = "N/A"

    def info(self):
        return f"VFS Name: {self.name}\nSHA-256: {self.sha256}"
