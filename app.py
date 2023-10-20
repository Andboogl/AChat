from design.design import Widgets
from PyQt6 import QtWidgets
from loguru import logger
from client import Client
from data import data
from sys import argv
import functions
import os


# Налаштовуємо логер
logger.add('log.log', format='{time} | {level} | {message}')
logger.info('Логгер налаштований')


# Класс вінка
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # Загружаємо віджети
        self.widgets = Widgets()
        self.widgets.setupUi(MainWindow=self)

        # Встановлюємо фіксований розмір вікна
        self.setFixedSize(640, 453)

        # Блокуємо поки-що непотрібні кнопки
        self.widgets.send_message_btn.setEnabled(False)
        self.widgets.quit_from_chat.setEnabled(False)
        self.widgets.user_message.setEnabled(False)

        # Налаштовуємо дії для кнопок
        self.widgets.save_settings_btn.clicked.connect(self.save_settings)
        self.widgets.connect_to_server_btn.clicked.connect(self.connect_to_server)
        self.widgets.send_message_btn.clicked.connect(self.send_msg)
        self.widgets.quit_from_chat.clicked.connect(self.exit)

        logger.info('Інтерфейс завантажений успішно')

        # Завантажуємо налаштування, якщо вони є
        if os.path.exists('data/settings'):
            settings = data.load_settings()
            self.widgets.server_ip.setText(settings['ip'])
            self.widgets.server_port.setText(settings['port'])
            self.widgets.user_nikname.setText(settings['nikname'])

            logger.info('Налаштування успішно завантаженні')

    # Вийти з чату
    def exit(self):
        try:
            self.client.exit_out()

            # Блокуємо кнопки
            self.widgets.send_message_btn.setEnabled(False)
            self.widgets.quit_from_chat.setEnabled(False)
            self.widgets.user_message.setEnabled(False)

            # Розблоковуємо кнопки
            self.widgets.connect_to_server_btn.setEnabled(True)
            self.widgets.save_settings_btn.setEnabled(True)

            logger.info('Виконано вихід з серверу')

        # Якщо сервер перестав працювати і ми стараємося відправити туди запрос на відкдючення ['EXIT']
        except:
            logger.error('Не вийшло вийти з сервера')

            self.widgets.send_message_btn.setEnabled(False)
            self.widgets.quit_from_chat.setEnabled(False)
            self.widgets.user_message.setEnabled(False)

            functions.show_message(self, 'Не вийшло вийти з чату. Можливо, сервер перестав працювати.')


    # Відправити повідомлення
    def send_msg(self):
        msg = self.widgets.user_message.text()

        # Якщо повідомлення не пусте
        if not functions.is_empty(msg):
            try:
                self.client.send_message(msg)
                self.widgets.user_message.clear()
                logger.info('Повідомлення відправленно')

            # Якщо программа не змогла відправити повідомлення
            except:
                logger.error('Не вдалося відправити повідлмлення')

                self.widgets.send_message_btn.setEnabled(False)
                self.widgets.quit_from_chat.setEnabled(False)
                self.widgets.user_message.setEnabled(False)

                self.widgets.connect_to_server_btn.setEnabled(True)
                self.widgets.save_settings_btn.setEnabled(True)

                functions.show_message(self, 'Не вийшло відправити повідомлення. Можливо, сервер перестав працювати.')

        else:
            functions.show_message(self, 'Ви не можете відправити пусте повідомлення')

    # Підключитися до серверу
    def connect_to_server(self):
        ip = self.widgets.server_ip.text()
        port = self.widgets.server_port.text()
        nikname = self.widgets.user_nikname.text()

        # Якщо порт є цілим числом
        if functions.is_number(port):
            if not functions.is_empty(ip) and not functions.is_empty(nikname):  # Якщо IP та нікнейм не пусті
                try:
                    self.client = Client(ip, int(port), nikname, self.widgets.textBrowser)  # Підключення до сервера

                    # Розблоковуємо кнопки
                    self.widgets.send_message_btn.setEnabled(True)
                    self.widgets.quit_from_chat.setEnabled(True)
                    self.widgets.user_message.setEnabled(True)

                    # Блокуємо кнопки підключитися та зберегти налаштування
                    self.widgets.connect_to_server_btn.setEnabled(False)
                    self.widgets.save_settings_btn.setEnabled(False)

                    logger.info('Було виконано успішне підключення до серверу')

                # Якщо не вдалося доєднатися до сервера
                except:
                    functions.show_message(self, 'Не вдалося доєднатися до серверу. Перевірте правильність данних')
                    logger.error('Не вдалося доєднатися до серверу')

            else:
                functions.show_message(self, 'Ви вказали не всі данні')

        else:
            functions.show_message(self, 'Порт повинен бути цілим числом')

    # Зберегти налаштування
    def save_settings(self):
        # Отримуємо данні з віджетів
        ip = self.widgets.server_ip.text()
        port = self.widgets.server_port.text()
        nikname = self.widgets.user_nikname.text()

        if functions.is_number(port):
            if functions.is_empty(ip) == False and functions.is_empty(nikname) == False:
                data.save_settings(ip, port, nikname)
                logger.info('Налаштування збережені')

            else:
                functions.show_message(self, 'Ви вказали не всі данні')

        else:
            functions.show_message(self, 'Порт повинен бути цілим числом')

    # Коли користувач закриває программу
    def closeEvent(self, a0):
        try:
            self.client.exit_out()
            logger.info('Виконано вихід з серверу')
            a0.accept()

        # Якщо користувач вийшов або не доєднувався до серверу
        except:
            logger.error('Не вийшло вийти з серверу, оскільки користувач не є доєднаним до нього')
            a0.accept()


def start_app():
    app = QtWidgets.QApplication(argv)
    win = MainWindow()
    win.show()
    app.exec()
