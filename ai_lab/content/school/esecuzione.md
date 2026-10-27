# Come eseguire Python e i notebook

Il sito distribuisce lezioni e file. Per eseguire gli esercizi e addestrare i modelli usa **Jupyter sul computer** oppure un ambiente notebook compatibile. I file `.ipynb` contengono spiegazioni italiane e codice inglese.

## Percorso principale: notebook e dati originali Kaggle

1. [Scarica il pacchetto studenti](downloads/ai-lab-studenti.zip) ed estrailo, oppure usa la fork clonata.
2. I [nove CSV originali](dataset.html) sono già inclusi: Melbourne e Iowa per ML; DL Course Data per DL. Mantieni la struttura delle cartelle del pacchetto.
3. Prepara l’ambiente Python dedicato ai controlli originali.

Dalla radice del pacchetto estratto o della fork:

```sh
python3.11 -m venv ai_lab/.venv-kaggle
source ai_lab/.venv-kaggle/bin/activate
python -m pip install -r ai_lab/requirements/kaggle-local.txt
python ai_lab/tools/datasets.py --check
jupyter lab
```

Su Windows attiva l’ambiente con `ai_lab\.venv-kaggle\Scripts\activate`. Nell’interfaccia Jupyter apri `ai_lab/notebooks/kaggle` se usi il pacchetto studenti; nella fork i notebook tradotti sono generati in `ai_lab/build/notebooks`.

I controlli originali DL usano attributi interni di **Keras 2**: l’ambiente dedicato evita di mescolarli con gli approfondimenti AI Lab per Keras moderno. Il file requirements indica le versioni previste; lo stato dell’esecuzione completa è nella [pagina delle verifiche](verifiche.html).

### Eseguire le celle

Usa **Maiusc + Invio** dall’inizio. La cella di preparazione AI Lab trova `learntools` e imposta la cartella di lavoro `ai_lab/runtime`: così i riferimenti originali **`../input/...`** leggono i CSV in **`ai_lab/input`**.

Le celle degli esercizi contengono spazi da completare. Scrivi la tua risposta prima di chiamare `check()`. Puoi chiedere `hint()` e, se necessario, `solution()`. Il componente AI Lab traduce etichette, suggerimenti e spiegazioni dei due corsi introduttivi, lasciando il codice delle soluzioni in inglese. Alcuni dettagli diagnostici tecnici restano nella forma originale.

Il bootstrap disattiva nel solo processo locale gli eventi verso l’iframe Kaggle. I controlli mantengono la loro logica originale: sono collegati ai dati originali, non a sostituzioni sintetiche.

## Laboratori aggiuntivi AI Lab

I notebook aggiuntivi illustrano concetti con piccoli esempi autonomi. Sono facoltativi. Per quelli scientifici moderni usa un ambiente separato:

```sh
python3.12 -m venv ai_lab/.venv-lab
source ai_lab/.venv-lab/bin/activate
python -m pip install jupyterlab
python -m pip install -r ai_lab/requirements/lab.txt
```

Se vuoi utilizzare gli starter TensorFlow moderni:

```sh
python -m pip install -r ai_lab/requirements/deep-learning.txt
```

Il riferimento logistico e i laboratori aggiuntivi 1–3 usano la sola libreria standard per i calcoli. Il laboratorio 4 usa NumPy. Il progetto principale Iowa richiede pandas e scikit-learn e riusa il dataset del corso. Non installare i due gruppi di requirements nello stesso ambiente.

## Google Colab e Kaggle Notebooks

Puoi caricare un file scaricato in [Colab](https://colab.research.google.com/) o in un notebook Kaggle. Servono anche codice `learntools`, dati e dipendenze compatibili; il semplice upload del singolo `.ipynb` non li trasferisce automaticamente. Non è stata verificata una sessione remota completa, quindi non vengono proposti pulsanti che ne dichiarino il funzionamento.

Su Kaggle il bootstrap riconosce la directory `/kaggle/input` e mantiene l’ambiente originale. Le competizioni possono richiedere account e accettazione delle regole. Il corso completo conserva i collegamenti originali come fonti.

## GitHub Pages e Python nel browser

GitHub Pages ospita file statici e non mantiene un processo Python per l’addestramento. La dimostrazione del modello sintetico è una piccola inferenza JavaScript da parametri esportati; il resto del lavoro avviene nel notebook.

Pyodide/JupyterLite possono eseguire alcuni pacchetti, ma la compatibilità di TensorFlow e dell’intero ambiente Kaggle non è garantita. Il progetto preferisce notebook scaricabili. [Documentazione JupyterLite](https://jupyterlite.readthedocs.io/en/stable/howto/pyodide/packages.html) · [Installazione TensorFlow](https://www.tensorflow.org/install/pip).

## Salvare il lavoro

Salva una tua copia del notebook, annota gli esperimenti e conserva i dati separatamente dagli output. Quando il codice è completo puoi riavviare il kernel ed eseguire tutte le celle per controllare che non dipenda da variabili rimaste in memoria. Le soluzioni presenti nel repository sono pubbliche; AI Lab non integra login, attestati o avanzamento dell’account Kaggle.
