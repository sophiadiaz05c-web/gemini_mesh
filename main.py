# main.py
import sys
from chatbot_manager import ChatbotManager
from utils import error_log

def clear_screen():
    print("\n" * 2)

def print_header(title):
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)

def print_bot_info(bot):
    print(f"ID: {bot.id} | Nombre: {bot.name} | Modelo: {bot.model}")
    print(f"Instruction: {bot.system_instruction[:50]}...")
    print(f"Temperatura: {bot.temperature}")

def main():
    manager = ChatbotManager()
    manager.load()
    
    while True:
        clear_screen()
        print_header("GEMINI MESH - ORQUESTACIÓN DE CHATBOTS")
        print("\n[ MENÚ PRINCIPAL ]")
        print("1. Gestión de Chatbots (Crear, Listar, Eliminar)")
        print("2. Seleccionar bot actual")
        print("3. Chatear con el bot actual")
        print("4. Modificar personalidad del bot actual (System Instruction / Temperatura)")
        print("5. Deshacer último cambio (Undo)")
        print("6. Ver contexto del bot actual (incluye cola de mensajes)")
        print("7. Ver Log de errores")
        print("8. Guardar todo")
        print("9. Salir")
        
        opcion = input("\nOpción: ").strip()
        
        if opcion == "1":
            # Submenú gestión de chatbots
            while True:
                clear_screen()
                print_header("GESTIÓN DE CHATBOTS")
                print("a. Listar todos los bots")
                print("b. Crear nuevo bot")
                print("c. Eliminar un bot")
                print("d. Volver al menú principal")
                sub = input("Opción: ").strip().lower()
                if sub == "a":
                    bots = manager.list_bots()
                    if not bots:
                        print("No hay bots registrados.")
                    else:
                        for bot in bots:
                            print_bot_info(bot)
                            print("-" * 40)
                    input("\nPresiona Enter para continuar...")
                elif sub == "b":
                    print("\n--- Crear nuevo bot ---")
                    name = input("Nombre del bot: ").strip()
                    model = input("Modelo (ej: gemini-1.5-flash): ").strip()
                    api_key = input("API Key: ").strip()
                    sys_inst = input("System Instruction (prompt base): ").strip()
                    temp_str = input("Temperatura (0.0 a 1.0, default 0.7): ").strip()
                    temp = 0.7
                    if temp_str:
                        try:
                            temp = float(temp_str)
                        except:
                            print("Valor inválido, se usará 0.7")
                    manager.create_bot(name, model, api_key, sys_inst, temp)
                    print("Bot creado exitosamente.")
                    input("Presiona Enter...")
                elif sub == "c":
                    bot_id = input("Ingresa el ID del bot a eliminar: ").strip()
                    if manager.delete_bot(bot_id):
                        print("Bot eliminado.")
                    else:
                        print("ID no encontrado.")
                    input("Presiona Enter...")
                elif sub == "d":
                    break
                else:
                    print("Opción no válida")
                    input("Presiona Enter...")
        
        elif opcion == "2":
            # Seleccionar bot
            bots = manager.list_bots()
            if not bots:
                print("No hay bots disponibles. Crea uno primero.")
                input("Presiona Enter...")
                continue
            print("\nBots disponibles:")
            for bot in bots:
                print(f"ID: {bot.id} -> {bot.name}")
            bot_id = input("\nIngresa el ID: ").strip()
            if manager.select_bot(bot_id):
                print(f"Bot '{manager.current_bot.name}' seleccionado.")
            else:
                print("ID inválido.")
            input("Presiona Enter...")
        
        elif opcion == "3":
            # Chatear
            if not manager.current_bot:
                print("Primero debes seleccionar un bot (opción 2).")
                input("Presiona Enter...")
                continue
            print(f"\n--- Chat con {manager.current_bot.name} (escribe 'exit-chatbot' para salir) ---")
            while True:
                user_msg = input("Tú: ").strip()
                if user_msg.lower() == "exit-chatbot":
                    break
                if not user_msg:
                    continue
                response = manager.send_message(user_msg)
                print(f"{manager.current_bot.name}: {response}")
            input("Chat finalizado. Presiona Enter...")
        
        elif opcion == "4":
            # Modificar personalidad
            if not manager.current_bot:
                print("Selecciona un bot primero.")
                input("Presiona Enter...")
                continue
            print("\n--- Modificar personalidad ---")
            print("Campos a modificar: instruction, temperatura")
            campo = input("Campo: ").strip().lower()
            valor = input("Nuevo valor: ").strip()
            if campo in ["instruction", "temperatura"]:
                if manager.modify_bot(campo, valor):
                    print("Cambio aplicado. Puedes deshacer con la opción 5.")
                else:
                    print("Error al modificar.")
            else:
                print("Campo no válido. Usa 'instruction' o 'temperatura'")
            input("Presiona Enter...")
        
        elif opcion == "5":
            # Undo
            if manager.undo_last_change():
                print("Estado anterior restaurado.")
            else:
                print("No se pudo deshacer (sin estados previos o sin bot seleccionado).")
            input("Presiona Enter...")
        
        elif opcion == "6":
            # Ver contexto
            if not manager.current_bot:
                print("No hay bot seleccionado.")
            else:
                ctx = manager.get_context()
                print_header(f"CONTEXTO DE {ctx['name']}")
                print(f"ID: {ctx['id']}")
                print(f"Modelo: {ctx['model']}")
                print(f"System Instruction: {ctx['system_instruction']}")
                print(f"Temperatura: {ctx['temperature']}")
                print("\n--- Historial de mensajes (cola) ---")
                if ctx['messages']:
                    for msg in ctx['messages']:
                        print(msg)
                else:
                    print("(Vacío)")
            input("\nPresiona Enter...")
        
        elif opcion == "7":
            # Ver log de errores
            logs = error_log.get_all()
            print_header("REGISTRO DE EVENTOS (LOG)")
            if logs:
                for entry in logs:
                    print(entry)
            else:
                print("No hay eventos registrados.")
            input("\nPresiona Enter...")
        
        elif opcion == "8":
            manager.save()
            print("Datos guardados en JSON.")
            input("Presiona Enter...")
        
        elif opcion == "9":
            print("Guardando antes de salir...")
            manager.save()
            print("¡Hasta luego!")
            sys.exit(0)
        
        else:
            print("Opción inválida. Intenta de nuevo.")
            input("Presiona Enter...")

if __name__ == "__main__":
    main()