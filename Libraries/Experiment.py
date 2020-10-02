import time
import nidaqmx
from Libraries import globals, settings

class Hardware:

    def __init__(self):

        # Crea la lista con i nomi delle porte attingendo dal file "settings
        globals.ports = [settings.port_V1, settings.port_V2, settings.port_V3, settings.port_V4, settings.port_DNI]
        globals.ports = [settings.device + '/' + globals.ports[i] for i in range(len(globals.ports))]

        # prova a spegnere i motori e nello stesso tempo controlla che non si siano errori nella scheda di acquisizione
        # altrimenti mostra il messaggio di errore (except)
        try:
            [self.send_signal_off(settings.dports[i]) for i in settings.dports] # Turn off motors

        except Exception as e:

            globals.errorWdw.show()

            print('\n---- NI-DAQ  Error! ----\n')
            print('- Check the name of the device in "LIbraries/settings"\n\n\t or \n\n- Close the NI Device Manager running in background')
            print('\nThe original error message is displayed below.\n\n')
            print('-' * 30+'\n')
            print(e)
            print('\n'+'-' * 30)
            input('\n\nPress Enter to close...')
            raise


    def acquisition(self):
        t_new = time.time()
        globals.updating_time = t_new - Data.time

        with nidaqmx.Task() as task:

            settings = {'terminal_config':nidaqmx.constants.TerminalConfiguration.RSE,
                                             'min_val':-10.0,
                                             'max_val':10.0,
                                              'units':nidaqmx.constants.VoltageUnits.VOLTS}

            for i in range(len(globals.ports)):
                task.ai_channels.add_ai_voltage_chan(globals.ports[i], **settings)

            Data.Voltages = task.read()

        Data.time = t_new

    def send_signal_on(self, port):
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(settings.device + '/' + port)
            task.write(True)

    def send_signal_off(self, port):

        with nidaqmx.Task() as task:

            task.do_channels.add_do_chan(settings.device + '/' + port)
            task.write(False)

class Data:

#inserire qui i dati acquisiti dalle task in Hardware

    Voltages = [1,2,3,4,5]
    time = 0

    def __init__(self):

        for i in range(len(globals.list_of_id)):
            exec('self.' + globals.list_of_id[i] + ' = self.Voltages[{}]'.format(i))
            exec('self.' + globals.list_of_id[i] + ' = self.' + globals.list_of_operations[i])

        self.P_az = ( (self.V3 + self.V4) - (self.V1 + self.V2) ) / (self.V1 + self.V2 + self.V3 + self.V4 )
        self.P_el = ( (self.V2 + self.V4) - (self.V1 + self.V3) ) / (self.V1 + self.V2 + self.V3 + self.V4 )


if __name__ == '__main__':
    hw = Hardware()
    hw.send_signal_on(port= settings.dports['port_en_az'])
