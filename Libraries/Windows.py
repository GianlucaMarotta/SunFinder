from PyQt5 import QtWidgets, QtCore, uic
from Libraries.settings import *
import pyqtgraph as pg
from Libraries import globals

class PlotWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(PlotWindow, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


        # Load the UI Page
        uic.loadUi('GUI/PlotWindow.ui', self)

        # Inizializzazioni
        self.x = [i for i in range(RANGE)] # nota: RANGE è definito in settings.py
        self.plots = list()
        self.pens = list()
        self.datas = list()
        self.yi = list()
        self.list_of_plotting = [globals.V1_is_plotting, globals.V2_is_plotting, globals.V3_is_plotting,
                                 globals.V4_is_plotting, globals.DNI_is_plotting,
                                 globals.P_el_is_plotting, globals.P_az_is_plotting, globals.el_enable_is_plotting,
                                 globals.az_enable_is_plotting] + globals.new_plots

        self.n_o_p = self.number_of_plots()

        # Impostazioni assi
        l_ax = pg.AxisItem('left')
        l_ax.setGrid(100)
        b_ax = pg.AxisItem('bottom')
        b_ax.setGrid(100)
        b_ax.setLabel('sample (a.u.)')

        # Impostazioni grafico
        self.graph.setBackground('k')
        self.graph.setAxisItems({'left': l_ax, 'bottom': b_ax})
        self.graph.addLegend()

        for i in range(self.n_o_p):
            self.yi.append([0 for i in range(RANGE)])
            self.pens.append(pg.mkPen((i, self.n_o_p)))  # inserisce in una lista gli oggetti "pen" che definiscono il tratto e i colori. Li imposta automaticamente in base al numero di linee
            self.plots.append(self.graph.plot(self.x, self.yi[i], pen=self.pens[i], name=self.plotted_names[i])) # inserisce in una lista gli oggetti plot

        # updating Data
        self.INTERVAL = 1  # msec
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.INTERVAL)
        self.timer.timeout.connect(self.updateGraph)
        self.timer.start()

        # serve per mostrare solo il primo errore nel loop di update. Sfortunatamente non è stato possibile implementare "press Enter"
        self.firstException = True

    def number_of_plots(self):

        self.plotted_names = [globals.names[i] for i in range(len(self.list_of_plotting)) if self.list_of_plotting[i] == True]  # crea una lista con i nomi delle variabili da plottare


        number = sum([1 for i in range(len(self.list_of_plotting)) if self.list_of_plotting[i] == True])  # conta il numero di variabili da graficare (nota: è una list comprehension)

        return number

    def data_to_plot(self):
        # aggiorna la lista con le variabili da plottare
        new_data = []
        self.datas = [globals.dt.V1, globals.dt.V2, globals.dt.V3, globals.dt.V4, globals.dt.DNI * 1E-3,
                      globals.dt.P_el, globals.dt.P_az, globals.az_mot, globals.el_mot]

        for i in range(len(globals.list_of_id) - 5):
            new_data.append(eval('globals.dt.' + globals.list_of_id[5 + i]))

        self.datas += new_data

        j = 0

        for i in range(len(self.datas)):
            if self.list_of_plotting[i]:
                self.yi[j] = self.yi[j][1:]
                self.yi[j].append(self.datas[i])
                j += 1

    def updateGraph(self):
        # aggiorna i dati del grafico
        try:
            for i in range(self.n_o_p):
                self.data_to_plot()
                self.plots[i].setData(self.x, self.yi[i])

        except Exception as e:

                # se ci sono errori fa vedere la finestra di errore e stampa su terminale i dettagli
                globals.errorWdw.show()

                print('\n---- Generic Error! ----\n')
                print('\nThe original error message is displayed below.\n')
                print('\n' + '-' * 30)
                self.timer.stop()
                raise

class AddWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(AddWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('GUI/addWindow.ui', self)

        self.initialize()

        self.button_submit.clicked.connect(self.click_submit)
        self.button_cancel.clicked.connect(self.click_cancel)

        self.lineEdit_device.textChanged.connect(self.update_device)
        self.lineEdit_port.textChanged.connect(self.update_port)
        self.lineEdit_name.textChanged.connect(self.update_name)
        self.lineEdit_operation.textChanged.connect(self.update_operation)
        self.lineEdit_units.textChanged.connect(self.update_units)

    def update_device(self):
        self.device = self.lineEdit_device.text()

    def update_port(self):
        self.port = self.lineEdit_port.text()

    def update_name(self):
        self.name = self.lineEdit_name.text()

    def update_operation(self):
        self.operation = self.lineEdit_operation.text()

    def update_units(self):
        self.units = self.lineEdit_units.text()

    def click_submit(self):

        if (self.name and self.port) and self.operation:

            if (self.name not in globals.list_of_labels) and ((self.device + '/' + self.port) not in globals.ports):
                globals.ports.append(self.device + '/' + self.port)
                globals.list_of_labels.append(self.name)
                globals.names.append(self.name + ' ('+ self.units+')')
                globals.list_of_operations.append(self.operation)
                globals.list_of_id.append(self.id)
                globals.list_of_units.append(self.units)
                globals.new_plots.append(False)
                globals.new_saves.append(False)

        self.initialize()
        self.close()

#           exec('self.lcdNumber_added.display(globals.dt.'+globals.list_of_id[-1]+')')

    def initialize(self):
        self.id = 'V'+str(len(globals.list_of_id) + 1)

        self.device = settings.device
        self.operation = self.id
        self.name = ''
        self.port = 'ai'
        self.units = ''

        self.lineEdit_device.setText(self.device)
        self.lineEdit_port.setText(self.port)
        self.lineEdit_name.setText(self.name)
        self.lineEdit_operation.setText(self.operation)
        self.label_id.setText(self.id)

    def click_cancel(self):

        self.deleteLater()




class NewDataWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):

        super(NewDataWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('GUI/NewDataWindow.ui', self)

        self.shift = 100

        self.setGeometry(1510, 125, 300, 50 +(self.shift*len(globals.new_plots)))

        self.addnewdata()

        # updating Data
        self.INTERVAL = 1  # msec
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.INTERVAL)
        self.timer.timeout.connect(self.update)
        self.timer.start()


    def createNewData(self, i):

        id = i-1

        print(id)

        exec('self.checkBox_save_' + globals.list_of_id[id] + '= QtWidgets.QCheckBox(self.centralwidget)')
        y_cBsave = str(eval('self.checkBox_save_' + globals.list_of_id[id - 1] + '.y()') + self.shift)
        x_cBsave = str(eval('self.checkBox_save_' + globals.list_of_id[id - 1] + '.x()'))
        width_cBsave = str(eval('self.checkBox_save_' + globals.list_of_id[id - 1] + '.width()'))
        height_cBsave = str(eval('self.checkBox_save_' + globals.list_of_id[id - 1] + '.height()'))
        exec('self.checkBox_save_' + globals.list_of_id[id] + '.setGeometry(QtCore.QRect(+' + x_cBsave + ',' + y_cBsave + ',' + width_cBsave + ',' + height_cBsave + '))')

        exec('self.checkBox_plot_' + globals.list_of_id[id] + '= QtWidgets.QCheckBox(self.centralwidget)')
        y_cBplot = str(eval('self.checkBox_plot_' + globals.list_of_id[id - 1] + '.y()') + self.shift)
        x_cBplot = str(eval('self.checkBox_plot_' + globals.list_of_id[id - 1] + '.x()'))
        width_cBplot = str(eval('self.checkBox_plot_' + globals.list_of_id[id - 1] + '.width()'))
        height_cBplot = str(eval('self.checkBox_plot_' + globals.list_of_id[id - 1] + '.height()'))
        exec('self.checkBox_plot_' + globals.list_of_id[id] + '.setGeometry(QtCore.QRect(+' + x_cBplot + ',' + y_cBplot + ',' + width_cBplot + ',' + height_cBplot + '))')


        exec('self.lcdNumber_' + globals.list_of_id[id] + '= QtWidgets.QLCDNumber(self.centralwidget)')
        y_lcd = str(eval('self.lcdNumber_' + globals.list_of_id[id - 1] + '.y()') + self.shift)
        x_lcd = str(eval('self.lcdNumber_' + globals.list_of_id[id - 1] + '.x()'))
        width_lcd = str(eval('self.lcdNumber_' + globals.list_of_id[id - 1] + '.width()'))
        height_lcd = str(eval('self.lcdNumber_' + globals.list_of_id[id - 1] + '.height()'))
        exec('self.lcdNumber_' + globals.list_of_id[id] + '.setGeometry(QtCore.QRect(+' + x_lcd + ',' + y_lcd + ',' + width_lcd + ',' + height_lcd + '))')

        exec('self.label_id_' + globals.list_of_id[id] + '= QtWidgets.QLabel(self.centralwidget)')
        y_id = str(eval('self.label_id_' + globals.list_of_id[id - 1] + '.y()') + self.shift)
        x_id = str(eval('self.label_id_' + globals.list_of_id[id - 1] + '.x()'))
        width_id = str(eval('self.label_id_' + globals.list_of_id[id - 1] + '.width()'))
        height_id = str(eval('self.label_id_' + globals.list_of_id[id - 1] + '.height()'))
        exec('self.label_id_' + globals.list_of_id[id] + '.setGeometry(QtCore.QRect(+' + x_id + ',' + y_id + ',' + width_id + ',' + height_id + '))')
        font = QtGui.QFont()
        font.setPointSize(7)
        exec('self.label_id_' + globals.list_of_id[id] + '.setFont(font)')

        exec('self.label_name_' + globals.list_of_id[id] + '= QtWidgets.QLabel(self.centralwidget)')
        y_name = str(eval('self.label_name_' + globals.list_of_id[id - 1] + '.y()') + self.shift)
        x_name = str(eval('self.label_name_' + globals.list_of_id[id - 1] + '.x()'))
        width_name = str(eval('self.label_name_' + globals.list_of_id[id - 1] + '.width()'))
        height_name = str(eval('self.label_name_' + globals.list_of_id[id - 1] + '.height()'))
        exec('self.label_name_' + globals.list_of_id[id] + '.setGeometry(QtCore.QRect(+' + x_name + ',' + y_name + ',' + width_name + ',' + height_name + '))')
        font = QtGui.QFont()
        font.setPointSize(12)
        exec('self.label_name_' + globals.list_of_id[id] + '.setFont(font)')

        exec('self.label_port_' + globals.list_of_id[id] + '= QtWidgets.QLabel(self.centralwidget)')
        y_port = str(eval('self.label_port_' + globals.list_of_id[id - 1] + '.y()') + self.shift)
        x_port = str(eval('self.label_port_' + globals.list_of_id[id - 1] + '.x()'))
        width_port = str(eval('self.label_port_' + globals.list_of_id[id - 1] + '.width()'))
        height_port = str(eval('self.label_port_' + globals.list_of_id[id - 1] + '.height()'))
        exec('self.label_port_' + globals.list_of_id[id] + '.setGeometry(QtCore.QRect(+' + x_port + ',' + y_port + ',' + width_port + ',' + height_port + '))')
        ont = QtGui.QFont()
        font.setPointSize(7)
        exec('self.label_port_' + globals.list_of_id[id] + '.setFont(font)')

        exec('self.label_unit_' + globals.list_of_id[id] + '= QtWidgets.QLabel(self.centralwidget)')
        y_unit = str(eval('self.label_unit_' + globals.list_of_id[id - 1] + '.y()') + self.shift)
        x_unit = str(eval('self.label_unit_' + globals.list_of_id[id - 1] + '.x()'))
        width_unit = str(eval('self.label_unit_' + globals.list_of_id[id - 1] + '.width()'))
        height_unit = str(eval('self.label_unit_' + globals.list_of_id[id - 1] + '.height()'))
        exec('self.label_unit_' + globals.list_of_id[id] + '.setGeometry(QtCore.QRect(+' + x_unit + ',' + y_unit + ',' + width_unit + ',' + height_unit + '))')

        exec('self.button_delete_' + globals.list_of_id[id] + '= QtWidgets.QToolButton(self.centralwidget)')
        y_delete = str(eval('self.button_delete_' + globals.list_of_id[id - 1] + '.y()') + self.shift)
        x_delete = str(eval('self.button_delete_' + globals.list_of_id[id - 1] + '.x()'))
        width_delete = str(eval('self.button_delete_' + globals.list_of_id[id - 1] + '.width()'))
        height_delete = str(eval('self.button_delete_' + globals.list_of_id[id - 1] + '.height()'))
        exec('self.button_delete_' + globals.list_of_id[id] + '.setGeometry(QtCore.QRect(+' + x_delete + ',' + y_delete + ',' + width_delete + ',' + height_delete + '))')
        exec('self.button_delete_' + globals.list_of_id[id] + '.setText("X")')

    def addnewdata(self):

        for i in range(len(globals.list_of_id) - 5):

            if len(globals.list_of_id) >= 7 and i>=1:
                self.createNewData(6 + i)

            exec('self.label_id_' + globals.list_of_id[5 + i] + '.setText("id = [" + globals.list_of_id[5+i]+"]")')
            exec('self.label_name_' + globals.list_of_id[5 + i] + '.setText(globals.list_of_labels[5+i])')
            exec('self.label_port_' + globals.list_of_id[5 + i] + '.setText("port = [" + globals.ports[5+i]+"]")')
            exec('self.label_unit_' + globals.list_of_id[5 + i] + '.setText("("+globals.list_of_units[5+i]+")")')
            eval('self.button_delete_' + globals.list_of_id[5 + i] + '.clicked.connect(lambda id, self=self: self.delete_variable(id=' + str(5 + i) + '))')

            eval('self.checkBox_plot_' + globals.list_of_id[5 + i] + '.stateChanged.connect(lambda id, self=self: self.setPlot(id='+ str(i) +'))')
            eval('self.checkBox_save_' + globals.list_of_id[5 + i] + '.stateChanged.connect(lambda id, self=self: self.setSave(id=' + str(i) + '))')

    def setPlot(self, id):
        globals.new_plots[id] = not globals.new_plots[id]
        print(globals.new_plots)

    def setSave(self, id):
        globals.new_saves[id] = not globals.new_saves[id]
        print(globals.new_saves)

    def update(self):

        for i in range(len(globals.list_of_id) - 5):

            exec('self.lcdNumber_' + globals.list_of_id[5 + i] + '.display(globals.dt.' + globals.list_of_id[5 + i] + ')')

        if len(globals.list_of_id) == 5:
            self.deleteLater()

    def delete_variable(self, id):

        globals.ports.pop(id)
        globals.list_of_labels.pop(id)
        globals.list_of_operations.pop(id)
        globals.list_of_id.pop(id)
        globals.list_of_units.pop(id)
        globals.new_plots.pop(id-5)
        globals.new_saves.pop(id - 5)
        globals.names.pop(id-5)


        if len(globals.list_of_id) == 5:
            self.deleteLater()