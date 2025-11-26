import subprocess
import time
import threading
from getAllCategories import get_all_leaf_links

# Максимум одновременно работающих скриптов
MAX_PROCESSES = 10

tasks = get_all_leaf_links()
for link in tasks:
        print(link)
        
#tasks = [
    #"https://lalafo.kg/kyrgyzstan/avtomobili-s-probegom/prodazha-avtomobiley/changan",
    #"https://lalafo.kg/kyrgyzstan/avtomobili-s-probegom/prodazha-avtomobiley/daihatsu",
    #"https://lalafo.kg/kyrgyzstan/avtomobili-s-probegom/prodazha-avtomobiley/exeed",
    #"https://lalafo.kg/kyrgyzstan/avtomobili-s-probegom/prodazha-avtomobiley/isuzu-avtomobili-s-probegom",
    # ... добавляй сколько хочешь
#]

# Список активных процессов
processes = []


def stream_output(proc, name):
    """Читает вывод процесса в реальном времени."""
    for line in proc.stdout:
        print(f"[{name}] {line.rstrip()}")


def start_new_task(url):
    print(f"▶ Запуск: {url}")

    proc = subprocess.Popen(
        ["py", "-X", "utf8", "parceCategory.py", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        bufsize=1
    )

    # Запускаем отдельный поток, чтобы читать stdout
    thread = threading.Thread(target=stream_output, args=(proc, url), daemon=True)
    thread.start()

    return proc


while tasks or processes:

    # Убираем завершённые процессы
    for p in processes[:]:
        if p.poll() is not None:  # процесс закончил работу
            print(f"✔ Завершён PID={p.pid}")
            processes.remove(p)

    # Запускаем новые пока не достигнут лимит
    while tasks and len(processes) < MAX_PROCESSES:
        url = tasks.pop(0)
        proc = start_new_task(url)
        processes.append(proc)

    time.sleep(0.2)

print("🎉 Все задачи выполнены.")
