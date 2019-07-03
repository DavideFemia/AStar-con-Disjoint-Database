# AStar-con-Disjoint-Database

Per riprodurre i risultati ottenuti in Relazione.pdf seguire i seguenti passi:

1. eseguire il modulo DBLoader.py per caricare i database sui file di testo nella cartella DB-15Tiles(Il processo richiederà all'incirca 1 ora).

Nel caso in cui si voglia apportare qualche modifica:

Come commentato nel codice se cambiate i valori delle variabili tiles ed n allora dovrete creare un giusto partizionamento delle tessere del problema delle n-1 tessere e settarlo alle variabili tiles; le stesse modifiche effettuate alle variabili tiles di DBLoader.py andranno apportate ai metodi disjointDatabases e disjointAndReflected delle classi Solver.
prestate attenzione ai nomi dei file se fate modifiche, per ogni variabile tiles avrete un opportuno database(file di testo)

2. riprodurre i risultati eseguendo il modulo Main.py che risolve 500 problemi del gioco del 15 con 4 euristiche.

Nel caso in cui si voglia apportare qualche modifica:

È possibile modificare le euristiche utilizzate dal RandomAStarSolver(o AStarSolver) passando una lista di stringhe opportune al suo costruttore(per vedere le stringhe consentite controllare il metodo setHeuristic della classe TilesProblem). Le euristiche disjointDatabase e disjointAndReflected non funzioneranno se prima non caricate gli opportuni database!!

È anche possibile risolvere specifiche istanze del problema del gioco delle n-tessere modificando i parametri n e utilizzandoAStarSolver(anche a quest'ultimo si può specificare le euristiche con cui deve lavorare passandogli fra i parametri formali al costruttore le opportune stringhe)
