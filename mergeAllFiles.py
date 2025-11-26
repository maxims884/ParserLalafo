import os
import openpyxl


INPUT_DIR = "excel_category"
OUTPUT_PREFIX = "all_"
ROWS_PER_FILE = 20000

# --- ПУТЬ К ТЕКУЩЕМУ СКРИПТУ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- ПАПКА ДЛЯ ФАЙЛОВ ---
EXCEL_FINAL_DIR = os.path.join(BASE_DIR, "excel_final")

# создаём папку, если она не существует
os.makedirs(EXCEL_FINAL_DIR, exist_ok=True)


def merge_excels():
    input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), INPUT_DIR)

    # собираем все xlsx
    files = [f for f in os.listdir(input_path) if f.endswith(".xlsx")]
    if not files:
        print("❌ Нет Excel-файлов ")
        return

    print(f"Найдено файлов: {len(files)}")

    all_rows = []
    header = None

    # ---- читаем все файлы ----
    for filename in files:
        full = os.path.join(input_path, filename)
        print(f"Читаю: {filename}")

        wb = openpyxl.load_workbook(full)
        sheet = wb.active

        rows = list(sheet.values)

        # первая строка — заголовок
        if header is None:
            header = rows[0]

        # пропускаем дублирующийся header
        data_rows = rows[1:]
        all_rows.extend(data_rows)

    print(f"Всего собрано строк: {len(all_rows)}")

    # ---- делим на файлы по 20к ----
    total_parts = (len(all_rows) + ROWS_PER_FILE - 1) // ROWS_PER_FILE

    print(f"Будет создано файлов: {total_parts}")

    for part in range(total_parts):
        start = part * ROWS_PER_FILE
        end = start + ROWS_PER_FILE
        chunk = all_rows[start:end]

        out_wb = openpyxl.Workbook()
        out_sheet = out_wb.active

        # записываем заголовок
        out_sheet.append(header)

        # записываем строки
        for row in chunk:
            out_sheet.append(row)

        out_filename = f"{OUTPUT_PREFIX}{part + 1}.xlsx"
        out_full_path = os.path.join(EXCEL_FINAL_DIR, out_filename)

        out_wb.save(out_full_path)
        print(f"✔ Сохранён {out_filename} ({len(chunk)} строк)")


if __name__ == "__main__":
    merge_excels()
