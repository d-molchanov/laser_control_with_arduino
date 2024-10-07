"""Module contains class MainWindowDesign which defines
main window design
"""
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QRadioButton


class PinWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.chx_mcu_pin = QCheckBox(self)
        self.chx_mcu_pin.setText('')
        # self.chx_mcu_pin.setStyleSheet('QCheckBox::indicator { background-color: #00d4aa; }')
        self.chx_mcu_pin.setDisabled(True)
        self.lbl_mcu_pin = QLabel()
        self.lbl_laser_pin = QLabel()
        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl_mcu_pin)
        vbox.addWidget(self.chx_mcu_pin)
        vbox.addWidget(self.lbl_laser_pin)
        self.setLayout(vbox)

    def setLaserPin(self, text):
        self.lbl_laser_pin.setText(text)

    def setMCUPin(self, text):
        self.lbl_mcu_pin.setText(text)

    def setCheckBoxState(self, value: bool):
        self.chx_mcu_pin.setChecked(value)


class MainWindowGUI:

    # def __init__(self):
    #     pass
        # super().__init__()
        # self.init_gui()

    def init_gui(self):
        # self.setStyleSheet('QWidget { border: 1px solid #000000; }')
        self.setWindowTitle('Laser Control with Arduino')
        self.setMinimumSize(400, 100)
        self.cbx_port = QComboBox(self)
        self.btn_refresh = QPushButton('Refresh', self)
        self.cbx_baudrate = QComboBox(self)
        self.cbx_baudrate.addItems(['4800', '9600', '38400', '57600', '115200'])
        self.cbx_baudrate.setCurrentIndex(1)
        self.spb_frequency = QSpinBox(self)
        self.spb_frequency.setRange(1, 1000)
        self.spb_frequency.setSingleStep(1)
        self.spb_intensity = QSpinBox(self)
        self.spb_intensity.setRange(3, 4095)    
        self.spb_intensity.setSingleStep(4)
        self.btn_generate = QPushButton('Generate', self)
        self.btn_connect = QPushButton('Connect', self)
        self.btn_disconnect = QPushButton('Disconnect', self)
        self.btn_stop = QPushButton('Stop', self)
        # self.spb_intensity.setSizePolicy(QSizePolicy.PolicyFlag.IgnoreFlag, QSizePolicy.PolicyFlag.IgnoreFlag)
        self.spb_intensity.resize(10, 80)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        self.gbx_connection = QGroupBox('Connection')

        vbox_connection = QVBoxLayout()
        vbox_connection.setSpacing(0)
        # vbox_connection.setContentsMargins(0, 0, 0, 0)
        # vbox_connection.setSpacing(8)
        # vbox_connection.addStretch(1)
        hbox_baud_rate = QHBoxLayout()
        # hbox_baud_rate.setSpacing(0)
        hbox_baud_rate.setContentsMargins(0, 0, 0, 0)

        hbox_baud_rate.addStretch(1)
        hbox_baud_rate.addWidget(QLabel('Baud rate:'))
        # hbox_baud_rate.addSpacing(4)
        hbox_baud_rate.addWidget(self.cbx_baudrate)
        hcontainer_baud_rate = QWidget(self)
        hcontainer_baud_rate.setLayout(hbox_baud_rate)
        vbox_connection.addWidget(hcontainer_baud_rate)
        vbox_connection.addSpacing(4)
        hbox_port = QHBoxLayout()
        hbox_port.setContentsMargins(0, 0, 0, 0)
        hbox_port.addStretch(1)
        hbox_port.addWidget(QLabel('Port:'))
        # hbox_port.addSpacing(4)
        hbox_port.addWidget(self.cbx_port)
        hcontainer_port = QWidget(self)
        hcontainer_port.setLayout(hbox_port)
        vbox_connection.addWidget(hcontainer_port)
        vbox_connection.addSpacing(4)
        # hbox_port.addSpacing(4)
        hbox_refresh_and_connect = QHBoxLayout()
        hbox_refresh_and_connect.addWidget(self.btn_refresh)
        hbox_refresh_and_connect.addWidget(self.btn_connect)
        hbox_refresh_and_connect.addWidget(self.btn_disconnect)
        hbox_refresh_and_connect.setContentsMargins(0, 0, 0, 0)
        hcontainer_refresh_and_connect = QWidget(self)
        hcontainer_refresh_and_connect.setLayout(hbox_refresh_and_connect)
        vbox_connection.addWidget(hcontainer_refresh_and_connect)
        # hcontainer1 = QWidget(self)
        # hcontainer1.setLayout(vbox_connection)
        # vbox.addWidget(hcontainer1)
        self.gbx_connection.setLayout(vbox_connection)
        # vbox.addWidget(self.gbx_connection)
        # vbox.addSpacing(4)

        hbox_mode_and_control = QHBoxLayout()
        hbox_mode_and_control.setContentsMargins(0, 0, 0, 0)
        hbox_mode_and_control.setSpacing(0)

        self.gbx_mode = QGroupBox('Mode')
        self.rbt_single_pulse = QRadioButton('Single Pulse')
        self.rbt_single_pulse.setChecked(True)
        self.rbt_periodic = QRadioButton('Periodic')
        self.rbt_continuous = QRadioButton('Continuous')

        vbox_mode = QVBoxLayout()
        vbox_mode.addWidget(self.rbt_single_pulse)
        vbox_mode.addSpacing(4)
        vbox_mode.addWidget(self.rbt_periodic)
        vbox_mode.addSpacing(4)
        vbox_mode.addWidget(self.rbt_continuous)
        self.gbx_mode.setLayout(vbox_mode)
        self.gbx_control = QGroupBox('Control')
        vbox_control = QVBoxLayout()
        vbox_control.addStretch(1)
        hbox_intensity = QHBoxLayout()
        hbox_intensity.setContentsMargins(0, 0, 0, 0)
        hbox_intensity.addWidget(QLabel('Intensity (3–4095, step 4):'))
        # vbox_control.addSpacing(4)
        hbox_intensity.addWidget(self.spb_intensity)
        hcontainer_intensity = QWidget(self)
        hcontainer_intensity.setLayout(hbox_intensity)
        vbox_control.addWidget(hcontainer_intensity)
        vbox_control.addSpacing(8)
        # vbox_control.addSpacing(4)
        hbox_frequency = QHBoxLayout()
        hbox_frequency.setContentsMargins(0, 0, 0, 0)
        self.lbl_frequency = QLabel('Duration, μs:')
        hbox_frequency.addWidget(self.lbl_frequency)
        hbox_frequency.addWidget(self.spb_frequency)
        hcontainer_frequency = QWidget(self)
        hcontainer_frequency.setLayout(hbox_frequency)
        vbox_control.addWidget(hcontainer_frequency)
        # vbox_control.addSpacing(16)
        vbox_control.addSpacing(8)
        hbox_generate_and_stop = QHBoxLayout()
        hbox_generate_and_stop.setContentsMargins(0, 0, 0, 0)
        hbox_generate_and_stop.addWidget(self.btn_generate)
        hbox_generate_and_stop.addStretch(1)
        hbox_generate_and_stop.addWidget(self.btn_stop)
        hcontainer_generate_and_stop = QWidget(self)
        hcontainer_generate_and_stop.setLayout(hbox_generate_and_stop)
        vbox_control.addWidget(hcontainer_generate_and_stop)
        self.gbx_control.setLayout(vbox_control)
        # vbox_control.addSpacing(4)
        # hcontainer_mode_and_control = QWidget(self)
        # hcontainer_mode_and_control.setLayout(vbox_control)
        # vbox.addWidget(hcontainer_mode_and_control)
        hbox_mode_and_control.addWidget(self.gbx_connection)
        hbox_mode_and_control.addStretch(1)
        hbox_mode_and_control.addWidget(self.gbx_mode)
        hbox_mode_and_control.addSpacing(8)
        hbox_mode_and_control.addWidget(self.gbx_control)
        hcontainer_mode_and_control = QWidget(self)
        hcontainer_mode_and_control.setLayout(hbox_mode_and_control)
        vbox.addWidget(hcontainer_mode_and_control)
        # vbox.addSpacing(4)

        self.gbx_pins = QGroupBox('Pins')
        hbox_pins = QHBoxLayout()
        # hbox_pins = QHBoxLayout(frame3)
        hbox_pins.setSpacing(0)
        hbox_pins.setContentsMargins(0, 0, 0, 0)
        hbox_pins.addStretch(1)
        self.pins = []
        self.pins.append(PinWidget())
        self.pins[0].setMCUPin('D2(~)')
        self.pins[0].setLaserPin('PIN25')
        self.pins[0].setCheckBoxState(True)
        for i in range(3, 15):
            self.pins.append(PinWidget())
            self.pins[-1].setMCUPin(f'D{i}')
            self.pins[-1].setLaserPin(f'PIN{i-2}')

        self.pins[-1].setMCUPin('')
        self.pins[-1].setCheckBoxState(True)
        self.pins[-2].setMCUPin('')
        self.pins[-2].setCheckBoxState(True)
        self.pins.append(PinWidget())
        self.pins[-1].setMCUPin('GND')
        self.pins[-1].setLaserPin('PIN14')
        self.pins[-1].setCheckBoxState(True)
        for p in self.pins:
            hbox_pins.addWidget(p)
        # hcontainer3 = QWidget(self)
        # hcontainer3.setLayout(hbox_pins)
        # # hcontainer3.setStyleSheet('PinWidget { border: 1px solid #000000; }')

        # # vbox.addWidget(frame)
        # vbox.addWidget(hcontainer3)
        self.gbx_pins.setLayout(hbox_pins)
        vbox.addWidget(self.gbx_pins)

        
        # vbox.addSpacing(4)
        vbox.addStretch(1)

        container = QWidget(self)
        container.setLayout(vbox)
        self.setCentralWidget(container)