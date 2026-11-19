# Microsoft: storia dell'apprendimento automatico

> **Nota AI Lab.** Questa è la traduzione italiana della [lezione originale Microsoft](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/2-history-of-ML/README.md), mantenuta integralmente nei contenuti. La traduzione automatica pubblicata da Microsoft è stata rivista linguisticamente da AI Lab; i link interni sono stati adattati. Date e interpretazioni sono quelle della fonte e alcune sono discusse nelle note AI Lab. Le lezioni NLP citate appartengono al corso Microsoft.

![Riassunto della storia dell'apprendimento automatico in uno sketchnote](assets/intro/ml-history.png)
> Sketchnote originale di [Tomomi Imura](https://github.com/girliemac), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), non modificato.

## [Quiz pre-lezione](https://ff-quizzes.netlify.app/en/ml/)

---

[![ML for beginners - History of Machine Learning](https://img.youtube.com/vi/N6wxM4wZ7V0/0.jpg)](https://youtu.be/N6wxM4wZ7V0 "ML for beginners - History of Machine Learning")

> 🎥 Clicca sull'immagine per un breve video che presenta la lezione.

In questa lezione ripercorriamo alcune tappe della storia del machine learning e dell'intelligenza artificiale.

La storia dell'intelligenza artificiale e quella del machine learning sono intrecciate: gli algoritmi e i progressi nel calcolo che hanno reso possibile il ML hanno contribuito anche allo sviluppo dell'IA. Questi campi iniziarono a delinearsi come discipline distinte negli anni Cinquanta, ma importanti [scoperte matematiche, statistiche, algoritmiche e tecniche](https://wikipedia.org/wiki/Timeline_of_machine_learning) li precedettero o si svilupparono contemporaneamente. L'idea di una «macchina pensante» ha inoltre [radici intellettuali più antiche](https://wikipedia.org/wiki/History_of_artificial_intelligence).

---
## Scoperte notevoli

- 1763, 1812 [Teorema di Bayes](https://wikipedia.org/wiki/Bayes%27_theorem) e i suoi predecessori. Questo teorema e le sue applicazioni costituiscono la base dell'inferenza, descrivendo la probabilità che un evento si verifichi basandosi su conoscenze precedenti.
- 1805 [Teoria dei minimi quadrati](https://wikipedia.org/wiki/Least_squares) del matematico francese Adrien-Marie Legendre. Questa teoria, che apprenderai nella nostra unità di regressione, aiuta nell'adattamento dei dati.
- **1913 — [Catene di Markov](https://wikipedia.org/wiki/Markov_chain):** prendono il nome dal matematico russo Andrey Markov e descrivono sequenze di eventi in cui le transizioni dipendono dallo stato precedente.
- **1957 — [Percettrone](https://wikipedia.org/wiki/Perceptron):** un classificatore lineare ideato dallo psicologo statunitense Frank Rosenblatt, fra i precursori delle reti neurali moderne.

---

- **1967 — [Vicino più prossimo](https://wikipedia.org/wiki/Nearest_neighbor):** la fonte lo presenta come algoritmo usato nella ricerca di percorsi; nel ML metodi basati sui vicini aiutano a riconoscere regolarità.
- **1970 — [Retropropagazione](https://wikipedia.org/wiki/Backpropagation):** viene usata per addestrare [reti neurali feedforward](https://wikipedia.org/wiki/Feedforward_neural_network).
- **1982 — [Reti neurali ricorrenti](https://wikipedia.org/wiki/Recurrent_neural_network):** reti neurali con connessioni ricorrenti, utili per rappresentare dipendenze nel tempo.

> **Nota AI Lab:** alcune date e attribuzioni dell’elenco sono semplificate o controverse: ad esempio il vicino più prossimo come metodo di classificazione precede il 1967 e la retropropagazione ha una storia con più contributi. Consulta le fonti e confronta le date.

✅ Fai un po' di ricerca. Quali altre date si distinguono come fondamentali nella storia di ML e AI?

---
## 1950: Macchine che pensano

Alan Turing contribuì a porre le basi della riflessione sulle «macchine che pensano». Per affrontare la questione propose quello che oggi è noto come [test di Turing](https://www.bbc.com/news/technology-18475646), affrontato anche nelle lezioni sul linguaggio del corso Microsoft. Nel 2019 fu scelto dal [pubblico di una trasmissione](https://wikipedia.org/wiki/Icons:_The_Greatest_Person_of_the_20th_Century) come scienziato più importante del XX secolo.

---
## 1956: Progetto di ricerca estivo di Dartmouth

"Il Progetto di ricerca estivo di Dartmouth sull’intelligenza artificiale fu un evento fondamentale per l'intelligenza artificiale come campo," ed è qui che fu coniato il termine 'intelligenza artificiale' ([fonte](https://250.dartmouth.edu/highlights/artificial-intelligence-ai-coined-dartmouth)).

> Ogni aspetto dell'apprendimento o qualsiasi altra caratteristica dell'intelligenza può in principio essere così precisamente descritto che una macchina può essere fatta per simularlo.

---

Il ricercatore principale, il professore di matematica John McCarthy, sperava "di procedere sulla base della congettura che ogni aspetto dell'apprendimento o qualsiasi altra caratteristica dell'intelligenza possa in principio essere così precisamente descritto che una macchina possa essere fatta per simularlo." Tra i partecipanti c'era un altro luminare nel campo, Marvin Minsky.

Al seminario si attribuisce il merito di aver incoraggiato il confronto su metodi simbolici, sistemi per domini limitati e approcci deduttivi e induttivi. [Approfondimento](https://wikipedia.org/wiki/Dartmouth_workshop).

---
## 1956 - 1974: "Gli anni d'oro"

Dagli anni '50 fino alla metà degli anni '70, l'ottimismo era alto nell'aspettativa che l'IA potesse risolvere molti problemi. Nel 1967, Marvin Minsky affermava con fiducia che "Entro una generazione ... il problema di creare 'intelligenza artificiale' sarà sostanzialmente risolto." (Minsky, Marvin (1967), Computation: Finite and Infinite Machines, Englewood Cliffs, N.J.: Prentice-Hall)

La ricerca sull'elaborazione del linguaggio naturale si sviluppò, gli algoritmi di ricerca migliorarono e nacquero i «micromondi»: ambienti semplificati in cui svolgere compiti a partire da istruzioni in linguaggio naturale.

---

Gli enti governativi finanziarono la ricerca; nel frattempo avanzarono il calcolo e gli algoritmi e furono realizzati diversi prototipi. Ecco alcuni esempi:

* [Shakey il robot](https://wikipedia.org/wiki/Shakey_the_robot), che poteva manovrare e decidere come eseguire i compiti in modo 'intelligente'.

    [Immagine originale di Shakey nella lezione Microsoft](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/2-history-of-ML/images/shakey.jpg)
    > Shakey nel 1972

---

* Eliza, uno dei primi chatbot, poteva conversare con le persone e agire come una 'terapeuta' primitiva. Imparerai di più su Eliza nelle lezioni di NLP.

    [Immagine originale di ELIZA nella lezione Microsoft](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/2-history-of-ML/images/eliza.png)
    > Una versione di Eliza, un chatbot

---

* Il «mondo dei blocchi» era un micromondo in cui impilare e ordinare blocchi e sperimentare come far prendere decisioni a una macchina. Sistemi come [SHRDLU](https://wikipedia.org/wiki/SHRDLU) contribuirono alla ricerca sull'elaborazione del linguaggio.

    [![blocks world con SHRDLU](https://img.youtube.com/vi/QAJz4YKUwqw/0.jpg)](https://www.youtube.com/watch?v=QAJz4YKUwqw "blocks world con SHRDLU")

    > 🎥 Clicca sull'immagine sopra per un video: Blocks world con SHRDLU

---
## 1974 - 1980: "Inverno dell'IA"

A metà degli anni Settanta apparve chiaro che la difficoltà di costruire «macchine intelligenti» era stata sottovalutata e che molte promesse superavano ciò che si poteva ottenere con le risorse disponibili. La fiducia e i finanziamenti diminuirono. Fra le difficoltà indicate dalla fonte:
---
- **Limitazioni**. La capacità di calcolo era limitata.
- **Esplosione combinatoria**. La quantità di parametri da addestrare cresceva esponenzialmente man mano che si chiedeva di più ai computer, senza un aumento parallelo della capacità di calcolo.
- **Poca disponibilità di dati**. La scarsità di dati ostacolava il processo di test, sviluppo e perfezionamento degli algoritmi.
- **Stiamo facendo le domande giuste?**. Le stesse domande poste iniziarono a essere messe in dubbio. I ricercatori iniziarono a ricevere critiche riguardo ai loro approcci:
  - Il Test di Turing venne messo in discussione tramite, tra le altre idee, la 'teoria della stanza cinese' che asseriva che "programmare un computer digitale può far sembrare che comprenda il linguaggio ma non può produrre una vera comprensione." ([fonte](https://plato.stanford.edu/entries/chinese-room/))
  - Furono sollevate questioni etiche sull'uso sociale di sistemi come la «terapeuta» ELIZA.

---

Nello stesso periodo, iniziarono a formarsi varie scuole di pensiero sull'IA. Si stabilì una dicotomia tra pratiche ["scruffy" vs. "neat AI"](https://wikipedia.org/wiki/Neats_and_scruffies). I laboratori _scruffy_ modificavano programmi per ore fino a ottenere i risultati desiderati. I laboratori _neat_ "si concentravano sulla logica e sulla risoluzione formale dei problemi". ELIZA e SHRDLU erano sistemi _scruffy_ ben noti. Negli anni '80, con la crescente domanda di rendere riproducibili i sistemi ML, l'approccio _neat_ prese gradualmente il sopravvento poiché fornisce risultati più spiegabili.

---
> **Nota AI Lab:** l’esplosione combinatoria riguarda la crescita delle possibilità da esplorare; non coincide necessariamente con il numero di parametri da addestrare. Anche la contrapposizione fra approcci «neat» e «scruffy» è una semplificazione storica.

## Anni '80 Sistemi esperti

Con la crescita del campo, divenne più chiaro il suo beneficio per il business, e negli anni Ottanta si diffusero i «sistemi esperti». "I sistemi esperti furono tra le prime forme veramente di successo di software di intelligenza artificiale (IA)." ([fonte](https://wikipedia.org/wiki/Expert_system)).

Un sistema esperto combina una base di regole con un motore di inferenza, che usa quelle regole per dedurre nuovi fatti.

In quegli anni crebbe anche l'attenzione per le reti neurali.

---
## 1987 - 1993: 'Pausa' dell'IA

L'hardware destinato ai sistemi esperti divenne molto specializzato, con i limiti che questo comportava. L'ascesa dei personal computer competeva anche con questi grandi sistemi centralizzati e specializzati. L'informatica cominciava così a diventare più accessibile, preparando il terreno alla successiva crescita dei big data.

---
## 1993 - 2011

In questo periodo la maggiore disponibilità di dati e capacità di calcolo contribuì a superare alcuni ostacoli incontrati dall'IA e dal machine learning. La quantità di dati disponibili crebbe rapidamente, con effetti positivi e negativi, anche con la diffusione degli smartphone intorno al 2007. Aumentò la capacità di calcolo, gli algoritmi si evolsero e il campo continuò a maturare.

---
## Adesso

Oggi l'apprendimento automatico e l'IA toccano quasi ogni parte della nostra vita. Questa era richiede una comprensione attenta dei rischi e dei potenziali effetti di questi algoritmi sulle vite umane. Come ha affermato Brad Smith di Microsoft, "La tecnologia dell'informazione solleva questioni che vanno al cuore delle protezioni fondamentali dei diritti umani come la privacy e la libertà di espressione. Queste questioni aumentano la responsabilità delle aziende tecnologiche che creano questi prodotti. A nostro avviso, richiedono anche una regolamentazione governativa ponderata e lo sviluppo di norme sugli usi accettabili" ([fonte](https://www.technologyreview.com/2019/12/18/102365/the-future-of-ais-impact-on-society/)).

---

Non sappiamo con certezza che cosa riservi il futuro. Comprendere questi sistemi, il software e gli algoritmi che usano ci aiuta però a formarci un giudizio autonomo.

[![La storia del deep learning](https://img.youtube.com/vi/mTtDfKgLm54/0.jpg)](https://www.youtube.com/watch?v=mTtDfKgLm54 "La storia del deep learning")
> 🎥 Clicca sull'immagine sopra per un video: Yann LeCun discute la storia del deep learning in questa lezione

---
## 🚀Sfida

Approfondisci uno di questi momenti storici e scopri di più sulle persone dietro di essi. Le scoperte scientifiche nascono in un contesto culturale e coinvolgono molte persone. Che cosa scopri?

## [Quiz post-lezione](https://ff-quizzes.netlify.app/en/ml/)

---
## Ripasso & Studio autonomo

Ecco alcuni elementi da guardare e ascoltare:

[Questo podcast in cui Amy Boyd discute l'evoluzione dell'IA](http://runasradio.com/Shows/Show/739)

[![La storia dell'IA di Amy Boyd](https://img.youtube.com/vi/EJt3_bFYKss/0.jpg)](https://www.youtube.com/watch?v=EJt3_bFYKss "La storia dell'IA di Amy Boyd")

---

## Compito

[Crea una timeline: consegna originale](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/2-history-of-ML/assignment.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
Traduzione automatica originale successivamente rivista da AI Lab.

**Disclaimer**:
Questo documento è stato tradotto utilizzando il servizio di traduzione AI [Co-op Translator](https://github.com/Azure/co-op-translator). Sebbene ci impegniamo per garantire la precisione, si prega di notare che le traduzioni automatizzate possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un essere umano. Non siamo responsabili per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->