# # ----------------------------------------------------------- # #
# #           CNR - INO  Solar Collector Lab                    # #
# #        "Sun Finder"  - versione del 01/10/20                # #
# # developed by Gianluca Marotta - gianlucamarotta18@gmail.com # #
# # ----------------------------------------------------------- # #

# # ------------------- # #
# # Importa le librerie # #
# # ------------------- # #

# nota: in una libreria ci possono essere variabili, funzioni (chiamate metodi), oggetti (insiemi di variabili e metodi)

# nel primo blocco vengono importate alcune librerie "di sistema".
# In caso di errore vanno installate da prompt con "pip install <nomelibreria>"
import sys
from PyQt5 import QtWidgets, QtCore, uic, QtGui
import pyqtgraph as pg
import numpy as np
import time
import datetime
import pandas as pd
from pvlib import solarposition
# nel secondo blocco vengono importate le librerie invece create appositamente per questo programma. 
# Sono file ".py" e sono presenti nella cartella "Libraries".
from Libraries.Experiment import Hardware, Data
from Libraries.Ephemerides import EphemeridesWindow
from Libraries.Windows import PlotWindow
from Libraries.Save import SaveFile, SaveWindow
from Libraries.AddData import AddWindow, NewDataWindow
from Libraries import globals, settings


# L'oggetto "MainWindow" definisce la finestra principale. Al suo interno sono definite le operazioni del programma
# nota: gli argomenti di un'"oggetto" sono altri oggetti di cui esso "eredita" variabili e metodi (vedi "Inheritance").
# Essi si chiamano oggetti "parent" (nell'esempio "QtWidgets.QMainWindow")

class MainWindow(QtWidgets.QMainWindow):

    # # ----------------------------- # #
    # # Inizializzazione dell'oggetto # #
    # # ----------------------------- # #

    # Il metodo __init__ è un metodo speciale che definisce le operazioni effettuate alla creazione dell'oggetto.
    def __init__(self, *args, **kwargs):

        # La riga seguente effettua le operazioni contenute nell'"__init__" dell'oggetto "parent"
        super(MainWindow, self).__init__(*args, **kwargs)

        # # ---------------- # #
        # # Load the UI Page # #
        # # ---------------- # #
        # Carica l'interfaccia grafica creata con QTCreator.
        # definisce gli "oggetti" grafici che vengono creati con il nome indicato nel QtDesigner.
        # Per creare e modificare questi file usare "QtDesigner"

        uic.loadUi('GUI/MainWindow_SunFinder.ui', self)

        # # ------------------------------- # #
        # # Inizializazione delle variabili # #
        # # ------------------------------- # #

        # Le seguenti sono variabili definite in "globals.py".
        # globals serve ad avere uno spazio di variabili esterno a MainWindow che può comunicare con gli altri oggetti.
        # per il loro significato si faccia riferimento al file "globals.py" in Libraries

        # Le "flags" vengono inizializzate False
        globals.is_moving_az = False
        globals.is_moving_el = False
        globals.is_finding_az = False
        globals.is_finding_el = False
        globals.is_showing_graph = False
        globals.V1_is_plotting = False
        globals.is_writing_data = False

        # !!!!!cos'é?
        globals.az_mot = 0
        globals.el_mot = 0

        # !!!!!cos'é?
        globals.time_0 = 0

        # liste iniziali relative alle variabili
        globals.list_of_id = ['V1', 'V2', 'V3', 'V4', 'DNI']
        globals.list_of_labels = ['V1', 'V2', 'V3', 'V4', 'DNI']
        globals.list_of_units = ['V', 'V', 'V', 'V', 'W/m^2']
        globals.list_of_operations = ['V1', 'V2', 'V3', 'V4', 'DNI*400']

        globals.new_plots = []
        globals.new_data = []
        globals.new_saves = []

        globals.names = ['V1 (V)', 'V2 (V)', 'V3 (V)', 'V4 (V)', 'DNI (W/m^2)',
                         'Position Elevation (a.u.)', 'Position Azimut (a.u.)', 'Azimut Motion (a.u.)',
                         'Elevation Motion (a.u.)']

        # E' la finestra che viene mostrata se ci sono errori nell'esecuzione

        globals.errorWdw = QtWidgets.QMessageBox()
        globals.errorWdw.setWindowTitle('Error!')
        globals.errorWdw.setText('There is an error!! - Check Terminal for specification')
        globals.errorWdw.setIcon(QtWidgets.QMessageBox.Critical)

        # queste variabili invece sono create e inizializzate nello spazio delle variabili dell'oggetto "MainWindow".
        # "self" definisce uno spazio per gli oggetti interni all'oggetto in cui vengono definiti. 
        # Al di fuori di MainWindow queste variabili non esistono
        self.in_finding_from_east = False
        self.in_finding_from_west = False
        self.in_finding_from_up = False
        self.in_finding_from_down = False

        self.az_single_pulse = False
        self.el_single_pulse = False

        # alcune variabili sono inizializzate con i valori di default definiti nel file "settings.py"
        self.az_threshold = settings.default_az_threshold
        self.el_threshold = settings.default_el_threshold
        self.buffer_zone = settings.default_buffer_zone
        self.startValue = settings.default_startValue

        # la velocità dei motori è impostata al massimo all'inizio
        self.velocity_azimuth = 1
        self.velocity_elevation = 1

        # la variabile old_number serve per il controllo nel caso vengano aggiunte nuove variabili
        self.old_number_of_data = len(globals.list_of_id)

        # usa il metodo "setValue" degli oggetti "SpinBox" definiti nel file ".ui" che imposta il valore della SpinBox
        # nota: dopo il caricamento del file ".ui" tutti gli oggetti grafici appartengono a self, ovvero esistono all'interno di MainWindow
        # (nota: sono gli unici oggetti grafici che devono essere inizializzati)
        self.dial_az_velocity.setValue(self.velocity_azimuth * 100)
        self.dial_el_velocity.setValue(self.velocity_elevation * 100)

        self.spinBox_az_threshold.setValue(self.az_threshold)
        self.spinBox_el_threshold.setValue(self.el_threshold)
        self.spinBox_buffer_zone.setValue(self.buffer_zone)
        self.spinBox_startValue.setValue(self.startValue)
        self.spinBox_az_velocity.setValue(self.velocity_azimuth)
        self.spinBox_el_velocity.setValue(self.velocity_elevation)


        # crea l'oggetto "hw" definito nel file Experiment.py come Hardware
        self.hw = Hardware()
        # manda a tutti i motori il segnale "off".
        # In contemporanea controlla che non ci siano errori
        #[self.hw.send_signal_off(settings.dports[i]) for i in settings.dports] # Turn off motors

        # crea l'oggetto definito in SaveFile definito nel file Save.py
        self.sv = SaveFile()

        # # -------------------------- # #
        # # Azioni legate ai "Buttons" # #
        # # -------------------------- # #
        # per ogni "button" presente nell'interfaccia, definisce l'azione da effettuare quando vengono cliccati
        # le azioni sono definite da un metodo della MainWindow (definito successivamente)

        self.button_az_enable.clicked.connect(self.click_az_en)
        self.button_el_enable.clicked.connect(self.click_el_en)
        self.button_showGraph.clicked.connect(self.click_showGraph)
        self.button_saveData.clicked.connect(self.click_save_file)
        self.button_az_find.clicked.connect(self.click_az_find)
        self.button_el_find.clicked.connect(self.click_el_find)
        self.button_addData.clicked.connect(self.click_add_data)
        self.button_showEphemerides.clicked.connect(self.click_show_ephem)

        # # ---------------------------- # #
        # # Azioni legate agli "Sliders" # #
        # # ---------------------------  # #
        # per ogni "slider" definisce l'azione da effettuare quando viene spostato

        self.slider_az_direction.valueChanged.connect(lambda: self.set_direction_az(dir=None)) # nota: l'utilizzo di lambda che definisce un metodo in una riga
        self.slider_el_direction.valueChanged.connect(lambda: self.set_direction_el(dir=None))

        # # ----------------------- # #
        # # Azioni legate ai "dial" # #
        # # ----------------------- # #
        # sono le manopole della velocità

        self.dial_az_velocity.valueChanged.connect(self.set_velocity_azimuth_dial)
        self.dial_el_velocity.valueChanged.connect(self.set_velocity_elevation_dial)

        # # ------------------------------- # #
        # # Azioni legate agli "Spin Boxes" # #
        # # ------------------------------- # #
        # per ogni "spinBox" definisce l'azione da effettuare quando viene cambiato il valore

        self.spinBox_az_threshold.valueChanged.connect(self.set_az_threshold)
        self.spinBox_el_threshold.valueChanged.connect(self.set_el_threshold)
        self.spinBox_buffer_zone.valueChanged.connect(self.set_buffer_zone)
        self.spinBox_startValue.valueChanged.connect(self.set_startValue)
        self.spinBox_az_velocity.valueChanged.connect(self.set_velocity_azimuth_spinBox)
        self.spinBox_el_velocity.valueChanged.connect(self.set_velocity_elevation_spinBox)

        # # ----------------------------- # #
        # # Azioni legate alle "checkBox" # #
        # # ----------------------------- # #

        # Plot Selection
        self.checkBox_V1_plot.stateChanged.connect(self.V1_plot)
        self.checkBox_V2_plot.stateChanged.connect(self.V2_plot)
        self.checkBox_V3_plot.stateChanged.connect(self.V3_plot)
        self.checkBox_V4_plot.stateChanged.connect(self.V4_plot)
        self.checkBox_DNI_plot.stateChanged.connect(self.DNI_plot)
        self.checkBox_P_el_plot.stateChanged.connect(self.P_el_plot)
        self.checkBox_P_az_plot.stateChanged.connect(self.P_az_plot)
        self.checkBox_az_enable_plot.stateChanged.connect(self.az_enable_plot)
        self.checkBox_el_enable_plot.stateChanged.connect(self.el_enable_plot)

        # Save Selection
        self.checkBox_V1_save.stateChanged.connect(self.V1_save)
        self.checkBox_V2_save.stateChanged.connect(self.V2_save)
        self.checkBox_V3_save.stateChanged.connect(self.V3_save)
        self.checkBox_V4_save.stateChanged.connect(self.V4_save)
        self.checkBox_DNI_save.stateChanged.connect(self.DNI_save)
        self.checkBox_P_el_save.stateChanged.connect(self.P_el_save)
        self.checkBox_P_az_save.stateChanged.connect(self.P_az_save)
        self.checkBox_az_enable_save.stateChanged.connect(self.az_enable_save)
        self.checkBox_el_enable_save.stateChanged.connect(self.el_enable_save)

        # Single Pulse
        self.checkBox_az_single_pulse.stateChanged.connect(self.change_state_az_single_pulse)
        self.checkBox_el_single_pulse.stateChanged.connect(self.change_state_el_single_pulse)

        # # -------------------------------- # #
        # # Definizione del "Position Graph" # #
        # # -------------------------------- # #

        # x e y sono le variabili plottate.
        # vengono inizializzate a 0, 0 e un NaN come secondo elemento
        # a quanto pare questo plot non permette di plottare liste con meno di due elementi
        self.x = [0, np.nan]
        self.y = [0, np.nan]

        # definisce gli oggetti degli assi e imposta la "griglia"
        l_axis = pg.AxisItem('left')
        l_axis.setGrid(100)
        b_axis = pg.AxisItem('bottom')
        b_axis.setGrid(100)
        self.position_graph.setAxisItems({'left': l_axis, 'bottom': b_axis})
        self.position_graph.setXRange(-1, 1)
        self.position_graph.setYRange(-1, 1)

        # imposta lo sfondo del grafico
        self.position_graph.setBackground('w')

        # disegna le linee nere verticali e orizzontali che disegnano i quadranti
        self.vline_neg= self.position_graph.plot([-1, -1], [-1, 1], pen=pg.mkPen('k'))
        self.vline_pos= self.position_graph.plot([1, 1], [-1, 1], pen=pg.mkPen('k'))
        self.hline_neg = self.position_graph.plot([-1, 1], [-1, -1], pen=pg.mkPen('k'))
        self.hline_pos = self.position_graph.plot([-1, 1], [1, 1], pen=pg.mkPen('k'))
        self.hline_0 = self.position_graph.plot([-1, 1], [0, 0], pen=pg.mkPen('k'))
        self.vline_0 = self.position_graph.plot([0, 0], [-1, 1], pen=pg.mkPen('k'))

        # crea l'oggetto plot
        self.plot = self.position_graph.plot(self.x, self.y, pen=None, symbol='+', symbolSize=30, symbolPen=None)

        # # ------------- # #
        # # Updating Data # #
        # # ------------- # #
        # imposta delle azioni legate ad un timer che verranno effettuate ad ogni "clock"

        # di fatto è un loop che è attivo fino a che non si termina l'applicazione
        # definisce l'intervallo tra due "clock"
        self.INTERVAL = 1 #msec
        # crea un'oggetto timer, definito nelle librerie di pyqt
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.INTERVAL)
        # definisce l'azione da effetturare ogni volta che il timer supera il valore di INTERVAL.
        self.timer.timeout.connect(self.update)
        # fa partire il timer (quindi il "loop")
        self.timer.start()

    # -> di seguito sono definiti tutti i metodi dell'oggetto MainWindow
    # -> essi sono utilizzati all'interno di __init__

    # # -------------- # #
    # # Update methods # #
    # # -------------- # #
    # le azioni da effettuare ad ogni "clock"

    def update(self):

        try:
            # acquisice i dati utilizzato il metodo "acquisition" dell'oggetto Hardware definito in Experiment.py
            self.hw.acquisition()

            # crea un oggetto "Data" definito in "Experiment.py". Nell'init dell'oggetto vengono spacchettati i dati acquisiti
            globals.dt = Data()

            # aggiorna i valori dei display numerici
            self.lcdNumber_P_az.display(globals.dt.P_az)
            self.lcdNumber_P_el.display(globals.dt.P_el)
            self.lcdNumber_V1.display(globals.dt.V1)
            self.lcdNumber_V2.display(globals.dt.V2)
            self.lcdNumber_V3.display(globals.dt.V3)
            self.lcdNumber_V4.display(globals.dt.V4)
            self.lcdNumber_DNI.display(globals.dt.DNI)
            self.lcdNumber_time.display(globals.updating_time)

            # Aggiorna i dati del "Position Graph"
            self.x = [globals.dt.P_az, np.nan]
            self.y = [globals.dt.P_el, np.nan]
            self.plot.setData(self.x, self.y)  # Update the data.

            # Salva i dati, quando avviato il salvataggio.
            # il valore di verità della variabile "globals.is_writing_data" e definito dal click del "button_save_data"
            if globals.is_writing_data:
                self.sv.save_data()
                self.button_saveData.setText('Stop Saving Data')
                self.led_saving.setPixmap(QtGui.QPixmap("Images/green_light.png"))
                self.label_saving.setText('is saving!')

            # Apre la nuova finestra quando vengono aggiunte nuove variabili. controlla la variabile old_number of datas
            if (len(globals.list_of_id) != self.old_number_of_data) and hasattr(globals.dt, globals.list_of_id[-1]) :

                # se esiste già una finestra la elimina per poterne creare una nuova
                if globals.nDWdw:
                    try:
                        globals.nDWdw.deleteLater()
                        globals.nDWdw = None
                    except:
                        globals.nDWdw = None

                # crea la finestra e la mostra
                globals.nDWdw = NewDataWindow()
                globals.nDWdw.setWindowTitle('Temporary Data')
                globals.nDWdw.show()

            if globals.is_moving_az:
                self.move_az()
            if globals.is_moving_el:
                self.move_el()

            if globals.is_finding_az:
                self.find_az()
            if globals.is_finding_el:
                self.find_el()

            # aggiorna il numero di dati per l'iterazione successiva del loop
            self.old_number_of_data = len(globals.list_of_id)


        except Exception:
            # se ci sono errori fa vedere la finestra di errore e stampa su terminale i dettagli
            globals.errorWdw.show()

            print('\n---- Error! ----\n')
            print('\nThe original error message is displayed below.')
            print('\n' + '-' * 30 + '\n')
            self.timer.stop()
            raise

    # # ------------- # #
    # # Click methods # #
    # # ------------- # #
    # sono i metodi che vengono eseguiti quando vengono cliccati i "buttons"


    def click_az_en(self):
        # se è già in movimento ferma il motore dell'azimut, altrimenti lo accende
        # attiva i "motion methods" definiti sotto
        if globals.is_moving_az:
            self.not_move_az()
        else:
            self.move_az()

    def click_el_en(self):
        # idem con il motore dell'elevation
        if globals.is_moving_el:
            self.not_move_el()
        else:
            self.move_el()

    def click_showGraph(self):
        # apre una finestra in cui viene mostrato il grafico delle variabili selezionate
        globals.var_opening_graph = True
        self.graph = PlotWindow(self)
        self.graph.setWindowTitle('Plot Data')
        self.graph.show()

    def click_save_file(self):
        # apre la finestra per il salvataggio dati.
        # crea e mostra l'oggetto corrispondente, definito in SaveWindow
        if not globals.is_writing_data:
            self.saveWdw = SaveWindow(self)
            self.saveWdw.setWindowTitle('Save Data')
            self.saveWdw.show()
            self.sv = SaveFile()

            #self.button_saveData.setText('Stop Saving Data')
        else:
            globals.is_writing_data = False
            self.button_saveData.setText('Save Data')
            self.sv.stop_saving()
            self.led_saving.setPixmap(QtGui.QPixmap("Images/red_light.png"))
            self.label_saving.setText('not saving')

    def click_add_data(self):
        self.addWdw = AddWindow(self)
        self.addWdw.setWindowTitle('Add Data')
        self.addWdw.show()

    def click_az_find(self):
        if globals.is_finding_az:
            self.led_az_find.setPixmap(QtGui.QPixmap("Images/red_light.png"))
            self.button_az_find.setText('Enable')
            globals.is_finding_az = False
            self.not_move_az()
        else:
            self.led_az_find.setPixmap(QtGui.QPixmap("Images/green_light.png"))
            self.button_az_find.setText('Stop')
            globals.is_finding_az = True

    def click_el_find(self):
        if globals.is_finding_el:
            self.led_el_find.setPixmap(QtGui.QPixmap("Images/red_light.png"))
            self.button_el_find.setText('Enable')
            globals.is_finding_el = False
            self.not_move_el()
        else:
            self.led_el_find.setPixmap(QtGui.QPixmap("Images/green_light.png"))
            self.button_el_find.setText('Stop')
            globals.is_finding_el = True

    def click_show_ephem(self):
        self.ephWdw = EphemeridesWindow(self)
        self.ephWdw.setWindowTitle('Ephemerides Calculation')
        self.ephWdw.show()
    # # -------------------- # #
    # # Read SpinBox methods # #
    # # -------------------- # #

    def set_buffer_zone(self):
        self.buffer_zone = self.spinBox_buffer_zone.value()

    def set_az_threshold(self):
        self.az_threshold = self.spinBox_az_threshold.value()

    def set_el_threshold(self):
        self.el_threshold = self.spinBox_el_threshold.value()

    def set_startValue(self):
        self.startValue = self.spinBox_startValue.value()

    # # ------------- # #
    # # Dial methods  # #
    # # ------------- # #

    def set_velocity_azimuth_dial(self):

        self.velocity_azimuth = self.dial_az_velocity.value()/100
        self.spinBox_az_velocity.setValue(self.velocity_azimuth)

    def set_velocity_azimuth_spinBox(self):

        self.velocity_azimuth = self.spinBox_az_velocity.value()
        self.dial_az_velocity.setValue(int(self.velocity_azimuth*100))

    def set_velocity_elevation_dial(self):

        self.velocity_elevation = self.dial_el_velocity.value() / 100
        self.spinBox_el_velocity.setValue(self.velocity_elevation)

    def set_velocity_elevation_spinBox(self):
        self.velocity_elevation = self.spinBox_el_velocity.value()
        self.dial_el_velocity.setValue(int(self.velocity_elevation * 100))


    # # --------------- # #
    # # Slider methods  # #
    # # --------------- # #
    # sono le azioni controllate dagli slider.
    # impostano la direzione di movimento dei motori

    def set_direction_az(self, dir=None):
        if dir == None:
            if self.slider_az_direction.sliderPosition() == 0:
                self.hw.send_signal_on(settings.dports['port_dir_az'])
            else:
                self.hw.send_signal_off(settings.dports['port_dir_az'])

        elif dir == 'East':
            self.hw.send_signal_on(settings.dports['port_dir_az'])

        elif dir == 'West':
            self.hw.send_signal_off(settings.dports['port_dir_az'])


    def set_direction_el(self, dir=None):
        if dir == None:
            if self.slider_el_direction.sliderPosition() == 0:
                self.hw.send_signal_off(settings.dports['port_dir_el'])
            else:
                self.hw.send_signal_on(settings.dports['port_dir_el'])

        elif dir == 'Down':
            self.hw.send_signal_off(settings.dports['port_dir_el'])

        elif dir == 'Up':
            self.hw.send_signal_on(settings.dports['port_dir_el'])

    # # -------------- # #
    # # Motion methods # #
    # # -------------- # #
    # sono i metodi che mettono in movimento i motori

    def move_az(self):
        self.led_az_enable.setPixmap(QtGui.QPixmap("Images/green_light.png"))
        self.button_az_enable.setText('Stop')
        globals.is_moving_az = True
        globals.az_mot = 1

        if self.az_single_pulse:
            self.hw.send_signal_on(port=settings.dports['port_en_az'])
            time.sleep(settings.time_on)
            self.not_move_az()

        else:

            if self.velocity_azimuth == 1:
                self.hw.send_signal_on(settings.dports['port_en_az'])  # Accende il motore dell'Azimut

            else:
                time_off = settings.time_on / self.velocity_azimuth - settings.time_on
                self.hw.send_signal_on(port=settings.dports['port_en_az'])
                time.sleep(settings.time_on)
                self.hw.send_signal_off(port=settings.dports['port_en_az'])
                time.sleep(time_off)

    def not_move_az(self):
        self.led_az_enable.setPixmap(QtGui.QPixmap("Images/red_light.png"))
        self.button_az_enable.setText('Enable')
        globals.is_moving_az = False
        self.hw.send_signal_off(settings.dports['port_en_az'])  # Spegne il motore dell'Azimut
        globals.az_mot = 0

    def move_el(self):

        self.led_el_enable.setPixmap(QtGui.QPixmap("Images/green_light.png"))
        self.button_el_enable.setText('Stop')
        globals.is_moving_el = True
        globals.el_mot = 1

        if self.el_single_pulse:
            self.hw.send_signal_on(port=settings.dports['port_en_el'])
            time.sleep(settings.time_on)
            self.not_move_el()

        else:

            if self.velocity_elevation == 1:
                self.hw.send_signal_on(settings.dports['port_en_el'])  # Accende il motore dell'Elevation
            else:
                time_off = settings.time_on / self.velocity_elevation - settings.time_on
                self.hw.send_signal_on(port=settings.dports['port_en_el'])
                time.sleep(settings.time_on)
                self.hw.send_signal_off(port=settings.dports['port_en_el'])
                time.sleep(time_off)

    def not_move_el(self):
        self.led_el_enable.setPixmap(QtGui.QPixmap("Images/red_light.png"))
        self.button_el_enable.setText('Enable')
        globals.is_moving_el = False
        self.hw.send_signal_off(settings.dports['port_en_el'])  # Spegne il motore dell'Azimut
        globals.el_mot = 0


    # # ------------------ # #
    # #   Finding methods  # #
    # # ------------------ # #

    def find_az(self):
        self.thresh_find_az()

    def find_el(self):
        self.thresh_find_el()

    def not_find_az(self):
        self.led_az_find.setPixmap(QtGui.QPixmap("Images/red_light.png"))
        self.button_az_find.setText('Enable')
        globals.is_finding_az = False
        self.not_move_az()

    def not_find_el(self):
        self.led_el_find.setPixmap(QtGui.QPixmap("Images/red_light.png"))
        self.button_el_find.setText('Enable')
        globals.is_finding_el = False
        self.not_move_el()



    def thresh_find_az(self):

        if ((globals.dt.V1 > self.startValue) and (globals.dt.V2 > self.startValue)) and (
                (globals.dt.V3 > self.startValue) and (globals.dt.V4 > self.startValue)):

            if globals.dt.P_az >= self.az_threshold:
                self.set_direction_az(dir='West')
                self.slider_az_direction.setValue(1)
                self.in_finding_from_west = True

            if self.in_finding_from_west:
                if (globals.dt.P_az > -self.az_threshold) :
                    self.move_az()
                else:
                    self.not_move_az()
                    self.in_finding_from_west = False
            else:
                if globals.dt.P_az <= -self.az_threshold-self.buffer_zone:
                    self.set_direction_az(dir='East')
                    self.in_finding_from_east = True
                    self.slider_az_direction.setValue(0)

            if self.in_finding_from_east:
                if (globals.dt.P_az < -self.az_threshold) :
                    self.move_az()
                else:
                    self.not_move_az()
                    self.in_finding_from_east = False
        else:
            self.not_move_az()

    def thresh_find_el(self):

        now = datetime.datetime.now()
        date = str(now.year) + '-' + str(now.month) + '-'+ str(now.day)

        times = pd.date_range(start=date, end=date, freq=None, tz=settings.timeZone)

        solpos = solarposition.sun_rise_set_transit_spa(times, settings.lat, settings.lon)
        noon = solpos.transit.array

        if ((globals.dt.V1 > self.startValue) and (globals.dt.V2 > self.startValue)) and (
                (globals.dt.V3 > self.startValue) and (globals.dt.V4 > self.startValue)):

            # se si è prima del mezzogiorno
            if datetime.datetime.now().hour < noon.hour and datetime.datetime.now().minute < noon.minute:

                if globals.dt.P_el >= self.el_threshold:
                    self.set_direction_el(dir='Down')
                    self.slider_el_direction.setValue(0)
                    self.in_finding_from_up = True

                if self.in_finding_from_up:
                    if globals.dt.P_el > -self.el_threshold:
                        self.move_el()
                    else:
                        self.not_move_el()
                        self.in_finding_from_up = False

                else:
                    if globals.dt.P_el <= -self.el_threshold-self.buffer_zone:
                        self.set_direction_el(dir='Up')
                        self.in_finding_from_down = True
                        self.slider_el_direction.setValue(1)

                if self.in_finding_from_down:
                    if (globals.dt.P_el < -self.el_threshold) :
                        self.move_el()
                    else:
                        self.not_move_el()
                        self.in_finding_from_down = False
            # dopo mezzogiorno
            else:

                if globals.dt.P_el <= -self.el_threshold:
                    self.set_direction_el(dir='Up')
                    self.slider_el_direction.setValue(1)
                    self.in_finding_from_down = True

                if self.in_finding_from_down:
                    if globals.dt.P_el < self.el_threshold:
                        self.move_el()
                    else:
                        self.not_move_el()
                        self.in_finding_from_down = False

                else:
                    if globals.dt.P_el >= self.el_threshold + self.buffer_zone:
                        self.set_direction_el(dir='Down')
                        self.in_finding_from_up = True
                        self.slider_el_direction.setValue(0)

                if self.in_finding_from_up:
                    if (globals.dt.P_el > self.el_threshold):
                        self.move_el()
                    else:
                        self.not_move_el()
                        self.in_finding_from_up = False
        else:
            self.not_move_el()

    # # ----------------- # #
    # # Check box methods # #
    # # ----------------- # #

    def V1_plot(self):
        globals.V1_is_plotting = not globals.V1_is_plotting
    def V2_plot(self):
        globals.V2_is_plotting = not globals.V2_is_plotting
    def V3_plot(self):
        globals.V3_is_plotting = not globals.V3_is_plotting
    def V4_plot(self):
        globals.V4_is_plotting = not globals.V4_is_plotting
    def DNI_plot(self):
        globals.DNI_is_plotting = not globals.DNI_is_plotting
    def P_el_plot(self):
        globals.P_el_is_plotting = not globals.P_el_is_plotting
    def P_az_plot(self):
        globals.P_az_is_plotting = not globals.P_az_is_plotting
    def az_enable_plot(self):
        globals.az_enable_is_plotting = not globals.az_enable_is_plotting
    def el_enable_plot(self):
        globals.el_enable_is_plotting = not globals.el_enable_is_plotting

    def V1_save(self):
        globals.V1_is_saving = not globals.V1_is_saving
    def V2_save(self):
        globals.V2_is_saving = not globals.V2_is_saving
    def V3_save(self):
        globals.V3_is_saving = not globals.V3_is_saving
    def V4_save(self):
        globals.V4_is_saving = not globals.V4_is_saving
    def DNI_save(self):
        globals.DNI_is_saving = not globals.DNI_is_saving
    def P_el_save(self):
        globals.P_el_is_saving = not globals.P_el_is_saving
    def P_az_save(self):
        globals.P_az_is_saving = not globals.P_az_is_saving
    def az_enable_save(self):
        globals.az_enable_is_saving = not globals.az_enable_is_saving
    def el_enable_save(self):
        globals.el_enable_is_saving = not globals.el_enable_is_saving
    def change_state_az_single_pulse(self):
        self.az_single_pulse = not self.az_single_pulse
    def change_state_el_single_pulse(self):
        self.el_single_pulse = not self.el_single_pulse

# # --------- # #
# # Execution # #
# # --------- # #

if __name__ == '__main__':

    print('Starting application...')
    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    w.setWindowTitle('Sun Finder Control - Solar Collector Lab - INO-CNR ')

    w.show()

    sys.exit(app.exec_())