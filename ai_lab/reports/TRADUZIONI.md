# Revisione della traduzione Kaggle

Il confronto è stato eseguito sui notebook originali in `notebooks/<corso>/raw`, al commit Kaggle `e9ba66dc899d3e17b80d3a1b9a5d29f430d310cb` registrato nell’inventario. Non è un confronto con eventuali revisioni successive del sito Kaggle.

La precedente versione italiana conteneva sintesi: la presenza di tutte le chiavi di traduzione non garantiva la conservazione dei contenuti. Sono state ritradotte tutte le 307 celle Markdown, leggendo le celle inglesi complete, inclusi materiali aggiuntivi e archivio storico.

| Materiali | Notebook | Celle Markdown | Parole originali | Italiano precedente | Italiano revisionato |
| --- | ---: | ---: | ---: | ---: | ---: |
| Machine Learning | 18 | 99 | 9429 | 5271 | 8404 |
| Intro to Deep Learning | 13 | 91 | 8491 | 4325 | 7843 |
| Archivio Deep Learning | 16 | 117 | 4917 | 2727 | 4259 |

I conteggi escludono blocchi di codice, tag HTML e URL. Servono a documentare l’entità della precedente riduzione, non a dimostrare equivalenza semantica tra lingue.

## Contenuti ripristinati

- Spiegazioni e passaggi argomentativi, compresi il caso delle porte verdi nella validazione, la crescita delle foglie dell’albero e il confronto tra errori di training e validazione.
- Esempi numerici, domande di riflessione, attività facoltative, tabelle di esperimenti e consegne complete.
- Figure nella posizione originale, didascalie e riquadri, compresi il diagramma ReLU e le spiegazioni di SGD, capacità, dropout e batch normalization.
- Istruzioni complete per gli invii, anche quelle prodotte dalla macro `SUBMIT_TO_COMP`, precedentemente abbreviata dal generatore.

Le note su AI Lab, Colab e materiali storici sono separate dalla traduzione. Le istruzioni sulle interfacce, le tariffe e i servizi esterni restano quelle della versione sorgente e non costituiscono una verifica del loro stato attuale. I video esterni non sono tradotti. Il capitolo Python aggiuntivo resta materiale originale AI Lab.

## Verifiche

La build e il controllo del sito passano: 63 pagine, 60 notebook, 26 copie Colab e pacchetto studenti. Gli hash degli originali Kaggle sono invariati. Il codice eseguibile delle 25 copie Colab Kaggle è identico alla versione precedente.

`tools/translation_checks.py`, eseguito dalla build, verifica per cella link, immagini inserite nel testo, macro, gerarchia dei titoli e token dei blocchi di codice, escludendo i commenti traducibili. Segnala inoltre riduzioni rilevanti del testo. Sono state simulate quattro regressioni: immagine trasformata in semplice link, esempio di codice alterato, macro rimossa e spiegazione sostituita da un riassunto. Tutte vengono rilevate.

Il rapporto dettagliato è `translation-checks.json`. Questi controlli strutturali integrano la revisione bilingue, non la sostituiscono. Nessuna pubblicazione remota è stata eseguita.
