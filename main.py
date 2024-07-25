import os
import ctypes
import sys
import requests

# ANSI-коды для изменения цвета текста
RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'

DISCORD_URL = "https://discord.com/invite/your-discord"  # Замените на реальный URL вашего Discord


# Проверка наличия обновлений
def check_for_updates():
    try:
        response = requests.get('https://example.com/latest_version')  # URL для проверки версии
        response.raise_for_status()
        latest_version = response.text.strip()
        return latest_version
    except requests.RequestException as e:
        print_error(f"Не удалось проверить обновления: {e}")
        return None


# Функция для вывода сообщений об ошибках
def print_error(message):
    print(f"{RED}[Error] {message}{RESET}")


# Функция для вывода сообщений об успешных действиях
def print_success(message):
    print(f"{GREEN}[Success] {message}{RESET}")


def main():
    current_version = "1.0.0"  # Текущая версия приложения
    print("Добро пожаловать в консоль администратора")

    while True:
        command = input("> ")

        if command.lower() in ["exit", "quit"]:
            break
        elif command.startswith("cd "):
            try:
                os.chdir(command[3:])
            except Exception as e:
                print_error(str(e))
        elif command.lower() == "/upgradeap":
            latest_version = check_for_updates()
            if latest_version:
                if latest_version != current_version:
                    print(f"{GREEN}[Warning] Мы нашли новую версию для обновления АП: {latest_version}")
                    # Здесь можно добавить логику для обновления приложения
                    print_success("Обновление завершено успешно.")
                else:
                    print_error("Нету обновлений.")
            else:
                print_error("Не удалось проверить наличие обновлений.")
        else:
            result = os.system(command)
            if result != 0:
                print_error(f"Команда '{command}' завершилась с кодом ошибки {result}")


if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Запуск от имени администратора...")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except Exception as e:
            print_error(str(e))
            sys.exit(1)
    else:
        main()
