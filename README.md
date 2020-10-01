# SunFinder
Software per il controllo dell'inseguitore solare del Laboratorio Collettori Solari del CNR-INO. 

## Requisiti:
Il software è scritto in liguaggio Python3. Per l'installazione di python: https://www.python.org/downloads/. Si raccomanda durante l'installazione di attivare l'opzione _"Add Python 3.x to PATH"_. Per ulteriori informazioni sull'installazione su Windows: https://docs.python.org/3/using/windows.html

Affinché il codice sia operativo devono essere installate le seguenti librerie:

* PyQT5
* pyqtgraph
* numpy
* time
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

### Ephemerides.py
E' il file corrispondente al software per il calcolo delle efemeridi. Viene eseguito cliccando il button "Show Ephemerides" della MainWindow. E' possibile anche eseguirlo indipendentemente da SunFinder.py,  da Windows Explorer o da terminale. 

### GUI
E' la cartella in cui sono presenti i file in cui sono definite le interfacce grafiche delle varie finestre. Questi file hanno un estensione .ui e sono creati e modificati con Qt Designer. 

### Images


### Libraries
E' la cartella in cui sono presenti i codici funzionali allo sviluppo di SunFinder. Essi non possono essere eseguiti indipendentemente da SunFinder.py. Di seguito un breve dettaglio, in ordine alfabetico: 

1. AddData.py

E' presente il codice che viene eseguito quando si preme il pulsante "Add Data" della finestra principale. Permette di aggiungere altri dati in acquisizione. Sono presenti i codici eseguiti nelle finestre " " (class  ) e " " (class  ). La prima permette di inserire i dettagli della nuova acquisione, mentre la seconda permette di visualizzare il valore dei nuovi dati inseriti. Per maggiore dettaglio si legga il paragrafo: "Aggiunta Dati"

2. Experiment.py

3. globals.py

4. Save.py

5. settings.py

6. Windows.py

## Gestione degli errori

## Logica di inseguimento

## Updating Time

## Azionamento dei motori

## Acquisizione dati puntatore e pireliometro

## Aggiunta dati 

## Salvataggio dati

## Grafico dei dati 

## Calcolo delle efemeridi
