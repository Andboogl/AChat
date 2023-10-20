from PyQt6.QtWidgets import QMessageBox


# Чи є obj цілим числом
def is_number(obj):
    try:
        int(obj)
        return True

    except:
        return False


# Чи пуста строка
def is_empty(string): return True if string.strip() == '' else False


# Показати повідомлення
def show_message(window, text):
    messageBox = QMessageBox(window)
    messageBox.setText(text)
    messageBox.exec()
