# GENERAL SETTINGS

time_on = 0.01 #s - E' la durata del minimo impulso dato ai motori.

# numero di punti mostrati nel grafico
RANGE = 100

# le soglie impostate di default
default_az_threshold = 0.02
default_el_threshold = 0.01
default_buffer_zone = 0.005
default_startValue = 0.01

# HARDWARE SETTINGS

# nome del device corrispondente alla scheda di acquisizione (Check con Labview) (inseguitore = dev6)
device = 'dev1'

# nome delle porte corrispondenti ai comandi dei motori (Check on Labview)

dports = {
'port_en_az' : 'port1/line0',
'port_dir_az' : 'port1/line1',
'port_en_el' : 'port1/line2',
'port_dir_el' : 'port1/line3'}

# nome delle porte corrispondenti all'acquisizione dei segnali analogici (Check on Labview)

port_V1 = 'ai1'
port_V2 = 'ai2'
port_V3 = 'ai3'
port_V4 = 'ai4'
port_DNI = 'ai5'

# coordinate geografiche. Utili per l'inseguimento sull'elevation. Di degault quelle della terrazza dell'inseguitore

lat = 43.74890
lon = 11.25182

#time zone

timeZone = 'Europe/Vatican'