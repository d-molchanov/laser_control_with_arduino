
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
from arduino import ArduinoCommunication
from mcu import FakeCommunicationTread


class Communicate(QObject):
    speak = Signal(str)



class MainWindow(QMainWindow, MainWindowGUI):
    """Class for creating main application window"""
    def __init__(self):
        super().__init__()
        self.init_gui()

        # self.arduino_com = ArduinoCommunication()
        self.arduino_com = FakeCommunicationTread()
        self.arduino_com.data_received.connect(self.test_thread)

        self.response = Communicate()
        self.connection = None
        self.update_ports()
        self.btn_refresh.clicked.connect(self.update_ports)

        # self.btn_send.pressed.connect(lambda: self.btn_send.setDisabled(True))
        self.btn_send.clicked.connect(self.send_to_mcu_new)
        self.btn_connect.clicked.connect(self.connect_to_port)
        self.btn_disconnect.clicked.connect(self.disconnect)
        self.spb_intensity.focusOutEvent = self.on_focus_out
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
        self.arduino_com.start()

    def test_thread(self, data):
        print(data)

    @Slot(str)    
    def test_signal(self):
        print("Hello!")

    def stop_laser_activity(self):
        self.spb_intensity.setValue(3)
        self.spb_frequency.setValue(0)
        if self.connection:
            self.btn_stop.setDisabled(True)
            self.send_to_mcu_new()

    def disconnect(self):
        if self.connection:
            self.arduino_com.close_connection(self.connection)

    def connect_to_port(self):
        port = self.cbx_port.currentText()
        baudrate = self.cbx_baudrate.currentText()
        self.connection = self.arduino_com.connect_to_port(port, baudrate)
        print(f'After connection: {self.connection = }')


    def choose_single_pulse_mode(self):
        self.lbl_frequency.setText('Duration, μs:')
        self.spb_frequency.setDisabled(False)

    def choose_periodic_mode(self):
        self.lbl_frequency.setText('Frequency, Hz:')
        self.spb_frequency.setDisabled(False)

    def choose_continuous_mode(self):
        self.lbl_frequency.setText('')
        self.spb_frequency.setDisabled(True)

    def on_focus_out(self, event):
        value = self.spb_intensity.value()
        mod4 = value % 4
        if mod4 != 3:
            value = (value // 4)*4 + 3
        self.spb_intensity.setValue(value)

    def update_ports(self):
        ports = self.arduino_com.check_available_ports()
        self.cbx_port.clear()
        self.cbx_port.addItems(ports)

    def send_to_mcu(self):
        frequency = self.spb_frequency.value()
        baud_rate = self.cbx_baudrate.currentText()
        intensity = self.spb_intensity.value()
        if self.rbt_single_pulse.isChecked():
            mode = 's'
        elif self.rbt_periodic.isChecked():
            mode = 'p'
        else:
            mode = 'c'
            frequency = 0
        print(f'{mode}{frequency}:{intensity}')

        self.arduino_com.send_data(
            self.cbx_port.currentText(),
            int(baud_rate), 
            f'{mode}{frequency}:{intensity}'
        )

        self.update_pins(intensity)

    def send_to_mcu_new(self):
        # self.btn_stop.setDisabled(True)
        if self.connection:
            frequency = self.spb_frequency.value()
            baud_rate = self.cbx_baudrate.currentText()
            intensity = self.spb_intensity.value()
            if self.rbt_single_pulse.isChecked():
                mode = 's'
            elif self.rbt_periodic.isChecked():
                mode = 'p'
            else:
                mode = 'c'
                frequency = 0
            # print(f'{mode}{frequency}:{intensity}')
            data = f'{mode}{frequency}:{intensity}'

            # self.response = self.arduino_com.send_data_new(
            #     self.connection,
            #     f'{mode}{frequency}:{intensity}'
            # )
            print(f'{data = }')
            print(f'{self.connection = }')
            self.arduino_com.send_data_signal.emit(data)
            # print(f'{self.response = }')
            self.update_pins(intensity)
            # self.btn_send.setEnabled(True)
            # self.btn_stop.setDisabled(False)

    def update_pins(self, value: int) -> None:
        for i in range(1, 11):
            self.pins[i].setCheckBoxState(False)
        pins_state = [(value>>i) & 1 for i in range(11, -1, -1)]    
        for el, pin in zip(pins_state, self.pins[1:11]):
            pin.setCheckBoxState(el)
        # list_value = [int(el) for el in list(bin(int(self.spb_intensity.value()))[2:])]
        # bin_value = [0]*(12 - len(list_value)) + list_value
        # for el, pin in zip(bin_value, self.pins[1:11]):
        #     pin.setCheckBoxState(el)
        # print(bin_value)
        # test = []
        # for i in range(12):
        #     test.append((value>>i) & 1)
        # print(test[::-1])


def test() -> None:
    """Function for testing MainWindow class methods"""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    test()