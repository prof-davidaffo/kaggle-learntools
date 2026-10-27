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

Per visualizzare una build già presente, dalla radice del repository:

```sh
python -m http.server 8000 --directory ai_lab/build
```

Apri `http://localhost:8000`. La compilazione è descritta nella guida completa. Non serve un backend Python per ospitare le pagine su GitHub Pages; l’addestramento viene svolto nei notebook.
