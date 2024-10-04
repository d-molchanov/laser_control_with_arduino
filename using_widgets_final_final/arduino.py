from serial import Serial
from serial.tools.list_ports import comports
from serial.serialutil import SerialException

import serial
import time
import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)s:\t%(message)s',
    level=logging.INFO
)


class ArduinoCommunication:


    def __init__(self):
        self.ports = []
        self.active_port = None

    def check_available_ports(self) -> list:
        return [
            port.device for port in list(comports())
        ]

    def connect_to_port(self, port, baud_rate) -> Serial:
        try:
            logging.info('Initializing port <%s> ...', port)
            ser = Serial(port, baud_rate, timeout=0.5)
            time.sleep(2)
            ser.flushInput()
            ser.flushOutput()
            self.active_port = port
            logging.info('Port <%s> was opened.', port)
            return ser
        except SerialException as e:
            logging.error('Port <%s> could not be opened. Check connection.', port)
            return None

    def send_data_new(self, ser: Serial, data) -> None:
        try:
            ser.write(data.encode(encoding='UTF-8'))
            logging.info('Message `%s` was sent to <%s>.', data, self.active_port)
            logging.info('Waiting for answer ...')
            time.sleep(1)
            response = [r.replace(':', ' was set to ') for r in ser.readall().decode('utf-8').split()]
            logging.info('Answer was received from <%s>: %s, %s, %s', self.active_port, *response)
        except SerialException as e:
            logging.error('Port <%s> could not be opened. Check connection.', self.active_port)

    def close_connection(self, ser: Serial) -> None:
        try:
            ser.close()
            logging.info('Port <%s> was closed.', self.active_port)
        except SerialException as e:
            logging.error('Port <%s> could not be opened. Check connection.', self.active_port)

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


