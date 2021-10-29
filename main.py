# importing libraries
from PyQt5.QtWidgets import *
import numpy as np
import sys
import cv2
import os


# creating a class
# that inherits the QDialog class
class Window(QDialog):

	# constructor
	def __init__(self):
		super(Window, self).__init__()
		self.loadData()
		self.check("test/19.png")
		# setting window title
		self.setWindowTitle("Python")

		# setting geometry to the window
		self.setGeometry(100, 100, 300, 400)

		# creating a group box
		self.formGroupBox = QGroupBox("Add new")
		self.formGroupBox.resize(300,300);
		# creating spin box to select age
		self.ageSpinBar = QSpinBox()

		# creating combo box to select degree
		self.degreeComboBox = QComboBox()

		# adding items to the combo box
		self.degreeComboBox.addItems(["BTech", "MTech", "PhD"])

		# creating a line edit
		self.nameLineEdit = QLineEdit()

		# creating a line edit
		self.idLineEdit = QLineEdit()

		# creating a line edit
		self.classLineEdit = QLineEdit()

		# calling the method that create the form
		self.createForm()

		# creating a dialog button for ok and cancel
		self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

		# adding action when form is accepted
		self.buttonBox.accepted.connect(self.getInfo)

		# addding action when form is rejected
		self.buttonBox.rejected.connect(self.reject)
		#add button check

		self.buttonCheck = QPushButton("Check")
		self.buttonCheck.clicked.connect(self.check())
		# creating a vertical layout
		mainLayout = QVBoxLayout()

		# adding form group box to the layout
		mainLayout.addWidget(self.formGroupBox)

		# adding button box to the layout
		mainLayout.addWidget(self.buttonBox)
		#add to check button layout
		mainLayout.addWidget(self.buttonCheck)
		# setting lay out
		self.setLayout(mainLayout)

	# get info method called when form is accepted
	def getInfo(self):
		name=self.nameLineEdit.text()
		id=self.idLineEdit.text()
		cla=self.classLineEdit.text()
		img=id+"-"+cla
		# printing the form information
		print("Person Name : {0}".format(self.nameLineEdit.text()))
		print("ID : {0}".format(self.idLineEdit.text()))
		print("Class : {0}".format(self.classLineEdit.text()))

		cam = cv2.VideoCapture(0)

		cv2.namedWindow("test")

		img_counter = 0

		while True:
			ret, frame = cam.read()
			if not ret:
				print("failed to grab frame")
				break
			cv2.imshow("test", frame)

			k = cv2.waitKey(1)
			if k % 256 == 27:
				# ESC pressed
				print("Escape hit, closing...")
				break
			elif k % 256 == 32:
				# SPACE pressed
				img_name = "images/"+img+".png"
				cv2.imwrite(img_name, frame)
				print("{} written!".format(img_name))

		cam.release()

		cv2.destroyAllWindows()
		# closing the window
		#self.close()
	# creat form method
	def createForm(self):

		# creating a form layout
		layout = QFormLayout()

		# adding rows
		# for name and adding input text
		layout.addRow(QLabel("Name"), self.nameLineEdit)

		# for degree and adding combo box
		layout.addRow(QLabel("ID"), self.idLineEdit)

		# for age and adding spin box
		layout.addRow(QLabel("Class"), self.classLineEdit)

		# setting layout
		self.formGroupBox.setLayout(layout)
	def loadData(self):
		list = os.listdir("images")  # dir is your directory path
		images = len(list)
		image_width = 720
		image_length = 1280
		variants = 8

		dim = (image_width, image_length)
		self.total_pixels = image_width * image_length
		self.total_images = images * variants

		face_vector = []
		for i in range(self.total_images):


			# resize image
			img = cv2.imread('images/'+str(i+1)+'.png', cv2.IMREAD_UNCHANGED)
			face_image = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
			#face_image = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
			face_image = face_image.reshape(self.total_pixels, )
			face_vector.append(face_image)
		face_vector = np.asarray(face_vector)
		face_vector = face_vector.transpose()

		self.avg_face_vector = face_vector.mean(axis=1)
		self.avg_face_vector = self.avg_face_vector.reshape(face_vector.shape[0], 1)
		normalized_face_vector = face_vector - self.avg_face_vector

		covariance_matrix = np.cov(np.transpose(normalized_face_vector))

		eigen_values, eigen_vectors = np.linalg.eig(covariance_matrix)

		k = 20
		k_eigen_vectors = eigen_vectors[0:k, :]

		self.eigen_faces = k_eigen_vectors.dot(np.transpose(normalized_face_vector))

		weights = np.transpose(normalized_face_vector).dot(np.transpose(self.eigen_faces))
	def check(self, test_add):
		test_img = cv2.imread(test_add)
		test_img = cv2.cvtColor(test_img, cv2.COLOR_RGB2GRAY)

		test_img = test_img.reshape(self.total_pixels, 1)
		test_normalized_face_vector = test_img - self.avg_face_vector
		test_weight = np.transpose(test_normalized_face_vector).dot(np.transpose(self.eigen_faces))

		index = np.argmin(np.linalg.norm(test_weight - self.weights, axis=1))
		print(index)
	# main method
if __name__ == '__main__':

	# create pyqt5 app
	app = QApplication(sys.argv)

	# create the instance of our Window
	window = Window()

	# showing the window
	window.show()

	# start the app
	sys.exit(app.exec())
