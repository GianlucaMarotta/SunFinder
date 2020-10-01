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

Per lo sviluppo dell'interfaccia grafica è stato utilizzato il sofwtare **QT Designer**. Per installarlo eseguire il comando _"pip install pyqt5-tools"_ da terminale. La sua posizione nel sistema è riferita alla cartella _" <Python_Directory>\Lib\site-packages\pyqt5_tools\Qt\bin\ "_. Per ritrovare la posizione della propria Python Directory si può risalire a partire dal collegamento presente nel Menu Start. E' consigliato creare un collegamento sul Desktop per QtDesigner.

## Struttura
### SunFinder.py
E' il file corrispondente al core del Software.  E' possibile eseguirlo con un doppio click dal Windows Explorer, assicurandosi che all'estensione .py sia associato Python come esecutore. In alternativa è possibile lanciarlo attraverso il comando _"python SunFinder.py"_ eseguito da terminale, a patto che ci si trovi nella stessa cartella in cui è presente il file. Aprendo il file con un editor di testo, è possibile vedere e modificare il codice sorgente. Si consiglia per questo scopo l'utilizzo di un IDE, come PyCharm.

### Ephemerides.py
E' il file corrispondente al software per il calcolo delle efemeridi. Può essere eseguito indipendentemente da SunFinder.py. Anch'esso si esegue da Windows Explorer o da terminale. 

### GUI


