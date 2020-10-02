# SunFinder
Software per il controllo dell'inseguitore solare del Laboratorio Collettori Solari del CNR-INO (https://fox.ino.it/home/solar)

## Requisiti:
Il software è scritto in liguaggio Python3 e la sua interfaccia grafica sviluppata in QT5. Per l'installazione di python: https://www.python.org/downloads/. Si raccomanda durante l'installazione di attivare l'opzione _"Add Python 3.x to PATH"_. Per ulteriori informazioni sull'installazione su Windows: https://docs.python.org/3/using/windows.html

Affinché il codice sia operativo devono essere installate le seguenti librerie:

* PyQT5
* pyqtgraph
* numpy
* time
* datetime
* nidaqmx
* pandas 
* pvlib
* sys
* os

Per l'installazione delle librerie si consiglia l'utilizzo di _"pip install <nome_libreria>"_ direttamente dal prompt dei comandi (terminale).
 
Si consiglia per lo sviluppo l'utilizzo dell'IDE **PYCHARM** (https://www.jetbrains.com/pycharm/). 

Per lo sviluppo dell'interfaccia grafica è stato utilizzato il sofwtare **QT Designer**. Per installarlo eseguire il comando _"pip install pyqt5-tools"_ da terminale. La sua posizione nel sistema è la seguente _" <Python_Directory>\Lib\site-packages\pyqt5_tools\Qt\bin\designer.exe "_. Per ritrovare la posizione della propria Python Directory si può risalire a partire dal collegamento presente nel Menu Start. E' consigliato creare un collegamento sul Desktop per QtDesigner.

## Struttura
### SunFinder.py
E' il file corrispondente al core del Software.  E' possibile eseguirlo con un doppio click dal Windows Explorer, assicurandosi che all'estensione .py sia associato Python come esecutore. In alternativa è possibile lanciarlo attraverso il comando _"python SunFinder.py"_ eseguito da terminale, a patto che ci si trovi nella stessa cartella in cui è presente il file. Aprendo il file con un editor di testo, è possibile vedere e modificare il codice sorgente. Si consiglia per questo scopo l'utilizzo di un IDE, come PyCharm.
Apre la finestra principale del programma (**MainWindow**)

![MainWindow](/Screenshots/MainWindow.JPG)

### Ephemerides.py
E' il file corrispondente al software per il calcolo delle efemeridi. Viene eseguito cliccando il button "Show Ephemerides" della MainWindow. E' possibile anche eseguirlo indipendentemente da SunFinder.py,  da Windows Explorer o da terminale. Per maggiori dettagli si veda "Calcolo delle Efemeridi"

### GUI
E' la cartella in cui sono presenti i file in cui sono definite le interfacce grafiche delle varie finestre. Questi file hanno un estensione .ui e sono creati e modificati con Qt Designer. 

### Images
E' la cartella in cui sono presenti le immagini utilizzate nella Interfaccia grafica. Al momento contiene le immagini corrispondenti ai led verde (green_light.png) e rosso (red_light.png). Per cambiare queste immagini nell'interfaccia, basta inserire delle nuove immagini con lo stesso nome all'interno della cartella. 

### Libraries
E' la cartella in cui sono presenti i codici funzionali allo sviluppo di SunFinder. Essi non possono essere eseguiti indipendentemente da SunFinder.py. Di seguito un breve dettaglio, in ordine alfabetico: 

1. **AddData.py**

E' presente il codice che viene eseguito quando si preme il pulsante "Add Data" della finestra principale. Permette di aggiungere altri dati in acquisizione. Sono presenti i codici eseguiti nelle finestre " " (class  ) e " " (class  ). La prima permette di inserire i dettagli della nuova acquisione, mentre la seconda permette di visualizzare il valore dei nuovi dati inseriti. Per maggiore dettaglio si legga il paragrafo: "Aggiunta Dati"

2. **Experiment.py**

E' presente il codice che permette di guidare l'esperimento, in particolare:

* la classe Hardware, che permette di acquisire i segnali analogici e di inviare i segnali digitali alla scheda della National Instruments
* la classe Data, che processa i dati grezzi. 

3. **globals.py**

E' una libreria di variabili "globali", ovvero che devono passare da un pezzo di codice all'altro. Sono semplicemente definite e inizializzate a "None" in questo file. La vera inizializzazione è demandata alle altre sezioni di codice. 

4. **Save.py**

E' presente il codice che permette di salvare i dati sperimentali, con la relativa finestra. Per il dettaglio si veda "Salvataggio Dati".

5. **settings.py**

Sono presenti le variabili che corrispondo alle impostazioni di base del sistema, inizializzate al valore richeisto. Esse sono:

* _time_on_; in secondi, è la durata del minimo impulso dato ai motori (vedi "Azionamento dei motori");
* _RANGE_;  è il numero di dati mostrati nei grafici "live" (vedi "Grafico dei dati");
* *default_az_threshold*, *default_el_threshold*, *default_buffer_zone*, *default_startValue*; sono i valori di default delle variabili di inseguimento (vedi "Logica di inseguimento");
* *device*; è il nome del device corrispondente alla scheda della National Instruments (NI) utilizzata;
* *dports*; è un dizionario in cui sono specificati i nomi delle porte "digitali" utilizzate per inviare i segnali ai motori;
* *port_V1*, *port_V2*, *port_V3*, *port_V4*, *port_DNI*; sono i nomi delle porte corrispenti ai relativi ingressi analogici;
* *lat*, *lon*, *timeZone* sono le coordinate geografiche e la zona oraria in cui viene utilizzato l'inseguitore, utili per il calcolo del mezzogiorno nell'inseguimento "a soglia" sull'elevazione (vedi "Logica di inseguimento")

Per cambiare le impostazioni basta modificare questo file e riavviare il programma. 

## Gestione degli errori

Lo sviluppo di codice originale è sempre molto vulnerabile ad errori o "bug" invisibili. Quando l'applicazione viene eseguita dal Windows Explorer (con doppio click) un envetuale errore comporta la chiusura del programma, senza ulteriori spiegazioni. Per una visualizzazione dell'errore si consiglia l'utilizzo di un IDE o l'esecuizione da terminale.

Per evitare interruzioni brusche inspiegabili del programma, è stato utilizzata la gestione delle eccezioni di python (per approfondire: https://docs.python.org/3/tutorial/errors.html). IN caso di errore, il programma fa comparire una finestra pop-up e stampa il contenuto dell'errore su terminale. Questo avviene anche all'inizio dell'esecuzione del programma, qual'ora ci fossero problemi con l'acquisizione da scheda NI (esempio in foto)

![Errore su NidaqMX](/Screenshots/NI-DAQ_error.JPG)

Se invece mancano le librerie indicate in "Requisiti" il programma non viene eseguito e nessun messaggio di errore viene mostrato. In questo caso, e in tutti i casi analoghi, si usi l'esecuzione tramite IDE o terminale. 

## Puntamento del sole e misura DNI

Il puntamento del sole viene effettuato da un puntatore a 4 quadranti montato sullo scheletro dell'inseguitore.  
La precisione dell'inseguimento è legata alla precisione dell'allineamento con cui l'asse ottico del puntatore è allineato con la normale al piano dell'inseguitore
Per approfondimento:  (https://doi.org/10.1063/1.5117585  e https://doi.org/10.18086/swc.2019.02.01).

![pointer](/Screenshots/pointer.JPG)

Il puntatore invia alla scheda di acquisizione della NI i 4 voltaggi (*V1*, *V2*, *V3* e *V4*) proporzionali alla radiazione che incide sui quattro quadranti. A partire da questa crea le variabili posizioni *Position Azimuth* e *Position Elevation*. Il grafico centrale mostra in tempo reale il valore di queste due ultime variabili. 
Il grafico centrale indica la posizione del sole rispetto alla normale del piano di inseguimento. 

## Acquisizione dati e Updating Time

I dati vengono acquisiti ad ogni ciclo del loop presente in MainWindow
Per il controllo dell'esecuzione tra un'acquisizione ed un'altra viene registato il tempo trascorso visualizzabile in alto a sinistra dall'indicatore Updating Time. 
Questo valore cresce naturalmente: 
* se vengono visualizzate delle finestre di Grafici. Ogni finestra aperta aumenta il tempo di aggiornamento;
* se vengono azionati i motori con una velocità diversa da 1. Minore sarà la velocità, maggiore sarà il tempo di aggiornamento (vedi Azionamento dei Motori)

## Azionamento dei motori

![motion](/Screenshots/Motion.JPG)

La velocità è regolata con un sistema PWM. 
Si noti che se si muove l'inseguitore verso Est, la posizione del sole si muoverà verso a Ovest rispetto il centro dei quattro qaudranti e viceversa. 
Se si muove il frame verso Up, il sole andrà verso Down e viceversa. 

## Logica di inseguimento

![comandiInseguimento](/Screenshots/Finding.png)

![zoneInseguimento](/Screenshots/inseguimento_zone.png)

## Aggiunta dati 
Premendo il button "Add Data" ...

![AddData](/Screenshots/AddDataWindow.JPG)              ![NewData](/Screenshots/newDataWindow.JPG) 

Il dato non viene aggiunto anche se non si inserisce il nome, mentre se il canale della daq non esiste, viene restituito un errore che blocca il canale. In quel caso riavviare il programma [bug da risolvere]. L'unità di misura può essere omessa, anche se questo è sconsigliato. 
Se si inserisce un canale già occupato il dato non viene aggiunto [inserire messaggio]

## Salvataggio dati

![SaveData](/Screenshots/SaveWindow.JPG) 

PlotSavedData -> non ancora implementato

## Grafico dei dati 

![ShowGraph](/Screenshots/PlotWindow.JPG) 

## Calcolo delle efemeridi

![Ephemerides](/Screenshots/Emphemerides.JPG)

Il calcolo è affidato alla libreria _pvlib.solarposition_. In particolare si utilizza il metodo _solarposition.spa_python_ che fa riferimento al Solar Position Algorithm sviluppato da NREL. Per ulteriori informazioni e altri metodi di calcolo si veda: https://pvlib-python.readthedocs.io/en/stable/api.html#solar-position

Spuntando la casella "live" è possibile ottenere il calcolo di azimut e elevation in tempo reale, per le coordinate inserite. 

Per il calcolo dell' orario di alba, tramonto e mezzogiorno solare viene utilizzata la libreria _solarposition.sun_rise_set_transit_spa_, basato anch'esso sull'algoritmo SPA. 
Si noti che i valori ottenuti possono differire di qualche secondo da valori ottenuti con altri metodi. Ad esempio si confrontino i dati con quello ottenuti in https://www.esrl.noaa.gov/gmd/grad/solcalc/



