import os
import zipfile
import unittest
from unittest.mock import patch, mock_open

# Импортируем класс Emulator и функции add_folder, remove_last_folder
from emulator import Emulator, add_folder, remove_last_folder

class TestEmulator(unittest.TestCase):

    def setUp(self):
        # Создаем временный ZIP-файл для тестирования
        self.zip_path = "test_ale.zip"
        self.script_path = "test_script.txt"
        self.username = "test_user"
        self.hostname = "test_host"
        self.emulator = Emulator(self.username, self.hostname, self.zip_path, self.script_path)

        # Создаем временный ZIP-файл с тестовыми данными
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr("papka/papkaodin/", "")
            zipf.writestr("papka/papkadva/", "")
            zipf.writestr("papka/aaa/", "")
            zipf.writestr("papka/ale.txt", "347921490")
            zipf.writestr("abc.txt", "abcdefg")
            zipf.writestr("months.txt", "january\nfebruary\nmarch")

    def tearDown(self):
        # Удаляем временный ZIP-файл после тестов
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)
        if os.path.exists(self.script_path):
            os.remove(self.script_path)

    def test_add_folder(self):
        path = "/root"
        folder_name = "subfolder"
        result = add_folder(path, folder_name)
        self.assertEqual(result, "/root\subfolder")

    def test_remove_last_folder(self):
        path = "/root/subfolder"
        result = remove_last_folder(path)
        self.assertEqual(result, "/root")

    def test_load_file_system(self):
        self.emulator._load_file_system()
        self.assertIn("papka/ale.txt", self.emulator.file_system)
        self.assertIn("abc.txt", self.emulator.file_system)
        self.assertIn("months.txt", self.emulator.file_system)

    def test_ls(self):
        self.emulator._load_file_system()
        result = self.emulator.ls()
        self.assertIn("abc.txt", result)
        self.assertIn("months.txt", result)

    def test_cd(self):
        self.emulator._load_file_system()
        self.emulator.cd("papka")
        self.assertEqual(self.emulator.current_directory, "papka/")
        self.emulator.cd("..")
        self.assertEqual(self.emulator.current_directory, "/")

    def test_pwd(self):
        self.emulator._load_file_system()
        self.assertEqual(self.emulator.pwd(), "/")
        self.emulator.cd("papka")
        self.assertEqual(self.emulator.pwd(), "papka/")

    def test_rev(self):
        self.emulator._load_file_system()
        result = self.emulator.rev("abc.txt")
        self.assertEqual(result, "gfedcba")

    def test_wc(self):
        self.emulator._load_file_system()
        result = self.emulator.wc("months.txt")
        self.assertEqual(result, "3 3 22")

    def test_execute_command(self):
        self.emulator._load_file_system()
        result = self.emulator.execute_command("ls")
        self.assertIn("abc.txt", result)
        self.assertIn("months.txt", result)

        result = self.emulator.execute_command("cd papka")
        self.assertEqual(result, "")
        self.assertEqual(self.emulator.current_directory, "papka/")

        result = self.emulator.execute_command("pwd")
        self.assertEqual(result, "papka/")

        result = self.emulator.execute_command("wc ale.txt")
        self.assertEqual(result, "1 1 9")

        result = self.emulator.execute_command("unknown_command")
        self.assertEqual(result, "Unknown command.")

if __name__ == "__main__":
    unittest.main()