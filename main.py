import re


def args_handler(args):
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

def command_handler():
    while True:
        print(f"VFS $ ", end = "")
        inp = input()
        inp = inp.split(" ", 1)

        command = inp[0]
        args = ''
        if len(inp) > 1:
            args = inp[1]

        args = args_handler(args)

        if command == "exit":
            return
        elif command == "ls":
            print(command, args)
        elif command == "cd":
            print(command, args)

if __name__ == "__main__":
    command_handler()
