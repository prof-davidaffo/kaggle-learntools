# Inventario e decisioni prima dell'implementazione

La copia locale è disponibile e pulita all'inizio del lavoro. Nessun AGENTS.md trovato nel repository. README originale, documentazione notebook, macro, metadati dei tre corsi, codice di verifica, setup e licenza sono stati letti. L'inventario macchina in `inventory.json` registra file, hash SHA-256, celle e registrazione nei metadati al commit analizzato.

## Contenuti

* `machine_learning`: 18 notebook, 16 registrati. Nove argomenti: funzionamento dei modelli, esplorazione, primo modello, validazione, underfitting/overfitting, random forest, competizioni, AutoML, Titanic. `tut8`/`ex8` sono materiale sulla classificazione non registrato, da recuperare separatamente. Non sono esercizi del modulo AutoML, benché condividano il numero 8.
* `deep_learning_intro`: 13 notebook registrati. Sei lezioni con esercizi su neurone, reti dense, SGD, capacità ed early stopping, dropout/batch normalization, classificazione binaria. Un settimo tutorial sulle TPU e sul bosone di Higgs.
* `deep_learning`: 16 notebook registrati del precedente corso, distinto da Intro to Deep Learning: convoluzioni, Keras, transfer learning, augmentation, reti da zero, dropout/strides e TPU. Archivio storico, con API e dipendenze da riesaminare; non sostituisce il corso introduttivo.

## Rendering e verifiche

`prepare_push.py` chiama `clean(in_path)`: non usarlo direttamente sui sorgenti originali. Il preprocessor espande macro di navigazione, usa `MacroProcessor` per rimuovere celle di test e commentare suggerimenti/soluzioni, aggiunge intestazioni e riferimenti al forum. `track_meta.py` associa tutorial ed esercizi. La generazione dei metadati e l'upload Kaggle non servono al sito.

Si riutilizza direttamente `MacroProcessor` originale per le macro di riga/cella; un adattatore locale gestisce navigazione e traduzioni senza invocare pulizia o upload. Le traduzioni devono avere copertura esplicita per cella, con hash delle sorgenti per individuare aggiornamenti. Gli originali rimangono immutati.

`learntools.core` offre controlli locali, hint e soluzioni, ma emette eventi JavaScript verso l'iframe Kaggle o usa kagglesdk se abilitato. I controlli dei corsi contengono anche risposte numeriche, forme e statistiche specifiche dei dataset. Sostituire i dataset senza cambiare i controlli darebbe verifiche errate. Non si dichiara compatibilità automatica con Colab. I laboratori originali della scuola avranno verifiche indipendenti e dati inclusi/generati, separati dagli esercizi tradotti.

## Vincoli di esecuzione

I CSV di Melbourne, Iowa, vino, Spotify, hotel e ionosfera non sono inclusi nel repository. Le competizioni possono richiedere account e accettazione delle regole. AutoML dipende da un wrapper Kaggle, credenziali cloud e servizi a pagamento: conservazione storica, esclusione dal laboratorio gratuito. TPU/Higgs usa TFRecord e infrastruttura remota, quindi approfondimento non eseguibile offline. Il corso DL storico usa pesi e immagini esterni e API Keras precedenti.

GitHub Pages distribuisce file statici; non può addestrare Python lato server. Download Jupyter come modalità di base; nessun pulsante Colab/Kaggle presentato come verificato finché non provato nell'ambiente remoto. Pyodide/JupyterLite richiederebbero un runtime aggiuntivo e verifica di tutti i pacchetti; non sono adottati per TensorFlow.

## Soluzione scelta

Generatore statico Python con Python-Markdown e Pygments, contenuti in Markdown e notebook JSON standard. MkDocs Material sarebbe adatto, ma non è installato e PyPI non è raggiungibile. Il generatore scelto consente build e controllo link immediati con le librerie disponibili e resta piccolo e riproducibile. Interfaccia italiana, ricerca locale, navigazione laterale, tema chiaro/scuro, formule MathJax con fallback leggibile, asset locali e link relativi funzionanti sotto il prefisso del repository. Nessun servizio persistente.

La rete dell'esecutore resta indisponibile anche dopo il clone effettuato dall'utente: l'installazione da PyPI è fallita. Le esecuzioni scientifiche mancanti saranno dichiarate, con workflow dedicato per l'ambiente Python compatibile.

## Licenze

Apache-2.0 nel LICENSE originale: conservarlo insieme agli avvisi e identificare i file modificati/tradotti. Non risultano file NOTICE nella copia analizzata. Dataset, pesi e immagini esterni non acquisiscono automaticamente la licenza del codice: non ridistribuirli senza verifica. Conservare URL e attribuzioni nei materiali e segnalare la dipendenza dalla rete. I nuovi materiali sono identificati come originali AI Lab; soluzioni in un repository pubblico sono pubbliche.
