"""Course metadata authored for AI Lab; source order comes from Kaggle metadata."""
TRACKS = {
    'machine_learning': {
        'title': 'Introduzione al Machine Learning', 'short': 'Machine Learning',
        'topics': [
            ('Come funzionano i modelli', 'Descrivere training, previsione e foglie di un albero.'),
            ('Esplorare i dati con pandas', 'Caricare un CSV e interpretare media, dispersione e percentili.'),
            ('Il primo modello', 'Distinguere feature e target; usare fit e predict.'),
            ('Validare un modello', 'Separare training e validazione e calcolare il MAE.'),
            ('Underfitting e overfitting', 'Confrontare la complessità degli alberi sul validation set.'),
            ('Random forest', 'Combinare più alberi e confrontare il MAE con la baseline.'),
            ('Competizioni di Machine Learning', 'Generare un CSV di previsioni e comprenderne la valutazione.'),
            ('AutoML: documento storico', 'Riconoscere le fasi automatizzabili e i vincoli dei servizi cloud.'),
            ('Primi passi con Titanic', 'Seguire un flusso completo di classificazione tabellare.'),
            ('Classificazione e probabilità', 'Leggere accuracy, matrice di confusione e probabilità.'),
        ],
        'lab': '01-primi-modelli',
    },
    'deep_learning_intro': {
        'title': 'Introduzione al Deep Learning', 'short': 'Deep Learning',
        'topics': [
            ('Un singolo neurone', 'Calcolare una combinazione lineare e definire ingressi e uscite.'),
            ('Reti neurali profonde', 'Combinare layer Dense e attivazioni ReLU.'),
            ('Discesa stocastica del gradiente', 'Distinguere loss, optimizer, batch, epoche e learning rate.'),
            ('Capacità ed early stopping', 'Interpretare learning curve e limitare l’overfitting.'),
            ('Dropout e batch normalization', 'Spiegare regolarizzazione e stabilità del training.'),
            ('Classificazione binaria', 'Usare sigmoid, cross-entropy e una soglia di decisione.'),
            ('Bosone di Higgs e TPU', 'Leggere una pipeline distribuita e una rete Wide and Deep.'),
        ],
        'lab': '04-reti-neurali',
    },
    'deep_learning': {
        'title': 'Archivio: Deep Learning e computer vision', 'short': 'Archivio computer vision',
        'topics': [
            ('Introduzione alle convoluzioni', 'Interpretare un filtro applicato a un’immagine.'),
            ('Combinare convoluzioni', 'Descrivere come i filtri formano gerarchie di rappresentazioni.'),
            ('Programmare con TensorFlow e Keras', 'Applicare e confrontare modelli preaddestrati.'),
            ('Transfer learning', 'Riutilizzare una rete per un nuovo problema.'),
            ('Data augmentation', 'Scegliere trasformazioni che preservano l’etichetta.'),
            ('Come apprende una rete', 'Collegare SGD, gradienti e backpropagation.'),
            ('Reti da zero', 'Definire una rete convoluzionale per piccole immagini.'),
            ('Dropout e stride', 'Confrontare memoria, velocità e generalizzazione.'),
            ('Classificare fiori con TPU', 'Studiare una pipeline multiclasse distribuita.'),
        ],
        'lab': '05-tensorflow',
    },
}
