# Розробіть програму, яка паралельно обробляє та аналізує текстові файли для пошуку визначених ключових слів. 
# Створіть з використанням модуля multiprocessing для багатопроцесорного програмування.
#   - Розділіть список файлів між різними процесами.
#   - Кожен процес має обробляти свою частину файлів, шукаючи ключові слова.
#   - Використайте механізм обміну даними (наприклад, через Queue) для збору та виведення результатів пошуку.
#   - Код вимірює та виводить час виконання кожного процесу.

from multiprocessing import Process, Queue
import os   
import time

def search_in_file(file_list, keywords, queue):
    """Функція для пошуку ключових слів у списку файлів."""
    start_time = time.time()
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                found_keywords = [k for k in keywords if k.lower() in content]
                if found_keywords:
                    result = f"У файлі {file_path} знайдено ключові слова: {', '.join(found_keywords)}"
                    end_time = time.time()
                    result += f" (Час виконання: {end_time - start_time:.2f} секунд)"
                    queue.put(result)
        except Exception as e:
            queue.put(f"Помилка при обробці файлу {file_path}: {e}")    

def search_files_in_directory(directory, keywords, queue):
    """Функція для пошуку ключових слів у всіх файлах директорії."""
    processes = []
    files_to_process = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)
                files_to_process.append(file_path)

    # Розділити файли між процесами
    num_processes = os.cpu_count()  # Кількість доступних процесорів
    chunk_size = len(files_to_process) // num_processes + 1
    print(f"Кількість процесів: {num_processes}, Кількість файлів: {len(files_to_process)}")

    for i in range(num_processes // chunk_size + 1):
        start_index = i * chunk_size
        end_index = min(start_index + chunk_size, len(files_to_process))
        process_files = files_to_process[start_index:end_index]
                
        process = Process(target=search_in_file, args=(process_files, keywords, queue))
        processes.append(process)
        process.start()
        print(f"Запущено процес: {process.name} для файлів: {process_files}")

    for process in processes:
        process.join()

    # Отримання та виведення всіх результатів з черги
    while not queue.empty():
        print(queue.get())

if __name__ == "__main__":
    keywords = ["представляє", "пропонує", "місто"]
    directory = "./txt/"
    queue = Queue()

    search_files_in_directory(directory, keywords, queue)

    # Закриття черги
    queue.close()
    queue.join_thread()