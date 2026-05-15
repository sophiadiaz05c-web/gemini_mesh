from models import DoublyLinkedList, BotNode
from utils import error_log
import random

class ChatbotManager:
    def __init__(self):
        self.bot_list = DoublyLinkedList()
        self.current_bot = None

    def load(self):
        from persistence import load_bots
        self.bot_list = load_bots()
        if self.bot_list.head:
            self.current_bot = self.bot_list.head
            error_log.add_error("INFO", "Datos cargados correctamente desde JSON")

    def save(self):
        from persistence import save_bots
        save_bots(self.bot_list)
        error_log.add_error("INFO", "Datos guardados correctamente")

    def create_bot(self, name: str, model: str, api_key: str, system_instruction: str, temperature: float = 0.7) -> bool:
        import uuid
        bot_id = str(uuid.uuid4())[:8]
        if self.bot_list.find_by_id(bot_id):
            bot_id = str(uuid.uuid4())[:8]
        new_bot = BotNode(bot_id, name, model, api_key, system_instruction, temperature)
        self.bot_list.append(new_bot)
        error_log.add_error("CREACION", f"Bot '{name}' creado con ID {bot_id}")
        return True

    def list_bots(self) -> list:
        return self.bot_list.get_all()

    def select_bot(self, bot_id: str) -> bool:
        bot = self.bot_list.find_by_id(bot_id)
        if bot:
            self.current_bot = bot
            error_log.add_error("SELECCION", f"Bot actual: {bot.name}")
            return True
        error_log.add_error("ERROR", f"ID {bot_id} no encontrado")
        return False

    def delete_bot(self, bot_id: str) -> bool:
        if self.current_bot and self.current_bot.id == bot_id:
            self.current_bot = None
        if self.bot_list.delete_by_id(bot_id):
            error_log.add_error("ELIMINACION", f"Bot ID {bot_id} eliminado")
            return True
        error_log.add_error("ERROR", f"No se pudo eliminar ID {bot_id}")
        return False

    def modify_bot(self, field: str, value: str):
        if not self.current_bot:
            error_log.add_error("ERROR", "No hay bot seleccionado para modificar")
            return False
        current_state = {
            "system_instruction": self.current_bot.system_instruction,
            "temperature": self.current_bot.temperature
        }
        self.current_bot.state_stack.push(current_state)

        if field == "nombre":
            self.current_bot.name = value
        elif field == "modelo":
            self.current_bot.model = value
        elif field == "instruction":
            self.current_bot.system_instruction = value
        elif field == "temperatura":
            try:
                self.current_bot.temperature = float(value)
            except ValueError:
                error_log.add_error("ERROR", "Temperatura debe ser un número")
                return False
        else:
            error_log.add_error("ERROR", f"Campo '{field}' no válido")
            return False
        error_log.add_error("MODIFICACION", f"Bot modificado: {field}={value}")
        return True

    def send_message(self, message: str) -> str:
        if not self.current_bot:
            error_log.add_error("ERROR", "No hay bot seleccionado")
            return "Error: Selecciona un bot primero."
        self.current_bot.message_queue.enqueue(f"Usuario: {message}")
        simulated_response = self._simulate_gemini_response(message)
        self.current_bot.message_queue.enqueue(f"Bot: {simulated_response}")
        error_log.add_error("CHAT", f"Mensaje enviado a {self.current_bot.name}")
        return simulated_response

    def _simulate_gemini_response(self, user_message: str) -> str:
        responses = [
            "Entiendo tu pregunta. Según mi instrucción de sistema, debo ayudarte con estructuras de datos.",
            "Interesante. Como bot creativo, te sugiero que explores más sobre el tema.",
            "De acuerdo con mi configuración actual, aquí tienes una explicación breve.",
            "No tengo una respuesta exacta, pero puedo guiarte con un ejemplo."
        ]
        return f"[Simulación] {random.choice(responses)} (Temperatura: {self.current_bot.temperature})"

    def get_context(self) -> dict:
        if not self.current_bot:
            return None
        return {
            "id": self.current_bot.id,
            "name": self.current_bot.name,
            "model": self.current_bot.model,
            "system_instruction": self.current_bot.system_instruction,
            "temperature": self.current_bot.temperature,
            "messages": self.current_bot.message_queue.get_all()
        }

    def undo_last_change(self) -> bool:
        if not self.current_bot:
            error_log.add_error("ERROR", "No hay bot seleccionado para deshacer")
            return False
        previous_state = self.current_bot.state_stack.pop()
        if previous_state:
            self.current_bot.system_instruction = previous_state["system_instruction"]
            self.current_bot.temperature = previous_state["temperature"]
            error_log.add_error("UNDO", f"Restaurado estado anterior del bot {self.current_bot.name}")
            return True
        else:
            error_log.add_error("UNDO", "No hay estados previos para restaurar")
            return False
