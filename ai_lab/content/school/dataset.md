# Scaricare e preparare i dataset originali

**I nove CSV originali del percorso principale sono già inclusi nella repository e nel pacchetto studenti.** Sono stati importati dagli archivi Kaggle forniti dal docente, senza modificare i dati. Non serve scaricarli nuovamente per iniziare le lezioni.

## Il pacchetto per gli studenti

[Scarica il pacchetto completo](downloads/ai-lab-studenti.zip) ed estrailo prima di aprire Jupyter. Contiene i notebook tradotti in `ai_lab/notebooks/kaggle`, il codice originale `learntools`, il manifesto dei dati e lo strumento di importazione. Include i nove CSV necessari, già organizzati nei percorsi richiesti dai notebook, oltre alle attribuzioni delle fonti. Per l’utilizzo locale non serve riscaricare i dati da Kaggle.

Puoi anche lavorare direttamente nella fork clonata. In quel caso i notebook tradotti si trovano nella cartella generata `ai_lab/build/notebooks` dopo la compilazione del sito.

## CSV inclusi

| File | Righe | Colonne |
| --- | ---: | ---: |
| [melb_data.csv](datasets/melbourne-housing-snapshot/melb_data.csv) | 13.580 | 21 |
| [train.csv — Iowa](datasets/home-data-for-ml-course/train.csv) | 1.460 | 81 |
| [test.csv — Iowa](datasets/home-data-for-ml-course/test.csv) | 1.459 | 80 |
| [red-wine.csv](datasets/dl-course-data/red-wine.csv) | 1.599 | 12 |
| [concrete.csv](datasets/dl-course-data/concrete.csv) | 1.030 | 9 |
| [fuel.csv](datasets/dl-course-data/fuel.csv) | 1.107 | 14 |
| [spotify.csv](datasets/dl-course-data/spotify.csv) | 32.833 | 23 |
| [hotel.csv](datasets/dl-course-data/hotel.csv) | 119.390 | 32 |
| [ion.csv](datasets/dl-course-data/ion.csv) | 351 | 36 |

I dati restano quelli originali. La raccolta DL includeva altri CSV non utilizzati: non sono stati duplicati nella piattaforma. Il file `songs.csv`, da oltre 500 MB, non serve a queste lezioni. [Inventario e hash dei file](data-inventory.json).

## Dati del percorso principale

| Materiale | Dati originali | Destinazione locale |
| --- | --- | --- |
| Esempi ML | [Melbourne Housing Snapshot](https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot) | ai_lab/input/melbourne-housing-snapshot/melb_data.csv |
| Esercizi ML 2–7 | [Home Data for ML Course](https://www.kaggle.com/competitions/home-data-for-ml-course/data) | ai_lab/input/home-data-for-ml-course/train.csv e test.csv |
| Sei moduli DL | [DL Course Data](https://www.kaggle.com/datasets/ryanholbrook/dl-course-data) | ai_lab/input/dl-course-data/ |
| Approfondimento ML tut8 | [Mobile Price Classification](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification) | ai_lab/input/mobile-price-classification/train.csv |
| Tutorial Titanic | [Titanic](https://www.kaggle.com/competitions/titanic/data) | ai_lab/input/titanic/ |

DL Course Data contiene i CSV **red-wine**, **concrete**, **fuel**, **spotify**, **hotel** e **ion**. Non è necessario riscrivere le lezioni con dati sintetici. I riferimenti sono ricavati dai metadati e dagli script `setup_data.sh` originali.

Per partecipare alle competizioni e inviare risultati può essere necessario accedere a Kaggle e accettarne le regole. I dati conservano condizioni proprie, distinte dalla licenza del codice: Melbourne indica CC BY-NC-SA 4.0. Gli archivi Iowa e DL ricevuti non contengono una licenza; la relativa verifica prima della pubblicazione remota resta documentata nelle attribuzioni. Questa versione è preparata localmente, senza pubblicazione remota.

## Aggiornare i dati: importazione manuale

Scarica lo ZIP dalla pagina del dataset o della competizione. Dalla radice del pacchetto estratto o della fork, importa ciascun archivio:

```sh
python ai_lab/tools/datasets.py melbourne --import-zip /path/to/archive.zip
python ai_lab/tools/datasets.py iowa --import-zip /path/to/home-data-for-ml-course.zip
python ai_lab/tools/datasets.py deep-learning --import-zip /path/to/dl-course-data.zip
python ai_lab/tools/datasets.py --check
```

Lo script controlla i file attesi, evita percorsi di estrazione pericolosi e non sovrascrive file locali differenti. Per Iowa crea anche gli alias `ai_lab/input/train.csv` e `test.csv` richiesti da alcune celle originali.

Se hai scaricato CSV singoli puoi importarli senza creare uno ZIP. Puoi anche importare i file un po’ alla volta:

```sh
python ai_lab/tools/datasets.py melbourne --import-files /path/to/melb_data.csv
python ai_lab/tools/datasets.py iowa --import-files /path/to/train.csv /path/to/test.csv
python ai_lab/tools/datasets.py deep-learning --import-files /path/to/red-wine.csv /path/to/concrete.csv /path/to/fuel.csv /path/to/spotify.csv /path/to/hotel.csv /path/to/ion.csv
```

## Aggiornare i dati: API ufficiale Kaggle

Installa e configura la CLI ufficiale seguendo la [documentazione Kaggle](https://github.com/Kaggle/kaggle-api). Conserva le credenziali fuori dal repository. Dopo aver accettato le regole necessarie:

```sh
python -m pip install kaggle
python ai_lab/tools/datasets.py melbourne iowa deep-learning
python ai_lab/tools/datasets.py --check
```

Lo strumento richiama la CLI e importa gli ZIP; non raccoglie né salva credenziali. Il download automatico non è stato eseguito in questa sessione perché il terminale non ha accesso a Internet. Questo è un limite dell’ambiente di sviluppo, non dei dataset.

## Ambiente Python e percorsi

Il bootstrap aggiunto ai notebook trova la fork o il pacchetto, aggiunge `learntools` al percorso Python e imposta come cartella di lavoro **`ai_lab/runtime`**. In questo modo i riferimenti originali `../input/...` puntano a **`ai_lab/input`**. Esegui quella cella prima delle celle originali.

I controlli DL originali leggono anche attributi interni di **Keras 2**. È quindi previsto un ambiente separato con Python **3.11** e `ai_lab/requirements/kaggle-local.txt`, distinto dall’ambiente Keras moderno degli approfondimenti AI Lab. Il file specifica un obiettivo di compatibilità; l’installazione e l’esecuzione completa con i dati restano da confermare su un computer connesso.

```sh
python3.11 -m venv .venv-kaggle
source .venv-kaggle/bin/activate
python -m pip install -r ai_lab/requirements/kaggle-local.txt
jupyter lab
```

Il bootstrap disattiva, soltanto nel processo locale, gli eventi verso l’iframe Kaggle e carica il componente di traduzione AI Lab. Etichette, suggerimenti e spiegazioni dei moduli introduttivi sono in italiano; codice delle soluzioni e diagnostica tecnica dei controlli conservano la forma originale. La logica dei checker non viene modificata.

## Approfondimenti con requisiti diversi

L’esercizio pulsar cita un percorso non registrato nei metadati: `predicting-a-pulsar-star/pulsar_stars.csv`. La fonte esatta e la licenza vanno identificate prima di automatizzarne il download. Lo script non inventa uno slug.

AutoML richiede anche servizi cloud e relativo wrapper; scaricare i CSV non rende gratuito quel servizio. TPU/Higgs e il corso storico di computer vision usano ulteriori pesi, immagini e TFRecord: sono approfondimenti distinti con riferimenti conservati nei sorgenti.
