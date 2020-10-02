import time
from Libraries.Experiment import Data
from PyQt5 import QtWidgets, uic
from Libraries import globals


class SaveFile:

    def __init__(self):
        self.list_of_saving = [True, globals.V1_is_saving, globals.V2_is_saving, globals.V3_is_saving, globals.V4_is_saving,
                             globals.DNI_is_saving, globals.P_el_is_saving, globals.P_az_is_saving, globals.az_enable_is_saving, globals.el_enable_is_saving] + globals.new_saves
        self.time_0 = 0

    def header_lines(self, comment=''):
        with open(globals.filename, 'w') as file:
            string_name_to_save = ''
            name_to_save = ['Time (s)'] + globals.names
            list_name_to_save = [name_to_save[i] for i in range(len(name_to_save)) if self.list_of_saving[i]]

            for i in range(len(list_name_to_save)):
                string_name_to_save += list_name_to_save[i] + '\t'

            file.write('# Sun Finder - Solar Collector Lab - CNR-INO Florence (Italy)\n')
            file.write('# ' + comment + '\n')
            file.write('# Start Time: ' + time.asctime() +'\n')
            globals.time_0 = time.time()
            file.write('#' + string_name_to_save + '\n')


    def save_data(self):
        new_data = []

        data_to_save = [round(Data.time - globals.time_0, 4), round(globals.dt.V1, 4), round(globals.dt.V2, 4), round(
            globals.dt.V3, 4), round(globals.dt.V4, 4),
                        round(globals.dt.DNI, 4), round(globals.dt.P_el, 4), round(globals.dt.P_az, 4), int(
                globals.az_mot), int(globals.el_mot)]

        for i in range(len(globals.list_of_id) - 5):
            new_data.append(round(eval('globals.dt.' + globals.list_of_id[5 + i]),4))

        data_to_save += new_data

        string_data_to_save = ''

        for i in range(len(data_to_save)):
            if self.list_of_saving[i]:
                string_data_to_save += str(data_to_save[i]) + '\t'

        with open(globals.filename, 'a') as file:
            time_1 = time.time()

            if time_1 - self.time_0 >= globals.save_update_time:
                self.time_0 = time.time()
                file.write(string_data_to_save + '\n')

    def stop_saving(self): #ancora da implementare
        with open(globals.filename, 'a') as file:
            file.write('# \n')
            file.write('# Stop Time: ' + time.asctime())


class SaveWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(SaveWindow, self).__init__(*args, **kwargs)
        self.sv = SaveFile()
        # Load the UI Page
        uic.loadUi('GUI/SaveWindow.ui', self)

        globals.save_update_time = self.spinBox_updatingTime.value()

        self.button_choosePath.clicked.connect(self.choosePath)
        self.button_startSaving.clicked.connect(self.start_saving)
        self.button_cancel.clicked.connect(self.close)

        self.spinBox_updatingTime.valueChanged.connect(self.set_updatingTime)

    def set_updatingTime(self):

        globals.save_update_time = self.spinBox_updatingTime.value()

    def choosePath(self):
        filename, filter = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption='Save file')
        self.lineEdit_insertPath.setText(filename)


    def start_saving(self):
        globals.filename = self.lineEdit_insertPath.text()

        if globals.filename:
            self.sv.header_lines(comment= self.lineEdit_comment.text())
            globals.is_writing_data = True #aggiorna l'update

        self.close()

