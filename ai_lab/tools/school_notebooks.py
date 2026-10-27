"""Generate self-contained notebooks authored for the school programme."""
import json
from pathlib import Path
import textwrap

LAB = Path(__file__).resolve().parents[1]


def md(source):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': source.strip()+'\n'}


def code(source):
    return {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [],
            'source': textwrap.dedent(source).strip()+'\n'}


def write(name, title, cells, dependencies=()):
    notebook = {'nbformat':4, 'nbformat_minor':5, 'metadata': {
        'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python'},
        'ai_lab':{'origin':'AI Lab — materiale originale scolastico', 'license':'Apache-2.0',
                  'dependencies':list(dependencies)}},
        'cells':[md(f'# {title}\n\nMateriale originale **AI Lab**, non una lezione Kaggle. Codice in inglese; attività e spiegazioni in italiano.\n\nEsegui le celle in ordine con **Maiusc + Invio**. Salva una copia prima di modificare il codice.')]+cells}
    for index, cell in enumerate(notebook['cells']):
        cell['id'] = f'ai-lab-{index}'
    (LAB/'notebooks'/f'{name}.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n')


REGRESSION_DATA = '''
import random
from statistics import mean

rng = random.Random(42)
rows = []
for _ in range(240):
    area = rng.uniform(30, 180)
    rooms = rng.randint(1, 6)
    price = 40000 + 1800 * area + 10000 * rooms + rng.gauss(0, 16000)
    rows.append(([area, rooms], price))
rng.shuffle(rows)
train_rows = rows[:144]
valid_rows = rows[144:192]
test_rows = rows[192:]
assert len(train_rows) + len(valid_rows) + len(test_rows) == len(rows)
print('Training / validation / test:', len(train_rows), len(valid_rows), len(test_rows))
'''
TREE = '''
def fit_tree(data, depth=0, max_depth=3):
    targets = [target for _, target in data]
    if depth >= max_depth or len(data) < 8:
        return mean(targets)
    best = None
    for feature in range(len(data[0][0])):
        values = sorted(set(features[feature] for features, _ in data))
        step = max(1, len(values) // 16)
        for threshold in values[1::step]:
            left = [row for row in data if row[0][feature] <= threshold]
            right = [row for row in data if row[0][feature] > threshold]
            if not left or not right:
                continue
            left_mean = mean(target for _, target in left)
            right_mean = mean(target for _, target in right)
            loss = sum((target - left_mean) ** 2 for _, target in left)
            loss += sum((target - right_mean) ** 2 for _, target in right)
            if best is None or loss < best[0]:
                best = (loss, feature, threshold, left, right)
    if best is None:
        return mean(targets)
    _, feature, threshold, left, right = best
    return (feature, threshold, fit_tree(left, depth+1, max_depth),
            fit_tree(right, depth+1, max_depth))


def predict_tree(model, features):
    if isinstance(model, (float, int)):
        return float(model)
    feature, threshold, left, right = model
    return predict_tree(left if features[feature] <= threshold else right, features)


def mae(model, data):
    return mean(abs(target - predict_tree(model, features)) for features, target in data)
'''
FLOWER_DATA = '''
import csv
import json
import math
import random
from pathlib import Path
from statistics import mean, pstdev

rng = random.Random(27)
rows = []
for index in range(600):
    label = index % 2
    length = min(9.5, max(0.5, rng.gauss(3.0 + 3.5 * label, 1.0)))
    width = min(5.0, max(0.2, rng.gauss(1.0 + 1.5 * label, 0.65)))
    rows.append(([length, width], label))
rng.shuffle(rows)
train_rows, valid_rows, test_rows = rows[:360], rows[360:480], rows[480:]
feature_mean = [mean(row[0][j] for row in train_rows) for j in range(2)]
feature_scale = [pstdev(row[0][j] for row in train_rows) for j in range(2)]


def transform(features):
    return [(value - center) / scale for value, center, scale in
            zip(features, feature_mean, feature_scale)]


def sigmoid(value):
    return 1 / (1 + math.exp(-max(-40, min(40, value))))

print('Synthetic examples:', len(rows), 'Features:', ['length', 'width'])
'''
FLOWER_TRAIN = '''
weights = [0.0, 0.0]
bias = 0.0
learning_rate = 0.15
loss_history = []
for epoch in range(350):
    gradient = [0.0, 0.0]
    bias_gradient = 0.0
    epoch_loss = 0.0
    for features, label in train_rows:
        scaled = transform(features)
        probability = sigmoid(sum(w*x for w, x in zip(weights, scaled)) + bias)
        error = probability - label
        for j in range(2):
            gradient[j] += error * scaled[j]
        bias_gradient += error
        clipped = min(1-1e-12, max(1e-12, probability))
        epoch_loss -= label*math.log(clipped) + (1-label)*math.log(1-clipped)
    weights = [w-learning_rate*g/len(train_rows) for w,g in zip(weights,gradient)]
    bias -= learning_rate*bias_gradient/len(train_rows)
    loss_history.append(epoch_loss/len(train_rows))
assert loss_history[-1] < loss_history[0]
print('Cross-entropy:', round(loss_history[0],4), '->', round(loss_history[-1],4))


def predict_probability(features):
    return sigmoid(sum(w*x for w, x in zip(weights, transform(features))) + bias)


def evaluate(data, threshold=0.5):
    matrix = [[0, 0], [0, 0]]
    for features, label in data:
        prediction = int(predict_probability(features) >= threshold)
        matrix[label][prediction] += 1
    accuracy = (matrix[0][0] + matrix[1][1]) / len(data)
    return accuracy, matrix

validation_accuracy, validation_matrix = evaluate(valid_rows)
print('Validation accuracy:', validation_accuracy)
print('Validation confusion matrix:', validation_matrix)
'''
FLOWER_TEST = '''
# Use the test set only after the modelling decisions are complete.
test_accuracy, test_matrix = evaluate(test_rows)
majority_label = int(mean(label for _, label in train_rows) >= 0.5)
baseline_accuracy = mean(label == majority_label for _, label in test_rows)
print('Baseline test accuracy:', baseline_accuracy)
print('Model test accuracy:', test_accuracy)
print('Test confusion matrix (rows=true, columns=predicted):', test_matrix)
assert test_accuracy > baseline_accuracy
assert test_accuracy >= 0.85
assert all(math.isfinite(value) for value in weights + [bias])
'''
FLOWER_EXPORT = '''
artifact = {
    'model_type': 'logistic_regression',
    'dataset': 'AI Lab synthetic flowers, seed 27, 600 samples',
    'features': ['length', 'width'], 'classes': ['alpha', 'beta'],
    'mean': feature_mean, 'scale': feature_scale,
    'weights': weights, 'bias': bias, 'threshold': 0.5,
    'test_accuracy': test_accuracy, 'baseline_accuracy': baseline_accuracy,
    'test_confusion_matrix': test_matrix,
    'train_size': len(train_rows), 'validation_size': len(valid_rows), 'test_size': len(test_rows),
}
Path('reference-model.json').write_text(json.dumps(artifact, indent=2)+'\\n')
with Path('synthetic-flowers.csv').open('w', newline='') as stream:
    writer = csv.writer(stream)
    writer.writerow(['length', 'width', 'label'])
    for features, label in rows:
        writer.writerow(features + [label])
print('Saved reference-model.json and synthetic-flowers.csv')
print('New example probability:', predict_probability([5.0, 2.0]))
'''
XOR_DATA = '''
import numpy as np

rng = np.random.default_rng(42)
features = rng.uniform(-1, 1, (800, 2)).astype('float32')
targets = ((features[:, 0] * features[:, 1]) > 0).astype('float32').reshape(-1, 1)
order = rng.permutation(len(features))
features, targets = features[order], targets[order]
X_train, X_valid, X_test = features[:480], features[480:640], features[640:]
y_train, y_valid, y_test = targets[:480], targets[480:640], targets[640:]
assert not np.isnan(features).any()
print('Training shape:', X_train.shape, 'Target shape:', y_train.shape)
'''
MLP = '''
# Two hidden layers learn a nonlinear XOR-like rule.
W1 = rng.normal(0, 0.5, (2, 16))
b1 = np.zeros((1, 16))
W2 = rng.normal(0, 0.3, (16, 8))
b2 = np.zeros((1, 8))
W3 = rng.normal(0, 0.3, (8, 1))
b3 = np.zeros((1, 1))
parameters = [W1, b1, W2, b2, W3, b3]
learning_rate = 0.15
batch_size = 32
history = []
best_loss = float('inf')
best_parameters = [value.copy() for value in parameters]
wait = 0


def forward(X):
    hidden1 = np.tanh(X @ W1 + b1)
    hidden2 = np.tanh(hidden1 @ W2 + b2)
    probabilities = 1 / (1 + np.exp(-np.clip(hidden2 @ W3 + b3, -40, 40)))
    return hidden1, hidden2, probabilities


def cross_entropy(actual, predicted):
    p = np.clip(predicted, 1e-8, 1-1e-8)
    return float(-np.mean(actual*np.log(p) + (1-actual)*np.log(1-p)))


for epoch in range(400):
    permutation = rng.permutation(len(X_train))
    for start in range(0, len(X_train), batch_size):
        selection = permutation[start:start+batch_size]
        X, y = X_train[selection], y_train[selection]
        h1, h2, probability = forward(X)
        d3 = (probability-y) / len(X)
        d2 = (d3 @ W3.T) * (1-h2*h2)
        d1 = (d2 @ W2.T) * (1-h1*h1)
        gradients = [X.T @ d1, d1.sum(axis=0, keepdims=True),
                     h1.T @ d2, d2.sum(axis=0, keepdims=True),
                     h2.T @ d3, d3.sum(axis=0, keepdims=True)]
        for parameter, gradient in zip(parameters, gradients):
            parameter -= learning_rate * gradient
    train_loss = cross_entropy(y_train, forward(X_train)[2])
    valid_loss = cross_entropy(y_valid, forward(X_valid)[2])
    history.append([train_loss, valid_loss])
    if valid_loss < best_loss - 0.0001:
        best_loss = valid_loss
        best_parameters = [value.copy() for value in parameters]
        wait = 0
    else:
        wait += 1
    if wait >= 25:
        break
for parameter, best in zip(parameters, best_parameters):
    parameter[:] = best
accuracy = float(np.mean((forward(X_test)[2] >= 0.5) == y_test))
assert np.isfinite(history).all()
assert history[-1][0] < history[0][0]
assert accuracy >= 0.85
print('Epochs:', len(history), 'Test accuracy:', accuracy)
print('Initial / final training loss:', history[0][0], history[-1][0])
'''


def generate():
    (LAB/'notebooks').mkdir(exist_ok=True)
    write('progetto-iowa', 'Progetto: prezzi delle case Iowa', [
        md('## Dati e obiettivo\nProgetto originale AI Lab basato sui dati **Home Data for ML Course** usati dagli esercizi Kaggle. Non genera dati sostitutivi. Scarica il dataset con la guida del sito. L’obiettivo è confrontare una baseline con una random forest e salvare una previsione riproducibile. Richiede pandas e scikit-learn; il codice è predisposto ma non eseguito in questa sessione.'),
        code('from pathlib import Path\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_absolute_error\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.ensemble import RandomForestRegressor\nimport joblib\n\nproject_root = next((path for path in [Path.cwd(), *Path.cwd().parents] if (path / "ai_lab/datasets.json").is_file()), None)\nif project_root is None:\n    raise FileNotFoundError("Open this notebook inside the extracted student bundle or repository.")\ndata_path = project_root / "ai_lab/input/home-data-for-ml-course/train.csv"\nif not data_path.is_file():\n    raise FileNotFoundError("Download the original Iowa dataset using the AI Lab data guide.")\nhome_data = pd.read_csv(data_path)\nfeatures = ["LotArea", "YearBuilt", "1stFlrSF", "2ndFlrSF", "FullBath", "BedroomAbvGr", "TotRmsAbvGrd"]\nX, y = home_data[features], home_data["SalePrice"]\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nX_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.25, random_state=42)\nprint("Training / validation / test:", len(X_train), len(X_valid), len(X_test))'),
        md('## Training e scelta\nL’imputazione delle feature viene appresa dentro la pipeline solo sui dati di training. Confronta la baseline e la random forest sulla validazione. Scegli i parametri qui, senza leggere il test.'),
        code('baseline_prediction = float(y_train.mean())\nprint("Baseline validation MAE:", mean_absolute_error(y_valid, [baseline_prediction]*len(y_valid)))\nmodel = make_pipeline(SimpleImputer(strategy="median"), RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=1))\nmodel.fit(X_train, y_train)\nprint("Model validation MAE:", mean_absolute_error(y_valid, model.predict(X_valid)))'),
        md('## Valutazione finale ed esportazione\nEsegui solo dopo aver concluso le scelte. Il salvataggio include preprocessing e ordine delle feature. Carica con joblib soltanto artefatti fidati.'),
        code('print("Final test MAE:", mean_absolute_error(y_test, model.predict(X_test)))\nartifact = {"model": model, "features": features, "target": "SalePrice"}\njoblib.dump(artifact, "iowa-model.joblib")\nrestored = joblib.load("iowa-model.joblib")\nsample = X_test.iloc[:1]\nprint("New prediction:", restored["model"].predict(sample))\nassert abs(float(restored["model"].predict(sample)[0])-float(model.predict(sample)[0])) < 1e-8'),
        md('## Attività\nConfronta un albero e una random forest. Registra due configurazioni sulla validazione; esamina gli immobili con errori maggiori. Non dichiarare prestazioni su altre città senza nuovi dati.\n\n## Interfaccia\nUn modulo con i sette valori delle feature può richiamare la pipeline salvata tramite Gradio su un runtime Python esterno a GitHub Pages. Il modello non viene eseguito automaticamente dal sito statico.')], ['pandas','sklearn'])
    write('01-primi-modelli', 'Primi modelli: un albero per prezzi simulati', [
        md('## Obiettivi e prerequisiti\nConoscere liste, funzioni e cicli. Distinguere feature, target e previsione. I dati immobiliari sono **simulati**: non sono Melbourne o Iowa. Unità monetarie arbitrarie. Nessun download o pacchetto esterno.'),
        code(REGRESSION_DATA),
        md('## Un albero piccolo\nLa funzione cerca divisioni che riducono la somma degli errori quadratici. Una foglia restituisce il prezzo medio. Questo è codice originale scolastico, semplificato rispetto a scikit-learn.'),
        code(TREE), code('model = fit_tree(train_rows, max_depth=3)\nprint("Validation MAE:", mae(model, valid_rows))\nprint("Prediction for area=90, rooms=3:", predict_tree(model, [90, 3]))\nassert mae(model, valid_rows) < mae(mean(target for _, target in train_rows), valid_rows)'),
        md('## Esercizi\n1. Descrivi feature e target.\n2. Cambia la casa da prevedere.\n3. Prova profondità 1 e 5; annota il MAE di validazione.\n\n## Riepilogo\nUn modello apprende dai dati di training e produce previsioni per nuovi esempi. La qualità deve essere confrontata con una baseline.')])
    write('02-validazione','Training, validazione e test',[
        md('## Obiettivo\nCapire perché non misuriamo la qualità soltanto sui dati di training. Conoscere il MAE. Dati simulati, libreria standard Python.'),code(REGRESSION_DATA),code(TREE),
        code('baseline = mean(target for _, target in train_rows)\nprint("Baseline validation MAE:", mae(baseline, valid_rows))\nfor depth in [1, 2, 3, 5, 8]:\n    model = fit_tree(train_rows, max_depth=depth)\n    print(depth, "Training MAE:", mae(model, train_rows), "Validation MAE:", mae(model, valid_rows))'),
        md('## Esercizi\nRegistra i risultati in una tabella. Scegli la profondità usando **solo la validazione**; poi impostala sotto prima dell’ultima valutazione. Ripeti l’esperimento con un altro seed e discuti la variabilità.\n\nUna divisione casuale non basta per dati temporali o per più esempi dello stesso soggetto: in quei casi occorre rispettare tempi e gruppi.'),
        code('chosen_depth = 3\nfinal_model = fit_tree(train_rows, max_depth=chosen_depth)\nprint("Final test MAE:", mae(final_model, test_rows))\nassert len(test_rows) > 0'),
        md('## Riepilogo\nTraining per apprendere, validazione per scegliere, test per una stima finale indipendente. Non modificare il modello in base al test e continuare a chiamarlo indipendente.')])
    write('03-confronto-modelli','Confrontare alberi e un ensemble',[
        md('## Obiettivo\nConfrontare una baseline, un albero e un ensemble. L’ensemble qui usa campioni bootstrap di alberi semplici: è un esperimento scolastico e non riproduce tutte le scelte di RandomForestRegressor.'),code(REGRESSION_DATA),code(TREE),
        code('baseline = mean(target for _, target in train_rows)\ntree = fit_tree(train_rows, max_depth=5)\nforest = [fit_tree(rng.choices(train_rows, k=len(train_rows)), max_depth=5) for _ in range(15)]\n\ndef predict_forest(features):\n    return mean(predict_tree(tree, features) for tree in forest)\n\nforest_mae = mean(abs(target-predict_forest(features)) for features,target in valid_rows)\nprint("Baseline MAE:", mae(baseline, valid_rows))\nprint("Tree MAE:", mae(tree, valid_rows))\nprint("Ensemble MAE:", forest_mae)\nassert forest_mae < mae(baseline, valid_rows)'),
        md('## Esercizi\nConfronta 3, 10 e 30 alberi. Misura anche il tempo con `time.perf_counter`. Cambia un parametro per volta e annota cosa succede. Un ensemble non garantisce sempre il risultato migliore.\n\n## Ponte verso scikit-learn\nNell’ambiente scientifico puoi ripetere il confronto con DecisionTreeRegressor e RandomForestRegressor: ritroverai fit, predict e i concetti delle lezioni tradotte.\n\n## Riepilogo\nLa valutazione comune permette un confronto ragionevole; più complessità non equivale automaticamente a più qualità.')])
    write('04-reti-neurali','Una rete profonda con NumPy',[
        md('## Obiettivi e requisiti\nNumPy installato. Riconoscere neuroni, due strati nascosti, sigmoid, cross-entropy e gradiente. Il problema sintetico assegna classe 1 ai punti nei quadranti con coordinate dello stesso segno: una sola retta non separa le classi. CPU sufficiente.'),code(XOR_DATA),
        md('## Addestramento reale\nLa rete ha due strati nascosti (16 e 8 unità tanh) e un’uscita sigmoid. Il codice applica la backpropagation e minibatch SGD. È materiale originale AI Lab, pensato per vedere i calcoli che Keras automatizza.'),code(MLP),
        md('## Leggere le curve\nOgni riga di `history` contiene loss di training e validazione. Un grafico SVG senza ulteriori dipendenze viene salvato qui sotto.'),
        code('from pathlib import Path\n\npoints = " ".join(f"{20+i*560/max(1,len(history)-1):.2f},{180-150*min(1,row[1]):.2f}" for i,row in enumerate(history))\nsvg = f\'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 210"><rect width="600" height="210" fill="white"/><polyline fill="none" stroke="teal" stroke-width="2" points="{points}"/><text x="20" y="205">Validation cross-entropy by epoch</text></svg>\'\nPath("learning-curve.svg").write_text(svg)\nprint("Saved learning-curve.svg")'),
        md('## Esercizi\n1. Cambia il learning rate a 0.03 e confronta.\n2. Riduci la prima dimensione nascosta e adegua W1, b1 e W2.\n3. Spiega perché separiamo y_valid da y_test.\n4. Individua nel codice la derivata di tanh e l’aggiornamento dei pesi.\n\n## Riepilogo\nLe non linearità permettono una frontiera complessa. Il gradiente aggiorna i pesi e la validazione guida l’arresto.')],['numpy'])
    write('05-tensorflow','La stessa rete con TensorFlow e Keras',[
        md('## Requisiti\nUn ambiente Python compatibile con i pacchetti in `ai_lab/requirements/deep-learning.txt`. Controlla la versione disponibile con `python --version`. CPU sufficiente, nessun dataset remoto. **Esecuzione TensorFlow locale non verificata in questa sessione**: il pacchetto non è disponibile e la rete impedisce di installarlo. Il workflow scientifico è predisposto per verificarla in un ambiente compatibile.'),
        code('import os\nos.environ["TF_NUM_INTRAOP_THREADS"] = "1"\nos.environ["TF_NUM_INTEROP_THREADS"] = "1"\nos.environ["OMP_NUM_THREADS"] = "1"\nimport tensorflow as tf\nfrom tensorflow import keras\nfrom tensorflow.keras import layers\nkeras.utils.set_random_seed(42)'),code(XOR_DATA),
        code('model = keras.Sequential([\n    keras.Input(shape=(2,)),\n    layers.Dense(16, activation="tanh"),\n    layers.Dense(8, activation="tanh"),\n    layers.Dense(1, activation="sigmoid"),\n])\nmodel.compile(optimizer=keras.optimizers.Adam(learning_rate=0.01),\n              loss="binary_crossentropy", metrics=["binary_accuracy"])\noptions = tf.data.Options()\noptions.threading.private_threadpool_size = 1\ntrain_data = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(480, seed=42).batch(32).with_options(options)\nvalid_data = tf.data.Dataset.from_tensor_slices((X_valid, y_valid)).batch(32).with_options(options)\nhistory = model.fit(train_data, validation_data=valid_data, epochs=80,\n                    callbacks=[keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)], verbose=0)\npredictions = model(X_test, training=False).numpy()\naccuracy = float(np.mean((predictions >= 0.5) == y_test))\nprint("Test accuracy:", accuracy)\nassert accuracy >= 0.85\nmodel.save("xor-model.keras")'),
        md('## Esercizi\nConfronta il codice con il laboratorio NumPy. Aggiungi Dropout da 0.1 fra gli strati nascosti, eseguendo nuovamente dall’inizio. Confronta le curve su validazione prima del test.\n\n## Riepilogo\nKeras automatizza gradienti e aggiornamenti. Dati, loss e protocollo di valutazione restano responsabilità di chi progetta il modello.')],['numpy','tensorflow'])
    write('06-preparare-progetto','Preparare un dataset e un protocollo',[
        md('## Obiettivo\nDefinire target, feature, unità e divisione dei dati. Il dataset di riferimento rappresenta due specie **fittizie** di fiori; serve a studiare il processo, non è utilizzabile per botanica reale. Nessuna dipendenza esterna.'),code(FLOWER_DATA),
        code('for name, split in [("train",train_rows),("validation",valid_rows),("test",test_rows)]:\n    print(name, "Count:",len(split),"Positive fraction:",mean(label for _,label in split))\nassert len({id(row) for row in train_rows} & {id(row) for row in test_rows}) == 0\nprint("Scaler fitted on training only:",feature_mean,feature_scale)'),
        md('## Esercizi\nScrivi una scheda con domanda, provenienza, licenza, feature disponibili al momento della previsione, target, metrica e baseline. Identifica dati personali e possibili proxy. Per un tuo CSV considera duplicati e gruppi; non eseguire preprocessing sull’intero dataset prima dello split.\n\n## Risultato\nUn protocollo che permetta di distinguere apprendimento e valutazione finale.')])
    write('07-progetto-riferimento','Progetto completo: classificare fiori simulati',[
        md('## Obiettivi\nRealizzare un modello dall’inizio alla previsione e all’esportazione. **Solo libreria standard Python, nessun account, download o GPU**. Dataset sintetico originale AI Lab, 600 esempi di due specie fittizie alfa/beta con lunghezza e larghezza in unità arbitrarie. Distribuzioni parzialmente sovrapposte.\n\n## Protocollo\n360 esempi per il training, 120 per scegliere configurazione/soglia e 120 per il test finale. La standardizzazione viene stimata solo sul training. Baseline: classe maggioritaria del training.'),code(FLOWER_DATA),
        md('## Addestrare\nUsiamo regressione logistica: due pesi e un bias producono una probabilità mediante sigmoid. Minimizza la cross-entropy con discesa del gradiente. Il classificatore è lineare nello spazio delle feature: non è una rete profonda.'),code(FLOWER_TRAIN),
        md('## Valutare una volta sul test\nPrima di eseguire la cella, concludi la scelta di learning rate, epoche e soglia. L’assert controlla solo una proprietà attesa del dataset sintetico, non sostituisce l’analisi degli errori.'),code(FLOWER_TEST),
        md('## Utilizzare ed esportare\nSalviamo parametri e preprocessing in JSON e i dati sintetici in CSV. Il sito include una piccola interfaccia statica che applica gli stessi pesi in JavaScript, senza server. Rigenerare il modello dal notebook permette di riprodurre il risultato.'),code(FLOWER_EXPORT),
        md('## Esercizi e miglioramenti\n1. Cambia la soglia usando solo la validazione e confronta falsi positivi e negativi.\n2. Aumenta il rumore nei dati e registra il cambiamento.\n3. Sostituisci i dati sintetici con un dataset documentato e autorizzato.\n4. Confronta una baseline e un albero.\n\n## Interfaccia facoltativa con Gradio\nGradio richiede un processo Python, quindi funziona localmente o in un ambiente notebook compatibile; non direttamente su GitHub Pages. Non viene installato automaticamente né presentato come verificato. La funzione da esporre è `predict_probability` con due ingressi numerici.\n\n## Riepilogo\nIl progetto comprende dati, split, preprocessing, training, baseline, valutazione, singola previsione ed esportazione. Le prestazioni riguardano solo il problema simulato.')])
    write('08-presentazione','Verificare e presentare il progetto',[
        md('## Preparazione\nLavora nella cartella in cui il notebook di riferimento ha salvato `reference-model.json`. Se non lo trovi, esegui prima il notebook 07. Non modificare il test set per migliorare il punteggio.'),
        code('import json\nimport math\nfrom pathlib import Path\n\nartifact_path = Path("reference-model.json")\nif artifact_path.exists():\n    artifact = json.loads(artifact_path.read_text())\n    assert len(artifact["weights"]) == len(artifact["features"])\n    assert all(value > 0 for value in artifact["scale"])\n    print("Model:", artifact["model_type"])\n    print("Recorded test accuracy:", artifact["test_accuracy"])\nelse:\n    print("Run notebook 07 in this directory to create reference-model.json.")'),
        md('## Consegna\nPrepara notebook eseguito, dataset o istruzioni riproducibili, licenza, tabella degli esperimenti, modello e breve relazione. Spiega un errore del modello e un limite dei dati.\n\n## Presentazione di 5 minuti\n1 minuto sul problema e sui dati; 1 sul protocollo; 1 sui risultati e sulla baseline; 1 di dimostrazione; 1 sui limiti e sul prossimo esperimento.\n\n## Riepilogo\nUn punteggio da solo non basta. Il progetto deve poter essere compreso, riprodotto e valutato.')])
    write('progetto-sentiment','Progetto iniziale: sentiment di brevi recensioni',[
        md('## Obiettivo e dataset\nClassificare recensioni positive/negative. Queste 24 frasi sono **originali AI Lab**, scritte per la didattica: dataset minuscolo, non rappresentativo. Servono per avviare il flusso; il progetto finale deve raccogliere più esempi autorizzati, documentando etichette e limiti. Richiede scikit-learn; esecuzione locale non verificata.'),
        code('from sklearn.pipeline import make_pipeline\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import classification_report\n\npositive = ["film bello e coinvolgente", "storia piacevole", "mi è piaciuto molto", "ottima esperienza", "consiglio questo film", "recitazione eccellente", "un racconto emozionante", "finale bellissimo", "musica splendida", "davvero divertente", "personaggi riusciti", "un film da vedere"]\nnegative = ["film brutto e noioso", "storia deludente", "non mi è piaciuto", "pessima esperienza", "sconsiglio questo film", "recitazione scarsa", "un racconto confuso", "finale terribile", "musica fastidiosa", "davvero pesante", "personaggi banali", "un film da evitare"]\ntexts, labels = positive + negative, [1]*12 + [0]*12\ntrain_texts, test_texts, train_labels, test_labels = train_test_split(texts, labels, stratify=labels, test_size=0.25, random_state=42)\nmodel = make_pipeline(TfidfVectorizer(ngram_range=(1,2)), LogisticRegression(random_state=42))\nmodel.fit(train_texts, train_labels)\nprint(classification_report(test_labels, model.predict(test_texts), zero_division=0))\nprint(model.predict_proba(["non è un film bello"]))'),
        md('## Attività\nAggiungi almeno 60 frasi indipendenti, senza dati personali. Evita duplicati fra split. Crea una validazione separata prima di regolare ngram e regolarizzazione. Studia negazioni e ironia; riporta anche confusion matrix e baseline.\n\n## Interfaccia\nUn campo testo con probabilità e avviso sui limiti. Gradio è possibile fuori GitHub Pages. Non usare il piccolo modello per giudicare persone.')],['sklearn'])
    write('progetto-cifre','Progetto iniziale: cifre scritte a mano',[
        md('## Obiettivi e dati\nUsa `load_digits` di scikit-learn: immagini 8×8 di cifre da 0 a 9, distribuite con la libreria, senza download aggiuntivo dopo l’installazione. Fonte: UCI Optical Recognition of Handwritten Digits, E. Alpaydin e C. Kaynak. Leggi `digits.DESCR` e la documentazione scikit-learn per provenienza e condizioni prima di ridistribuire. CPU sufficiente. Esecuzione locale non verificata.'),
        code('from sklearn.datasets import load_digits\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import accuracy_score, confusion_matrix\n\ndigits = load_digits()\nX_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2, stratify=digits.target, random_state=42)\nX_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.25, stratify=y_train, random_state=42)\nmodel = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=42))\nmodel.fit(X_train, y_train)\nprint("Validation accuracy:",accuracy_score(y_valid,model.predict(X_valid)))\nprint("Final test accuracy:",accuracy_score(y_test,model.predict(X_test)))\nprint(confusion_matrix(y_test,model.predict(X_test)))\nprint("First prediction:",model.predict(X_test[:1]))'),
        md('## Esercizi\nPrima del test, confronta un classificatore semplice con un MLP sul validation set. Esamina almeno cinque errori e gli effetti della normalizzazione.\n\n## Interfaccia\nUna griglia 8×8 o un’immagine ridimensionata e normalizzata come il training. Un disegno esterno può avere una distribuzione diversa: non promettere la stessa accuracy. Gradio può essere eseguito separatamente dal sito.')],['sklearn'])
    write('progetto-immagini','Progetto iniziale: immagini sintetiche e CNN',[
        md('## Obiettivi\nClassificare barre orizzontali e verticali in immagini sintetiche 16×16. Dati originali AI Lab generati qui, nessun download né GPU. Richiede NumPy e TensorFlow, esecuzione locale non verificata. Dopo aver capito la pipeline puoi sostituire i dati con immagini autorizzate.'),
        code('import os\nos.environ["TF_NUM_INTRAOP_THREADS"] = "1"\nos.environ["TF_NUM_INTEROP_THREADS"] = "1"\nimport numpy as np\nimport tensorflow as tf\nfrom tensorflow import keras\nfrom tensorflow.keras import layers\n\nkeras.utils.set_random_seed(42)\nrng = np.random.default_rng(42)\nimages = rng.normal(0, 0.05, (300,16,16,1)).astype("float32")\nlabels = np.arange(300) % 2\nfor index,label in enumerate(labels):\n    location = rng.integers(3,12)\n    if label == 0:\n        images[index,location:location+2,:,0] += 1\n    else:\n        images[index,:,location:location+2,0] += 1\norder = rng.permutation(300)\nimages, labels = images[order], labels[order]\nmodel = keras.Sequential([keras.Input(shape=(16,16,1)), layers.Conv2D(8,3,activation="relu"), layers.GlobalAveragePooling2D(), layers.Dense(1,activation="sigmoid")])\nmodel.compile(optimizer="adam",loss="binary_crossentropy",metrics=["binary_accuracy"])\noptions = tf.data.Options()\noptions.threading.private_threadpool_size = 1\ntrain_data = tf.data.Dataset.from_tensor_slices((images[:180], labels[:180])).batch(16).with_options(options)\nvalid_data = tf.data.Dataset.from_tensor_slices((images[180:240], labels[180:240])).batch(16).with_options(options)\nmodel.fit(train_data,validation_data=valid_data,epochs=30,verbose=0)\npredictions = model(images[240:],training=False).numpy().ravel() >= 0.5\nprint("Test accuracy:",np.mean(predictions == labels[240:]))'),
        md('## Esercizi\nConfronta la CNN con una baseline. Aggiungi rumore e variazioni di posizione; non usare rotazioni che scambiano le etichette. Se usi immagini reali, separa soggetti e sequenze fra gli split e registra le licenze.\n\n## Interfaccia\nCaricamento di immagine, conversione a 16×16 in scala di grigi e probabilità; possibile con Gradio in un ambiente Python esterno al sito.')],['numpy','tensorflow'])
    print('Generated school notebooks:', len(list((LAB/'notebooks').glob('*.ipynb'))))


if __name__ == '__main__':
    generate()
