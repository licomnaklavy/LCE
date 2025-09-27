# Linux Console Emulator (LCE)

Эмулятор консоли Linux с виртуальной файловой системой, написанный на Python.

## Оглавление
1. [Общее описание](#-общее-описание)
2. [Функции и настройки](#-функции-и-настройки)
3. [Установка и запуск](#-установка-и-запуск)
4. [Примеры использования](#-примеры-использования)

## Общее описание

LCE (Linux Console Emulator) - это программа, эмулирующая базовые команды командной строки Linux в рамках виртуальной файловой системы. Система загружает структуру файлов и директорий из XML-файла и предоставляет интерактивный интерфейс для навигации и работы с файлами.

### Основные возможности:
- Навигация по виртуальной файловой системе
- Базовые команды Linux (ls, cd, cat, touch, clear и др.)
- Запуск стартовых скриптов
- Поддержка аргументов командной строки
- Время работы системы (uptime)
- Информация о системе (uname)

## Функции и настройки

### Архитектура проекта

Проект построен вокруг основного класса `VirtualFileSystem`, который управляет всей логикой эмулятора.

### Поддерживаемые команды

| Команда | Описание | Пример использования |
|---------|----------|---------------------|
| `help` | Показать список всех доступных команд | `help` |
| `ls` | Показать содержимое текущей директории | `ls` |
| `cd` | Сменить текущую директорию | `cd folder_name` |
| `clear` | Очистить консоль | `clear` |
| `uptime` | Показать время работы системы | `uptime` |
| `uname` | Показать информацию о системе | `uname -a` |
| `who` | Показать текущих пользователей | `who` |
| `touch` | Создать пустой файл | `touch filename` |
| `cat` | Показать содержимое файла | `cat filename` |
| `exit` | Выйти из файловой системы | `exit` |

### Аргументы командной строки

Программа поддерживает следующие аргументы при запуске:

```bash
python main.py [--vfs-root VFS_FILE] [--start-script SCRIPT_FILE]
```

## Установка и запуск
### Требования

Python 3.6+ - основная среда выполнения

Стандартные библиотеки Python:

* argparse - парсинг аргументов командной строки
* xml.etree.ElementTree - работа с XML
* time, datetime - работа со временем
* os - системные функции
* base64 - кодирование/декодирование данных

### Запуск с настройками по умолчанию:

```bash
py main.py
```

### Запуск с пользовательской VFS:

```bash
py main.py --vfs-root my_vfs.xml
```

### Запуск со стартовым скриптом:

```bash
py main.py --start-script startup.txt
```

### Комбинированный запуск:

```bash
py main.py --vfs-root custom_vfs.xml --start-script init_commands.txt
```

### Структура файлов

```text
lce-emulator/
├── main.py              # Основной файл программы
├── vfs.xml              # Файл виртуальной файловой системы (по умолчанию)
├── startup.txt          # Пример стартового скрипта
└── README.md           # Документация
```

### Пример файла VFS (vfs.xml)

```xml

<directory path="/" name="root">
    <directory path="/home" name="home">
        <directory path="/home/user" name="user">
            <file path="/home/user/test.txt" name="test.txt" content="VGhpcyBpcyBhIHRlc3QgZmlsZQ=="/>
        </directory>
    </directory>
    <directory path="/etc" name="etc">
        <file path="/etc/config.conf" name="config.conf" content="c2V0dGluZz12YWx1ZQ=="/>
    </directory>
    <file path="/readme.md" name="readme.md" content="V2VsY29tZSB0byBMQ0Uh"/>
</directory>
```

### Пример стартового скрипта (startup.txt)

```bash
# Стартовый скрипт LCE
clear
ls
cd home
ls
cd user
cat test.txt
cd /
uname -a
uptime
who
```

### Тестирование

Ручное тестирование команд:
```bash
# После запуска программы тестируйте команды:
help
ls
cd home
ls
cat test.txt
uname -s
uptime
```

Автоматическое тестирование через скрипт:
```bash
python main.py --start-script test_commands.txt
```

### Примечания
* Программа использует файл vfs.xml по умолчанию, если не указан параметр --vfs-root
* Стартовые скрипты поддерживают комментарии (строки, начинающиеся с #)
* Для выхода из программы используйте команду exit
* Все созданные через touch файлы существуют только в текущей сессии


## Примеры использования
### Базовые сценарии

Пример 1: Простой запуск и навигация
```bash
# Запуск с VFS по умолчанию
python main.py

# В интерактивном режиме:
/ $ ls
home    etc    readme.md

/ $ cd home
/home $ ls
user

/home $ cd user
/home/user $ ls
test.txt

/home/user $ cat test.txt
This is a test file

/home/user $ cd /
/ $ exit
```

Пример 2: Запуск со стартовым скриптом
```bash
# Содержимое файла init.txt:
clear
ls
cd home/user
cat test.txt
uptime

# Запуск:
python main.py --start-script init.txt
```

Пример 3: Пользовательская VFS
```bash
# Создание custom_vfs.xml
python main.py --vfs-root custom_vfs.xml
```

### Примеры работы с командами
Команда help
```bash
/ $ help
Доступные команды:
--------------------------------------------------
help       - Показать список всех доступных команд
ls         - Показать содержимое текущей директории
cd         - Сменить текущую директорию
clear      - Очистить консольно
uptime     - Показать время работы системы
uname      - Показать информацию о системе
who        - Показать текущих пользователей
touch      - Создать пустой файл
cat        - Показать содержимое файла
exit       - Выйти из файловой системы
--------------------------------------------------
```

Команда uname с различными опциями
```bash
/ $ uname
VirtualFS

/ $ uname -a
VirtualFS 1.0 x86_64 GNU/Linux

/ $ uname -s -r -m
VirtualFS 1.0.0 x86_64

/ $ uname -v
#1 SMP Virtual Kernel
```

Команда uptime
```bash
/ $ uptime
up 00:05:23

# После длительной работы
/ $ uptime
up 1 days, 03:45:12
```

Команда who
```bash
/ $ who
Current user: username 
Current terminal: LCE 
Time of using this terminal: 327.45
```

### Практические примеры
Пример 4: Создание и просмотр файлов

```bash
/ $ touch newfile.txt
Создан файл: newfile.txt

/ $ ls
home    etc    readme.md    newfile.txt

/ $ cat readme.md
Welcome to LCE!
```

Пример 5: Навигация по файловой системе
```bash
/ $ cd etc
/etc $ ls
config.conf

/etc $ cat config.conf
setting=value

/etc $ cd ..
/ $ cd home/user
/home/user $ cd /
/ $ clear  # Очистка экрана
```

### Расширенные сценарии
Пример 6: Автоматизация с помощью скрипта

Файл: deployment.txt
```bash
# Скрипт развертывания системы
clear
echo "Starting system deployment..."
uname -a
cd /etc
cat config.conf
cd /home/user
touch deployment.log
ls
echo "Deployment completed!"
uptime
```

Запуск:
```bash
python main.py --start-script deployment.txt
```

Пример 7: Комплексная VFS структура

Файл: complex_vfs.xml
```xml
<directory path="/" name="root">
    <directory path="/bin" name="bin">
        <file path="/bin/ls" name="ls" content=""/>
        <file path="/bin/cat" name="cat" content=""/>
    </directory>
    <directory path="/var" name="var">
        <directory path="/var/log" name="log">
            <file path="/var/log/system.log" name="system.log" content=""/>
        </directory>
    </directory>
    <directory path="/tmp" name="tmp"/>
</directory>
```

Пример 8: Отладка и мониторинг
```bash
# Скрипт мониторинга system_check.txt
clear
echo "=== System Information ==="
uname -a
echo ""
echo "=== Uptime ==="
uptime
echo ""
echo "=== Current User ==="
who
echo ""
echo "=== Disk Usage ==="
ls -l
echo ""
echo "=== Check completed ==="
```