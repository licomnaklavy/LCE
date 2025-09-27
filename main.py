import re
import argparse
import xml.etree.ElementTree as ET
import time
from datetime import datetime, timedelta
import os
import base64


class VirtualFileSystem:
    def __init__(self, vfs_root):
        try:
            with open(vfs_root, 'r', encoding='utf-8') as file:
                xml_content = file.read()
                self.root = ET.fromstring(xml_content)
        except FileNotFoundError:
            print(f"Ошибка: vfs '{vfs_root}' не найдена")
            with open("vfs.xml", 'r', encoding='utf-8') as file:
                xml_content = file.read()
                self.root = ET.fromstring(xml_content)

        self.current_path = "/"
        self.current_dir = "/"
        self.vfs = self.build_structure()
        self.commands = {
            'help': 'Показать список всех доступных команд',
            'ls': 'Показать содержимое текущей директории',
            'cd': 'Сменить текущую директорию',
            'clear': 'Очистить консольно',
            'uptime': 'Показать время работы системы',
            'uname': 'Показать информацию о системе',
            'who': 'Показать текущих пользователей',
            'touch': 'Создать пустой файл',
            'exit': 'Выйти из файловой системы'
        }
        self.start_time = time.time()

    def build_structure(self):
        structure = {}

        def process_element(element, parent_path):
            path = element.get('path')
            name = element.get('name')
            is_dir = element.tag == 'directory'
            content = element.get('content') #############################################

            structure[path] = {
                'name': name,
                'path': path,
                'is_directory': is_dir,
                'children': [],
                'parent': parent_path,
                'content': content #############################################
            }

            for child in element:
                child_path = child.get('path')
                structure[path]['children'].append(child_path)
                process_element(child, path)

        process_element(self.root.find('directory'), "")
        return structure

    def args_handler(self, args):
        pattern = r'\"([^\"]*)\"|\'([^\']*)\'|(\S+)'

        matches = re.findall(pattern, args)
        result = []

        for match in matches:
            if match[0]:
                result.append(match[0])
            elif match[1]:
                result.append(match[1])
            elif match[2]:
                result.append(match[2])

        return result

    def command_handler(self):
        while True:
            print(f"{self.current_dir} $ ", end = "")

            command, args_arr = self.split_line()

            if self.execute_command(command, args_arr) == 0:
                break

    def split_line(self):
        inp = input()
        inp = inp.split(" ", 1)

        command = inp[0]
        args_line = ''
        if len(inp) > 1:
            args_line = inp[1]

        args_arr = self.args_handler(args_line)

        return command, args_arr

    def run_start_script(self, script_path):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    if not line or line.startswith('#'):
                        continue

                    print(f"{self.current_dir} $ ", end = "")

                    try:
                        inp = line.split(" ", 1)
                        print(*inp)
                        command = inp[0]
                        args_line = ''
                        if len(inp) > 1:
                            args_line = inp[1]

                        args_arr = self.args_handler(args_line)

                        if not self.execute_command(command, args_arr):
                            break
                    except Exception as e:
                        print(f"Ошибка в строке {line_num}: {e}")
                        continue

        except FileNotFoundError:
            print(f"Ошибка: стартовый скрипт '{script_path}' не найден")
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")

    def execute_command(self, command, args_arr):
        if command == "exit":
            return False
        elif command == "ls":
            print(self.ls())
        elif command == "cd":
            if not self.cd(args_arr):
                print(f"{args_arr[0]} не является директорией")
        elif command == "clear":
            self.clear()
        elif command == "help":
            self.help()
        elif command == "uptime":
            print(self.uptime())
        elif command == "uname":
            print(self.uname(args_arr))
        elif command == "who":
            self.who()
        elif command == "touch":
            self.touch(args_arr)
        elif command == "cat":
            self.cat(args_arr)
        else:
            print(f"Неизвестная команда: {command}")

        return True

    def ls(self):
        current_dir = self.vfs.get(self.current_path)
        if not current_dir or not current_dir['is_directory']:
            return []

        return [self.vfs[child]['name'] for child in current_dir['children']]

    def cd(self, args_arr):
        if args_arr:
            target = args_arr[0]
        else:
            target = ""

        if not target:
            self.current_path = "/"
            self.current_dir = "/"
            return True
        if target == ".":
            return True
        if target == "..":
            parent = self.vfs[self.current_path]['parent']
            if parent:
                self.current_path = parent
                self.current_dir = parent
                return True
            return False

        current_dir = self.vfs.get(self.current_path)
        if not current_dir:
            return False

        for child_path in current_dir['children']:
            child = self.vfs[child_path]
            if child['name'] == target and child['is_directory']:
                self.current_path = child_path
                self.current_dir = child['path']
                return True

        return False

    def clear(self):
        print("\033[H\033[J", end="")

    def help(self):
        print("Доступные команды:")
        print("-" * 50)
        for command, description in self.commands.items():
            print(f"{command:10} - {description}")
        print("-" * 50)

    def uptime(self):
        uptime_seconds = time.time() - self.start_time
        uptime_timedelta = timedelta(seconds=int(uptime_seconds))

        days = uptime_timedelta.days
        hours, remainder = divmod(uptime_timedelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"up {days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"up {hours:02d}:{minutes:02d}:{seconds:02d}"

    def uname(self, args_arr):
        if not args_arr:
            args_arr = ['-s']  # По умолчанию только имя системы

        result = []

        for arg in args_arr:
            if arg == '-a':  # Все информация
                result.append(f"VirtualFS 1.0 x86_64 GNU/Linux")
            elif arg == '-s':  # Имя ядра
                result.append("VirtualFS")
            elif arg == '-n':  # Имя сети
                result.append("localhost")
            elif arg == '-r':  # Версия ядра
                result.append("1.0.0")
            elif arg == '-v':  # Версия
                result.append("#1 SMP Virtual Kernel")
            elif arg == '-m':  # Архитектура
                result.append("x86_64")
            elif arg == '-p':  # Процессор
                result.append("x86_64")
            elif arg == '-i':  # Платформа
                result.append("virtual")
            elif arg == '-o':  # ОС
                result.append("GNU/Linux")
            else:
                return f"uname: неизвестный аргумент: '{arg[1:]}'"

        return ' '.join(result)

    def who(self):
        print(f"Current user: {os.getlogin()} \n"
                            + f"Current terminal: LCE \n"
                            + f"Time of using this terminal: {time.time() - self.start_time}")

    def touch(self, args_arr):
        filename = ""
        if args_arr:
            filename = args_arr[0]
        if not filename:
            print("Укажите имя файла")
            return False

        current_dir = self.vfs.get(self.current_path)

        for child_path in current_dir['children']:
            child = self.vfs[child_path]
            if child['name'] == filename and not child['is_directory']:
                print(f"Файл уже существует!")
                return False

        new_file_path = f"{self.current_path.rstrip('/')}/{filename}"

        self.vfs[new_file_path] = {
            'name': filename,
            'path': new_file_path,
            'is_directory': False,
            'children': [],
            'parent': self.current_path,
        }

        current_dir['children'].append(new_file_path)

        print(f"Создан файл: {filename}")
        return True

    def cat(self, args_arr):
        filename = ""
        if args_arr:
            filename = args_arr[0]
        if not filename:
            print("Укажите имя файла")
            return False

        current_dir = self.vfs.get(self.current_path)

        for child_path in current_dir['children']:
            child = self.vfs[child_path]
            if child['name'] == filename and not child['is_directory']:
                content = child.get('content')
                if content:
                    content = base64.b64decode(content).decode('utf-8')
                    print(content)
                    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Linux Condole Emulator')
    parser.add_argument('--vfs-root', '-r', help='Путь до физического расположения VFS')
    parser.add_argument('--start-script', '-s', help='Путь до стартового скрипта')

    args = parser.parse_args()

    if args.vfs_root:
        vfs = VirtualFileSystem(args.vfs_root)
    else:
        vfs = VirtualFileSystem("vfs.xml")

    if not args.start_script is None:
        vfs.run_start_script(args.start_script)

    vfs.command_handler()