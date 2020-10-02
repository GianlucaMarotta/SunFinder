# SunFinder
Software per il controllo dell'inseguitore solare del Laboratorio Collettori Solari del CNR-INO. 

## Requisiti:
Il software è scritto in liguaggio Python3. Per l'installazione di python: https://www.python.org/downloads/. Si raccomanda durante l'installazione di attivare l'opzione _"Add Python 3.x to PATH"_. Per ulteriori informazioni sull'installazione su Windows: https://docs.python.org/3/using/windows.html

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
E' il file corrispondente al software per il calcolo delle efemeridi. Viene eseguito cliccando il button "Show Ephemerides" della MainWindow. E' possibile anche eseguirlo indipendentemente da SunFinder.py,  da Windows Explorer o da terminale.

![Ephemerides](/Screenshots/Emphemerides.JPG)

### GUI
E' la cartella in cui sono presenti i file in cui sono definite le interfacce grafiche delle varie finestre. Questi file hanno un estensione .ui e sono creati e modificati con Qt Designer. 

### Images


### Libraries
E' la cartella in cui sono presenti i codici funzionali allo sviluppo di SunFinder. Essi non possono essere eseguiti indipendentemente da SunFinder.py. Di seguito un breve dettaglio, in ordine alfabetico: 

1. AddData.py

E' presente il codice che viene eseguito quando si preme il pulsante "Add Data" della finestra principale. Permette di aggiungere altri dati in acquisizione. Sono presenti i codici eseguiti nelle finestre " " (class  ) e " " (class  ). La prima permette di inserire i dettagli della nuova acquisione, mentre la seconda permette di visualizzare il valore dei nuovi dati inseriti. Per maggiore dettaglio si legga il paragrafo: "Aggiunta Dati"

   ![AddData](/Screenshots/AddDataWindow.JPG)              ![NewData](/Screenshots/newDataWindow.JPG) 

2. Experiment.py

3. globals.py

4. Save.py

![SaveData](/Screenshots/SaveWindow.JPG) 

5. settings.py


## Gestione degli errori

![Errore su NidaqMX](/Screenshots/NI-DAQ_error.JPG)

Se mancano le librerie il programma, con doppio click il programma non viene esguito e la finestra del prompt si chiude subito dopo l'apertura. Per un miglior controllo degli errori, lanciare il software da terminale o attraverso l'uso di un IDE.

## Logica di inseguimento

## Puntamento del sole

link a pubblicazioni? 

## Updating Time

## Azionamento dei motori
Si noti che se si muove l'inseguitore verso Est, la posizione del sole si muoverà verso a Ovest rispetto il centro dei quattro qaudranti e viceversa. 
Se si muove il frame verso Up, il sole andrà verso Down. 

## Acquisizione dati 

## Aggiunta dati 
Il dato non viene aggiunto anche se non si inserisce il nome, mentre se il canale della daq non esiste, viene restituito un errore che blocca il canale. In quel caso riavviare il programma [bug da risolvere]. L'unità di misura può essere omessa, anche se questo è sconsigliato. 
Se si inserisce un canale già occupato il dato non viene aggiunto [inserire messaggio]

## Salvataggio dati
PlotSavedData -> non ancora implementato

## Grafico dei dati 

## Calcolo delle efemeridi
