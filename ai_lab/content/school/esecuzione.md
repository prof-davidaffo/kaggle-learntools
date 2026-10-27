# Eseguire gli esercizi

## Google Colab

Per seguire il corso puoi usare Colab dal browser. Non serve installare Python sul computer.

1. Apri le [esercitazioni](esercitazioni.html) e scegli **Apri in Colab**. Lo stesso pulsante è presente nelle lezioni e nel [capitolo Python](python.html).
2. Accedi con il tuo account Google e salva una copia del notebook nel tuo Drive, così conservi le modifiche.
3. Esegui la cella **Preparazione in Colab** con **Maiusc + Invio** e attendi il messaggio «Preparazione completata».
4. Esegui le altre celle dall'alto verso il basso. Negli esercizi sostituisci i segnaposto `____` con il tuo codice.
5. Usa `check()` per controllare la risposta, `hint()` per un suggerimento e `solution()` per consultare la soluzione.

La preparazione carica i CSV e il codice dei controlli dal repository del corso. Non devi caricare file a mano, collegare Drive ai dati o configurare le credenziali Kaggle. Mantieni il runtime standard; per iniziare non serve selezionare una GPU.

Se Colab interrompe o riavvia la sessione, le variabili in memoria vengono perse. Riesegui la preparazione e le celle precedenti. Il notebook salvato nel tuo Drive conserva il codice: controlla di avere salvato prima di chiudere.

I dati e le librerie della sessione non vengono salvati automaticamente nella tua copia del notebook. La prima cella li prepara nuovamente quando necessario. Le risorse gratuite di Colab hanno limiti variabili: [documentazione Colab](https://research.google.com/colaboratory/faq.html).

## Jupyter sul computer

Puoi anche scaricare il [pacchetto studenti](downloads/ai-lab-studenti.zip), che contiene notebook, CSV e controlli, ed estrarlo mantenendo la struttura delle cartelle.

Dalla radice del pacchetto o della fork, controlla l'interprete con `python --version` e crea un ambiente virtuale:

```sh
python -m venv ai_lab/.venv-kaggle
source ai_lab/.venv-kaggle/bin/activate
python -m pip install -r ai_lab/requirements/kaggle-local.txt
jupyter lab
```

Se il comando disponibile è `python3`, usalo al posto di `python`. Su Windows puoi creare l'ambiente con `py -m venv ai_lab/.venv-kaggle` e attivarlo con `ai_lab\.venv-kaggle\Scripts\activate`.

I requirements locali conservano le dipendenze dei vecchi controlli Keras 2: la compatibilità va verificata con l'interprete installato. Questa installazione non è necessaria per usare Colab, che impiega un adattatore per i metadati dei modelli Keras moderni.

In Jupyter apri `ai_lab/notebooks/kaggle` nel pacchetto studenti; nella fork i notebook tradotti si trovano in `ai_lab/build/notebooks`. Il ripasso Python è in `ai_lab/notebooks/preparazione` nel pacchetto. Esegui la cella iniziale di preparazione per impostare i percorsi dei CSV.

## Materiali aggiuntivi

I pulsanti Colab coprono il capitolo Python e i due corsi introduttivi completi. Gli approfondimenti storici su AutoML, TPU e computer vision hanno dipendenze diverse e non sono configurati per Colab.

I progetti e i laboratori aggiuntivi indicano le proprie dipendenze. Per quelli moderni puoi usare un ambiente separato con `ai_lab/requirements/lab.txt` e, se richiesto, `ai_lab/requirements/deep-learning.txt`.

[Dataset](dataset.html) · [Verifiche tecniche](verifiche.html).
