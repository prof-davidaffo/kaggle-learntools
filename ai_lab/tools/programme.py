"""Generate the eight meetings from the maintained teaching plan."""
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1]/'content/school'
MEETINGS = [{'title': 'AI e primi modelli',
  'notebook': '01-primi-modelli',
  'objectives': 'Distinguere programmazione tradizionale e apprendimento dai dati; riconoscere feature, '
                'target, training e previsione.',
  'lessons': [('machine_learning/tut1', 'Come funzionano i modelli'),
              ('machine_learning/tut2', 'Esplorazione dei dati'),
              ('machine_learning/tut3', 'Il primo modello')],
  'schedule': [(15,
                'Confronto iniziale: che cosa significa imparare dai dati? Formulare una previsione e una '
                'regola scritta a mano.'),
               (20, 'Leggere insieme un albero e identificare feature, target e foglie.'),
               (15,
                'Aprire i notebook tradotti, caricare Iowa e controllare statistiche e nomi delle colonne.'),
               (45,
                'Completare ex2 ed ex3: scegliere feature e target, addestrare l’albero e produrre '
                'previsioni.'),
               (15, 'Confrontare con la media dei prezzi e spiegare un errore.'),
               (10, 'Salvare il notebook e scrivere tre righe nel diario.')],
  'exercises': 'Completa ex2 ed ex3 con i dati Iowa originali: carica home_data, seleziona y e X, crea '
               'iowa_model ed esegui predict. Se il tempo è limitato, riprendi le ultime domande all’inizio '
               'del secondo incontro.',
  'result': 'Un notebook eseguito e una previsione commentata. Lo studente sa indicare da quali dati ha '
            'appreso il modello.',
  'extra': 'Approfondisci la descrizione delle colonne Iowa e interpreta percentili, valori mancanti ed età '
           'degli immobili.'},
 {'title': 'Dataset, training e validazione',
  'notebook': '02-validazione',
  'objectives': 'Calcolare il MAE, distinguere training/validazione/test e spiegare perché un risultato sul '
                'training può ingannare.',
  'lessons': [('machine_learning/tut4', 'Validazione'),
              ('machine_learning/tut5', 'Underfitting e overfitting')],
  'schedule': [(10, 'Riprendere le previsioni del primo incontro.'),
               (20, 'Esempio delle porte verdi e discussione sulle correlazioni casuali.'),
               (20, 'Leggere train_test_split e mean_absolute_error nei notebook originali.'),
               (45, 'Confrontare cinque profondità su training e validazione, compilando una tabella.'),
               (15,
                'Scegliere la dimensione usando la validazione e discutere con il docente come riservare un '
                'test indipendente aggiuntivo.'),
               (10, 'Confrontare in coppia e registrare i limiti.')],
  'exercises': 'Completa ex4 sullo split e sul MAE. In ex5 confronta le dimensioni dell’albero usando la '
               'validazione. Discuti con il docente la distinzione fra la procedura originale e un test '
               'indipendente aggiuntivo.',
  'result': 'Una tabella degli errori, una scelta motivata della dimensione dell’albero e una spiegazione '
            'del ruolo di un test indipendente.',
  'extra': 'Confronta un secondo split e discuti perché più prove sullo stesso validation set possono '
           'orientare le scelte verso quel campione.'},
 {'title': 'Migliorare e confrontare i modelli',
  'notebook': '03-confronto-modelli',
  'objectives': 'Confrontare baseline, albero ed ensemble con la stessa metrica; variare un solo parametro '
                'per volta.',
  'lessons': [('machine_learning/tut6', 'Random forest'),
              ('machine_learning/tut8', 'Classificazione e probabilità')],
  'schedule': [(15, 'Ripasso di generalizzazione e baseline.'),
               (20, 'Come combinare più alberi; differenza fra regressione e classificazione.'),
               (50,
                'Completare ex6 sui dati Iowa, confrontare il MAE con il precedente albero e provare un '
                'parametro della random forest.'),
               (15, 'Leggere una matrice di confusione e discutere classi sbilanciate.'),
               (10, 'Confrontare risultati senza pretendere che l’ensemble vinca sempre.'),
               (10, 'Scrivere una breve conclusione nel diario.')],
  'exercises': 'Completa ex6 e confronta la random forest con l’albero di ex5 sulla stessa validazione. '
               'Studia la matrice di confusione di tut8 come introduzione alla classificazione; l’esercizio '
               'pulsar è facoltativo e richiede una fonte dati da verificare.',
  'result': 'Un confronto riproducibile fra almeno tre configurazioni e una spiegazione del compromesso '
            'tempo/qualità.',
  'extra': 'Prova ex7 per generare il CSV di invio; competizioni e Titanic sono approfondimenti '
           'facoltativi.'},
 {'title': 'Introduzione alle reti neurali',
  'notebook': '04-reti-neurali',
  'objectives': 'Riconoscere pesi, bias, layer e attivazioni; definire modelli Keras per i dataset originali '
                'Red Wine e Concrete.',
  'lessons': [('deep_learning_intro/tut1', 'Un neurone'),
              ('deep_learning_intro/tut2', 'Reti profonde'),
              ('deep_learning_intro/tut3', 'SGD')],
  'schedule': [(15, 'Calcolare a mano y = wx + b.'),
               (20, 'Perché servono attivazioni non lineari? Disegnare il problema dei quadranti.'),
               (20, 'Esaminare Red Wine in ex1: forma degli ingressi, target e pesi.'),
               (40,
                'Completare ex1 ed ex2: unità lineare e rete densa per Concrete; esplorare ReLU e le altre '
                'attivazioni.'),
               (15,
                'Confrontare numero di ingressi, strati e uscite; anticipare loss e training del prossimo '
                'incontro.'),
               (10, 'Salvare risultati e domande per Keras.')],
  'exercises': 'Completa input_shape, modello lineare e lettura dei pesi in ex1; definisci i layer nascosti '
               'e separa le attivazioni in ex2. Il laboratorio NumPy è un approfondimento facoltativo.',
  'result': 'Due architetture Keras definite sui dataset originali e una spiegazione di ingressi, pesi e '
            'attivazioni.',
  'extra': 'Studia le derivate di tanh e sigmoid; confronta ReLU e tanh a livello concettuale.'},
 {'title': 'Deep Learning con TensorFlow e Keras',
  'notebook': '05-tensorflow',
  'objectives': 'Collegare Input, Dense, compile e fit; usare early stopping e riconoscere lo scopo di '
                'dropout e batch normalization.',
  'lessons': [('deep_learning_intro/tut3', 'Training con Keras'),
              ('deep_learning_intro/tut4', 'Early stopping'),
              ('deep_learning_intro/tut5', 'Dropout e batch normalization'),
              ('deep_learning_intro/tut6', 'Classificazione binaria')],
  'schedule': [(15, 'Riprendere la rete definita nel quarto incontro e spiegare pesi e attivazioni.'),
               (20,
                'Definire loss MAE e optimizer Adam per Fuel Economy; distinguere regressione e '
                'classificazione.'),
               (40, 'Completare compile e fit di ex3 e leggere la curva della loss.'),
               (20, 'Riprendere Spotify in ex4 e aggiungere EarlyStopping con i parametri richiesti.'),
               (15, 'Discutere curve di training e validazione e consultare i risultati dell’esempio.'),
               (10, 'Salvare i notebook e annotare quale configurazione si intende confrontare.')],
  'exercises': 'Completa compile e fit in ex3 usando Fuel Economy. In ex4 aggiungi EarlyStopping per '
               'Spotify. Se il tempo non basta, le domande sulle curve diventano attività da concludere '
               'prima dell’incontro 6. Dropout, batch normalization e classificazione binaria restano '
               'letture/approfondimenti accessibili nel corso completo.',
  'result': 'Una rete addestrata sui dati originali, con curve di training e validazione e callback di '
            'arresto anticipato.',
  'extra': 'Prova batch normalization e confronta la stabilità; non sono richieste TPU o GPU.'},
 {'title': 'Scegliere il progetto e preparare i dati',
  'notebook': '06-preparare-progetto',
  'objectives': 'Definire una domanda realistica, documentare origine/licenza dei dati e progettare un '
                'protocollo senza leakage.',
  'lessons': [('machine_learning/tut4', 'Validazione'),
              ('deep_learning_intro/tut6', 'Classificazione binaria')],
  'schedule': [(15, 'Presentare le proposte e i livelli di difficoltà.'),
               (20, 'Scegliere il problema e definire target, feature, metrica e baseline.'),
               (20, 'Controllare dati, permessi, duplicati, valori mancanti e classi.'),
               (40, 'Eseguire lo starter, separare gli split e controllarne le distribuzioni.'),
               (15, 'Scrivere la scheda e concordare una consegna minima.'),
               (10, 'Breve confronto con il docente.')],
  'exercises': 'Completa una scheda con problema, utente, dati, licenza, target, feature, baseline, metrica, '
               'split e due rischi. Se i dati personali non sono necessari, non raccoglierli.',
  'result': 'Una scheda approvata didatticamente e un notebook che carica o genera i dati e li divide '
            'correttamente.',
  'extra': 'Raccogli esempi aggiuntivi autorizzati oppure indaga gli errori di etichettatura.'},
 {'title': 'Addestrare il modello e usarlo',
  'notebook': '07-progetto-riferimento',
  'objectives': 'Eseguire un flusso completo: preprocessing sul training, training, baseline, valutazione e '
                'uso su un nuovo esempio.',
  'lessons': [('machine_learning/tut3', 'Fit e predict'),
              ('deep_learning_intro/tut6', 'Probabilità e soglie')],
  'schedule': [(15, 'Controllare la scheda e il protocollo.'),
               (35, 'Addestrare una baseline e il modello scelto.'),
               (25, 'Confrontare sulla validazione e scegliere una sola modifica.'),
               (25, 'Valutare il modello finale sul test e salvarlo con il preprocessing.'),
               (10, 'Provare una previsione da un piccolo modulo o interfaccia.'),
               (10, 'Documentare un errore e il risultato ottenuto.')],
  'exercises': 'Conserva almeno due esperimenti e la baseline. Salva modello, ordine delle feature e '
               'preprocessing. Nel progetto Iowa controlla che la pipeline ricaricata produca la stessa '
               'previsione.',
  'result': 'Un modello salvato, una previsione riproducibile e una piccola dimostrazione sui dati del '
            'progetto scelto.',
  'extra': 'Aggiungi una UI Gradio su un computer con Python; l’interfaccia statica del riferimento '
           'sintetico è un esempio aggiuntivo.'},
 {'title': 'Completare e presentare i progetti',
  'notebook': '08-presentazione',
  'objectives': 'Verificare la riproducibilità, comunicare risultati e limiti e distinguere una '
                'dimostrazione da un prodotto validato.',
  'lessons': [],
  'schedule': [(15, 'Riavviare il kernel e verificare la consegna dall’inizio.'),
               (20, 'Completare relazione, tabella esperimenti e indicazioni sui dati.'),
               (15, 'Preparare una dimostrazione e una previsione su un caso nuovo.'),
               (50,
                'Presentazioni: massimo otto gruppi da cinque minuti più transizioni; con più gruppi usare '
                'poster e dimostrazioni a rotazione.'),
               (15, 'Confronto collettivo e domande su errori e generalizzazione.'),
               (5, 'Consegna finale e autovalutazione.')],
  'exercises': 'Consegna notebook eseguito, dati o istruzioni per ottenerli, licenze, modello e relazione '
               'breve. Presenta baseline, risultato, un errore e una possibile estensione.',
  'result': 'Un progetto leggibile e riproducibile con una dimostrazione funzionante nel proprio ambiente.',
  'extra': 'Pianifica un esperimento successivo senza riutilizzare il test come validazione.'}]


def generate():
    primary = {
        1: ('machine_learning', ['tut2','ex2','tut3','ex3'], 'Melbourne e Iowa'),
        2: ('machine_learning', ['tut4','ex4','tut5','ex5'], 'Melbourne e Iowa'),
        3: ('machine_learning', ['tut6','ex6'], 'Melbourne e Iowa'),
        4: ('deep_learning_intro', ['tut1','ex1','tut2','ex2'], 'DL Course Data: red-wine e concrete'),
        5: ('deep_learning_intro', ['tut3','ex3','tut4','ex4'], 'DL Course Data: red-wine, fuel e spotify'),
    }
    for number, meeting in enumerate(MEETINGS,1):
        assert sum(minutes for minutes,_ in meeting['schedule']) == 120
        links = '\n'.join(f'- [{title}](corsi/{path}.html)' for path,title in meeting['lessons'])
        if not links:
            links = 'Rileggi la guida al tuo progetto e il diario degli esperimenti.'
        agenda = '\n'.join(f'| {minutes} min | {task} |' for minutes,task in meeting['schedule'])
        if number in primary:
            track, notebooks, data = primary[number]
            primary_text = '\n'.join(f'- [Notebook originale tradotto: {name}](notebooks/{track}-{name}.ipynb)' for name in notebooks)
            notebook_section = f'**Materiale principale: notebook Kaggle tradotti, con dati originali.** Dataset: {data}. Preparali prima dell’incontro con la [guida ai dataset](dataset.html). Usa i tutorial come riferimento e completa gli esercizi indicati.\n\n{primary_text}\n\nIl notebook aggiuntivo [{meeting["notebook"]}](notebooks/{meeting["notebook"]}.ipynb) è un supporto facoltativo per visualizzare i concetti, non un sostituto dei dati e degli esercizi Kaggle.'
        else:
            notebook_section = 'Usa lo starter del [progetto scelto](progetti.html), con preferenza per il [progetto Iowa](progetto-iowa.html) se vuoi restare sui dati del corso. I notebook aggiuntivi di preparazione e presentazione sono strumenti di supporto.'
        text = f'''# Incontro {number} · {meeting['title']}

**Durata: 120 minuti.** Programma originale AI Lab. [Torna agli otto incontri](percorso.html).

## Obiettivi

{meeting['objectives']}

## Contenuti da consultare

{links}

## Notebook e ambiente

{notebook_section}

## Lavoro nelle due ore

| Tempo | Attività |
| --- | --- |
{agenda}

## Esercizi da completare

{meeting['exercises']}

## Risultato pratico atteso

{meeting['result']}

## Approfondimento facoltativo

{meeting['extra']}
'''
        (CONTENT/f'incontro-{number}.md').write_text(text)
    print('Generated eight meetings, 120 minutes each.')


if __name__ == '__main__':
    generate()
