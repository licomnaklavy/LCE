import os

absolute_path = "."
current_dir = "."

while True:
    print("terminal@terminal-temple " + current_dir + " $ ", end="")
    inp = input().split()
    command = inp[0]
    args = inp[1:]
    if command == "exit":
        break
    if command == "ls":
        all_items = os.listdir(absolute_path)
        folders = [item for item in all_items if os.path.isdir(absolute_path + "/" + item)]
        print(*folders, sep="\t")
    if command == "cd":
        all_items = os.listdir(absolute_path)
        if args[0] in all_items:
            absolute_path = absolute_path + "/" + args[0]
            current_dir = args[0]
        elif all(char == '.' for char in args[0]) and len(args[0]) > 0:
            temp = absolute_path
            for i in range(len(args[0]) - 1):
                temp = temp[0:temp.rfind("/")]
            if temp:
                absolute_path = temp
                current_dir = temp[temp.rfind("/") + 1:]
            else:
                print("cd: no such file or directory: " + args[0])
        else:
            print("cd: no such file or directory: " + args[0])