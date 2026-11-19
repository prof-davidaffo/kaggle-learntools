# Microsoft: introduzione al machine learning

> **Nota AI Lab.** Questa è la traduzione italiana della [lezione originale Microsoft](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/1-intro-to-ML/README.md), mantenuta integralmente nei contenuti. È basata sulla traduzione automatica pubblicata da Microsoft, rivista linguisticamente da AI Lab; i link interni sono stati adattati e le figure sono quelle originali in inglese. Le indicazioni sul programma e sugli strumenti riguardano il corso Microsoft, non AI Lab. Per il nostro ambiente consulta [Come lavorare](esecuzione.html).

## [Quiz pre-lezione](https://ff-quizzes.netlify.app/en/ml/)

---

[![ML per principianti - Introduzione al Machine Learning per principianti](https://img.youtube.com/vi/6mSx_KJxcHI/0.jpg)](https://youtu.be/6mSx_KJxcHI "ML per principianti - Introduzione al Machine Learning per principianti")

> 🎥 Clicca sull'immagine sopra per un breve video che descrive questa lezione.

Benvenuto nel corso Microsoft sul machine learning classico per principianti. Il corso si rivolge sia a chi parte da zero sia a chi desidera ripassare. Gli autori invitano a condividere [commenti e osservazioni](https://github.com/microsoft/ML-For-Beginners/discussions).

[![Introduzione al ML](https://img.youtube.com/vi/h0e2HAPTGF4/0.jpg)](https://youtu.be/h0e2HAPTGF4 "Introduzione al ML")

> 🎥 Clicca sull'immagine sopra per un video: John Guttag del MIT introduce il machine learning

---
## Iniziare con il machine learning

Il corso Microsoft suggerisce di preparare il computer per eseguire i notebook e di familiarizzare con i seguenti strumenti:

- **Configurazione:** le guide video spiegano come [installare Python](https://youtu.be/CXZYvNRIAKM) e [configurare un editor](https://youtu.be/EU8eayHWoZg).
- **Python:** è utile conoscerne le basi; Microsoft propone questo [percorso di apprendimento](https://docs.microsoft.com/learn/paths/python-language/?WT.mc_id=academic-77952-leestott).
- **Node.js e JavaScript:** alcune applicazioni web del corso originale richiedono [Node.js](https://nodejs.org), npm e [Visual Studio Code](https://code.visualstudio.com/).
- **GitHub:** gli autori suggeriscono di creare un account e una copia (*fork*) del curriculum, se si vuole lavorare direttamente sul repository e condividere osservazioni.
- **Scikit-learn:** la [guida ufficiale](https://scikit-learn.org/stable/user_guide.html) presenta la libreria usata nelle lezioni di machine learning.

> **Per AI Lab:** segui invece le nostre [istruzioni di esecuzione](esecuzione.html). Node.js e un fork del corso Microsoft non sono prerequisiti del nostro percorso.

---
## Cos'è il machine learning?

Il termine *machine learning* è molto diffuso, ma il funzionamento dei sistemi che lo usano può sembrare misterioso. Per comprenderlo è utile procedere gradualmente, partendo da esempi concreti.

---
## La curva dell'entusiasmo

![curva hype ml](assets/intro/hype.png)

> Immagine originale del corso Microsoft; dati storici, non una misurazione aggiornata. Google Trends mostra la recente 'curva dell'entusiasmo' del termine 'machine learning'

---
## Un universo misterioso

Viviamo in un universo pieno di domande. Scienziati come Stephen Hawking e Albert Einstein hanno dedicato la vita a cercare informazioni capaci di chiarire i misteri del mondo. Anche crescendo impariamo continuamente: un bambino scopre poco alla volta regolarità nel proprio ambiente.

## Il cervello del bambino

Attraverso i sensi, un bambino raccoglie informazioni sull'ambiente e impara gradualmente a riconoscere situazioni e regolarità. La capacità del cervello di cambiare con l'esperienza è legata alla [plasticità cerebrale](https://www.simplypsychology.org/brain-plasticity.html). Gli autori propongono un'analogia generale con il machine learning: in entrambi i casi l'esperienza offre informazioni da cui apprendere.

## Il cervello umano

Il [cervello umano](https://www.livescience.com/29365-human-brain.html) riceve informazioni, le elabora e contribuisce alle decisioni e alle azioni. La lezione originale usa questo esempio per introdurre l'idea di riprodurre con una macchina alcuni comportamenti associati all'intelligenza.

> **Nota AI Lab:** è un'analogia introduttiva, non una descrizione equivalente di cervello e modello: i sistemi di machine learning apprendono con meccanismi diversi e le persone non prendono sempre decisioni razionali.

---
## La terminologia

Il machine learning (ML) è una parte importante dell'intelligenza artificiale. Usa algoritmi per individuare informazioni e regolarità nei dati e aiutare a formulare previsioni o prendere decisioni.

---
## IA, ML e deep learning

![AI, ML, deep learning, data science](assets/intro/ai-ml-ds.png)

> Un diagramma che mostra le relazioni tra AI, ML, deep learning e data science. Infografica di [Jen Looper](https://twitter.com/jenlooper) ispirata da [questa grafica](https://softwareengineering.stackexchange.com/questions/366996/distinction-between-ai-ml-neural-networks-deep-learning-and-data-mining)

---
## Concetti da trattare

Il corso Microsoft presenta i concetti fondamentali del machine learning classico, usando soprattutto la libreria Scikit-learn. Gli autori propongono queste basi come preparazione per affrontare temi più ampi dell'IA e del deep learning.

---
## In questo corso Microsoft imparerai:

- i concetti fondamentali del machine learning
- la storia del ML
- ML e equità
- tecniche ML di regressione
- tecniche ML di classificazione
- tecniche ML di clustering
- tecniche ML di elaborazione del linguaggio naturale
- tecniche ML di previsione di serie temporali
- apprendimento per rinforzo
- applicazioni reali del ML

---
## Cosa non tratta il corso Microsoft

- deep learning
- reti neurali
- AI

Il curriculum Microsoft tratta reti neurali, deep learning e altri temi dell'IA in un percorso distinto e rimanda a un curriculum separato sulla data science. AI Lab, invece, comprende anche un corso introduttivo al deep learning dopo quello sul machine learning.

---
## Perché studiare il machine learning?

Da una prospettiva sistemica, il machine learning permette di costruire sistemi che individuano regolarità nei dati per supportare previsioni e decisioni.

Gli autori accostano questa idea, come spunto generale, al modo in cui le persone imparano dall'esperienza.

✅ Pensa per un attimo al motivo per cui un'azienda vorrebbe usare strategie di machine learning piuttosto che creare un sistema basato su regole scritte a mano.

---
## Perché la qualità dei dati è importante

Dati di alta qualità possono migliorare le prestazioni del modello. Dati scadenti o rumorosi possono portare a previsioni inaccurate, anche usando algoritmi avanzati di machine learning.

---
## Applicazioni del machine learning

Il machine learning trova applicazione in molti ambiti, anche grazie ai dati prodotti da smartphone, dispositivi connessi e altri sistemi. I ricercatori ne studiano l'uso per affrontare problemi reali che coinvolgono più dimensioni e discipline.

---
## Esempi di ML applicato

**Puoi usare il machine learning in molti modi**:

- Per prevedere la probabilità di malattia dalla storia medica o dai referti di un paziente.
- Per sfruttare i dati meteo per prevedere eventi meteorologici.
- Per capire il sentimento di un testo.
- Per rilevare fake news e fermare la diffusione della propaganda.

> **Nota AI Lab:** rilevare automaticamente disinformazione è un problema difficile: un modello può sbagliare e non sostituisce la verifica delle fonti. Per gli impieghi sanitari sono necessarie valutazione e supervisione adeguate.

Finanza, economia, scienze della terra, esplorazione spaziale, ingegneria biomedica, scienze cognitive e persino campi delle scienze umane hanno adattato il machine learning per risolvere i complessi problemi di elaborazione dati dei loro domini.

---
## Conclusione

Il machine learning aiuta a individuare regolarità in dati reali o generati ed è impiegato, fra l'altro, in ambito aziendale, sanitario e finanziario.

La sua diffusione rende utile comprenderne le basi anche per chi lavora in settori diversi dall'informatica.

---
# 🚀 Sfida

Disegna, su carta o con un'app come [Excalidraw](https://excalidraw.com/), una mappa delle differenze tra IA, ML, deep learning e data science. Aggiungi esempi di problemi adatti a ciascun ambito.

# [Quiz post-lezione](https://ff-quizzes.netlify.app/en/ml/)

---
# Revisione & Autoapprendimento

Per imparare di più su come lavorare con algoritmi ML nel cloud, segui questo [Percorso di apprendimento](https://docs.microsoft.com/learn/paths/create-no-code-predictive-models-azure-machine-learning/?WT.mc_id=academic-77952-leestott).

Segui un [Percorso di apprendimento](https://docs.microsoft.com/learn/modules/introduction-to-machine-learning/?WT.mc_id=academic-77952-leestott) sulle basi del ML.

---
# Compito

[Inizia subito: consegna originale](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/1-intro-to-ML/assignment.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
Traduzione automatica originale successivamente rivista da AI Lab.

**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->