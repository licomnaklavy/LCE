import re
import argparse
import xml.etree.ElementTree as ET


class VirtualFileSystem:
    def __init__(self, file):
        self.current_directory = "/"
        self.vfs = file

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
            print(f"{self.vfs} {self.current_directory} $ ", end = "")

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

                    print(f"{self.vfs} {self.current_directory} $ ", end = "")

                    try:
                        inp = line.split(" ", 1)
                        print(*inp)
                        command = inp[0]
                        args_line = ''
                        if len(inp) > 1:
                            args_line = inp[1]

                        args_arr = self.args_handler(args_line)

                        if self.execute_command(command, args_arr) == 0:
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
            return 0
        elif command == "ls":
            print(command, args_arr)
        elif command == "cd":
            print(command, args_arr)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Linux Condole Emulator')
    parser.add_argument('--vfs-root', '-r', help='Путь до физического расположения VFS')
    parser.add_argument('--start-script', '-s', help='Путь до стартового скрипта')

    args = parser.parse_args()

    if not args.vfs_root is None:
        vfs = VirtualFileSystem(args.vfs_root)
    else:
        vfs = VirtualFileSystem("base_vfs.xml")

    if not args.start_script is None:
        vfs.run_start_script(args.start_script)

    vfs.command_handler()