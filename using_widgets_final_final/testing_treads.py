import time
import sys
import random

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit
from PySide6.QtCore import QThread, Signal

class WorkerTread(QThread):

	data_received = Signal(str)
	send_data_signal = Signal(str, str)
	send_request_signal = Signal(str)

	def __init__(self):
		super().__init__()
		self.request = None
		self.send_data_signal.connect(self.send_data)
		# self.send_request_signal.connect(self.send_request)

	def run(self):
		while True:
			if self.request:
				t = random.randint(1, 5)
				print(f'Sleeping {t} seconds...')
				time.sleep(t)
				self.data_received.emit(self.request)
				self.request = None

	# def send_request(self, data):
	# 	t = random.randint(1, 5)
	# 	print(f'Sleeping {t} seconds...')
	# 	time.sleep(t)
	# 	self.data_received.emit(f'{data}:{t}')

	def send_data(self, data, val):
		print(data*2 + val)
		self.request = data*2

	def read_data(self):
		pass


class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle('Testing threads')
		self.label = QLabel('Waiting...', self)
		self.label.move(50, 50)
		self.edit = QLineEdit(self)
		self.edit.move(50, 80)
		self.button = QPushButton('Send', self)
		self.button.move(50, 110)
		self.button.clicked.connect(self.send_data_to_worker)

		self.worker = WorkerTread()
		self.worker.data_received.connect(self.update_label)
		self.worker.start()

	def send_data_to_worker(self):
		data = self.edit.text()
		self.button.setDisabled(True)
		self.worker.send_data_signal.emit(data, 'Hello from MainThread!')
		# self.worker.send_request_signal.emit(data)

	def update_label(self, data):
		self.label.setText(data)
		self.button.setEnabled(True)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())

