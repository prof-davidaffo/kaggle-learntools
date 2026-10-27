# Progetto: riconoscere cifre scritte a mano

**Livello intermedio · CPU · scikit-learn · materiale originale AI Lab.**

## Descrizione e obiettivi

Riconoscere cifre da 0 a 9 in immagini 8×8. Imparerai a trasformare immagini in feature, risolvere una classificazione multiclasse e capire quali cifre vengono confuse.

## Dataset e notebook

[Scarica lo starter cifre](notebooks/progetto-cifre.ipynb). Usa **`sklearn.datasets.load_digits`**, distribuito con scikit-learn: dopo l’installazione non serve scaricare immagini. Fonte: UCI Optical Recognition of Handwritten Digits, **E. Alpaydin e C. Kaynak**. Il notebook invita a leggere `digits.DESCR`; conserva provenienza e condizioni del dataset se ridistribuisci i dati. Non è MNIST 28×28.

## Addestramento

Lo starter separa training, validazione e test con stratificazione, poi usa StandardScaler e LogisticRegression nella stessa pipeline. Il preprocessing viene appreso sul training. L’esecuzione locale dello starter non è stata verificata in questa sessione. Nell’ambiente scientifico predisposto confronta la baseline con una rete MLP solo dopo aver eseguito il modello semplice.

## Valutazione

Usa accuracy globale, matrice di confusione e risultati per classe. Cerca almeno cinque errori e visualizza le relative matrici 8×8. Mantieni il test separato dalle scelte. Se estendi il dataset, evita che immagini dello stesso autore o della stessa sequenza finiscano in entrambi gli split.

## Miglioramenti

Confronta regolarizzazione e numero di unità; controlla tempi e convergenza. Osserva gli effetti della normalizzazione. Disegni raccolti da una nuova interfaccia possono essere molto diversi dagli esempi di training.

## Possibile interfaccia

Una griglia 8×8 o un campo immagine convertito in scala di grigi, ridimensionato e normalizzato esattamente come i dati di training. Una UI Gradio può essere eseguita localmente; GitHub Pages non ospita il relativo processo Python. Riporta i limiti sui disegni esterni.

**Risultato atteso:** un classificatore multiclasse con analisi degli errori e previsione su un’immagine di test documentata.
