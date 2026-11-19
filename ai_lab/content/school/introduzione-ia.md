# Prima di iniziare: che cosa c'entra l'intelligenza artificiale?

Apri una piattaforma di video e trovi suggerimenti scelti per te. Fotografi un testo e il telefono lo riconosce. Chiedi a un assistente di scrivere una poesia e, in pochi secondi, compare una risposta. **Che cosa hanno in comune questi sistemi? E come possiamo capire quando fidarci?**

In questo percorso passeremo dall'uso di strumenti già pronti alla costruzione di semplici modelli: lavoreremo con dati, faremo previsioni e misureremo gli errori. Questa introduzione ti dà una mappa per capire dove stiamo andando. Non serve conoscere Python per leggerla.

> **Prima domanda.** Un programma che calcola la media dei voti usa necessariamente l'IA? E un filtro antispam? Annota le tue idee: ci torneremo tra poco.

## 1. Perché studiare l'IA?

L'IA può aiutare a riconoscere immagini, cercare informazioni, prevedere consumi o individuare messaggi indesiderati. Non tutti questi problemi richiedono la stessa tecnica: riconoscere un gatto, stimare il prezzo di una casa e generare un testo sono compiti diversi.

Studiare come funzionano i modelli permette di andare oltre l'effetto sorpresa. Possiamo chiederci **quali dati hanno visto, che cosa stanno cercando di prevedere, come si misura un errore e chi subisce le conseguenze di una decisione**. Sono domande utili sia a chi costruisce sistemi sia a chi li usa. Il [quadro UNESCO sulle competenze degli studenti](https://www.unesco.org/en/articles/ai-competency-framework-students) affianca infatti conoscenze tecniche, progettazione, etica e attenzione alle persone.

## 2. IA, machine learning e deep learning: una mappa

- **Intelligenza artificiale (IA)**: un ampio campo dell'informatica che studia e costruisce sistemi capaci di svolgere compiti associati a capacità come ragionare, riconoscere o prendere decisioni. Comprende approcci diversi, anche basati su regole scritte dalle persone.
- **Machine learning (ML)**, o apprendimento automatico: una famiglia di metodi che costruiscono modelli a partire dai dati. Per esempio, un modello può imparare una relazione tra caratteristiche delle case e prezzo.
- **Deep learning (DL)**: un insieme di tecniche di machine learning basate su reti neurali con più strati. Sono usate, fra l'altro, per immagini, audio e linguaggio.
- **IA generativa**: sistemi progettati per generare contenuti, come testo, immagini o audio. Molti sistemi attuali usano il deep learning; il termine descrive soprattutto il tipo di compito svolto.

Una mappa semplificata è **IA → machine learning → deep learning**. L'IA generativa si può descrivere come un insieme di applicazioni: non coincide con tutta l'IA e non esaurisce il deep learning. Il machine learning usa algoritmi che individuano regolarità nei dati per aiutare a formulare previsioni e prendere decisioni: è l'idea presentata nell'[introduzione Microsoft al machine learning](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/1-intro-to-ML/README.md).

![Tre cerchi concentrici: il deep learning è nel machine learning, che è nell'intelligenza artificiale](assets/intro/cerchi-ia.svg)

*I cerchi mostrano una relazione di inclusione: ogni metodo di deep learning è un metodo di machine learning, ma molti metodi di machine learning non sono deep learning. Schema originale AI Lab.*

La media dei voti calcolata seguendo una formula è un algoritmo, ma non per questo è IA. Un filtro antispam può invece usare un modello addestrato su esempi di messaggi; potrebbe anche essere costruito con regole esplicite. **Dal solo risultato non sempre si può capire quale metodo sia stato usato.**

## 3. Una storia fatta di idee, entusiasmo e ostacoli

L'IA non nasce con i chatbot. Le sue radici intrecciano matematica, informatica, logica e studio dell'intelligenza. Questa linea del tempo seleziona alcune tappe: non è una gara verso un unico traguardo, ma la storia di approcci diversi che si sono spesso sviluppati insieme.

| Periodo | Un'idea o un passaggio | Perché ci interessa |
| --- | --- | --- |
| **1950** | Alan Turing propone il «gioco dell'imitazione» per discutere la domanda se le macchine possano pensare. | Il comportamento osservabile solleva domande difficili su linguaggio e intelligenza. [Articolo originale](https://doi.org/10.1093/mind/LIX.236.433). |
| **1956** | Il progetto estivo di Dartmouth contribuisce a dare un nome e un'identità al campo dell'«artificial intelligence». | L'IA diventa un programma di ricerca esplicito. [Dartmouth](https://250.dartmouth.edu/highlights/artificial-intelligence-ai-coined-dartmouth). |
| **Anni 1960–70** | Si esplorano programmi basati su simboli e regole, robot e dialoghi come ELIZA. | Un sistema può produrre risposte convincenti in un contesto limitato senza risolvere tutti i problemi del linguaggio. |
| **Anni 1970–80** | Dopo grandi aspettative emergono difficoltà; alcuni finanziamenti diminuiscono. Si parla di «inverni dell'IA». Negli anni Ottanta si diffondono anche i sistemi esperti. | I progressi non sono lineari: contano risorse, dati, problemi scelti e limiti delle tecniche. |
| **Anni 1990–2000** | Crescono metodi statistici e apprendimento dai dati; aumentano dati disponibili e capacità di calcolo. | Il machine learning diventa sempre più importante in molte applicazioni. |
| **2012** | Una rete neurale profonda ottiene un risultato decisivo nella competizione di riconoscimento immagini ImageNet. | Algoritmi, dati e capacità di calcolo contribuiscono insieme al successo del deep learning. [Articolo AlexNet](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html). |
| **2017 e dopo** | L'architettura Transformer apre nuove possibilità nell'elaborazione del linguaggio; in seguito i sistemi generativi diventano accessibili a un pubblico vasto. | Generare un testo plausibile è una capacità potente, ma la plausibilità non garantisce verità. [Articolo Transformer](https://arxiv.org/abs/1706.03762). |

![Linea del tempo illustrata in inglese sulla storia del machine learning, dai primi sviluppi ai sistemi moderni](assets/intro/ml-history.png)

*Illustrazione originale in inglese di Tomomi Imura, dal corso [ML for Beginners](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/2-history-of-ML/README.md), Microsoft. [Licenza CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), immagine non modificata. La figura è una sintesi storica: per gli sviluppi successivi confrontala con la tabella.*

> **Attività · Storia sotto la lente** — Scegli una tappa e cerca una fonte affidabile. Quale problema si voleva risolvere? Quali strumenti erano disponibili? Raccontala alla classe in tre frasi, indicando la fonte.

## 4. Come fa un modello a imparare dai dati?

Immagina di voler stimare il prezzo di una casa. Potresti scrivere a mano una regola: «più è grande, più costa». Ma posizione, numero di stanze e condizioni dell'immobile possono contare molto. Un modello può cercare relazioni a partire da **esempi di case con prezzi già noti**.

| Fase | Esempio delle case |
| --- | --- |
| **Dati** | Raccogliamo esempi con superficie, stanze e prezzo. |
| **Caratteristiche e obiettivo** | Superficie e stanze sono caratteristiche (*feature*); il prezzo noto è l'obiettivo (*target*). |
| **Addestramento** | Un algoritmo costruisce un modello usando una parte degli esempi. |
| **Validazione** | Confrontiamo le previsioni con prezzi noti di esempi tenuti separati dall'addestramento. |
| **Uso** | Se i risultati sono adeguati allo scopo, il modello può stimare prezzi di nuove case, restando soggetto a errori. |

Il modello non consulta una risposta magica: produce una **stima** in base alle relazioni trovate. Non è detto che funzioni bene per case molto diverse da quelle nei dati. Inoltre, valutare sugli stessi esempi usati per addestrare può dare un'impressione troppo ottimistica: per questo useremo dati separati.

Questo è un esempio di **apprendimento supervisionato**: ogni esempio di addestramento ha una risposta nota. Se la risposta è un numero, come un prezzo, parliamo di *regressione*; se è una categoria, come «spam» o «non spam», di *classificazione*. Esistono anche altri approcci: per esempio, nell'apprendimento non supervisionato si cercano strutture nei dati senza avere per ogni esempio una risposta corretta assegnata in anticipo.

> **Prova tu · Il filtro antispam** — Quali caratteristiche di un messaggio potrebbero essere utili? Qual è l'etichetta da prevedere? Che cosa succede se il filtro blocca un messaggio importante? Confronta le tue risposte con quelle di un compagno.

![Schema illustrato in inglese su esempi di applicazioni del machine learning nel mondo reale](assets/intro/ml-realworld.png)

*Applicazioni del machine learning: illustrazione originale di Tomomi Imura, [ML for Beginners](https://github.com/microsoft/ML-For-Beginners/tree/main/sketchnotes), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), non modificata.*

## 5. Quando un modello sbaglia

Un buon risultato medio non racconta tutto. Un modello può sbagliare più spesso su alcuni gruppi o in situazioni poco rappresentate nei dati; un filtro può lasciar passare spam oppure bloccare messaggi legittimi. I due tipi di errore hanno conseguenze diverse.

La qualità dei dati conta: esempi incompleti, etichette errate o raccolte poco rappresentative possono influenzare le previsioni. Un modello può inoltre sfruttare correlazioni che non indicano un rapporto di causa ed effetto. **Misurare, confrontare e discutere gli errori fa parte del lavoro**, non è un dettaglio da aggiungere alla fine.

Anche un chatbot può inventare informazioni o citazioni e presentarle con sicurezza. Quando un'affermazione conta, cerchiamo fonti verificabili e controlliamo i risultati. Evitiamo di inserire dati personali o riservati negli strumenti senza averne valutato le condizioni d'uso. L'obiettivo è mantenere alle persone la responsabilità delle decisioni.

![Schema illustrato in inglese sulle possibili fonti di disuguaglianza nei sistemi di machine learning](assets/intro/ml-fairness.png)

*Equità nel machine learning: illustrazione originale di Tomomi Imura, [ML for Beginners](https://github.com/microsoft/ML-For-Beginners/tree/main/sketchnotes), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), non modificata.*

> **Discussione · Un solo numero basta?** — Due filtri riconoscono correttamente 95 messaggi su 100. Il primo blocca molte comunicazioni importanti; il secondo lascia passare più spam. Quale sceglieresti e quali altre informazioni ti servono?

## 6. Che cosa faremo nel corso?

Inizieremo con [Python per il corso](python.html), per prendere confidenza con la sintassi. In **Introduzione al Machine Learning** esploreremo dati su immobili, costruiremo alberi decisionali e valuteremo le previsioni su dati separati. Poi in **Introduzione al Deep Learning** passeremo dai singoli neuroni alle reti, osservando come vengono addestrate e come si controlla l'overfitting.

Non serve ricordare subito tutti i termini: incontrerai ogni concetto nei notebook e negli esercizi. L'obiettivo è imparare a porre domande e verificare le risposte con i dati.

## Mettiti alla prova

1. Spiega con parole tue la differenza tra una regola scritta a mano e un modello addestrato su esempi.
2. Inserisci IA, machine learning e deep learning in una mappa. Dove collocheresti un'applicazione generativa?
3. Perché una buona prestazione sugli esempi di addestramento non basta a dimostrare che il modello funzionerà su nuove case?
4. Scegli un'applicazione dell'IA che conosci: quali dati potrebbe usare e quale errore potrebbe commettere?

<details markdown="1">
<summary>Spunti per verificare le risposte</summary>

1. Una regola è specificata direttamente; nell'apprendimento automatico l'algoritmo costruisce un modello usando dati. I sistemi reali possono combinare entrambi.
2. Il deep learning è una famiglia di metodi di ML, a sua volta parte dell'IA. Molte applicazioni generative attuali usano deep learning, ma «generativa» indica il compito.
3. Il modello potrebbe adattarsi troppo agli esempi visti; occorre valutarlo anche su esempi separati e rappresentativi.
4. Le risposte dipendono dall'applicazione: distingui dati realmente noti da ipotesi e considera le conseguenze per le persone.

</details>

## Le lezioni Microsoft complete

Per non perdere le spiegazioni, le attività e i riferimenti del materiale che ha ispirato questa introduzione, puoi leggere anche le due lezioni complete: [Introduzione al machine learning](microsoft-intro-ml.html) e [Storia del machine learning](microsoft-storia-ml.html). Le note AI Lab distinguono il percorso originale dal nostro e segnalano punti da leggere criticamente.

## Fonti e approfondimenti

Questa pagina è un percorso originale AI Lab, ispirato nella scelta di temi e attività alle lezioni [Introduction to machine learning](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/1-intro-to-ML/README.md) e [History of machine learning](https://github.com/microsoft/ML-For-Beginners/blob/main/1-Introduction/2-history-of-ML/README.md) del progetto Microsoft *ML for Beginners*. La figura è riprodotta dal repository; attribuzione e licenza sono riportate sotto l'immagine. Le altre fonti sono collegate per consultazione.

- [Elements of AI](https://www.elementsofai.com/): corso gratuito introduttivo, disponibile anche in italiano.
- [MOOCs for AI · Politecnico di Milano](https://www.pok.polimi.it/moocs4ai): percorsi di approfondimento su tecnologie e impatto dell'IA.
- [UNESCO · AI competency framework for students](https://www.unesco.org/en/articles/ai-competency-framework-students): quadro delle competenze, in inglese e altre lingue.

**Prossimo passo:** [Python per il corso →](python.html)
