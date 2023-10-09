from PyQt5 import QtCore, QtWidgets
from typing import Callable


class UIWidget(QtWidgets.QWidget):
    def __init__(self, d2n: Callable, parent=None):
        super(UIWidget, self).__init__(parent=parent)
        self.d2n = d2n
 
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.input_url = QtWidgets.QInputDialog(self)
        self.verticalLayout.addWidget(self.input_url)
        self.input_db_id = QtWidgets.QInputDialog(self)
        self.verticalLayout.addWidget(self.input_db_id)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText('Start')
        self.pushButton.setGeometry(QtCore.QRect(160, 130, 93, 28))
        self.verticalLayout.addWidget(self.pushButton)  
 
        self.pushButton.clicked.connect(self.takeinputs)
         
    def takeinputs(self):
        url, done1 = QtWidgets.QInputDialog.getText(
             self, 'Input Dialog', 'Enter the url of the douban page:') 
 
        db_id, done2 = QtWidgets.QInputDialog.getText(
           self, 'Input Dialog', 'Enter the database id in Notion')  
 
        if done1 and done2:
            self.d2n.process_group(url, db_id)
            QtWidgets.QMessageBox.information(self, "complete", "Task Done!")

        return