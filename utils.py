import base64
from datetime import datetime
from typing import Optional

class LogNode:
    def __init__(self, error_code: str, description: str):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.error_code = error_code
        self.description = description
        self.next = None

class ErrorLogList:
    def __init__(self):
        self.head = None

    def add_error(self, error_code: str, description: str):
        new_node = LogNode(error_code, description)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_all(self):
        result = []
        current = self.head
        while current:
            result.append(f"[{current.timestamp}] {current.error_code}: {current.description}")
            current = current.next
        return result

    def clear(self):
        self.head = None

def encrypt_api_key(key: str) -> str:
    return base64.b64encode(key.encode()).decode()

def decrypt_api_key(encrypted: str) -> str:
    return base64.b64decode(encrypted.encode()).decode()

error_log = ErrorLogList()
