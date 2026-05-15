from typing import Any, Optional
from utils import encrypt_api_key, decrypt_api_key, error_log

class QueueNode:
    def __init__(self, message: str):
        self.message = message
        self.next = None

class Queue:
    def __init__(self, max_size: int = 10):
        self.front = None
        self.rear = None
        self.size = 0
        self.max_size = max_size

    def enqueue(self, message: str):
        new_node = QueueNode(message)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1
        if self.size > self.max_size:
            self.dequeue()

    def dequeue(self) -> Optional[str]:
        if self.front is None:
            return None
        removed = self.front.message
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return removed

    def get_all(self) -> list:
        messages = []
        current = self.front
        while current:
            messages.append(current.message)
            current = current.next
        return messages

    def to_list(self) -> list:
        return self.get_all()

    def from_list(self, messages: list, max_size: int = 10):
        self.front = self.rear = None
        self.size = 0
        self.max_size = max_size
        for msg in messages:
            self.enqueue(msg)

class StackNode:
    def __init__(self, state: dict):
        self.state = state
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, state: dict):
        new_node = StackNode(state)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self) -> Optional[dict]:
        if self.top is None:
            return None
        popped = self.top.state
        self.top = self.top.next
        self.size -= 1
        return popped

    def peek(self) -> Optional[dict]:
        return self.top.state if self.top else None

    def to_list(self) -> list:
        items = []
        current = self.top
        while current:
            items.append(current.state)
            current = current.next
        return items[::-1]

    def from_list(self, states: list):
        self.top = None
        self.size = 0
        for state in reversed(states):
            self.push(state)

class BotNode:
    def __init__(self, bot_id: str, name: str, model: str, api_key: str, system_instruction: str, temperature: float = 0.7):
        self.id = bot_id
        self.name = name
        self.model = model
        self.api_key_encrypted = encrypt_api_key(api_key)
        self.system_instruction = system_instruction
        self.temperature = temperature
        self.message_queue = Queue()
        self.state_stack = Stack()
        self.prev = None
        self.next = None

    def get_api_key(self) -> str:
        return decrypt_api_key(self.api_key_encrypted)

    def set_api_key(self, api_key: str):
        self.api_key_encrypted = encrypt_api_key(api_key)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "api_key_encrypted": self.api_key_encrypted,
            "system_instruction": self.system_instruction,
            "temperature": self.temperature,
            "message_queue": self.message_queue.to_list(),
            "state_stack": self.state_stack.to_list()
        }

    def from_dict(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.model = data["model"]
        self.api_key_encrypted = data["api_key_encrypted"]
        self.system_instruction = data["system_instruction"]
        self.temperature = data.get("temperature", 0.7)
        self.message_queue.from_list(data.get("message_queue", []))
        self.state_stack.from_list(data.get("state_stack", []))

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, node: BotNode):
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self.size += 1

    def find_by_id(self, bot_id: str) -> Optional[BotNode]:
        current = self.head
        while current:
            if current.id == bot_id:
                return current
            current = current.next
        return None

    def delete_by_id(self, bot_id: str) -> bool:
        current = self.find_by_id(bot_id)
        if not current:
            return False
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev
        self.size -= 1
        return True

    def get_all(self) -> list:
        result = []
        current = self.head
        while current:
            result.append(current)
            current = current.next
        return result

    def to_list(self) -> list:
        bots_data = []
        current = self.head
        while current:
            bots_data.append(current.to_dict())
            current = current.next
        return bots_data

    def from_list(self, bots_data: list):
        self.head = self.tail = None
        self.size = 0
        for data in bots_data:
            node = BotNode("", "", "", "", "")  # temporal
            node.from_dict(data)
            self.append(node)
