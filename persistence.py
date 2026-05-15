# persistence.py
import json
import os
from models import DoublyLinkedList, BotNode

CONFIG_FILE = "data/config.json"
DATA_FILE = "data/chatbots.json"

def ensure_data_folder():
    if not os.path.exists("data"):
        os.makedirs("data")

def load_config() -> str:
    ensure_data_folder()
    if not os.path.exists(CONFIG_FILE):
        default_config = {"data_file": DATA_FILE}
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        return DATA_FILE
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        return config.get("data_file", DATA_FILE)

def save_bots(bot_list: DoublyLinkedList):
    data_file = load_config()
    bots_data = bot_list.to_list()
    with open(data_file, "w") as f:
        json.dump(bots_data, f, indent=4)

def load_bots() -> DoublyLinkedList:
    bot_list = DoublyLinkedList()
    data_file = load_config()
    if not os.path.exists(data_file):
        default_bots = [
            {
                "id": "1",
                "name": "Asistente Académico",
                "model": "gemini-1.5-flash",
                "api_key_encrypted": "dGVzdF9hcGlfa2V5XzEyMzQ1Ng==",
                "system_instruction": "Eres un tutor universitario que explica estructuras de datos.",
                "temperature": 0.7,
                "message_queue": [],
                "state_stack": []
            },
            {
                "id": "2",
                "name": "Bot Creativo",
                "model": "gemini-1.5-pro",
                "api_key_encrypted": "dGVzdF9hcGlfa2V5Xzc4OTAxMg==",
                "system_instruction": "Eres un escritor creativo que ayuda a generar historias.",
                "temperature": 0.9,
                "message_queue": [],
                "state_stack": []
            }
        ]
        with open(data_file, "w") as f:
            json.dump(default_bots, f, indent=4)
        bots_data = default_bots
    else:
        with open(data_file, "r") as f:
            bots_data = json.load(f)
    for data in bots_data:
        node = BotNode("", "", "", "", "")
        node.from_dict(data)
        bot_list.append(node)
    return bot_list
