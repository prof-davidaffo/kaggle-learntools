# Il tuo progetto di intelligenza artificiale

Scegli un problema abbastanza piccolo da arrivare a una dimostrazione nelle ore disponibili. I progetti seguenti sono **materiale originale AI Lab**, ispirato ai concetti del corso, non esercizi ufficiali Kaggle.

| Progetto | Difficoltà | Ambiente | Dati |
| --- | --- | --- | --- |
| [Prezzi delle case Iowa](progetto-iowa.html) | Essenziale | pandas e scikit-learn, CPU | Dataset originale del corso Kaggle |
| [Esempio aggiuntivo completo](progetto-tabellare.html) | Essenziale | Python standard, CPU | Fiori simulati, per studiare il flusso |
| [Sentiment](progetto-sentiment.html) | Intermedia | scikit-learn, CPU | Frasi originali, da ampliare |
| [Cifre scritte a mano](progetto-cifre.html) | Intermedia | scikit-learn, CPU | load_digits, incluso nella libreria |
| [Classificazione di immagini](progetto-immagini.html) | Avanzata | TensorFlow, CPU per lo starter | Barre sintetiche; immagini reali solo come estensione |

## Una consegna comune

1. **Domanda:** cosa vuoi prevedere e a chi serve?
2. **Dati:** origine, autorizzazioni, feature, target e limiti.
3. **Protocollo:** split, metrica e baseline scelti prima del test.
4. **Esperimenti:** almeno due configurazioni confrontate sulla validazione.
5. **Risultato:** test finale, errori e limiti, senza promettere capacità non misurate.
6. **Uso:** una nuova previsione e un modello salvato con il preprocessing.
7. **Comunicazione:** notebook eseguito e presentazione di cinque minuti.

## Come valuteremo il lavoro

| Aspetto | Peso indicativo |
| --- | --- |
| Chiarezza di domanda e dati | 20% |
| Protocollo e confronto con baseline | 25% |
| Correttezza del codice e riproducibilità | 25% |
| Analisi degli errori e dei limiti | 20% |
| Dimostrazione e comunicazione | 10% |

Il punteggio più alto non è l’unico obiettivo: un modello semplice ben valutato è un buon progetto. I pesi sono una proposta scolastica modificabile dal docente.

## Un riferimento completo

Il progetto principale [Iowa](progetto-iowa.html) riusa dati ed esercizi del corso. Come supporto, il [riferimento sintetico già eseguito](progetto-tabellare.html) mostra l’intero flusso con dati sintetici e sola libreria standard. Il sito può utilizzare il modello esportato **senza un server Python**. Gli altri tre notebook sono starter con codice di training e attività di estensione; il loro stato di esecuzione è dichiarato nei [controlli di qualità](verifiche.html).
