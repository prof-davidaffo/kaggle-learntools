# Incontro 5 · Deep Learning con TensorFlow e Keras

**Durata: 120 minuti.** Programma originale AI Lab. [Torna agli otto incontri](percorso.html).

## Obiettivi

Collegare Input, Dense, compile e fit; usare early stopping e riconoscere lo scopo di dropout e batch normalization.

## Contenuti da consultare

- [Training con Keras](corsi/deep_learning_intro/tut3.html)
- [Early stopping](corsi/deep_learning_intro/tut4.html)
- [Dropout e batch normalization](corsi/deep_learning_intro/tut5.html)
- [Classificazione binaria](corsi/deep_learning_intro/tut6.html)

## Notebook e ambiente

**Materiale principale: notebook Kaggle tradotti, con dati originali.** Dataset: DL Course Data: red-wine, fuel e spotify. Preparali prima dell’incontro con la [guida ai dataset](dataset.html). Usa i tutorial come riferimento e completa gli esercizi indicati.

- [Notebook originale tradotto: tut3](notebooks/deep_learning_intro-tut3.ipynb)
- [Notebook originale tradotto: ex3](notebooks/deep_learning_intro-ex3.ipynb)
- [Notebook originale tradotto: tut4](notebooks/deep_learning_intro-tut4.ipynb)
- [Notebook originale tradotto: ex4](notebooks/deep_learning_intro-ex4.ipynb)

Il notebook aggiuntivo [05-tensorflow](notebooks/05-tensorflow.ipynb) è un supporto facoltativo per visualizzare i concetti, non un sostituto dei dati e degli esercizi Kaggle.

## Lavoro nelle due ore

| Tempo | Attività |
| --- | --- |
| 15 min | Riprendere la rete definita nel quarto incontro e spiegare pesi e attivazioni. |
| 20 min | Definire loss MAE e optimizer Adam per Fuel Economy; distinguere regressione e classificazione. |
| 40 min | Completare compile e fit di ex3 e leggere la curva della loss. |
| 20 min | Riprendere Spotify in ex4 e aggiungere EarlyStopping con i parametri richiesti. |
| 15 min | Discutere curve di training e validazione e consultare i risultati dell’esempio. |
| 10 min | Salvare i notebook e annotare quale configurazione si intende confrontare. |

## Esercizi da completare

Completa compile e fit in ex3 usando Fuel Economy. In ex4 aggiungi EarlyStopping per Spotify. Se il tempo non basta, le domande sulle curve diventano attività da concludere prima dell’incontro 6. Dropout, batch normalization e classificazione binaria restano letture/approfondimenti accessibili nel corso completo.

## Risultato pratico atteso

Una rete addestrata sui dati originali, con curve di training e validazione e callback di arresto anticipato.

## Approfondimento facoltativo

Prova batch normalization e confronta la stabilità; non sono richieste TPU o GPU.
