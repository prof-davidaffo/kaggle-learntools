# AI Lab — Machine Learning e Deep Learning con Python

Piattaforma statica in italiano per la scuola secondaria di secondo grado. Il percorso principale usa **lezioni, esercizi e dataset originali Kaggle**. I laboratori AI Lab aggiuntivi sono identificati e separati. Non è una piattaforma ufficiale Kaggle.

## Stato e materiali

- 47 notebook sorgente recuperati: 18 ML, 13 Intro to Deep Learning e 16 del precedente corso di computer vision.
- Capitolo introduttivo «Python per il corso», con esempi ed esercizi. La pagina `python.html` viene generata dal notebook sorgente `notebooks/00-python-essenziale.ipynb`: modifica quel file per aggiornare entrambi. Nel pacchetto studenti si trova in `ai_lab/notebooks/preparazione/`.
- Traduzioni adattate di tutte le 307 celle Markdown e dei commenti didattici nel codice; istruzioni Python e identificatori originali conservati. Il preprocessor Kaggle è riutilizzato. I video esterni non sono tradotti né ricostruiti.
- I due corsi originali completi, con 7 moduli ML e 6 moduli DL, ricerca locale, temi chiaro/scuro, formule KaTeX locali e download. Altri sorgenti recuperati e attività AI Lab restano nei materiali aggiuntivi.
- Pacchetto studenti ZIP con notebook tradotti, `learntools` originale e strumenti di acquisizione dei dati.
- I nove CSV principali sono stati importati dagli archivi forniti dal docente in `data/`. Sono presenti in `ai_lab/input`, nel sito generato e nel pacchetto studenti. Il download dal terminale resta impedito dalla rete, ma i file locali sono disponibili.
- Il componente locale AI Lab traduce etichette, suggerimenti e spiegazioni dei due corsi introduttivi; la diagnostica tecnica dei controlli resta originale. L’esecuzione completa con i dataset resta da completare.
- 26 notebook per Colab (ripasso Python, 13 notebook ML e 12 DL), con link diretti alle 12 esercitazioni, caricamento automatico dei CSV e adattatore dei controlli Keras. La sessione autenticata remota non è stata eseguita qui.
- Nessun push, modifica delle impostazioni o pubblicazione effettuati.

## Struttura

```text
notebooks/                  # Unchanged Kaggle sources and pipeline
learntools/                 # Unchanged original exercise checkers
ai_lab/
  config.json               # Title, teacher, repository, canonical URL
  datasets.json             # Original dataset sources and expected files
  content/it/               # Italian translations keyed by source cell
  content/school/           # New teaching material and project guides
  tools/                    # Build, generation, data import and validation
  notebooks/                # Additional school notebooks
  colab/                    # Generated, versioned Colab notebooks and runtime manifest
  requirements/             # Separate site and notebook environments
  assets/                   # CSS, JS, local KaTeX and example model
  input/                    # Nine original CSVs, source attributions and legacy aliases
  runtime/                  # Working directory for original relative paths
  reports/                  # Inventory, provenance and verification results
  build/                    # Generated site, ignored by Git
.github/workflows/ai-lab-pages.yml
```

Il README originale nella radice resta intatto. `ai_lab/reports/ANALISI.md` contiene l’analisi iniziale; `inventory.json` registra hash e metadati al commit esaminato.

## Installazione e build del sito

Dalla radice del repository, genera e verifica il sito con:

```sh
./build.sh
```

Lo script crea e riutilizza `ai_lab/.venv`, installa le dipendenze, genera i notebook e il sito ed esegue i controlli. Serve Python 3 e, per installare le dipendenze mancanti, una connessione Internet. Per scegliere l’interprete alla creazione dell’ambiente: `PYTHON=python3.12 ./build.sh` (la CI usa Python 3.12).

Avvia poi il server sul sito già generato:

```sh
./start.sh
```

Apri `http://localhost:8000` e ferma il server con `Ctrl+C`. Per cambiare porta usa `./start.sh --port 8001`. Il server non installa dipendenze e non rigenera il sito: dopo aver modificato i contenuti, esegui di nuovo `./build.sh`.

In alternativa, puoi eseguire i passaggi manualmente.

Usa l’interprete Python disponibile sul computer e crea un ambiente virtuale. Controlla la versione con `python --version`:

```sh
python -m venv ai_lab/.venv
source ai_lab/.venv/bin/activate
python -m pip install -r ai_lab/requirements/site.txt
python ai_lab/tools/school_notebooks.py
python ai_lab/tools/build.py
python ai_lab/tools/check.py
python -m http.server 8000 --directory ai_lab/build
```

Apri `http://localhost:8000`. Non usare il protocollo `file://`: la ricerca locale e il caricamento del modello usano fetch. La build non richiede dataset, credenziali o esecuzione dei modelli.

Il generatore usa Python-Markdown, Pygments e il preprocessor originale di nbconvert. La scelta consente un sito statico con pochi strumenti, senza backend. KaTeX e i suoi font sono locali. Le immagini e i video dei materiali originali conservano i riferimenti esterni.

## Dataset originali e notebook Kaggle

La guida pubblicata si trova in `content/school/dataset.md`. Per i moduli principali servono Melbourne, Iowa e DL Course Data. Gli script `setup_data.sh` originali confermano queste sorgenti.

Con CLI Kaggle configurata e regole delle competizioni accettate:

```sh
python -m pip install kaggle
python ai_lab/tools/datasets.py melbourne iowa deep-learning
python ai_lab/tools/datasets.py --check
```

Oppure importa gli ZIP scaricati dalla pagina originale:

```sh
python ai_lab/tools/datasets.py melbourne --import-zip /path/to/melbourne.zip
python ai_lab/tools/datasets.py iowa --import-zip /path/to/home-data-for-ml-course.zip
python ai_lab/tools/datasets.py deep-learning --import-zip /path/to/dl-course-data.zip
```

Se hai scaricato CSV singoli puoi importarli senza creare uno ZIP. Puoi anche importare i file un po’ alla volta:

```sh
python ai_lab/tools/datasets.py melbourne --import-files /path/to/melb_data.csv
python ai_lab/tools/datasets.py iowa --import-files /path/to/train.csv /path/to/test.csv
python ai_lab/tools/datasets.py deep-learning --import-files /path/to/red-wine.csv /path/to/concrete.csv /path/to/fuel.csv /path/to/spotify.csv /path/to/hotel.csv /path/to/ion.csv
```

Lo script controlla i file attesi, estrae in sicurezza e non sovrascrive file diversi già presenti. Per Iowa crea gli alias train.csv/test.csv richiesti dalle celle storiche.

Per il codice e i checker originali Keras 2 usa un ambiente separato. Il file `requirements/kaggle-local.txt` contiene dipendenze storiche: la compatibilità va verificata con la versione di Python effettivamente disponibile, non presunta dal comando seguente:

```sh
python -m venv ai_lab/.venv-kaggle
source ai_lab/.venv-kaggle/bin/activate
python -m pip install -r ai_lab/requirements/kaggle-local.txt
jupyter lab ai_lab/build/notebooks
```

La prima cella aggiunta individua la fork/pacchetto, configura `ai_lab/runtime` e il percorso di `learntools`. I riferimenti `../input/...` restano invariati. Disattiva nel processo locale soltanto gli eventi destinati all’iframe Kaggle. Il codice delle lezioni originali non viene riscritto. L’ambiente di compatibilità è predisposto, ma non è stato verificato con i dati in questa sessione.

Dopo la build puoi distribuire `ai_lab/build/downloads/ai-lab-studenti.zip`: contiene notebook, codice e guida; **contiene i nove CSV principali già pronti nei percorsi corretti**. I pulsanti Colab aprono le versioni dedicate in `ai_lab/colab`; Kaggle rimane una fonte esterna e non ha pulsanti di esecuzione verificati.

## Google Colab

Per gli studenti l’ambiente principale è Colab: dalla pagina **Esercitazioni in Colab** o da una lezione aprono il notebook, salvano una copia nel proprio Drive ed eseguono la preparazione. Non sono richieste installazioni locali o credenziali Kaggle.

La build genera `colab/*.ipynb` e `colab/runtime.json`, che vanno **versionati e inviati su GitHub**. La duplicazione dei notebook distribuiti serve ai link Colab basati su file GitHub: non modificare queste copie manualmente. Cambia i sorgenti, rigenera e includi anche `ai_lab/colab` nel commit. La CI segnala copie obsolete.

`config.json` contiene `colab_ref`, il branch o riferimento usato sia nei link sia nei download. La prima cella scarica circa 28 MB di file, verifica gli hash, riusa i file già presenti nella sessione e crea gli alias Iowa. Usa le librerie scientifiche di Colab e installa solo quelle mancanti; non impone una versione locale di Python né effettua downgrade di TensorFlow.

`tools/keras_compat.py` adatta esclusivamente i controlli: espone forma degli input, loss e metriche tramite le API correnti e gestisce i pesi Keras. Non modifica il training, i modelli degli studenti o i file Kaggle. I controlli originali continuano a decidere se la risposta è corretta.

Verifiche senza addestramento:

```sh
python -m pip install pandas scikit-learn matplotlib ipython
python ai_lab/qa/check-colab.py
```

In un ambiente con TensorFlow, oppure nel job CI dedicato:

```sh
python ai_lab/qa/check-colab.py --keras
```

Il secondo comando verifica i controlli con modelli Keras reali e risposte corrette ed errate, senza chiamare `fit()`. Il primo controlla download, cache, recupero dei file incompleti, hash e lettura dei metadati; esegue inoltre la preparazione in un processo isolato usando soltanto i file scaricati e verifica un controllo ML con risposte corrette ed errate. I rapporti sono `reports/colab.json` e `reports/colab-checks.json`. Questi controlli non certificano un accesso autenticato a Colab: dopo il push occorre aprire un esercizio ML e uno DL dal sito con l’account usato a scuola.

## Dati nella repository e licenze

L’autorizzazione del docente include il download e l’inclusione dei dataset. Prima della redistribuzione va conservata la licenza specifica, che non coincide automaticamente con Apache-2.0 del codice. Melbourne Housing Snapshot indica **CC BY-NC-SA 4.0**, con attribuzione a Dan Becker e alla fonte di Tony Pino. Per gli altri dati la verifica delle condizioni non è stata completata. Nessun CSV è stato inventato o sostituito con dati sintetici sotto lo stesso nome.

I CSV importati non sono esclusi da Git: la struttura è pronta a versionarli. Il manifesto registra separatamente lo stato di verifica delle condizioni, senza attribuire Apache-2.0 ai dati. La build prepara localmente i nove CSV nel sito e nel pacchetto studenti, con file di attribuzione. Melbourne dichiara CC BY-NC-SA 4.0; per Iowa e DL gli archivi non contengono una licenza e la verifica prima della pubblicazione remota resta aperta. Nessuna pubblicazione è stata effettuata. I riferimenti pulsar non registrati, AutoML, pesi e TFRecord dell’archivio storico richiedono verifiche ulteriori.

## Contenuti e aggiornamenti

Le traduzioni in `content/it/<track>.txt` sono divise da marcatori `@@ nome_notebook:indice_cella`. Mantieni tutti i marcatori e scrivi spiegazioni italiane. Variabili, funzioni, API e docstring restano in inglese. I commenti didattici sono tradotti durante la build tramite `localization/comments.it.json` e `tools/code_translation.py`, anche nei blocchi Python del testo. La trasformazione confronta i token prima e dopo ed esclude qualsiasi modifica al codice eseguibile. Gli esempi di codice commentati e le direttive del generatore restano codice. Il confronto delle chiavi garantisce copertura per cella, non certifica da solo la qualità della traduzione.

Per modificare titolo, sottotitolo, docente e URL cambia `config.json`. Il programma principale segue integralmente i due corsi Kaggle; il precedente piano di otto incontri è conservato soltanto in `archive/school-plan` e non viene pubblicato. Le altre guide sono Markdown in `content/school`. I notebook aggiuntivi sono generati da `tools/school_notebooks.py`; modifica il generatore per evitare di perdere interventi alla rigenerazione.

Per aggiornare Kaggle, prima conserva le modifiche locali. Recupera upstream in modo non distruttivo, confronta sorgenti e metadati, esegui `python ai_lab/tools/inventory.py` per vedere file nuovi, rimossi o cambiati, rivedi le traduzioni interessate e aggiorna gli hash con `python ai_lab/tools/inventory.py --update` **dopo** la revisione. Il blocco include anche metadati e preprocessor originali. La build si ferma se un hash differisce: non aggiornare semplicemente gli hash per aggirare il controllo. Non lanciare `prepare_push.py` sugli originali: chiama una pulizia dei file. Il generatore AI Lab usa il preprocessor su copie in memoria.

Per aggiungere un corso aggiorna `tools/catalog.py`, inventario, traduzioni e ordine dei metadati. Per aggiungere una guida basta un Markdown in `content/school`; collega la pagina nel catalogo o nella navigazione.

## Verifiche

`tools/check.py` controlla pagine previste, link e ancore interne, percorsi per project Pages, indice di ricerca, schema notebook, hash dei sorgenti e integrità del pacchetto studenti. Non scarica dati né addestra modelli.

I rapporti in `reports` distinguono controlli del sito ed esecuzioni didattiche. Le celle di sette laboratori aggiuntivi erano state eseguite come Python; questo non certifica kernel Jupyter o servizi remoti. La rete NumPy ha raggiunto accuracy 0,975 sul problema sintetico; il riferimento logistico 0,967 su 120 esempi sintetici, contro 0,442 della baseline. Non sono risultati dei corsi/dataset Kaggle. TensorFlow, scikit-learn e gli originali con dati non sono stati eseguiti in questa sessione. Non si ripete l’addestramento durante la build o nelle Actions Pages.

Per una verifica manuale futura dei soli notebook aggiuntivi, se desiderata, `tools/execute_notebooks.py` supporta Python o `--kernel` con nbclient; registra esplicitamente dipendenze mancanti. Non fa parte della build.

## GitHub Pages

La [guida operativa alla pubblicazione](PUBBLICAZIONE.md) contiene i comandi per il primo invio, i collegamenti alle impostazioni e la procedura per gli aggiornamenti.

Il workflow **compila, controlla e pubblica automaticamente a ogni push su `master`**. Le pull request sui percorsi configurati eseguono build e controlli. Il deploy parte soltanto quando build e controlli Colab/Keras terminano con successo.

Per la configurazione iniziale seleziona **GitHub Actions** in **Settings → Pages → Build and deployment → Source**, consenti le Actions e il branch `master` nell’ambiente `github-pages`. Per gli aggiornamenti basta il push su `master`: controlla i job in **Actions → AI Lab — build e GitHub Pages**. L’URL previsto è `https://prof-davidaffo.github.io/kaggle-learntools/`.

Resta disponibile l’avvio manuale con **Run workflow**: `publish=true` pubblica il sito, `publish=false` esegue soltanto build e controlli.

Il workflow usa `pages:write` e `id-token:write` solo nel job deploy. I link del sito sono relativi e funzionano sotto `/kaggle-learntools/`; `site_url` definisce i canonical. Per cambiare repository o dominio aggiorna `config.json`. GitHub Actions non è stata eseguita remotamente qui: la configurazione predisposta non equivale a una pubblicazione verificata.

## Limiti rispetto a Kaggle

Nessun login, certificato, classifica o sincronizzazione con Kaggle. GitHub Pages non addestra Python. Il codice e i dettagli diagnostici dei controlli originali restano in inglese; il feedback didattico dei corsi introduttivi è localizzato da un componente separato. AutoML è materiale storico collegato a servizi esterni a pagamento; TPU e vecchie API sono approfondimenti. Immagini e video possono richiedere rete. Le soluzioni in un repository pubblico sono pubbliche.

## Licenze e attribuzioni

Il LICENSE originale Apache-2.0 resta intatto. Traduzioni e aggiunte sono identificate, con `ai_lab/LICENSE` e `ai_lab/NOTICE`. KaTeX 0.16.21 è distribuito con la propria licenza MIT. Dataset, immagini e video conservano condizioni autonome. La pagina `attribuzioni.html` riepiloga autori e provenienza. Non rinominare il materiale scolastico attribuendolo a Kaggle.

## Archivi forniti dal docente

Gli originali ZIP restano in `data/` e non vengono cancellati. `data/.gitignore` li esclude dal versionamento: `archive.zip` supera i 100 MB. L’importatore estrae soltanto i file del manifesto e la documentazione di accompagnamento, evitando di includere `songs.csv` (oltre 500 MB) e gli altri dati DL non utilizzati. `reports/data-inventory.json` registra hash, dimensioni, righe, colonne e file omessi. I CSV necessari, tutti sotto 100 MB, restano versionabili nella directory dedicata. Non viene addestrato alcun modello durante l’importazione.

## Controlli funzionali dell’interfaccia

La cartella `ai_lab/qa` è separata dalla build Python e contiene un controllo facoltativo con jsdom. Esercita l’HTML e il JavaScript generati senza rete e senza addestrare modelli:

```sh
npm install --prefix ai_lab/qa --ignore-scripts
npm run check --prefix ai_lab/qa
```

Il controllo verifica ricerca, tema, menu, tastiera, formule e modulo di inferenza; produce `reports/ui-checks.json`. Non è una verifica grafica desktop/mobile: controllare anche il sito in un browser reale quando l’ambiente consente di avviarlo.
