from provide_data_for_gui import *
import config as con
import sys
from youlg_predict import *
from rexiaolv_model import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from numpy import arange
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib


class MyTimeDlg(QDialog):
    time_signal = pyqtSignal(str)

    def __init__(self):
        super(MyTimeDlg, self).__init__()
        self.setFixedSize(260, 330)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(90, 280, 75, 23))
        self.pushButton.setObjectName("pushButton")

        date = get_all_date()

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 211, 211))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(len(date))
        self.tableWidget.setHorizontalHeaderLabels(['日期', '小时'])
        for i in range(len(date)):
            for j in range(2):
                newItem = QTableWidgetItem(str(date[i][j]))
                self.tableWidget.setItem(i, j, newItem)
                self.tableWidget.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 单击选中一行
        self.tableWidget.horizontalHeader().setDefaultSectionSize(75)  # 列宽
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 20, 54, 12))
        self.label.setObjectName("label")

        self.setWindowTitle("选择时间")
        self.pushButton.setText("OK")
        self.label.setText("选择时间")

        self.pushButton.clicked.connect(self.Accept)
        self.show()

    def Accept(self):
        try:
            row = self.tableWidget.currentRow()
            # print(self.tableWidget.item(row, 0).text() + self.tableWidget.item(row, 1).text())
            self.time_signal.emit(self.tableWidget.item(row, 0).text() + self.tableWidget.item(row, 1).text())
            self.close()
        except Exception:
            self.close()


class MyDataSimDlg(QDialog):
    def __init__(self, time):
        super(MyDataSimDlg, self).__init__()
        name, value = get_by_hour(time)
        metric = QDesktopWidget().screenGeometry()
        width = metric.width()
        height = metric.height()
        self.setFixedSize(800 * width / 1366, 600 * height / 768)
        self.label = QtWidgets.QLabel(self)
        self.label.move(20, 30)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 70, 321, 471))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(len(name))
        self.tableWidget.setHorizontalHeaderLabels(['表头', '原数据', '模拟数据'])
        self.tableWidget.horizontalHeader().setDefaultSectionSize(90)  # 列宽

        for i in range(len(name)):
            newItem = QTableWidgetItem(name[i])
            self.tableWidget.setItem(i, 0, newItem)
            if value[i] == None:
                newItem = QTableWidgetItem('')
            else:
                newItem = QTableWidgetItem(str(value[i]))
            self.tableWidget.setItem(i, 1, newItem)
            self.tableWidget.item(i, 0).setFlags(Qt.ItemIsEnabled)
            self.tableWidget.item(i, 1).setFlags(Qt.ItemIsEnabled)

        name2, value2 = get_target_data(time)
        self.tableWidget_2 = QtWidgets.QTableWidget(self)
        self.tableWidget_2.setGeometry(QtCore.QRect(430, 70, 321, 471))
        self.tableWidget_2.setAlternatingRowColors(False)
        self.tableWidget_2.setColumnCount(4)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setRowCount(len(name2))
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(70)  # 列宽
        self.tableWidget_2.setHorizontalHeaderLabels(['表头', '原结果', '模拟结果', '变化幅度'])

        for i in range(len(name2)):
            newItem = QTableWidgetItem(name2[i])
            self.tableWidget_2.setItem(i, 0, newItem)
            if value2[i] == None:
                newItem = QTableWidgetItem('')
            else:
                newItem = QTableWidgetItem(str(value2[i]))
            self.tableWidget_2.setItem(i, 1, newItem)
            self.tableWidget_2.item(i, 0).setFlags(Qt.ItemIsEnabled)
            self.tableWidget_2.item(i, 1).setFlags(Qt.ItemIsEnabled)
        self.tableWidget_2.resizeColumnsToContents()

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(360, 270, 61, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)

        self.label_3.move(430, 31)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(670, 550, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.setWindowTitle("Dialog")
        self.label.setText("模拟数据")
        self.label.setFont(QFont("Roman times", 15, QFont.Bold))

        self.statePic = QPixmap('picture\\white.png')
        self.label_2.setPixmap(self.statePic.scaled(50, 30))
        self.label_3.setText("生产预警变化")
        self.label_3.setFont(QFont("Roman times", 15, QFont.Bold))
        self.pushButton.setText("OK")
        self.pushButton.clicked.connect(self.Accept)

        self.show()

    def Accept(self):
        self.statePic = QPixmap('picture\\red.png')
        self.label_2.setPixmap(self.statePic.scaled(50, 30))
        col_data = []
        for i in range(self.tableWidget.rowCount()):
            try:
                col_data.append(self.tableWidget.item(i, 2).text())
            except Exception:
                col_data.append('')
        print(col_data)


class MyDataLeadInDlg(QDialog):
    def __init__(self):
        super(MyDataLeadInDlg, self).__init__()
        self.setFixedSize(460, 390)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 70, 450, 250))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(3)
        self.tableWidget.horizontalHeader().setVisible(False)

        self.tableWidget.horizontalHeader().setDefaultSectionSize(80)
        self.label = QtWidgets.QLabel(self)
        self.label.move(20, 20)
        # self.label.setGeometry(QtCore.QRect(20, 20, 54, 12))
        self.label.setObjectName("label")

        self.setWindowTitle("设置标准表头")
        self.label.setText("从左至右，自上而下按顺序添加表头")
        self.label.setFont(QFont("Roman times", 15, QFont.Bold))
        self.lay = QHBoxLayout()
        self.pushButton = QtWidgets.QPushButton(self)
        # self.pushButton.setGeometry(QtCore.QRect(90, 280, 75, 23))
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setText('Add')
        self.pushButton.setText("OK")
        self.pushButton.clicked.connect(self.Accept)
        self.pushButton_2.clicked.connect(self.Add)
        self.lay.addWidget(self.pushButton_2)
        self.lay.addWidget(self.pushButton)
        self.lay.setGeometry(QtCore.QRect(260, 350, 175, 23))
        self.initTable()
        self.show()

    def initTable(self):
        name = get_table_name()

        for i in range(len(name)):
            if i >= self.tableWidget.rowCount() * 5:
                self.Add()
            newItem = QTableWidgetItem(name[i])
            self.tableWidget.setItem(i / 5, i % 5, newItem)
        if self.tableWidget.rowCount() * 5 == len(name):
            self.Add()

    def Add(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.scrollToBottom()

    def Accept(self):
        try:
            row = self.tableWidget.currentRow()
            # print(self.tableWidget.item(row, 0).text() + self.tableWidget.item(row, 1).text())
            self.close()
        except Exception:
            self.close()


class MyStandardDlg(QDialog):
    def __init__(self):
        super(MyStandardDlg, self).__init__()
        self.setFixedSize(260, 330)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(90, 280, 75, 23))
        self.pushButton.setObjectName("pushButton")

        name = get_table_name()
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 211, 211))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(len(name))
        self.tableWidget.setHorizontalHeaderLabels(['名称', '标准值'])

        for i in range(len(name)):
            newItem = QTableWidgetItem(str(name[i]))
            self.tableWidget.setItem(i, 0, newItem)
            self.tableWidget.item(i, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(80)  # 列宽
        self.label = QtWidgets.QLabel(self)
        self.label.move(20, 10)
        self.setWindowTitle("生产数据标准设置")
        self.pushButton.setText("OK")
        self.label.setText("生产数据标准设置")
        self.label.setFont(QFont("Roman times", 15, QFont.Bold))
        self.pushButton.clicked.connect(self.Accept)
        self.show()

    def Accept(self):
        try:
            row = self.tableWidget.currentRow()
            # print(self.tableWidget.item(row, 0).text() + self.tableWidget.item(row, 1).text())
            self.close()
        except Exception:
            self.close()


class MyYaoDlg(QDialog):
    def __init__(self):
        super(MyYaoDlg, self).__init__()
        self.setFixedSize(563, 515)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 521, 461))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(4)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(['设备', '个数', '描述', '数据'])
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget.verticalHeader().setDefaultSectionSize(120)
        self.loadPic()
        self.loadTable()
        self.setWindowTitle("窑系统数据")

        self.show()

    def loadPic(self):
        self.xft = QPixmap('picture\\xft_dl.png')

    def loadTable(self):
        self.lay1 = QHBoxLayout()
        self.item1 = QLabel()
        self.item1.setPixmap(self.xft.scaled(120, 120, aspectRatioMode=Qt.KeepAspectRatio))
        self.lay1.addWidget(self.item1)
        self.lay1.setAlignment(Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(self.lay1)
        self.tableWidget.setCellWidget(0, 0, widget)


class MyLoginDlg(QDialog):
    login_signal = pyqtSignal(str, str)

    def __init__(self):
        super(MyLoginDlg, self).__init__()
        metric = QDesktopWidget().screenGeometry()
        width = metric.width()
        height = metric.height()
        self.setFixedSize(400 * width / 1366, 300 * height / 768)
        self.setWindowTitle('Login')
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(-60 * width / 1366, 240 * height / 768, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(80 * width / 1366, 90 * height / 768, 270, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)

        self.lineEdit.setFocus()
        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(80 * width / 1366, 140 * height / 768, 189, 81))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self)

        self.label_3.setGeometry(QtCore.QRect(80 * width / 1366, 20 * height / 768, 231, 51))
        self.label_3.setPixmap(QPixmap('picture\\logo.png').scaled(231, 50, aspectRatioMode=Qt.KeepAspectRatio))
        self.label_3.setObjectName("label_3")

        self.registBtn = QPushButton()
        self.registBtn.setText('注册用户')
        self.horizontalLayout.addWidget(self.registBtn)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.registBtn.clicked.connect(self.registe)
        self.label.setText("用户名：")
        self.label_2.setText("密码：  ")
        self.lineEdit.setText('moujun')
        self.lineEdit_2.setText('123456')

    def registe(self):
        print('123')

    def accept(self):
        self.login_signal.emit(self.lineEdit.text(), self.lineEdit_2.text())

    def reject(self):
        qApp.quit()


class MyDeviceDlg(QDialog):
    yao_par_signal = pyqtSignal(int, str)

    def __init__(self):
        super(MyDeviceDlg, self).__init__()

        self.setWindowTitle('配置设备')
        self.resize(400, 300)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)  # 禁止窗口最大化
        self.setFixedSize(self.width(), self.height())  # 禁止拉伸窗口
        self.lay_ser = QHBoxLayout()
        self.lay_xft = QHBoxLayout()
        self.lay_main = QVBoxLayout()
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 291, 78))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle('窑系统类型')

        self.serial_sin = QRadioButton('单系列', self.groupBox)
        self.serial_sin.setGeometry(QtCore.QRect(50, 30, 106, 16))
        self.serial_dou = QRadioButton('双系列', self.groupBox)
        self.serial_dou.setGeometry(QtCore.QRect(170, 30, 161, 16))
        self.serial_dou.setChecked(True)

        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 110, 291, 101))
        self.groupBox_2.setTitle('旋风筒参数')
        self.xft_num = QtWidgets.QComboBox(self.groupBox_2)
        self.xft_num.setGeometry(QtCore.QRect(150, 40, 69, 22))
        self.xft_num.setObjectName("comboBox")
        self.label_xft = QLabel('旋风筒个数', self.groupBox_2)
        self.label_xft.setGeometry(QtCore.QRect(63, 42, 61, 20))
        self.num = ['2', '3', '4', '5', '6', '7', '8', '9']
        for i in self.num:
            self.xft_num.addItem(i)
        self.xft_num.setCurrentIndex(3)
        self.buttonBox.accepted.connect(self.Accept)
        self.buttonBox.rejected.connect(self.Reject)

        self.setModal(True)

    def Accept(self):
        if self.serial_sin.isChecked():
            flag = 1
            # con.setValue_flag_Ser(1)
        else:
            flag = 2
            # con.setValue_flag_Ser(2)
        # con.setValue_number(int(self.xft_num.currentText()))
        self.yao_par_signal.emit(flag, self.xft_num.currentText())
        self.close()

    def Reject(self):
        self.close()


class MyDataInputDlg(QMainWindow):  # 数据输入功能窗口
    def __init__(self):
        super(MyDataInputDlg, self).__init__()
        metric = QDesktopWidget().screenGeometry()
        width = metric.width()
        height = metric.height()
        self.setObjectName("数据输入")
        self.BtnAddData = QPushButton('录入一行', self)
        self.BtnOk = QPushButton('确认', self)
        self.BtnCancle = QPushButton('取消', self)
        self.BtnAddData.clicked.connect(self.addRowData)
        self.BtnOk.clicked.connect(self.accept)
        self.BtnCancle.clicked.connect(self.reject)
        self.Btn_layout = QHBoxLayout()
        self.Btn_layout.addWidget(self.BtnAddData)
        self.Btn_layout.addWidget(self.BtnOk)
        self.Btn_layout.addWidget(self.BtnCancle)
        self.Btn_layout.setGeometry(QtCore.QRect(width * 0.7, height * 0.85, 341, 32))
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, height * 0.73, width, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(width * 0.01, height * 0.04, width * 0.98, height * 0.69))
        self.tableWidget.setObjectName("dataInputWidget")
        '''
        day = str(con.getValue_day())
        hour = str(con.getValue_hour())
        print(123)
        '''
        date = get_time_now()
        day = date[:8]
        hour = date[8:]
        value, name = get_by_fragment()
        self.col_num = len(value[0]) - 3
        self.row_num = len(value)
        self.tableWidget.setColumnCount(self.col_num)
        self.tableWidget.setRowCount(len(value) + 1)
        col_label = []
        for i in range(self.col_num):
            col_label.append(name[i])
        self.new_data = []

        self.tableWidget.setHorizontalHeaderLabels(col_label)
        for i in range(len(value)):
            for j in range(self.col_num):
                newItem = QTableWidgetItem(str(value[i][j]))
                self.tableWidget.setItem(i, j, newItem)
                self.tableWidget.item(i, j).setFlags(Qt.ItemIsEnabled)

        newItem = QTableWidgetItem(str(day))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, newItem)
        newItem = QTableWidgetItem(str(hour))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, newItem)

        '''date = int(self.tableWidget.item(self.row_num - 1, 0).text())
        hour = int(self.tableWidget.item(self.row_num - 1, 1).text())

        if hour < 24:
            newItem = QTableWidgetItem(str(day))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, newItem)
            newItem = QTableWidgetItem(str(hour + 1))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, newItem)

        else:
            newItem = QTableWidgetItem(str(date + 1))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, newItem)
            newItem = QTableWidgetItem(str(0))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, newItem)'''

        self.red = 180
        self.green = 180
        self.blue = 180
        self.tableWidget.item(self.tableWidget.rowCount() - 1, 0).setBackground(
            QBrush(QColor(self.red, self.green, self.blue)))
        self.tableWidget.item(self.tableWidget.rowCount() - 1, 1).setBackground(
            QBrush(QColor(self.red, self.green, self.blue)))
        for i in arange(2, self.col_num):
            newItem = QTableWidgetItem('')
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, i, newItem)
            self.tableWidget.item(self.tableWidget.rowCount() - 1, i).setBackground(
                QBrush(QColor(self.red, self.green, self.blue)))
        self.tableWidget.scrollToBottom()
        self.showMaximized()

    def delFirstRow(self):  # 删除第一行
        self.tableWidget.removeRow(0)

    def addRow(self):  # 在最后一行的下面新增一行
        self.tableWidget.insertRow(self.tableWidget.rowCount())

    # 以上两个函数是为了实现保持行数不变

    def addRowData(self):
        self.delFirstRow()
        new_row = []
        for col in range(2):
            item = self.tableWidget.item(self.tableWidget.rowCount() - 1, col)
            item.setBackground(QBrush(QColor(255, 255, 255)))
            try:
                new_row.append(int(item.text()))
            except Exception:
                new_row.append('')
        for col in range(2, self.tableWidget.columnCount()):
            item = self.tableWidget.item(self.tableWidget.rowCount() - 1, col)
            item.setBackground(QBrush(QColor(255, 255, 255)))
            try:
                new_row.append(float(item.text()))
            except Exception:
                new_row.append('')
                self.tableWidget.setItem(self.row_num - 1, col, QTableWidgetItem(''))  # 单元格为None无法设置不可编辑

            self.tableWidget.item(self.row_num - 1, col).setFlags(Qt.ItemIsEnabled)

        self.addRow()

        date = int(self.tableWidget.item(self.row_num - 1, 0).text())
        hour = int(self.tableWidget.item(self.row_num - 1, 1).text())

        if hour < 23:
            newItem = QTableWidgetItem(str(date))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, newItem)
            newItem = QTableWidgetItem(str(hour + 1))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, newItem)
        else:
            newItem = QTableWidgetItem(str(date + 1))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, newItem)
            newItem = QTableWidgetItem(str(0))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, newItem)

        self.tableWidget.item(self.tableWidget.rowCount() - 1, 0).setBackground(
            QBrush(QColor(self.red, self.green, self.blue)))
        self.tableWidget.item(self.tableWidget.rowCount() - 1, 1).setBackground(
            QBrush(QColor(self.red, self.green, self.blue)))
        for i in arange(2, self.col_num):
            newItem = QTableWidgetItem('')
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, i, newItem)
            self.tableWidget.item(self.tableWidget.rowCount() - 1, i).setBackground(
                QBrush(QColor(self.red, self.green, self.blue)))
        self.new_data.append(new_row)

    def accept(self):
        self.addRowData()
        if save_data(self.new_data):
            reply = QMessageBox.information(self, '提示', '最新数据已经导入，是否自动生成生产预警', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.warningDlg = MyProduceWarDlg(con.getValue_day(), con.getValue_hour(), 1)

                self.close()
            else:
                self.close()
        else:
            QMessageBox.information(self, '提示', '上传失败', QMessageBox.Yes)

    def reject(self):
        reply = QMessageBox.information(self, '提示', '确认放弃上传？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            pass


class MyDataReviseDlg(QMainWindow):  # 数据修改功能窗口
    def __init__(self):
        super(MyDataReviseDlg, self).__init__()
        metric = QDesktopWidget().screenGeometry()
        width = metric.width()
        height = metric.height()

        self.setObjectName("数据修改")
        self.BtnOk = QPushButton('确认', self)
        self.BtnCancle = QPushButton('取消', self)
        self.BtnOk.clicked.connect(self.accept)
        self.BtnCancle.clicked.connect(self.reject)
        self.Btn_layout = QHBoxLayout()
        self.Btn_layout.addWidget(self.BtnOk)
        self.Btn_layout.addWidget(self.BtnCancle)

        self.Btndelete = QPushButton('删除选中行数据', self)
        self.Btndelete.clicked.connect(self.Delete)
        self.Btn_layout.addWidget(self.Btndelete)

        self.Btn_layout.setGeometry(QtCore.QRect(width * 0.7, height * 0.85, 341, 32))

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, height * 0.73, width, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(width * 0.01, height * 0.04, width * 0.98, height * 0.69))
        self.tableWidget.setObjectName("dataShowWidget")

        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        day = str(con.getValue_day())
        hour = str(con.getValue_hour())

        value, name = get_by_fragment()

        self.col_num = len(value[0]) - 3  # 最后三列不要
        self.row_num = len(value)
        self.tableWidget.setColumnCount(self.col_num)
        self.tableWidget.setRowCount(len(value))
        col_label = []

        for i in range(self.col_num):
            col_label.append(name[i])

        self.new_data = []  # 修改过的数据
        self.row_changed = []  # 修改过的数据的行下标

        self.tableWidget.setHorizontalHeaderLabels(col_label)
        for i in range(len(value)):
            for j in range(2):
                newItem = QTableWidgetItem(str(value[i][j]))
                self.tableWidget.setItem(i, j, newItem)
                self.tableWidget.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # 不可双击编辑但可单击选中

            for j in range(2, self.col_num):
                newItem = QTableWidgetItem(str(value[i][j]))
                self.tableWidget.setItem(i, j, newItem)

        self.tableWidget.itemChanged[QTableWidgetItem].connect(self.tableItemChanged)  # 编辑单元格后字体会显示红色
        self.tableWidget.scrollToBottom()
        self.showMaximized()

    def tableItemChanged(self):
        self.tableWidget.currentItem().setForeground(QBrush(QColor(255, 0, 0)))
        self.row_changed.append(self.tableWidget.currentRow())

    def Delete(self):
        selected=self.tableWidget.selectedItems()
        Rows=set()
        for item in selected:
            Rows.add(item.row())
        print(Rows)
        pass
        '''row_dedata = []
        for row in list(set(self.row_delete)):
            row_data = []
            for col in range(2):
                item = self.tableWidget.item(row, col)
                row_data.append(str(item.text()))
            row_dedata.append(row_data)
        if delete_data(row_dedata):
            reply = QMessageBox.information(self, '提示', '删除成功，是否继续操作?', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()
                self.__init__()
                pass
            else:
                self.close()
        else:
            QMessageBox.information(self, '提示', '删除失败', QMessageBox.Yes)'''

    def accept(self):

        for row in list(set(self.row_changed)):
            row_data = []
            for col in range(2):
                item = self.tableWidget.item(row, col)
                try:
                    row_data.append(int(item.text()))
                except Exception:
                    row_data.append('')
            for col in arange(2, self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                try:
                    row_data.append(float(item.text()))
                except Exception:
                    row_data.append(None)
            self.new_data.append(row_data)
        if update_data(self.new_data):
            reply = QMessageBox.information(self, '提示', '修改成功', QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.close()
        else:
            QMessageBox.information(self, '提示', '修改失败', QMessageBox.Yes)

    def reject(self):
        reply = QMessageBox.information(self, '提示', '确认放弃修改？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
        else:
            pass


class MyProduceWarDlg(QMainWindow):
    def __init__(self, day, hour, number=1):
        super(MyProduceWarDlg, self).__init__()

        self.setWindowTitle('生产预警')
        # 调整窗口显示时的大小
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.pageView = QTabWidget()
        self.tab = {}
        self.pic = {}

        for i in range(number):
            self.tab[i] = QLabel()
            self.pageView.addTab(self.tab[i], '%d小时' % (hour + i))
            self.pic[i] = QVBoxLayout(self.tab[i])
            data = get_by_hour(str(day) + str(hour))
            value = Production_warning_youligai(data[1])
            Ca = MyCaMplCanvas(value)
            self.pic[i].addWidget(QLabel('游离钙合格比'))
            self.pic[i].addWidget(Ca)

            self.line = QtWidgets.QFrame(self)
            self.line.setGeometry(QtCore.QRect(0, QDesktopWidget().screenGeometry().height() * 0.73,
                                               QDesktopWidget().screenGeometry().width(), 16))
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.pic[i].addWidget(self.line)

            value = Production_warning_rexiaolv(data[1])
            Effic = MyEfficMpCanvas(value)
            self.pic[i].addWidget(QLabel('热效率分析'))
            self.pic[i].addWidget(Effic)
            self.line2 = QtWidgets.QFrame(self)
            self.line2.setGeometry(QtCore.QRect(0, QDesktopWidget().screenGeometry().height() * 0.73,
                                                QDesktopWidget().screenGeometry().width(), 16))
            self.line2.setFrameShape(QtWidgets.QFrame.HLine)
            self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.pic[i].addWidget(self.line2)
            Coal = MyCoalMpCanvas(value)
            self.pic[i].addWidget(Coal)

        # 设置将self.pageView为中心Widget
        self.setCentralWidget(self.pageView)
        self.show()


class MyMplCanvas(FigureCanvas):
    """这是一个窗口部件，即QWidget（当然也是FigureCanvasAgg）"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # 每次plot()调用的时候，我们希望原来的坐标轴被清除(所以False)
        # self.axes.hold(False)
        fig.set_tight_layout(True)
        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyCaMplCanvas(MyMplCanvas):
    def __init__(self, value):
        self.value = value
        super(MyCaMplCanvas, self).__init__()

    def compute_initial_figure(self):
        # data = MyMplCanvas.find_data(self.day, self.hour)

        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False

        # data是选中的那一行的数据，利用data来将合格、不合格的数据求出来，存在Percentage的列表中

        # Percentage
        Percentage = [30, 70]  # 前者为合格，后者为不合格
        Percentage[0] = self.value[1] * 100
        Percentage[1] = self.value[0] * 100
        self.axes.barh(range(2), Percentage, height=0.7, color='steelblue', alpha=0.8)
        self.axes.set_yticks(range(2))
        self.axes.set_yticklabels(['合格', '不合格'])
        self.axes.set_xlim(0, 100)
        self.axes.set_xlabel('百分比 %')
        self.axes.set_title('游离钙是否合格的百分比')

        for x, y, in zip(Percentage, range(2)):
            self.axes.text(x + 5, y, '%.2f' % x, ha='right', va='center', fontsize=10)


class MyEfficMpCanvas(MyMplCanvas):
    def __init__(self, value):
        self.value = value
        super(MyEfficMpCanvas, self).__init__()

    def compute_initial_figure(self):
        #        data = MyMplCanvas.find_data(self.day, self.hour)  # data是选中那天的输入的所有数据

        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False

        # 利用data算出热耗，以及1减去热耗剩余的值，放在size列表中，后面一个是热耗
        size = [100 - self.value * 100, self.value * 100]  # 测试用
        label_list = ['', '热效率']
        color = ['yellow', 'red']
        explode = [0, 0]
        self.axes.pie(size, explode=explode, colors=color, labels=label_list, labeldistance=1.1,
                      autopct="%1.2f%%", shadow=False, startangle=90, pctdistance=0.6)
        self.axes.axis("equal")  # 设置横轴和纵轴大小相等，这样饼才是圆的
        self.axes.set_title('回转窑的热效率')
        self.axes.legend()


class MyCoalMpCanvas(QWidget):
    def __init__(self, date):
        super(MyCoalMpCanvas, self).__init__()
        self.compute_initial_figure()

    def compute_initial_figure(self):
        #        data = self.find_data(self.day, self.hour)  # 和上面的data相同

        # consumption       利用data求出煤耗
        consumption = 60

        self.Label = QLabel()
        self.lay = QVBoxLayout()

        self.Label.setText('分解炉的标煤耗：  %d   kJ/kg' % consumption)
        ft = QFont()
        ft.setPointSize(12)
        self.Label.setFont(ft)
        # self.Label.show()

        for i in range(2):
            self.lay.addWidget(QLabel(''))
        self.lay.addWidget(self.Label)
        for i in range(3):
            self.lay.addWidget(QLabel(''))

        self.setLayout(self.lay)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # form = MyDataSimDlg('2017012313')
    # form = MyDataInputDlg()
    # form = MyDataLeadInDlg()
    # form = MyStandardDlg()
    # form=MyTimeDlg()
    form = MyDataReviseDlg()
    form.show()
    app.exec_()
