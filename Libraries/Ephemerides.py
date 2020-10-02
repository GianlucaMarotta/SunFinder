# -*- coding: utf-8 -*-
"""
--- G. Marotta ---
Calculation of Solar Position with Sun Position Algorithm (SPA)
"""

import pandas as pd
from pvlib import solarposition
import sys
import os
from PyQt5 import QtWidgets, uic, QtCore


class EphemeridesWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(EphemeridesWindow, self).__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        name = str(os.path.join(ui_path, "../GUI/EphemeridesWindow.ui"))
        uic.loadUi(name, self)

        self.tz = 'Europe/Vatican'
        self.live_bool = False
        self.exclude_solar_noon = False
        self.exclude_solar_set = False
        self.exclude_solar_rise = False

        self.radioButton_live.toggled.connect(self.live)
        self.button_calculate.clicked.connect(self.calculate)


    def live(self):

        self.live_bool = not self.live_bool

        if self.live_bool:
            self.INTERVAL = 1  # msec
            self.timer = QtCore.QTimer()
            self.timer.setInterval(self.INTERVAL)
            self.timer.timeout.connect(self.live_update)
            self.timer.start()
        else:
            self.timer.stop()

    def live_update(self):
        self.now = pd.Timestamp.now(self.tz)
        self.date = QtCore.QDate(self.now.year,self.now.month, self.now.day)
        self.time = QtCore.QTime(self.now.hour, self.now.minute, second= self.now.second, msec = int(self.now.microsecond/1000))

        self.dateEdit.setDate(self.date)
        self.timeEdit.setTime(self.time)

        self.lat = self.spinBox_latitude.value()
        self.lon = self.spinBox_longitude.value()

        self.solpos = solarposition.get_solarposition(self.now, self.lat, self.lon)

        self.lcdNumber_azimuth.display(self.solpos.azimuth.array[0])
        self.lcdNumber_elevation.display(self.solpos.elevation.array[0])

    def calculate(self):
        date = str(self.dateEdit.date().year()) + '-' + str(self.dateEdit.date().month()) +'-' + str(self.dateEdit.date().day())
        time = str(self.timeEdit.time().hour()) + ':' + str(self.timeEdit.time().minute()) + ':' + str(self.timeEdit.time().second()) + '.' + str(self.timeEdit.time().msec())

        self.now = pd.Timestamp(date+ ' ' + time)

        self.lat = self.spinBox_latitude.value()
        self.lon = self.spinBox_longitude.value()

        self.solpos = solarposition.spa_python(self.now, self.lat, self.lon)

        self.lcdNumber_azimuth.display(self.solpos.azimuth.array[0])
        self.lcdNumber_elevation.display(self.solpos.elevation.array[0])

        self.calculate_sunRise_sunSet_sunNoon()


    def calculate_sunRise_sunSet_sunNoon(self):

        date = str(self.dateEdit.date().year()) + '-' + str(self.dateEdit.date().month()) + '-' + str(self.dateEdit.date().day())
        times = pd.date_range(start=date, end=date, freq= None, tz=self.tz)

        solpos = solarposition.sun_rise_set_transit_spa(times, self.lat, self.lon)

        solar_rise = solpos.sunrise.array
        hour = (str(solar_rise.hour[0]) if solar_rise.hour[0] >= 10 else ('0' + str(solar_rise.hour[0])))
        minute = (str(solar_rise.minute[0]) if solar_rise.minute[0] >= 10 else ('0' + str(solar_rise.minute[0])))
        second = (str(solar_rise.second[0]) if solar_rise.second[0] >= 10 else ('0' + str(solar_rise.second[0])))
        result = hour + ':' + minute + ':' + second
        self.label_solarRise.setText(result)

        solar_set = solpos.sunset.array
        hour = (str(solar_set.hour[0]) if solar_set.hour[0] >= 10 else ('0' + str(solar_set.hour[0])))
        minute = (str(solar_set.minute[0]) if solar_set.minute[0] >= 10 else ('0' + str(solar_set.minute[0])))
        second = (str(solar_set.second[0]) if solar_set.second[0] >= 10 else ('0' + str(solar_set.second[0])))
        result = hour + ':' + minute + ':' + second
        self.label_solarSet.setText(result)

        solar_noon = solpos.transit.array
        hour = (str(solar_noon.hour[0]) if solar_noon.hour[0] >= 10 else ('0' + str(solar_noon.hour[0])))
        minute = (str(solar_noon.minute[0]) if solar_noon.minute[0] >= 10 else ('0' + str(solar_noon.minute[0])))
        second = (str(solar_noon.second[0]) if solar_noon.second[0] >= 10 else ('0' + str(solar_noon.second[0])))
        result = hour + ':' + minute + ':' + second
        self.label_solarNoon.setText(result)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    w = EphemeridesWindow()
    w.setWindowTitle('Ephemerides Calculation')
    w.show()

    sys.exit(app.exec_())