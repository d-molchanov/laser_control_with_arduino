from serial import Serial
from serial.tools.list_ports import comports
from serial.serialutil import SerialException
from PySide6.QtCore import QThread, Signal

import serial
import time
import logging
import random


logging.basicConfig(
    format='%(asctime)s %(levelname)s:\t%(message)s',
    level=logging.INFO
)


class FakeCommunicationTread(QThread):
    data_received = Signal(str)
    send_data_signal = Signal(str, str)
    send_request_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.ports = []
        self.active_port = None
        self.request = None
        self.running = True
        self.send_data_signal.connect(self.send_data_new)
        # self.send_data_signal.connect(lambda: self.send_data_new(self.active_port, self.request))

    def run(self):
        while self.running:
            if self.request:
                logging.info('Message `%s` was sent to <%s>.', self.request, self.active_port)
                logging.info('Waiting for answer ...')
                time.sleep(1)
                logging.info('Answer was received from <%s>: %s', self.active_port, self.request)
                self.data_received.emit(self.request)
                self.request = None
                # t = random.randint(1, 5)
                # print(f'Sleeping {t} seconds...')
                # time.sleep(t)
                # self.data_received.emit(self.request)
                # self.request = None

    def check_available_ports(self) -> list:
        return [
            f'COM{i}' for i in range(1, 5)
        ]

    def connect_to_port(self, port, baud_rate) -> None:
        logging.info('Initializing port <%s> ...', port)
        time.sleep(2)
        self.active_port = port
        logging.info('Port <%s> was opened.', port)
        return self.active_port

    def send_data_new(self, ser, data) -> None:
        self.request = data
        # logging.info('Message `%s` was sent to <%s>.', data, self.active_port)
        # logging.info('Waiting for answer ...')
        # time.sleep(1)
        # logging.info('Answer was received from <%s>: %s', self.active_port, data)
        # self.data_received.emit(data)
        # self.request = None
        return data

    def close_connection(self) -> None:
        if self.active_port:
            logging.info('Port <%s> was closed.', self.active_port)
            self.active_port = None
            self.running = False
            self.wait()

    def send_data(self, port, baud_rate, data) -> None:
        try:
            logging.info('Initializing port <%s> ...', port)
            ser = Serial(port, baud_rate, timeout=0.5)
            time.sleep(2)
            ser.flushInput()
            ser.flushOutput()
            logging.info('Port <%s> was opened.', port)

            ser.write(data.encode(encoding='UTF-8'))
            logging.info('Message `%s` was sent to <%s>.', data, port)
            logging.info('Waiting for answer ...')
            time.sleep(2)

            response = [r.replace(':', ' was set to ') for r in ser.readall().decode('utf-8').split()]
            logging.info('Answer was received from <%s>: %s, %s, %s', port, *response)
            ser.close()
            logging.info('Port <%s> was closed.', port)
        except SerialException as e:
            logging.error('Port <%s> could not be opened. Check connection.', port)


class MCUCommunicationTread(QThread):
    data_received = Signal(str)
    send_data_signal = Signal(str, str)
    send_request_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.ports = []
        self.serial_port = None
        self.active_port = None
        self.request = None
        self.running = True
        self.send_data_signal.connect(self.send_data_new)
        # self.send_data_signal.connect(lambda: self.send_data_new(self.active_port, self.request))

    def run(self):
        while self.running:
            if self.request:
                try:
                    self.serial_port.write(self.request.encode(encoding='UTF-8'))
                    logging.info('Message `%s` was sent to <%s>.', self.request, self.active_port)
                    logging.info('Waiting for answer ...')
                    time.sleep(1)
                    response = [
                        r.replace(':', ' was set to ') for r in 
                        self.serial_port.readall().decode('utf-8').split()
                    ]
                    logging.info('Answer was received from <%s>: %s, %s, %s', self.active_port, *response)
                    self.data_received.emit(self.request)
                except SerialException as e:
                    logging.error('Port <%s> could not be opened. Check connection.', self.active_port)
                self.request = None

                # logging.info('Message `%s` was sent to <%s>.', self.request, self.active_port)
                # logging.info('Waiting for answer ...')
                # time.sleep(1)
                # logging.info('Answer was received from <%s>: %s', self.active_port, self.request)
                # self.data_received.emit(self.request)
                # self.request = None
                # t = random.randint(1, 5)
                # print(f'Sleeping {t} seconds...')
                # time.sleep(t)
                # self.data_received.emit(self.request)
                # self.request = None

    def check_available_ports(self) -> list:
        return [
            port.device for port in list(comports())
        ]

    def connect_to_port(self, port, baud_rate) -> None:
        try:
            logging.info('Initializing port <%s> ...', port)
            ser = Serial(port, baud_rate, timeout=0.5)
            time.sleep(2)
            ser.flushInput()
            ser.flushOutput()
            self.active_port = port
            self.serial_port = ser
            logging.info('Port <%s> was opened.', port)
            return ser
        except SerialException as e:
            logging.error('Port <%s> could not be opened. Check connection.', port)
            return None
        # logging.info('Initializing port <%s> ...', port)
        # time.sleep(2)
        # self.active_port = port
        # logging.info('Port <%s> was opened.', port)
        # return self.active_port

    def send_data_new(self, ser, data) -> None:
        self.request = data
        # logging.info('Message `%s` was sent to <%s>.', data, self.active_port)
        # logging.info('Waiting for answer ...')
        # time.sleep(1)
        # logging.info('Answer was received from <%s>: %s', self.active_port, data)
        # self.data_received.emit(data)
        # self.request = None
        return data

    def close_connection(self) -> None:
        if self.active_port:
            try:
                self.serial_port.close()
                logging.info('Port <%s> was closed.', self.active_port)
                self.active_port = None
                self.serial_port = None
                self.running = False
                self.wait()
            except SerialException as e:
                logging.error('Port <%s> could not be opened. Check connection.', self.active_port)
        
        # if self.active_port:
        #     logging.info('Port <%s> was closed.', self.active_port)
        #     self.active_port = None
        #     self.running = False
        #     self.wait()

    def send_data(self, port, baud_rate, data) -> None:
        try:
            logging.info('Initializing port <%s> ...', port)
            ser = Serial(port, baud_rate, timeout=0.5)
            time.sleep(2)
            ser.flushInput()
            ser.flushOutput()
            logging.info('Port <%s> was opened.', port)

            ser.write(data.encode(encoding='UTF-8'))
            logging.info('Message `%s` was sent to <%s>.', data, port)
            logging.info('Waiting for answer ...')
            time.sleep(2)

            response = [r.replace(':', ' was set to ') for r in ser.readall().decode('utf-8').split()]
            logging.info('Answer was received from <%s>: %s, %s, %s', port, *response)
            ser.close()
            logging.info('Port <%s> was closed.', port)
        except SerialException as e:
            logging.error('Port <%s> could not be opened. Check connection.', port)