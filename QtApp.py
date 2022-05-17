import socket
import threading

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtWidgets, QtCore, QtGui

import sys  # Только для доступа к аргументам командной строки

# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)

stop_threading = False

class RegisterWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(160, 80)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 160, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.name_edit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.name_edit.setObjectName("name_edit")
        self.verticalLayout.addWidget(self.name_edit)
        self.name_confirmation = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.name_confirmation.setCheckable(False)
        self.name_confirmation.setObjectName("name_confirmation")
        self.verticalLayout.addWidget(self.name_confirmation)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ввод имени"))
        self.label.setText(_translate("MainWindow", "Введите имя"))
        self.name_confirmation.setText(_translate("MainWindow", "Подтвердить"))
        self.name_confirmation.clicked.connect(self.onclick)

    def onclick(self):
        global main_window
        self.name = self.name_edit.text()
        main_window(self.name)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, name):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(393, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.enter_message = QtWidgets.QLineEdit(self.centralwidget)
        self.enter_message.setGeometry(QtCore.QRect(0, 564, 331, 31))
        self.enter_message.setObjectName("enter_message")
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(340, 560, 41, 31))
        self.send_button.setStyleSheet("border-radius: 4px;")
        self.send_button.setText("Send")
        self.send_button.setObjectName("send_button")
        self.show_messages = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.show_messages.setEnabled(True)
        self.show_messages.setGeometry(QtCore.QRect(3, 9, 331, 541))
        self.show_messages.setStyleSheet("background: #333; color: #eee;")
        self.show_messages.setReadOnly(True)
        self.show_messages.setPlainText("")
        self.show_messages.setObjectName("show_messages")
        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(340, 10, 51, 25))
        self.clear_button.setStyleSheet("border: none;\n"
"border-bottom: 2px solid gray;\n"
"background: #222;\n"
"color: #eee;")
        self.clear_button.setObjectName("clear_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sor.bind(('', 0))  # Задаем сокет как клиент
        self.name = name
        self.server = 'localhost', 5050  # Данные сервера

        self.sor.sendto((self.name + ' Connect to server').encode('utf-8'), self.server)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.clear_button.setText(_translate("MainWindow", "Clear"))
        self.send_button.clicked.connect(self.send)
        self.clear_button.clicked.connect(self.clear)

    def append_message(self, message):
        message = message.strip()
        if len(message) > 0:
            self.show_messages.setPlainText(message + '\n' + self.show_messages.toPlainText() )

    def send(self):
        mensahe = self.enter_message.text()
        self.sor.sendto(('[' + self.name + ']' + mensahe).encode('utf-8'), self.server)
        self.append_message(mensahe)
        print('sended')

    def clear(self):
        self.show_messages.setPlainText("")

    def start_read(self):
        def read_sok():
            global stop_threading
            while 1:
                data = self.sor.recv(1024)
                print('data readed')
                self.append_message(data.decode('utf-8'))
                if stop_threading:
                    break

        self.potok = threading.Thread(target=read_sok)
        self.potok.start()

    def closeEvent(self, event):
        global stop_threading
        stop_threading = True
        self.sor.sendto(('Server:   ' + self.name + ' покидает чат').encode('utf-8'), self.server)
        self.potok.join()
        event.accept()


class InputFrame(QtWidgets.QMainWindow, RegisterWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MainFrame(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, name):
        super().__init__()
        self.setupUi(self, name)


window = InputFrame()
window.show()  # Важно: окно по умолчанию скрыто.
m_window = None


def main_window(name):
    global m_window
    window.close()
    m_window = MainFrame(name)
    m_window.show()
    m_window.start_read()


# Запускаем цикл событий.
app.exec()

"""
import socket
import threading
def read_sok():
     while 1 :
         data = sor.recv(1024)
         print(data.decode('utf-8'))
 server = '192.168.0.1', 5050  # Данные сервера
 alias = input() # Вводим наш псевдоним
 sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 sor.bind(('', 0)) # Задаем сокет как клиент
 sor.sendto((alias+' Connect to server').encode('utf-8'), server)# Уведомляем сервер о подключении
 potok = threading.Thread(target= read_sok)
 potok.start()
 while 1 :
     mensahe = input()
     sor.sendto(('['+alias+']'+mensahe).encode('utf-8'), server)
"""