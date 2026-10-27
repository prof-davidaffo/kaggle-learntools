# Progetto: prevedere i prezzi delle case Iowa

**Percorso principale · pandas e scikit-learn · dati originali Kaggle.**

## Descrizione e obiettivi

Riutilizza il dataset **Home Data for ML Course** e le sette feature degli esercizi del corso per prevedere `SalePrice`. Il progetto AI Lab aggiunge uno split training/validazione/test, una pipeline di preprocessing e il salvataggio del modello. Le aggiunte non sono attribuite a Kaggle.

## Dati e notebook

[Prepara i dati Iowa](dataset.html), poi [scarica il notebook del progetto](notebooks/progetto-iowa.ipynb). Il CSV è quello originale della competizione, non una simulazione. Account, accesso e condizioni della competizione vanno rispettati; il sito non ridistribuisce il dataset.

## Addestramento

Le feature sono `LotArea`, `YearBuilt`, `1stFlrSF`, `2ndFlrSF`, `FullBath`, `BedroomAbvGr` e `TotRmsAbvGrd`. Il notebook separa 60% training, 20% validazione e 20% test. Una pipeline apprende l’imputazione sul training e addestra RandomForestRegressor. Confronta il MAE con una baseline che prevede sempre la media dei prezzi del training.

## Valutazione

Scegli feature e parametri sulla validazione. Esamina il test una sola volta dopo le decisioni. Riporta MAE, dimensioni degli split e almeno tre esempi con errori elevati. Dati immobiliari di un luogo e periodo specifici non garantiscono validità altrove.

## Miglioramenti

Confronta un albero con la random forest, modifica la profondità e aggiungi feature una alla volta. Gestisci eventuali categorie in una pipeline e controlla il leakage. Annota risultati e tempi senza usare la classifica come unico criterio.

## Utilizzo finale

Il notebook salva pipeline e ordine delle feature in `iowa-model.joblib` e mostra il caricamento e una nuova previsione. Carica soltanto artefatti fidati. Una possibile UI Gradio raccoglie i sette ingressi e richiama la pipeline; richiede un runtime Python separato da GitHub Pages.

Il dataset originale è incluso nel pacchetto studenti. Le prestazioni da riportare sono quelle ottenute e documentate nella tua esecuzione; non sono assegnati punteggi predefiniti al progetto. Il riferimento sintetico già eseguito resta disponibile come [esempio aggiuntivo](progetto-tabellare.html).
