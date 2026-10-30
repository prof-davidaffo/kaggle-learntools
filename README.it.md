# AI Lab — Machine Learning e Deep Learning con Python

Corso in italiano per la scuola secondaria di secondo grado: i corsi completi **Intro to Machine Learning** e **Intro to Deep Learning**, con lezioni ed esercizi tradotti dai sorgenti Kaggle Learn e dataset originali.

La piattaforma è in `ai_lab/`. Le directory originali Kaggle e il README originale rimangono intatti.

- [Guida completa in italiano](ai_lab/README.md): installazione, build, manutenzione e pubblicazione.
- [Istruzioni per Colab e Jupyter](ai_lab/content/school/esecuzione.md).
- [Dataset e istruzioni per gli studenti](ai_lab/content/school/dataset.md).
- [Inventario e risultati delle verifiche](ai_lab/reports/VERIFICA.md).
- [Workflow GitHub Pages](.github/workflows/ai-lab-pages.yml): pubblicazione manuale, successiva alla revisione.
- [Pubblicazione passo per passo](ai_lab/PUBBLICAZIONE.md): primo invio, impostazioni Pages e aggiornamenti.

Il sito generato è in `ai_lab/build/`; il pacchetto completo con notebook e nove CSV è `ai_lab/build/downloads/ai-lab-studenti.zip`. I prodotti di build non vengono versionati: sono generati localmente o da GitHub Actions.

Dalla radice del repository, genera e verifica il sito con:

```sh
./build.sh
```

Lo script prepara automaticamente l’ambiente virtuale e installa le dipendenze. Serve Python 3 e, per le dipendenze mancanti, una connessione Internet.

Per avviare il server sul sito generato:

```sh
./start.sh
```

Apri `http://localhost:8000` e usa `Ctrl+C` per fermare il server. Per cambiare porta usa `./start.sh --port 8001`. Dopo aver modificato i contenuti, esegui di nuovo `./build.sh`.

Per visualizzare una build già presente:

```sh
python -m http.server 8000 --directory ai_lab/build
```

Apri `http://localhost:8000`. La compilazione è descritta nella guida completa. Non serve un backend Python per ospitare le pagine su GitHub Pages; l’addestramento viene svolto nei notebook.
