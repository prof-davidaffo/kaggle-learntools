# Verifica finale locale

## Sito e materiali

Build completata: **69 pagine**, delle quali **47 pagine notebook Kaggle**, e **59 notebook scaricabili** (47 tradotti e 12 aggiuntivi AI Lab). Tutte le 307 celle Markdown delle sorgenti esaminate hanno una traduzione adattata. I video esterni non sono stati tradotti.

Controllo statico: **5393 riferimenti locali** esaminati, nessun collegamento o frammento mancante. Indice di ricerca: 69 voci. Schemi notebook, hash dei sorgenti e integrità ZIP studenti verificati. Nessuna modifica ai file già tracciati dal repository originale (`git diff --exit-code` riuscito).

Sintassi JavaScript e Python degli strumenti verificata. Le otto espressioni delimitate da parentesi LaTeX nelle pagine sono state accettate dal motore KaTeX locale. La probabilità calcolata in JavaScript dal JSON del modello di esempio coincide con Python: 0.7045370869511655 per l'ingresso [5, 2]. Non si è ripetuto l'addestramento.

Workflow YAML letto e struttura verificata: build separata da deploy, pubblicazione soltanto su workflow_dispatch con publish=true, permessi Pages/OIDC nel solo deploy. Nessuna esecuzione su GitHub né pubblicazione.

## Verifica visiva non completata

Il server HTTP locale è stato tentato ma la creazione del socket è rifiutata con `PermissionError: Operation not permitted`. Un successivo tentativo Chromium/Playwright con risorse locali intercettate è stato impedito dall'ambiente (`sandbox_host_linux.cc`, shutdown: Operation not permitted). Non sono state prodotte schermate desktop/mobile e non si dichiara una verifica grafica riuscita. CSS responsive, ricerca, menu mobile, temi e formule devono essere controllati nel browser su un computer che consenta l'avvio del sito.

## Esecuzioni didattiche già svolte

Il rapporto execution.json conserva sette esecuzioni riuscite di celle Python dei laboratori aggiuntivi. È una modalità diversa da un kernel Jupyter reale. Non sono state ripetute dopo la richiesta del docente. TensorFlow, scikit-learn, notebook Kaggle con i dataset e servizi remoti non sono stati eseguiti in questa sessione. Il progetto Iowa aggiunto successivamente non è stato eseguito.

## Acquisizione dati

I nove CSV principali sono stati importati dagli archivi forniti dal docente in `data/`. Sono inclusi nei percorsi locali, nel sito e nello ZIP studenti. Controllati struttura, integrità e corrispondenza delle copie, senza addestrare modelli. Dettagli in DATASET.md e data-inventory.json.

## Interventi ancora necessari

Confermare le condizioni di redistribuzione dei dataset Iowa e DL, le cui licenze non sono incluse negli ZIP ricevuti; installare l'ambiente scientifico e avviare i notebook reali; completare eventualmente la traduzione della diagnostica tecnica dei controlli originali; controllare il sito desktop/mobile; eseguire la Action dopo il push autorizzato e attivare Pages. Nessuna di queste operazioni è dichiarata già conclusa.

## Revisione successiva

Aggiunto il componente locale di feedback: 29 messaggi didattici risolti dai sorgenti, più etichette e strutture dei suggerimenti. Verificato che i frammenti Python restino in inglese. Il componente cambia soltanto la presentazione, senza riscrivere checker o addestrare modelli.

Importazione CSV verificata con file temporanei: importazione parziale, alias Iowa, rifiuto di sovrascrittura di file differenti e rifiuto di percorsi ZIP esterni alla destinazione. Nessun file di prova è incluso fra i dataset.

## Integrazione dati completata

Nove CSV originali inclusi nei percorsi locali, nel sito e nello ZIP studenti. Hash delle copie e presenza degli alias Iowa verificati. ZIP studenti: circa 5,3 MiB. Nessun modello addestrato nuovamente. Gli archivi originali restano nella cartella data e sono esclusi dal versionamento; il file songs.csv non necessario non è stato estratto.

## Controlli funzionali dell’interfaccia

Eseguiti con jsdom sull’HTML e sul JavaScript generati: ricerca e link sotto il prefisso `/kaggle-learntools/`, tema persistente, menu e tasto Escape con focus mobile, formule locali, fallback per immagini e ricerca non disponibili, modulo di inferenza da parametri già salvati. Tutti i controlli sono riusciti. Si tratta di verifiche DOM, non di rendering grafico o schermate; la limitazione della verifica visiva resta valida. Rapporto: ui-checks.json.

Le condizioni dei dati sono documentate separatamente in LICENZE-DATI.md. Per Iowa e DL non è stata trovata una prova primaria sufficiente a dichiarare autorizzata la redistribuzione: il punto rimane aperto, senza bloccare la preparazione locale e senza pubblicazione remota.
