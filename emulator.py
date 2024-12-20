import os
import zipfile
import tkinter as tk
from tkinter import scrolledtext

def add_folder(path, folder_name):
    return os.path.join(path, folder_name)

def remove_last_folder(path):
    return os.path.dirname(path)

class Emulator:
    def __init__(self, username, hostname, zip_path, script_path):
        self.username = username
        self.hostname = hostname
        self.current_directory = '/'  # Текущая директория (начинаем с корня '/')
        self.absolute_path = r"C:\Users\ksen\config1.5"
        self.zip_path = zip_path
        self.script_path = script_path
        self.file_system = {}
        self._load_file_system()

    def _get_prompt_directory(self):
        """Метод для получения текущей директории для отображения в prompt."""
        return self.current_directory if self.current_directory != '/' else '/'

    def _load_file_system(self):
        """Загружает файловую систему из ZIP-архива."""
        if not zipfile.is_zipfile(self.zip_path):
            print("")
            return

        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                normalized_path = file.lstrip('/')
                try:
                    self.file_system[normalized_path] = zip_ref.read(file).decode('utf-8')
                except Exception as e:
                    print(f"Error reading file {file} from ZIP: {e}")

    def ls(self, directory=None):
        """Выводит содержимое директории."""
        if directory:
            path = os.path.join(self.current_directory, directory).lstrip('/')
        else:
            path = self.current_directory.lstrip('/')

        output = []
        found_files = False
        for file in self.file_system:
            if file.startswith(path):
                relative_path = file[len(path):].strip('/')
                if '/' not in relative_path:
                    output.append(relative_path)
                    found_files = True

        if not found_files:
            output.append("Directory is empty.")

        response = '\n'.join(output)
        print(response)
        return response

    def cd(self, path):
        """Меняет текущую директорию."""
        if path == "..":
            if self.current_directory != '/':
                self.current_directory = os.path.dirname(self.current_directory.rstrip('/')) + '/'
                self.absolute_path = remove_last_folder(self.absolute_path)
        else:
            new_directory = os.path.join(self.current_directory, path).lstrip('/')
            if any(f.startswith(new_directory) for f in self.file_system.keys()):
                self.current_directory = new_directory.rstrip('/') + '/'
                self.absolute_path = add_folder(self.absolute_path, path)
            else:
                response = "Error: directory not found."
                print(response)
                return response
        return ""

    def pwd(self):
        """Выводит текущую рабочую директорию."""
        return self.current_directory

    def rev(self, file_name):
        """Переворачивает содержимое файла."""
        file_path = os.path.join(self.current_directory, file_name).lstrip('/')
        if file_path in self.file_system:
            content = self.file_system[file_path]
            return content[::-1]
        else:
            return "Error: file not found."

    def wc(self, file_name):
        """Подсчитывает количество строк, слов и символов в файле."""
        file_path = os.path.join(self.current_directory, file_name).lstrip('/')
        if file_path in self.file_system:
            content = self.file_system[file_path]
            lines = content.count('\n') + 1
            words = len(content.split())
            chars = len(content)
            return f"{lines} {words} {chars}"
        else:
            return "Error: file not found."

    def _run_script(self, gui):
        """Выполняет команды из скрипта."""
        try:
            with open(self.script_path, 'r') as script_file:
                for command in script_file:
                    command = command.strip()
                    if command:
                        gui.output_text.config(state='normal')
                        gui.output_text.insert(tk.END, f"{self.username}@{self.hostname}:{self._get_prompt_directory()}$ {command}\n")
                        gui.output_text.config(state='disabled')
                        output = self.execute_command(command)
                        gui.output_text.config(state='normal')
                        gui.output_text.insert(tk.END, f"{output}\n")
                        gui.output_text.config(state='disabled')
                        gui.output_text.yview(tk.END)
        except FileNotFoundError:
            print(f"Error: script file not found at {self.script_path}")
        except Exception as e:
            print(f"Error running script: {e}")

    def execute_command(self, command):
        """Выполняет команду."""
        if command.startswith("ls"):
            args = command.split(" ")
            if len(args) == 2:
                return self.ls(args[1])
            else:
                return self.ls()
        elif command.startswith("cd "):
            return self.cd(command.split(" ")[1])
        elif command == "pwd":
            return self.pwd()
        elif command.startswith("rev "):
            return self.rev(command.split(" ")[1])
        elif command.startswith("wc "):
            return self.wc(command.split(" ")[1])
        elif command == "exit":
            return "Exiting emulator..."
        else:
            return "Unknown command."

class EmulatorGUI:
    def __init__(self, emulator, script_path):
        self.emulator = emulator
        self.script_path = script_path
        self.window = tk.Tk()
        self.window.title("Linux Emulator")
        self.window.configure(bg="black")
        self.window.minsize(900, 500)
        self.output_text = scrolledtext.ScrolledText(self.window, width=80, height=20, bg="black", fg="green", state='disabled', font=("Consolas", 12))
        self.output_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.host_display = tk.Label(self.window, text=f"current directory: {emulator.username}@{emulator.hostname}:{emulator._get_prompt_directory()}$", bg="black", fg="green", font=("Consolas", 12), anchor="w")
        self.host_display.grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.command_entry = tk.Entry(self.window, width=80, bg="black", fg="green", font=("Consolas", 12), insertbackground="green")
        self.command_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.command_entry.bind('<Return>', self.run_command)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_rowconfigure(2, weight=0)
        self.window.grid_columnconfigure(0, weight=1)
        emulator._run_script(self)
        self.window.mainloop()

    def run_command(self, event):
        command = self.command_entry.get()
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, f"{self.emulator.username}@{self.emulator.hostname}:{self.emulator._get_prompt_directory()}$ {command}\n")
        self.output_text.config(state='disabled')
        self.command_entry.delete(0, tk.END)
        output = self.execute_command(command)
        self.host_display.config(text=f"current directory: {self.emulator.username}@{self.emulator.hostname}:{self.emulator._get_prompt_directory()}$")
        self.host_display.update()
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, f"{output}\n")
        self.output_text.config(state='disabled')
        self.output_text.yview(tk.END)

    def execute_command(self, command):
        return self.emulator.execute_command(command)

if __name__ == "__main__":
    username = "ksen"
    hostname = "my_pc"
    zip_path = "C:/Users/ksen/config1.5/ale.zip"
    script_path = "C:/Users/ksen/config1.5/script.txt"
    absolute_path = r"C:\Users\ksen\config1.5"
    emulator = Emulator(username, hostname, zip_path, script_path)
    gui = EmulatorGUI(emulator, script_path)