# -*- coding: utf-8 -*-
"""
--- G. Marotta ---
Calculation of Solar Position with Sun Position Algorithm (SPA)
"""

import pandas as pd
from pvlib import solarposition
import matplotlib.pyplot as plt
import sys
import os
from PyQt5 import QtWidgets, uic, QtCore


class EphemeridesWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(EphemeridesWindow, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        name = str(os.path.join(ui_path, "GUI/EphemeridesWindow.ui"))
        uic.loadUi(name, self)

        self.tz = 'Europe/Vatican'
        self.live_bool = False
        self.radioButton_live.toggled.connect(self.live)
        self.dateEdit.dateChanged.connect(lambda: self.label_solarNoon.setText(''))

        self.button_calculate_solarNoon.clicked.connect(self.calculate_solarNoon)

        self.lat = self.spinBox_latitude.value()
        self.lon = self.spinBox_longitude.value()

    def live(self):

        self.live_bool = not self.live_bool

        if self.live_bool:
            self.INTERVAL = 1  # msec
            self.timer = QtCore.QTimer()
            self.timer.setInterval(self.INTERVAL)
            self.timer.timeout.connect(self.update)
            self.timer.start()
        else:
            self.timer.stop()

    def update(self):
        self.now = pd.Timestamp.now(self.tz)
        self.date = QtCore.QDate(self.now.year,self.now.month, self.now.day)
        self.time = QtCore.QTime(self.now.hour, self.now.minute, second= self.now.second, msec = int(self.now.microsecond/1000))

        self.dateEdit.setDate(self.date)
        self.timeEdit.setTime(self.time)
        self.solpos = solarposition.get_solarposition(self.now, self.lat, self.lon)

        self.lcdNumber_azimuth.display(self.solpos.azimuth.array[0])
        self.lcdNumber_elevation.display(self.solpos.elevation.array[0])

    def calculate_solarNoon(self):
        print('calculating...(1)')
        date = str(self.dateEdit.date().year()) + '-' + str(self.dateEdit.date().month()) +'-' + str(self.dateEdit.date().day())
        print(date)
        #time = str(self.now.year) + '-' + str(self.now.month) + '-' + str(self.now.day)
        times = pd.date_range(start=date, periods=60 * 60 * 24, freq='1s', tz=self.tz)

        solpos = solarposition.get_solarposition(times, self.lat, self.lon)
        solar_noon = times[solpos.apparent_elevation.array == max(solpos.apparent_elevation.array)]
        print('calculating...(2)')
        if solar_noon.hour[0]>=10:
            hour = str(solar_noon.hour[0])
        else:
            hour = '0' + str(solar_noon.hour[0])

        if solar_noon.minute[0] >= 10:
            minute= str(solar_noon.minute[0])
        else:
            minute = '0' + str(solar_noon.minute[0])

        if solar_noon.second[0] >= 10:
            second= str(solar_noon.second[0])
        else:
            second = '0' + str(solar_noon.second[0])

        print(solar_noon)
        result = hour +':' + minute + ':' + second

        self.label_solarNoon.setText(result)

def example():

    tz = 'Europe/Vatican'
    lat, lon = 40, 11

    times = pd.date_range(start='2019-01-01', periods=60*24,  freq='1min', tz=tz)
    solpos = solarposition.get_solarposition(times, lat, lon)

    with open('Libraries/checkSPA.txt', 'w') as file:
        for i in range(len(solpos)):
            file.write(str(times[i])+ '\t' + str(solpos.apparent_elevation.array[i])+ '\t' + str(solpos.zenith.array[i]) + '\n')

    print(type(solpos.zenith.array.to_numpy()))

    plt.plot(solpos.zenith.array.to_numpy())
    plt.plot(solpos.apparent_elevation.array.to_numpy())
    print(times[solpos.apparent_elevation.array == max(solpos.apparent_elevation.array)])
    plt.show()

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    print(os.path.dirname(os.path.abspath(__file__)))
    w = EphemeridesWindow()
    w.show()

    sys.exit(app.exec_())