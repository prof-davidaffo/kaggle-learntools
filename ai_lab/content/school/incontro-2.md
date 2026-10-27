# Incontro 2 · Dataset, training e validazione

**Durata: 120 minuti.** Programma originale AI Lab. [Torna agli otto incontri](percorso.html).

## Obiettivi

Calcolare il MAE, distinguere training/validazione/test e spiegare perché un risultato sul training può ingannare.

## Contenuti da consultare

- [Validazione](corsi/machine_learning/tut4.html)
- [Underfitting e overfitting](corsi/machine_learning/tut5.html)

## Notebook e ambiente

**Materiale principale: notebook Kaggle tradotti, con dati originali.** Dataset: Melbourne e Iowa. Preparali prima dell’incontro con la [guida ai dataset](dataset.html). Usa i tutorial come riferimento e completa gli esercizi indicati.

- [Notebook originale tradotto: tut4](notebooks/machine_learning-tut4.ipynb)
- [Notebook originale tradotto: ex4](notebooks/machine_learning-ex4.ipynb)
- [Notebook originale tradotto: tut5](notebooks/machine_learning-tut5.ipynb)
- [Notebook originale tradotto: ex5](notebooks/machine_learning-ex5.ipynb)

Il notebook aggiuntivo [02-validazione](notebooks/02-validazione.ipynb) è un supporto facoltativo per visualizzare i concetti, non un sostituto dei dati e degli esercizi Kaggle.

## Lavoro nelle due ore

| Tempo | Attività |
| --- | --- |
| 10 min | Riprendere le previsioni del primo incontro. |
| 20 min | Esempio delle porte verdi e discussione sulle correlazioni casuali. |
| 20 min | Leggere train_test_split e mean_absolute_error nei notebook originali. |
| 45 min | Confrontare cinque profondità su training e validazione, compilando una tabella. |
| 15 min | Scegliere la dimensione usando la validazione e discutere con il docente come riservare un test indipendente aggiuntivo. |
| 10 min | Confrontare in coppia e registrare i limiti. |

## Esercizi da completare

Completa ex4 sullo split e sul MAE. In ex5 confronta le dimensioni dell’albero usando la validazione. Discuti con il docente la distinzione fra la procedura originale e un test indipendente aggiuntivo.

## Risultato pratico atteso

Una tabella degli errori, una scelta motivata della dimensione dell’albero e una spiegazione del ruolo di un test indipendente.

## Approfondimento facoltativo

Confronta un secondo split e discuti perché più prove sullo stesso validation set possono orientare le scelte verso quel campione.
