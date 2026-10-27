# AI Lab — Machine Learning e Deep Learning con Python

Piattaforma statica in italiano per la scuola secondaria di secondo grado. Il percorso principale usa **lezioni, esercizi e dataset originali Kaggle**. I laboratori AI Lab aggiuntivi sono identificati e separati. Non è una piattaforma ufficiale Kaggle.

## Stato e materiali

- 47 notebook sorgente recuperati: 18 ML, 13 Intro to Deep Learning e 16 del precedente corso di computer vision.
- Traduzioni adattate di tutte le 307 celle Markdown; codice originale in inglese e preprocessor Kaggle riutilizzato. I video esterni non sono tradotti né ricostruiti.
- Corso completo, 8 incontri da 120 minuti, guide ai progetti, ricerca locale, temi chiaro/scuro, formule KaTeX locali e download.
- Pacchetto studenti ZIP con notebook tradotti, `learntools` originale e strumenti di acquisizione dei dati.
- I nove CSV principali sono stati importati dagli archivi forniti dal docente in `data/`. Sono presenti in `ai_lab/input`, nel sito generato e nel pacchetto studenti. Il download dal terminale resta impedito dalla rete, ma i file locali sono disponibili.
- Il componente locale AI Lab traduce etichette, suggerimenti e spiegazioni dei due corsi introduttivi; la diagnostica tecnica dei controlli resta originale. L’esecuzione completa con i dataset resta da completare.
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

Usa Python 3.12 in un ambiente virtuale:

```sh
python3.12 -m venv ai_lab/.venv
source ai_lab/.venv/bin/activate
python -m pip install -r ai_lab/requirements/site.txt
python ai_lab/tools/school_notebooks.py
python ai_lab/tools/programme.py
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

Per il codice e i checker originali Keras 2 è previsto un ambiente separato Python **3.11**:

```sh
python3.11 -m venv ai_lab/.venv-kaggle
source ai_lab/.venv-kaggle/bin/activate
python -m pip install -r ai_lab/requirements/kaggle-local.txt
jupyter lab ai_lab/build/notebooks
```

La prima cella aggiunta individua la fork/pacchetto, configura `ai_lab/runtime` e il percorso di `learntools`. I riferimenti `../input/...` restano invariati. Disattiva nel processo locale soltanto gli eventi destinati all’iframe Kaggle. Il codice delle lezioni originali non viene riscritto. L’ambiente di compatibilità è predisposto, ma non è stato verificato con i dati in questa sessione.

Dopo la build puoi distribuire `ai_lab/build/downloads/ai-lab-studenti.zip`: contiene notebook, codice e guida; **contiene i nove CSV principali già pronti nei percorsi corretti**. Non sono previsti pulsanti Colab/Kaggle presentati come verificati: l’upload nei servizi remoti resta da provare dopo l’accesso ai dati.

## Dati nella repository e licenze

L’autorizzazione del docente include il download e l’inclusione dei dataset. Prima della redistribuzione va conservata la licenza specifica, che non coincide automaticamente con Apache-2.0 del codice. Melbourne Housing Snapshot indica **CC BY-NC-SA 4.0**, con attribuzione a Dan Becker e alla fonte di Tony Pino. Per gli altri dati la verifica delle condizioni non è stata completata. Nessun CSV è stato inventato o sostituito con dati sintetici sotto lo stesso nome.

I CSV importati non sono esclusi da Git: la struttura è pronta a versionarli. Il manifesto registra separatamente lo stato di verifica delle condizioni, senza attribuire Apache-2.0 ai dati. La build prepara localmente i nove CSV nel sito e nel pacchetto studenti, con file di attribuzione. Melbourne dichiara CC BY-NC-SA 4.0; per Iowa e DL gli archivi non contengono una licenza e la verifica prima della pubblicazione remota resta aperta. Nessuna pubblicazione è stata effettuata. I riferimenti pulsar non registrati, AutoML, pesi e TFRecord dell’archivio storico richiedono verifiche ulteriori.

## Contenuti e aggiornamenti

Le traduzioni in `content/it/<track>.txt` sono divise da marcatori `@@ nome_notebook:indice_cella`. Mantieni tutti i marcatori; scrivi spiegazioni italiane e lascia codice, variabili, commenti e docstring in inglese. Il confronto delle chiavi garantisce copertura per cella, non certifica da solo la qualità della traduzione.

Per modificare titolo, sottotitolo, docente e URL cambia `config.json`. Per modificare gli incontri cambia `tools/programme.py`, che verifica 120 minuti per incontro. Le altre guide sono Markdown in `content/school`. I notebook aggiuntivi sono generati da `tools/school_notebooks.py`; modifica il generatore per evitare di perdere interventi alla rigenerazione.

Per aggiornare Kaggle, prima conserva le modifiche locali. Recupera upstream in modo non distruttivo, confronta sorgenti e metadati, esegui `python ai_lab/tools/inventory.py` per vedere file nuovi, rimossi o cambiati, rivedi le traduzioni interessate e aggiorna gli hash con `python ai_lab/tools/inventory.py --update` **dopo** la revisione. Il blocco include anche metadati e preprocessor originali. La build si ferma se un hash differisce: non aggiornare semplicemente gli hash per aggirare il controllo. Non lanciare `prepare_push.py` sugli originali: chiama una pulizia dei file. Il generatore AI Lab usa il preprocessor su copie in memoria.

Per aggiungere un corso aggiorna `tools/catalog.py`, inventario, traduzioni e ordine dei metadati. Per aggiungere una guida basta un Markdown in `content/school`; collega la pagina nel catalogo o nella navigazione.

## Verifiche

`tools/check.py` controlla pagine previste, link e ancore interne, percorsi per project Pages, indice di ricerca, schema notebook, hash dei sorgenti e integrità del pacchetto studenti. Non scarica dati né addestra modelli.

I rapporti in `reports` distinguono controlli del sito ed esecuzioni didattiche. Le celle di sette laboratori aggiuntivi erano state eseguite come Python; questo non certifica kernel Jupyter o servizi remoti. La rete NumPy ha raggiunto accuracy 0,975 sul problema sintetico; il riferimento logistico 0,967 su 120 esempi sintetici, contro 0,442 della baseline. Non sono risultati dei corsi/dataset Kaggle. TensorFlow, scikit-learn e gli originali con dati non sono stati eseguiti in questa sessione. Non si ripete l’addestramento durante la build o nelle Actions Pages.

Per una verifica manuale futura dei soli notebook aggiuntivi, se desiderata, `tools/execute_notebooks.py` supporta Python o `--kernel` con nbclient; registra esplicitamente dipendenze mancanti. Non fa parte della build.

## GitHub Pages

La [guida operativa alla pubblicazione](PUBBLICAZIONE.md) contiene i comandi per il primo invio, i collegamenti alle impostazioni e la procedura per gli aggiornamenti.

Il workflow si attiva su push/PR per **compilare, controllare e produrre un artefatto da revisionare**. Non pubblica automaticamente. Per pubblicare, dopo l’autorizzazione:

1. Invia sul repository le modifiche approvate, senza operazioni Git distruttive.
2. In **Settings → Pages → Build and deployment → Source**, seleziona **GitHub Actions**. Non è stato fatto da questa sessione.
3. Consenti le Actions e, se necessario, autorizza il branch nell’ambiente `github-pages`.
4. In **Actions → AI Lab — build e GitHub Pages → Run workflow**, seleziona il branch e imposta **publish=true**.
5. Controlla build e deploy. L’URL previsto è `https://prof-davidaffo.github.io/kaggle-learntools/`.

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
