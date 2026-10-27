# Progetto: sentiment di brevi recensioni

**Livello intermedio · CPU · scikit-learn · materiale originale AI Lab.**

## Descrizione e obiettivi

Classificare un breve testo come positivo o negativo. Imparerai a trasformare parole in feature, creare una pipeline TF-IDF + regressione logistica e analizzare errori dovuti a negazione e ambiguità.

## Dataset e notebook

[Scarica lo starter sentiment](notebooks/progetto-sentiment.ipynb). Contiene 24 frasi italiane scritte per AI Lab, bilanciate fra le due classi. **Sono troppo poche per una valutazione attendibile**: servono per avviare il codice. Aggiungi almeno 60 frasi indipendenti autorizzate, descrivi i criteri di etichettatura e non raccogliere dati personali. Le frasi originali del progetto sono distribuite con Apache-2.0.

## Addestramento

Lo starter costruisce una pipeline in cui TF-IDF viene appreso soltanto sui testi di training. È un punto di partenza eseguibile in un ambiente scikit-learn compatibile, ma l’esecuzione locale non è stata verificata qui. Con dati aggiuntivi separa training, validazione e test **prima** di provare n-grammi, vocabolario e regolarizzazione. Non distribuire versioni quasi identiche della stessa frase fra gli split.

## Valutazione

Riporta baseline della classe maggioritaria, accuracy, precision, recall, F1 e matrice di confusione. Esamina esempi con «non», sarcasmo e parole mai viste. Con campioni piccoli le misure variano molto: riportane la dimensione e discuti almeno cinque errori, se disponibili.

## Miglioramenti

Confronta parole singole e bigrammi, regolarizzazione e bilanciamento. Migliora prima qualità e quantità delle etichette, poi la complessità del modello. Testa su frasi nuove senza ottimizzare sulla risposta del test.

## Possibile interfaccia

Un campo testo, un pulsante per classificare e una probabilità con una nota sui limiti. Gradio richiede un runtime Python esterno a GitHub Pages. Non usare lo starter per valutare persone o attribuire loro caratteristiche.

**Risultato atteso:** pipeline riproducibile, piccolo dossier di errori e dimostrazione su una frase nuova; non un servizio generale di analisi del linguaggio.
