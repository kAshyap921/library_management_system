import csv
import os


# only sirf save aur load

class CSVHandler:

    @staticmethod
    def load(filepath):
        if not os.path.exists(filepath):
            return[]
        try:
            with open(filepath, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"File padhne mein error: {e}")
            return []

    @staticmethod
    def save(filepath, data, fieldnames):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", newline="",encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(f"File save karne mein error: {e}")

    @staticmethod
    def append_row(filepath, row, fieldnames):
        file_exists = os.path.exists(filepath)
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
               
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
        except Exception as e:
            print(f"Row add karne mein error: {e}")

    @staticmethod
    def find_one(filepath, key, value):
      
        rows = CSVHandler.load(filepath)
        for row in rows:
            if row.get(key) == value:
                return row
        return None

    @staticmethod
    def update_row(filepath, key, value, updated_data, fieldnames):
        rows = CSVHandler.load(filepath)
        found = False
        for i, row in enumerate(rows):
            if row.get(key) == value:
                rows[i].update(updated_data)
                found = True
                break
        if found:
            CSVHandler.save(filepath, rows, fieldnames)
        return found

    @staticmethod
    def delete_row(filepath, key, value, fieldnames):
        rows = CSVHandler.load(filepath)
        new_rows = [r for r in rows if r.get(key) != value]
        CSVHandler.save(filepath, new_rows, fieldnames)