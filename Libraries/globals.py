# In questo file sono presenti le variabili "globali".
# Essendo definite in una libreria esterna, è possibile invocarle e modificarle nelle varie sezioni del programma.

# Tutte le variabili sono inizializzate con "None".
# E' una buona pratica per non dimenticare l'inizializzazione nella parte di codice realmente interessata.


# # ----- # #
# # Flags # #
# # ----- # #

# Le flags servono a controllare l'attivazione di parti di codice se il loro valore è True. Sono variabili booleane.
# Esse sono attivate da funzioni esterne alla MainWindow e controllate nel "loop" definito dal metodo update.

is_showing_graph = None

is_moving_az = None
is_moving_el = None
is_finding_az = None
is_finding_el = None

# Flags per i garfici
V1_is_plotting = None
V2_is_plotting = None
V3_is_plotting = None
V4_is_plotting = None
DNI_is_plotting = None
P_el_is_plotting = None
P_az_is_plotting = None
el_enable_is_plotting = None
az_enable_is_plotting = None

# Flags per il salvataggio
V1_is_saving = None
V2_is_saving = None
V3_is_saving = None
V4_is_saving = None
DNI_is_saving = None
P_el_is_saving = None
P_az_is_saving = None
el_enable_is_saving = None
az_enable_is_saving = None

# indicatori di movimento
az_mot = None
el_mot = None

# Dati acquisiti, viene assegnata al type Data definito nel file corrispondente
dt = None

# tempo di aggiornamento dei dati acquisiti
updating_time = None

# tempo di update dei dati salvati
save_update_time = 1

# nome del file da salvare
filename = None

#tempo di inizio salvataggio dati
time_0 = None

is_writing_data = None

ports = None
list_of_labels = None
list_of_units = None
list_of_operations = None
list_of_id = None

names = None
nDWdw = None

errorWdw = None


name_of_plots = None
list_of_plots = None

new_plots = None
new_data = None
new_saves = None