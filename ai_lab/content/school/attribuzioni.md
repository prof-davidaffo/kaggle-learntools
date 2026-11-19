# Fonti, attribuzioni e licenze

Questo sito è una **traduzione italiana e riorganizzazione didattica dei corsi originali Kaggle Learn**, a cura di **AI Lab**, progetto scolastico indipendente. La riorganizzazione riguarda presentazione, navigazione e accesso ai materiali; le lezioni conservano integralmente il contenuto dei notebook sorgente. Non è una piattaforma ufficiale Kaggle e non rilascia attestati Kaggle.

## Materiali Kaggle

Sorgenti: [fork del docente](https://github.com/prof-davidaffo/kaggle-learntools) e [repository originale Kaggle/learntools](https://github.com/Kaggle/learntools). I materiali sono derivati dal commit registrato nell’[inventario](inventory.json). I file sorgente originali sono conservati.

Il repository originale usa **Apache License 2.0**. La [licenza completa](LICENSE-Kaggle.txt) è inclusa nel sito; il file `LICENSE` originale resta nella radice. Nella copia analizzata non è presente un file NOTICE. Restano validi gli avvisi degli autori presenti nei sorgenti.

I metadati originali attribuiscono il corso Machine Learning a **Dan Becker**, con contributi di **Alexis Cook**, e Intro to Deep Learning a **Ryan Holbrook**. Il corso storico Deep Learning è attribuito a Dan Becker, con materiali TPU di Ryan Holbrook. Le pagine collegano i file di provenienza e ne conservano i riferimenti.

Le traduzioni italiane AI Lab riportano integralmente i testi disponibili nei notebook sorgente, conservando spiegazioni, esempi, domande, figure e riferimenti nell’ordine originale. Il riferimento è la versione registrata nell’inventario. Le note sull’ambiente locale o Colab sono aggiunte separate e identificate come AI Lab. Sono tradotti anche i commenti didattici; istruzioni Python, identificatori e API restano invariati. I video esterni non sono tradotti.

## Introduzione all’IA

La pagina [Alla scoperta dell’IA](introduzione-ia.html) è un percorso originale AI Lab, ispirato alle lezioni introduttive di [Microsoft ML for Beginners](https://github.com/microsoft/ML-For-Beginners). La linea del tempo illustrata in inglese è di **Tomomi Imura**, tratta dalla [lezione originale sulla storia](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/2-history-of-ML/README.md); e le altre due illustrazioni della stessa autrice sono riprodotte senza modifiche dal repository Microsoft, con [licenza CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), come specificato nella [cartella originale degli sketchnote](https://github.com/microsoft/ML-For-Beginners/tree/main/sketchnotes). L’infografica di Jen Looper è conservata nella lezione Microsoft, con [licenza MIT del repository](assets/intro/LICENSE-Microsoft.txt); lo schema a cerchi è originale AI Lab. Le due lezioni complete sono traduzioni adattate dal progetto Microsoft, licenza MIT; conservano l’avviso della traduzione automatica originale e le note AI Lab distinguono il nostro percorso. Le altre fonti sono collegate nella pagina e non sono riprodotte.

## Materiale originale AI Lab

Programma, guide ai progetti, notebook scolastici, strumenti e interfaccia sono nuovi materiali del progetto e sono distribuiti con **Apache-2.0**, come indicato in `ai_lab/LICENSE`. I dataset sintetici sono generati dal codice originale AI Lab e non rappresentano persone, immobili o specie reali.

## Immagini, video e dataset esterni

Le immagini e le animazioni dei notebook sono conservate in copie locali nel sito e nel pacchetto studenti; i notebook scaricabili le incorporano. L’[inventario delle immagini](assets/kaggle-images/manifest.json) riporta l’URL originale, il nome del file, la dimensione e l’impronta SHA-256. La licenza del codice non viene attribuita automaticamente alle immagini: le loro condizioni specifiche restano da verificare.

I video del corso storico sono collegamenti esterni: non sono inclusi né tradotti. I nove CSV del percorso principale sono stati acquisiti dagli archivi forniti dal docente e integrati localmente nel sito e nel pacchetto studenti, senza modifiche ai dati. L’inventario registra provenienza prevista, hash e dimensioni. Melbourne Housing Snapshot dichiara CC BY-NC-SA 4.0 e richiede le relative attribuzioni e condizioni, distinte dalla licenza del codice. Per Iowa, la fonte riconosce il dataset Ames Housing di Dean De Cock; DL Course Data è la raccolta preparata da Ryan Holbrook per le lezioni. Gli ZIP ricevuti per queste due raccolte non contengono licenze: le condizioni specifiche restano da confermare prima della pubblicazione remota, senza attribuire loro Apache-2.0. TFRecord e pesi preaddestrati dell’archivio storico non sono inclusi.

Per il progetto cifre, `load_digits` rimanda al dataset **Optical Recognition of Handwritten Digits**, E. Alpaydin e C. Kaynak, UCI. Leggi la descrizione distribuita da scikit-learn e la relativa provenienza prima di riusarlo fuori dal laboratorio. Le frasi del progetto sentiment sono nuovi esempi scolastici, non recensioni raccolte da altri siti.

## Software del sito

- **Python-Markdown**, licenza BSD, per convertire Markdown.
- **Pygments**, licenza BSD, per evidenziare il codice.
- **nbformat/nbconvert**, licenza BSD, per notebook e preprocessor.
- **KaTeX 0.16.21**, licenza MIT, per le formule anche offline. [Licenza inclusa](assets/vendor/katex/LICENSE). JavaScript, CSS e font sono distribuiti localmente dalla distribuzione KaTeX già disponibile nella workspace.

Le dipendenze installate restano soggette alle proprie licenze. Non è stata effettuata alcuna pubblicazione remota durante lo sviluppo.
