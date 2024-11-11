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
from PySide6.QtWidgets import QStyle
from PySide6.QtCore import Qt


class PinWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.chx_mcu_pin = QCheckBox(self)
        self.chx_mcu_pin.setText('')
        self.chx_mcu_pin.setDisabled(True)
        self.lbl_mcu_pin = QLabel()
        self.lbl_laser_pin = QLabel()
        vbox = QVBoxLayout()
        # vbox.setAlignment(Qt.AlignRight)
        vbox.addWidget(self.lbl_mcu_pin, alignment=Qt.AlignCenter)
        vbox.addWidget(self.chx_mcu_pin, alignment=Qt.AlignCenter)
        vbox.addWidget(self.lbl_laser_pin, alignment=Qt.AlignCenter)
        self.setLayout(vbox)

    def setLaserPin(self, text):
        self.lbl_laser_pin.setText(text)

    def setMCUPin(self, text):
        self.lbl_mcu_pin.setText(text)

    def setCheckBoxState(self, value: bool):
        self.chx_mcu_pin.setChecked(value)

class IntensitySpinBox(QSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def focusOutEvent(self, event):
        value = self.value()
        mod4 = value % 4
        if mod4 != 3:
            value = (value // 4)*4 + 3
            self.setValue(value)
        super().focusOutEvent(event)

class MainWindowGUI:

    # def __init__(self):
    #     pass
        # super().__init__()
        # self.init_gui()

    def init_gui(self):
        self.setWindowTitle('Laser Control with Arduino')
        self.setMinimumSize(400, 100)

        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        vbox_connection = QVBoxLayout()
        vbox_connection.setSpacing(0)

        hbox_connection_mode_and_control = QHBoxLayout()
        hbox_connection_mode_and_control.setContentsMargins(0, 0, 0, 0)
        hbox_connection_mode_and_control.setSpacing(0)

        self.gbx_connection = QGroupBox('Connection')
        self.gbx_connection.setFixedWidth(210)

        hbox_baud_rate = QHBoxLayout()
        # hbox_baud_rate.setSpacing(0)
        hbox_baud_rate.setContentsMargins(0, 0, 0, 0)

        hbox_baud_rate.addStretch(1)
        hbox_baud_rate.addWidget(QLabel('Baud rate:'))
        # hbox_baud_rate.addSpacing(4)

        self.cbx_baudrate = QComboBox(self)
        self.cbx_baudrate.setFixedWidth(120)
        self.cbx_baudrate.addItems(['4800', '9600', '38400', '57600', '115200'])
        self.cbx_baudrate.setCurrentIndex(1)
        hbox_baud_rate.addWidget(self.cbx_baudrate)

        hcontainer_baud_rate = QWidget(self)
        hcontainer_baud_rate.setLayout(hbox_baud_rate)
        vbox_connection.addWidget(hcontainer_baud_rate)
        vbox_connection.addSpacing(4)

        hbox_port = QHBoxLayout()
        hbox_port.setContentsMargins(0, 0, 0, 0)
        hbox_port.addWidget(QLabel('Port:'))
        # hbox_port.addSpacing(4)
        # hbox_port.addStretch(1)
        self.cbx_port = QComboBox(self)
        self.cbx_port.setFixedWidth(100)

        hbox_port.addWidget(self.cbx_port)
        
        self.btn_refresh = QPushButton('', self)
        self.btn_refresh.setToolTip('Refresh')
        self.btn_refresh.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        hbox_port.addWidget(self.btn_refresh)

        hcontainer_port = QWidget(self)
        hcontainer_port.setLayout(hbox_port)
        vbox_connection.addWidget(hcontainer_port)
        vbox_connection.addSpacing(4)

        hbox_connect_and_disconnect = QHBoxLayout()
        hbox_connect_and_disconnect.setContentsMargins(0, 0, 0, 0)
        self.btn_connect = QPushButton('Connect', self)
        hbox_connect_and_disconnect.addWidget(self.btn_connect)
        self.btn_disconnect = QPushButton('Disconnect', self)
        hbox_connect_and_disconnect.addWidget(self.btn_disconnect)
        hcontainer_connect_and_disconnect = QWidget(self)
        hcontainer_connect_and_disconnect.setLayout(hbox_connect_and_disconnect)
        vbox_connection.addWidget(hcontainer_connect_and_disconnect)
        self.gbx_connection.setLayout(vbox_connection)
        hbox_connection_mode_and_control.addWidget(self.gbx_connection)
        hbox_connection_mode_and_control.addStretch(1)

        vbox_mode = QVBoxLayout()
        vbox_mode.addSpacing(4)

        self.gbx_mode = QGroupBox('Mode')
        
        self.rbt_single_pulse = QRadioButton('Single Pulse')
        vbox_mode.addWidget(self.rbt_single_pulse)
        self.rbt_single_pulse.setChecked(True)
        vbox_mode.addSpacing(4)
        self.rbt_periodic = QRadioButton('Periodic')
        vbox_mode.addWidget(self.rbt_periodic)
        self.rbt_continuous = QRadioButton('Continuous')
        vbox_mode.addWidget(self.rbt_continuous)

        self.gbx_mode.setLayout(vbox_mode)
        hbox_connection_mode_and_control.addWidget(self.gbx_mode)
        hbox_connection_mode_and_control.addSpacing(8)

        self.gbx_control = QGroupBox('Control')
        
        vbox_control = QVBoxLayout()
        vbox_control.addStretch(1)
        
        hbox_intensity = QHBoxLayout()
        hbox_intensity.setContentsMargins(0, 0, 0, 0)
        self.lbl_intensity = QLabel('Intensity:')
        self.lbl_intensity.setFixedWidth(50)
        hbox_intensity.addWidget(self.lbl_intensity)
        self.spb_intensity = IntensitySpinBox(self)
        self.spb_intensity.setRange(3, 4095)    
        self.spb_intensity.setSingleStep(4)
        self.spb_intensity.setToolTip('3–4095, step 4')
        self.spb_intensity.setFixedWidth(100)
        hbox_intensity.addWidget(self.spb_intensity)
        # hbox_intensity.addStretch(1)
        hbox_intensity.addSpacing(420)
        hcontainer_intensity = QWidget(self)
        hcontainer_intensity.setLayout(hbox_intensity)
        vbox_control.addWidget(hcontainer_intensity)
        vbox_control.addSpacing(8)
        
        hbox_frequency = QHBoxLayout()
        hbox_frequency.setContentsMargins(0, 0, 0, 0)
        self.lbl_frequency = QLabel('Duration:')
        hbox_frequency.addWidget(self.lbl_frequency)
        self.spb_frequency = QSpinBox(self)
        self.spb_frequency.setRange(1, 16000)
        self.spb_frequency.setSingleStep(1)
        self.spb_frequency.setFixedWidth(100)
        hbox_frequency.addWidget(self.spb_frequency)
        self.cbx_duration_units = QComboBox(self)
        self.cbx_duration_units.addItems(['μs', 'ms'])
        self.cbx_duration_units.setFixedWidth(50)
        hbox_frequency.addWidget(self.cbx_duration_units)
        self.lbl_pause = QLabel('Pause:')
        self.lbl_pause.setHidden(True)
        hbox_frequency.addWidget(self.lbl_pause)
        self.spb_pause = QSpinBox(self)
        self.spb_pause.setRange(1, 16000)
        self.spb_pause.setSingleStep(1)
        self.spb_pause.setFixedWidth(100)
        self.spb_pause.setHidden(True)
        hbox_frequency.addWidget(self.spb_pause)
        self.cbx_pause_units = QComboBox(self)
        self.cbx_pause_units.addItems(['μs', 'ms'])
        self.cbx_pause_units.setFixedWidth(50)
        self.cbx_pause_units.setHidden(True)
        hbox_frequency.addWidget(self.cbx_pause_units)
        self.lbl_amount = QLabel('Amount:')
        self.lbl_amount.setHidden(True)
        hbox_frequency.addWidget(self.lbl_amount)
        self.spb_amount = QSpinBox(self)
        self.spb_amount.setRange(1, 1000000)
        self.spb_amount.setSingleStep(1)
        self.spb_amount.setFixedWidth(100)
        self.spb_amount.setHidden(True)
        hbox_frequency.addWidget(self.spb_amount)
        hbox_frequency.addStretch(1)
        self.hcontainer_frequency = QWidget(self)
        self.hcontainer_frequency.setLayout(hbox_frequency)
        vbox_control.addWidget(self.hcontainer_frequency)
        vbox_control.addSpacing(8)

        hbox_generate_and_stop = QHBoxLayout()
        hbox_generate_and_stop.setContentsMargins(0, 0, 0, 0)
        self.btn_generate = QPushButton('Generate', self)
        self.btn_generate.setFixedWidth(103)
        hbox_generate_and_stop.addWidget(self.btn_generate)
        # hbox_generate_and_stop.addSpacing(6)
        self.btn_stop = QPushButton('Stop', self)
        self.btn_stop.setFixedWidth(103)
        hbox_generate_and_stop.addWidget(self.btn_stop)
        hbox_generate_and_stop.addStretch(1)
        # hbox_generate_and_stop.addSpacing(55)
        hcontainer_generate_and_stop = QWidget(self)
        hcontainer_generate_and_stop.setLayout(hbox_generate_and_stop)
        vbox_control.addWidget(hcontainer_generate_and_stop)
        
        self.gbx_control.setLayout(vbox_control)
        hbox_connection_mode_and_control.addWidget(self.gbx_control)
        hcontainer_mode_and_control = QWidget(self)
        
        hcontainer_mode_and_control.setLayout(hbox_connection_mode_and_control)
        vbox.addWidget(hcontainer_mode_and_control)

        self.gbx_pins = QGroupBox('Pins')
        hbox_pins = QHBoxLayout()
        hbox_pins.setSpacing(0)
        hbox_pins.setContentsMargins(0, 0, 0, 0)
        hbox_pins.addStretch(1)
        self.pins = []
        self.pins.append(PinWidget())
        self.pins[0].setMCUPin('D2(~)')
        self.pins[0].setLaserPin('PIN25')
        self.pins[0].setCheckBoxState(False)
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
        
        self.gbx_pins.setLayout(hbox_pins)
        vbox.addWidget(self.gbx_pins)
        vbox.addStretch(1)

        container = QWidget(self)
        container.setLayout(vbox)
        self.setCentralWidget(container)