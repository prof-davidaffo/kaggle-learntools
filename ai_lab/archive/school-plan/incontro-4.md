# Incontro 4 · Introduzione alle reti neurali

**Durata: 120 minuti.** Programma originale AI Lab. [Torna agli otto incontri](percorso.html).

## Obiettivi

Riconoscere pesi, bias, layer e attivazioni; definire modelli Keras per i dataset originali Red Wine e Concrete.

## Contenuti da consultare

- [Un neurone](corsi/deep_learning_intro/tut1.html)
- [Reti profonde](corsi/deep_learning_intro/tut2.html)
- [SGD](corsi/deep_learning_intro/tut3.html)

## Notebook e ambiente

**Materiale principale: notebook Kaggle tradotti, con dati originali.** Dataset: DL Course Data: red-wine e concrete. Preparali prima dell’incontro con la [guida ai dataset](dataset.html). Usa i tutorial come riferimento e completa gli esercizi indicati.

- [Notebook originale tradotto: tut1](notebooks/deep_learning_intro-tut1.ipynb)
- [Notebook originale tradotto: ex1](notebooks/deep_learning_intro-ex1.ipynb)
- [Notebook originale tradotto: tut2](notebooks/deep_learning_intro-tut2.ipynb)
- [Notebook originale tradotto: ex2](notebooks/deep_learning_intro-ex2.ipynb)

Il notebook aggiuntivo [04-reti-neurali](notebooks/04-reti-neurali.ipynb) è un supporto facoltativo per visualizzare i concetti, non un sostituto dei dati e degli esercizi Kaggle.

## Lavoro nelle due ore

| Tempo | Attività |
| --- | --- |
| 15 min | Calcolare a mano y = wx + b. |
| 20 min | Perché servono attivazioni non lineari? Disegnare il problema dei quadranti. |
| 20 min | Esaminare Red Wine in ex1: forma degli ingressi, target e pesi. |
| 40 min | Completare ex1 ed ex2: unità lineare e rete densa per Concrete; esplorare ReLU e le altre attivazioni. |
| 15 min | Confrontare numero di ingressi, strati e uscite; anticipare loss e training del prossimo incontro. |
| 10 min | Salvare risultati e domande per Keras. |

## Esercizi da completare

Completa input_shape, modello lineare e lettura dei pesi in ex1; definisci i layer nascosti e separa le attivazioni in ex2. Il laboratorio NumPy è un approfondimento facoltativo.

## Risultato pratico atteso

Due architetture Keras definite sui dataset originali e una spiegazione di ingressi, pesi e attivazioni.

## Approfondimento facoltativo

Studia le derivate di tanh e sigmoid; confronta ReLU e tanh a livello concettuale.
