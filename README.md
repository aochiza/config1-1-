# Конфигурационное управление. Домашнее задание
# Hi there, I'm [ksen](https://daniilshat.ru/) ![](https://github.com/blackcater/blackcater/raw/main/images/Hi.gif) 
### Задание №1, 2 вариант<br />
### Постановка задачи:<br />
Задание №1 <br />
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. <br />
Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя. <br />
Эмулятор принимает образ виртуальной файловой системы в виде файла формата zip. Эмулятор должен работать в режиме GUI. <br />
Ключами командной строки задаются: <br />
• Имя компьютера для показа в приглашении к вводу. <br />
• Путь к архиву виртуальной файловой системы. <br />
• Путь к стартовому скрипту. <br />
Стартовый скрипт служит для начального выполнения заданного списка команд из файла. <br />
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также <br />
следующие команды: <br />
1. rev. <br />
2. pwd. <br />
3. wc. <br />
Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 2 теста.<br />
### Структура zip файла
```
├── papka/
│   ├── papkadva/
│   ├── papkaodin/
│   ├── qwerty/
│   ├── ale.txt
│── abc.txt
│── months.txt
```
### Команда для запуска emulator.py
```
python emulator.py --hostname "ksen" --vfs "C:/Users/ksen/config1.5/ale.zip" --script "C:/Users/ksen/config1.5/script.txt"
```
### Содердание скриптового файла
```
ls
cd folder1
ls
cd ..
pwd
rev file1.txt
wc file1.txt
```
### Результат тестов emulator.py
![image](https://github.com/user-attachments/assets/2efca4d6-2998-418e-b8c2-9a04df899dc2)

### Результат тестов test.py
![image](https://github.com/user-attachments/assets/58d9c620-5817-471f-8592-93df2cb18961)

