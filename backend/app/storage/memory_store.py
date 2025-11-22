from typing import Dict, Any

class MemoryStore:
    def __init__(self):
        self.data: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def delete(self, key: str):
        if key in self.data:
            del self.data[key]

memory_store = MemoryStore()
