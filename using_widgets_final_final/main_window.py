
"""Module contains class MainWindow for creating
main application window
"""
import sys
from typing import List
from PySide6.QtCore import QObject
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QVBoxLayout
import logging


from gui.main_window_gui import MainWindowGUI
# from arduino import ArduinoCommunication
# from mcu import FakeCommunicationTread
from mcu import MCUCommunicationTread


# class Communicate(QObject):
#     speak = Signal(str)



class MainWindow(QMainWindow, MainWindowGUI):
    """Class for creating main application window"""
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.STOP_LASER_REQUEST = 't'
        # self.arduino_com = ArduinoCommunication()
        # self.arduino_com = FakeCommunicationTread()
        self.arduino_com = MCUCommunicationTread()
        self.arduino_com.data_received.connect(self.receive_response)
        # self.arduino_com.start()

        self.response = None
        # self.connection = None
        self.update_ports()
        self.btn_refresh.clicked.connect(self.update_ports)

        # self.btn_generate.pressed.connect(lambda: self.btn_generate.setDisabled(True))
        self.btn_generate.clicked.connect(self.send_to_mcu_new)
        self.btn_connect.clicked.connect(self.connect_to_port)
        self.btn_disconnect.clicked.connect(self.disconnect)
        self.rbt_single_pulse.clicked.connect(
            self.choose_single_pulse_mode
        )
        self.rbt_periodic.clicked.connect(
            self.choose_periodic_mode
        )
        self.rbt_continuous.clicked.connect(
            self.choose_continuous_mode

        )
        self.btn_stop.clicked.connect(self.stop_laser_activity)
        self.cbx_duration_units.currentTextChanged.connect(self.change_duration_range)
        self.cbx_pause_units.currentTextChanged.connect(self.change_pause_range)

    def change_duration_range(self):
        if self.cbx_duration_units.currentText() == 'μs':
            self.spb_frequency.setRange(1, 16000)
            self.cbx_pause_units.setCurrentIndex(0)
        if self.cbx_duration_units.currentText() == 'ms':
            self.spb_frequency.setRange(1, 100000)
            self.cbx_pause_units.setCurrentIndex(1)


    def change_pause_range(self):
        if self.cbx_pause_units.currentText() == 'μs':
            self.spb_pause.setRange(1, 16000)
            self.cbx_duration_units.setCurrentIndex(0)
        if self.cbx_pause_units.currentText() == 'ms':
            self.spb_pause.setRange(1, 100000)
            self.cbx_duration_units.setCurrentIndex(1)

    def parse_response(self, response: str, separator: str) -> dict:
        if not response:
            return {}
        splitted_response = response.strip().split(separator)
        return {
            'mode': splitted_response[0],
            'intensity': int(splitted_response[1]),
            'pulse_duration': int(splitted_response[2]),
            'pause_duration': int(splitted_response[3]),
            'iterations': int(splitted_response[4])
        }



    def receive_response(self, data):
        print(f'{data=}')
        response = self.parse_response(data, ';')
        print(f'{response = }')
        if not response:
            logging.error('There is no response from MCU.')
        else: 
            if response['mode'] in ['s', 'l', 'p', 'm', 'c']:
                self.pins[0].setCheckBoxState(True)
            else:
                self.pins[0].setCheckBoxState(False)
            self.update_pins(response['intensity'])
            self.btn_generate.setEnabled(True)
            self.gbx_mode.setEnabled(True)
        # response = data.split(':')
        # mode = 't'
        # frequency = 0
        # intensity = 0
        # if len(response) > 0:
        #     if len(response[0]) > 0:
        #         mode = response[0][0]
        #         frequency = int(response[0][1:])
        # if len(response) > 1:
        #     intensity = int(response[1])
        # self.btn_generate.setEnabled(True)
        # self.gbx_mode.setEnabled(True)
        # self.update_pins(intensity)

        # if mode in {'s', 'l', 'c'}:
        #     self.pins[0].setCheckBoxState(True)
        # else:
        #     self.pins[0].setCheckBoxState(False)


    @Slot(str)    
    def test_signal(self):
        print("Hello!")

    def stop_laser_activity(self):
        self.spb_intensity.setValue(3)
        self.spb_frequency.setValue(0)
        if self.arduino_com.active_port:
            # self.btn_stop.setDisabled(True)
            # self.send_to_mcu_new()
            # self.arduino_com.send_data_signal.emit(self.connection, 't0:3')
            self.arduino_com.send_data_signal.emit(self.arduino_com.active_port, self.STOP_LASER_REQUEST)
            self.gbx_mode.setDisabled(True)
            self.btn_generate.setDisabled(True)

    def disconnect(self):
        self.arduino_com.close_connection()

    def connect_to_port(self):
        self.arduino_com.start()
        
        port = self.cbx_port.currentText()
        baudrate = self.cbx_baudrate.currentText()
        self.arduino_com.connect_to_port(port, baudrate)


    def choose_single_pulse_mode(self):
        # self.lbl_frequency.setText('Duration:')
        self.lbl_pause.setHidden(True)
        self.spb_pause.setHidden(True)
        self.cbx_pause_units.setHidden(True)
        self.lbl_amount.setHidden(True)
        self.spb_amount.setHidden(True)
        self.hcontainer_frequency.setDisabled(False)
        if self.arduino_com.active_port:
            self.arduino_com.send_data_signal.emit(self.arduino_com.active_port, self.STOP_LASER_REQUEST)
            self.gbx_mode.setDisabled(True)
            self.btn_generate.setDisabled(True)




    def choose_periodic_mode(self):
        # self.lbl_frequency.setText('Frequency, Hz:')
        self.lbl_pause.setHidden(False)
        self.spb_pause.setHidden(False)
        self.cbx_pause_units.setHidden(False)
        self.lbl_amount.setHidden(False)
        self.spb_amount.setHidden(False)
        self.hcontainer_frequency.setEnabled(True)
        if self.arduino_com.active_port:
            self.arduino_com.send_data_signal.emit(self.arduino_com.active_port, self.STOP_LASER_REQUEST)
            self.gbx_mode.setDisabled(True)
            self.btn_generate.setDisabled(True)





    def choose_continuous_mode(self):
        # self.lbl_frequency.setText('')
        self.hcontainer_frequency.setDisabled(True)
        if self.arduino_com.active_port:
            self.arduino_com.send_data_signal.emit(self.arduino_com.active_port, self.STOP_LASER_REQUEST)
            self.gbx_mode.setDisabled(True)
            self.btn_generate.setDisabled(True)


        

    def update_ports(self):
        ports = self.arduino_com.check_available_ports()
        self.cbx_port.clear()
        self.cbx_port.addItems(ports)

    # def send_to_mcu(self):
    #     frequency = self.spb_frequency.value()
    #     baud_rate = self.cbx_baudrate.currentText()
    #     intensity = self.spb_intensity.value()
    #     if self.rbt_single_pulse.isChecked():
    #         mode = 's'
    #     elif self.rbt_periodic.isChecked():
    #         mode = 'p'
    #     else:
    #         mode = 'c'
    #         frequency = 0
    #     print(f'{mode}{frequency}:{intensity}')

    #     self.arduino_com.send_data(
    #         self.cbx_port.currentText(),
    #         int(baud_rate), 
    #         f'{mode}{frequency}:{intensity}'
    #     )

    #     # self.update_pins(intensity)

    def create_request_from_gui(self):
        frequency = self.spb_frequency.value()
        baud_rate = self.cbx_baudrate.currentText()
        intensity = self.spb_intensity.value()
        if self.rbt_single_pulse.isChecked():
            if self.cbx_duration_units.currentText() == 'μs':
                mode = 's'
            elif self.cbx_duration_units.currentText() == 'ms':
                mode = 'l'
        elif self.rbt_periodic.isChecked():
            mode = 'p'
        else:
            mode = 'c'
            frequency = 0
        request = f'{mode}{frequency}:{intensity}'
        return request

    def send_request_to_mcu(self, request: str) -> None:
        if self.arduino_com.active_port:
            # self.arduino_com.send_data_signal.emit(self.connection, request)
            self.arduino_com.send_data_signal.emit(self.arduino_com.active_port, request)
            self.btn_generate.setDisabled(True)
            self.gbx_mode.setDisabled(True)


    def send_to_mcu_new(self):
        if self.arduino_com.active_port:
            # frequency = self.spb_frequency.value()
            # baud_rate = self.cbx_baudrate.currentText()
            # intensity = self.spb_intensity.value()
            # if self.rbt_single_pulse.isChecked():
            #     mode = 's'
            # elif self.rbt_periodic.isChecked():
            #     mode = 'p'
            # else:
            #     mode = 'c'
            #     frequency = 0
            # data = f'{mode}{frequency}:{intensity}'
            data = self.create_request_from_gui()
            print(f'{data = }')
            # print(f'{self.connection = }')
            # self.arduino_com.send_data_signal.emit(self.connection, data)
            self.arduino_com.send_data_signal.emit(self.arduino_com.active_port, data)
            self.btn_generate.setDisabled(True)
            self.gbx_mode.setDisabled(True)


    def update_pins(self, value: int) -> None:
        for i in range(1, 11):
            self.pins[i].setCheckBoxState(False)
        pins_state = [(value>>i) & 1 for i in range(11, -1, -1)]    
        for el, pin in zip(pins_state, self.pins[1:11]):
            pin.setCheckBoxState(el)

    def closeEvent(self, *args, **kwargs):
        self.arduino_com.running = False
        self.arduino_com.wait()


def test() -> None:
    """Function for testing MainWindow class methods"""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    test()