# Dataset originali acquisiti

Gli archivi forniti dal docente in `data/` sono stati importati nella directory dedicata `ai_lab/input`. I nove CSV del percorso principale sono completi. I dati originali non sono stati modificati.

| Raccolta | CSV | Righe | Colonne |
| --- | --- | ---: | ---: |
| melbourne | melb_data.csv | 13580 | 21 |
| iowa | train.csv | 1460 | 81 |
| iowa | test.csv | 1459 | 80 |
| deep-learning | red-wine.csv | 1599 | 12 |
| deep-learning | concrete.csv | 1030 | 9 |
| deep-learning | fuel.csv | 1107 | 14 |
| deep-learning | spotify.csv | 32833 | 23 |
| deep-learning | hotel.csv | 119390 | 32 |
| deep-learning | ion.csv | 351 | 36 |

## Integrazione

La build copia i CSV nel sito e nel pacchetto studenti, con file di attribuzione distinti dalla licenza del codice. Gli alias Iowa `input/train.csv` e `input/test.csv` sono inclusi per conservare i percorsi delle celle originali. I requirements di tutti gli ambienti sono presenti nel pacchetto. L’inventario JSON registra hash, dimensioni e provenienza prevista degli archivi e dei file.

Gli ZIP originali restano in `data/`, senza cancellazioni. Sono esclusi dal versionamento tramite `data/.gitignore`: `archive.zip` supera i 100 MB. Il CSV `songs.csv` supera i 500 MB e non è usato dal percorso; non è stato estratto né incluso. Sono omessi anche gli altri CSV DL non usati e le copie `.gz` Iowa. Nessun CSV necessario supera i 100 MB.

## Licenze e attribuzioni

Melbourne Housing Snapshot dichiara CC BY-NC-SA 4.0: fonte Dan Becker, derivata dal lavoro di Tony Pino. La pagina di provenienza è https://www.kaggle.com/dansbecker/melbourne-housing-snapshot/metadata .

Iowa deriva da Ames Housing, compilato da Dean De Cock; la fonte del corso è la competizione Home Data for ML Course di Kaggle. DL Course Data è la raccolta preparata da Ryan Holbrook per le lezioni. Gli archivi ricevuti di Iowa e DL non contengono licenze: il relativo stato resta `not-verified` nel manifesto, senza attribuire Apache-2.0 ai dati. La conferma delle condizioni prima della pubblicazione remota resta un intervento aperto. Il pacchetto è stato preparato localmente e non è stato pubblicato.

## Verifiche di questa integrazione

Controllati nomi dei file, intestazioni CSV, dimensioni, righe e colonne; la build verifica che le copie nel sito e nello ZIP coincidano con i CSV importati. Non è stato eseguito alcun nuovo addestramento dei modelli.
