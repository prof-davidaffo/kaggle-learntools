# Progetto: classificare fiori simulati

**Livello essenziale · CPU · Python standard · materiale originale AI Lab.** È il progetto completo di riferimento, dimensionato per le ore in presenza.

## Problema e obiettivi

Classificare un oggetto fra due specie **fittizie**, alfa e beta, usando lunghezza e larghezza. Imparerai split, standardizzazione, regressione logistica, cross-entropy, valutazione, esportazione e previsione. Non è un sistema botanico reale: dati, specie e unità sono simulati.

## Dataset

Il notebook genera 600 esempi con seed 27: due distribuzioni parzialmente sovrapposte. Non serve scaricare dati. La suddivisione è 360 training, 120 validazione e 120 test. Media e deviazione standard sono stimate esclusivamente sul training. Il CSV può essere rigenerato e salvato dal notebook.

## Notebook iniziale e soluzione di riferimento

[Scarica il notebook completo](notebooks/07-progetto-riferimento.ipynb). Il codice iniziale è già eseguibile: completa le attività modificando soglia, rumore o modello. Le soluzioni sono pubbliche, come tutto il repository.

## Addestramento

Il modello calcola una combinazione lineare delle feature standardizzate e applica sigmoid. La discesa del gradiente minimizza la cross-entropy per 350 epoche con learning rate 0,15. Il notebook conserva la loss e controlla che diminuisca. Si tratta di **regressione logistica**, non di una rete profonda.

## Valutazione

Confronta accuracy e matrice di confusione con la baseline della classe maggioritaria del training. Scegli soglia e configurazione sulla validazione. Solo alla fine esamina il test. Le prestazioni descrivono il dataset simulato, non fiori reali. Il notebook controlla anche che i parametri siano finiti.

## Dimostrazione con il modello salvato

Il modulo seguente carica parametri e preprocessing esportati in JSON dal notebook di riferimento. La previsione è calcolata nel browser; non addestra il modello. Le misure sono in unità arbitrarie.

<form class="demo" id="model-demo"><label>Lunghezza: <span data-value>5.0</span><input aria-label="Lunghezza simulata" type="range" min="0.5" max="9.5" step="0.1" value="5"></label><label>Larghezza: <span data-value>2.0</span><input aria-label="Larghezza simulata" type="range" min="0.2" max="5" step="0.1" value="2"></label><output aria-live="polite">Caricamento del modello…</output></form>

[Scarica i parametri del modello](assets/reference-model.json). Per rigenerarli esegui il notebook e copia il JSON nella directory degli asset, verificando poi la corrispondenza fra Python e JavaScript.

## Miglioramenti

- Confronta soglie diverse sulla validazione e analizza falsi positivi/negativi.
- Aumenta il rumore e misura la riduzione di prestazioni.
- Confronta un albero con la regressione logistica.
- Passa a un dataset reale solo dopo aver documentato origine e condizioni d’uso.

## Interfaccia alternativa

Puoi esporre la funzione di previsione con Gradio su un computer o servizio che esegue Python. È un’estensione, non necessaria alla consegna e non ospitata da GitHub Pages. La UI statica qui sopra è sufficiente per il progetto di riferimento.
