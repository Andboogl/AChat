import pickle
import os


# Зберегти налаштування
def save_settings(ip, port, nikname):
    # Якщо файл налаштувань вже існує
    if os.path.exists('data/settings'):
        with open('data/settings', 'wb') as file:
            data = {
                'ip': ip,
                'port': port,
                'nikname': nikname,
            }
            pickle.dump(data, file)


    # Якщо файлу налаштувань ще не існує
    else:
        with open('data/settings', 'xb') as file:
            data = {
                'ip': ip,
                'port': port,
                'nikname': nikname,
            }
            pickle.dump(data, file)


# Загрузити налаштування
def load_settings():
    # Якщо файл налаштувань існує
    if os.path.exists('data/settings'):
        with open('data/settings', 'rb') as file:
            data = pickle.load(file)
            return data


    # Якщо файлу налаштувань не існує
    else:
        return None
