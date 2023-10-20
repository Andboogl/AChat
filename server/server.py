from loguru import logger
import threading
import socket
import pickle


# Налаштовуємо логгер
logger.add(
    'log.log',
    format='{time} | {level} | {message}'
)


# Класс серверу
class Server:
    def __init__(self, ip, port):
        self.server = socket.socket()
        self.server.bind((ip, port))
        self.server.listen()

        self.users = []  # Список користувачів

        logger.info('Сервер запущений')

        self.users_monitor()


    # Моніторінг підключень
    def users_monitor(self):
        while True:
            user, adress = self.server.accept()
            user_nikname = user.recv(1024)
            user_nikname = pickle.loads(user_nikname)

            # Розсилаємо всім повідомлення про підключення
            for _ in self.users:
                request = ['NEW_USER', user_nikname]
                _.send(pickle.dumps(request))

            self.users.append(user)  # Додаємо користувача у список користувачів

            # Запускаємо обробник користувача
            threading.Thread(target=self.user_handler, args=(user, user_nikname)).start()

            logger.info(f'До серверу підʼєднався новий користучав з нікнеймом {user_nikname}')

    # Обробник користувача
    def user_handler(self, user, nikname):
        logger.info('Запущений обробник користувача')

        while True:
            user_request = user.recv(1024)
            user_request = pickle.loads(user_request)

            if user_request[0] == 'MESSAGE':
                for _ in self.users:
                    if _ == user:
                        request = ['MESSAGE', user_request[1], 'Ви']

                    else:
                        request = ['MESSAGE', user_request[1], nikname]
                        _.send(pickle.dumps(request))

                logger.info(f'Користувач {nikname} відправив/відправила повідомлення {user_request[1]}')

            elif user_request[0] == 'EXIT':
                for _ in self.users:
                    request = ['EXIT', nikname]
                    _.send(pickle.dumps(request))

                self.users.remove(user)
                logger.info(f'Користувач {nikname} вийшов/вийшла з сервера')
                break


if __name__ == '__main__':
    Server('127.0.0.1', 5555)
