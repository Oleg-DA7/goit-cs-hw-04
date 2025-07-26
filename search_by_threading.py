# Розробіть програму, яка паралельно обробляє та аналізує текстові файли 
# для пошуку визначених ключових слів з використанням модуля threading
from threading import Thread
import os

def search_in_file(file_path, keywords):
    """Функція для пошуку ключових слів у файлі."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            found_keywords = [k for k in keywords if k in content]
            if found_keywords:
                print(f"У файлі {file_path} знайдено ключові слова: {', '.join(found_keywords)}")
    except Exception as e:
        print(f"Помилка при обробці файлу {file_path}: {e}")

def search_files_in_directory(directory, keywords):
    """Функція для пошуку ключових слів у всіх файлах директорії."""
    threads = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)
                thread = Thread(target=search_in_file, args=(file_path, keywords))
                threads.append(thread)
                thread.start()
                print(f"Запущено потік: {thread.name} для файлу: {file_path}")
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    keywords = ["представляє", "пропонує", "місто"]
    directory = ".//txt"

    search_files_in_directory(directory, keywords)  