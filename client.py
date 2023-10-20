from loguru import logger
import threading
import socket
import pickle


# Налаштовуємо логгер
logger.add(
    'log.log',
    format='{time} | {level} | {message}'
)


# Класс кліента
class Client:
    def __init__(self, ip, port, nikname, text_browser):
        self.client = socket.socket()
        self.client.connect((ip, port))
        self.client.send(pickle.dumps(nikname))

        self.text_browser = text_browser
        self.nikname = nikname

        threading.Thread(target=self.message_monitor).start()  # Запускаємо моніторінг повідомлень з серверу
        self.text_browser.append('Ви успішно підключилися к серверу!')
        logger.info('Підключення з сервером створене')

    # Моніторінг повідомлень
    def message_monitor(self):
        while True:
            msg = self.client.recv(1024)
            msg = pickle.loads(msg)

            if msg[0] == 'MESSAGE':
                text = f'{msg[2]}: {msg[1]}'
                self.text_browser.append(text)
                logger.info(text)

            elif msg[0] == 'EXIT':
                text = f'{msg[1]} вийшов/вийшла з чату!'
                self.text_browser.append(text)
                logger.info(text)

            elif msg[0] == 'NEW_USER':
                text = f'{msg[1]} підʼєднався/підʼєдналася до чату!'
                self.text_browser.append(text)
                logger.info(text)

    # Відправити повідомлення на сервер
    def send_message(self, msg):
        request = ['MESSAGE', msg]
        self.client.send(pickle.dumps(request))
        self.text_browser.append(f'Ви ({self.nikname}): {request[1]}')

    # Вийти з чату
    def exit_out(self):
        request = ['EXIT']
        self.client.send(pickle.dumps(request))
        self.client.close()
