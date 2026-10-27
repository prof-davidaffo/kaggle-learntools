# Progetto: classificare immagini

**Livello avanzato · TensorFlow/Keras · CPU per lo starter · materiale originale AI Lab.**

## Descrizione e obiettivi

Distinguere barre orizzontali e verticali in immagini sintetiche 16×16. Il problema piccolo permette di capire convoluzioni e pipeline prima di affrontare immagini reali. L’obiettivo è confrontare il modello con una baseline e studiare trasformazioni che preservano l’etichetta.

## Dataset e notebook

[Scarica lo starter immagini](notebooks/progetto-immagini.ipynb). Genera 300 immagini originali AI Lab, con rumore e posizioni diverse. Non richiede download, pesi preaddestrati o GPU. I dati sono sintetici e non documentano prestazioni su immagini reali. TensorFlow non è disponibile nell’ambiente locale di sviluppo: lo starter è predisposto, **non certificato da un’esecuzione locale**.

## Addestramento

La rete usa Conv2D, global average pooling e uscita sigmoid, con binary cross-entropy. Lo split è 180 training, 60 validazione, 60 test. Esegui lo starter in un ambiente compatibile prima di ampliare il progetto. Controlla tempi e memoria; usa dimensioni piccole e poche epoche.

## Valutazione

Confronta accuracy, matrice di confusione e baseline. Visualizza errori e curve. Le varianti di una stessa immagine di base devono restare nello stesso split quando aggiungi augmentation: altrimenti la valutazione può essere contaminata.

## Miglioramenti

Aumenta il rumore, varia posizione e spessore e prova pochi filtri diversi. Una rotazione di 90 gradi cambia l’etichetta, quindi non è una trasformazione valida da applicare senza correggere il target.

Come estensione, usa un piccolo dataset di immagini autorizzate con due categorie. Documenta licenze e provenienza, separa soggetti e sessioni e valuta se i tempi restano compatibili con le ore disponibili. Il corso storico offre riferimenti su transfer learning, ma codice e video originali possono richiedere adattamenti.

## Possibile interfaccia

Carica un’immagine, applica lo stesso preprocessing e mostra probabilità ed etichetta. Gradio è un’opzione in un runtime Python esterno. Non promettere la stessa accuracy su dati raccolti fuori dal dataset di laboratorio.

**Risultato atteso:** pipeline di classificazione di immagini riproducibile e spiegazione degli errori; dataset reali e transfer learning sono approfondimenti facoltativi.
