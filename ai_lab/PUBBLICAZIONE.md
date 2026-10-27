# Pubblicare AI Lab su GitHub Pages

Indirizzo configurato: **https://prof-davidaffo.github.io/kaggle-learntools/**.

Questa guida prepara il primo invio e gli aggiornamenti. Nessun comando Git riportato qui è stato eseguito automaticamente. Il workflow compila su push e pull request; pubblica soltanto quando avviato manualmente con `publish` attivato. Non richiede token personali o altri segreti.

## 1. Controllo locale

Dalla radice del repository, usando l’interprete Python disponibile sul computer (`python --version`):

```sh
python -m venv ai_lab/.venv
source ai_lab/.venv/bin/activate
python -m pip install -r ai_lab/requirements/site.txt
python ai_lab/tools/school_notebooks.py
python ai_lab/tools/build.py
python ai_lab/tools/check.py
python ai_lab/qa/check-colab.py
```

La build non scarica dataset e non addestra modelli. I nove CSV necessari sono già in `ai_lab/input/`; il controllo verifica che siano presenti anche nel sito e nel pacchetto studenti. Gli ZIP originali in `data/` e la cartella `ai_lab/build/` sono esclusi da Git.

Per controllare in un browser lo stesso prefisso usato da Pages:

```sh
mkdir -p /tmp/ai-lab-pages-preview/kaggle-learntools
cp -R ai_lab/build/. /tmp/ai-lab-pages-preview/kaggle-learntools/
python -m http.server 8000 --directory /tmp/ai-lab-pages-preview
```

Apri `http://localhost:8000/kaggle-learntools/`. Controlla homepage, una lezione, ricerca, formule, tema, menu a larghezza mobile e download del pacchetto studenti. La verifica grafica richiede un browser locale: non è stata possibile nell'ambiente di preparazione.

## 2. Verifica delle condizioni dei dati

Il sito contiene i CSV scaricabili. Attribuzioni e riscontri sono in [LICENZE-DATI.md](reports/LICENZE-DATI.md). Per Melbourne è indicata CC BY-NC-SA 4.0; per Iowa e DL Course Data il permesso di redistribuzione non è ancora confermato dalle fonti consultabili. Prima di rendere pubblici i CSV, completa questo riscontro sulle pagine originali e aggiorna il manifesto e le attribuzioni. La licenza Apache-2.0 del codice non si applica automaticamente ai dataset.

## 3. Primo invio al repository

Il branch locale attuale è `master`. Prima controlla il remoto e le modifiche:

```sh
git remote -v
git status --short
git diff --check
git add -- .github/workflows/ai-lab-pages.yml README.it.md ai_lab data/.gitignore
git diff --cached --stat
git diff --cached --check
```

Rivedi l'elenco: deve includere sorgenti del sito, traduzioni, notebook studenti, la cartella generata `ai_lab/colab` e CSV estratti. Non deve includere ZIP scaricati, ambienti virtuali o prodotti di build. Non è necessario aggiungere altre directory originali Kaggle.

Quando hai approvato il contenuto e completato il riscontro sui dati:

```sh
git commit -m "Add Italian AI Lab course and GitHub Pages workflow"
git push origin master
```

Questi comandi inviano i file; non avviano automaticamente la pubblicazione. Il workflow manuale deve essere presente nel branch predefinito del repository per comparire in Actions. Se il branch predefinito remoto è diverso da `master`, integra le modifiche con una normale pull request verso quel branch, senza push forzati.

## 4. Abilitare Pages

1. Apri [Settings → Pages](https://github.com/prof-davidaffo/kaggle-learntools/settings/pages).
2. In **Build and deployment → Source**, scegli **GitHub Actions**. Non selezionare una cartella `/docs` o un branch `gh-pages`: il workflow carica direttamente il sito generato.
3. Se le Actions sono disabilitate, abilita le azioni GitHub ufficiali in [Settings → Actions → General](https://github.com/prof-davidaffo/kaggle-learntools/settings/actions).
4. Se l'ambiente `github-pages` impone restrizioni sui branch, consenti il branch da cui pubblicherai in **Settings → Environments → github-pages**.

Il workflow dichiara già i permessi necessari: `contents: read` per la build, `pages: write` e `id-token: write` per il deploy. Non occorre concedere permessi di scrittura generali al repository. Non viene configurato un dominio personalizzato.

## 5. Prima pubblicazione

1. Apri [Actions → AI Lab — build e GitHub Pages](https://github.com/prof-davidaffo/kaggle-learntools/actions/workflows/ai-lab-pages.yml).
2. Attendi che la build del push sia verde. L'artefatto **ai-lab-static-site** contiene il sito pronto; **ai-lab-verification** contiene il rapporto dei controlli.
3. Seleziona **Run workflow**, scegli il branch approvato, attiva **Pubblicare su GitHub Pages** (`publish=true`) e avvia.
4. Attendi il completamento dei job **build**, **colab-checks** e **deploy**. Se è prevista una revisione dell'ambiente, approvala dalla pagina dell'esecuzione.
5. Apri l'URL mostrato dal job deploy: **https://prof-davidaffo.github.io/kaggle-learntools/**. Controlla anche ricerca, una lezione e un download.

Lasciando `publish=false` ottieni una build verificata e gli artefatti, senza deploy. Il job deploy dipende dalla build e dai controlli Keras senza addestramento: un errore interrompe la pubblicazione. Il rapporto aggiuntivo è nell’artefatto **ai-lab-colab-compatibility**.

## Aggiornamenti e problemi comuni

Modifica i sorgenti in `ai_lab/`, rigenera e controlla il sito, invia le modifiche approvate e ripeti il workflow manuale. Non modificare direttamente `ai_lab/build/`: viene rigenerato. Per cambiare titolo, docente o indirizzo usa `config.json`; `base_path` deve corrispondere al percorso di `site_url`, inclusa la barra finale.

| Problema | Verifica |
| --- | --- |
| Il pulsante Run workflow non compare | Il file del workflow deve essere nel branch predefinito; le Actions devono essere abilitate. |
| Configure Pages fallisce | In Settings → Pages la sorgente deve essere GitHub Actions; controlla i permessi del repository. |
| Deploy rifiutato | Controlla branch ammessi ed eventuale approvazione nell'ambiente github-pages. |
| Errore sui CSV nella build | Versiona i file estratti in ai_lab/input; il workflow non estrae gli ZIP locali. |
| Pagina 404 dopo il deploy | Usa l'URL completo con /kaggle-learntools/ e verifica che il job deploy sia terminato con successo. |
| Sorgenti Kaggle aggiornati e build bloccata | Segui la procedura di aggiornamento nel README: rivedi traduzioni e inventario prima di aggiornare gli hash. |

Riferimento: [documentazione GitHub sui workflow Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). Il workflow remoto e il sito pubblicato potranno essere verificati solo dopo il primo invio e deploy autorizzati.

## Controllare i collegamenti Colab

I pulsanti aprono i file versionati in `ai_lab/colab` e caricano i dati dal riferimento `colab_ref` di `config.json` (attualmente `master`). Sono disponibili dopo il push dei nuovi file, senza attendere il deploy di Pages per il download dei dati. Dopo la pubblicazione apri un esercizio ML e uno DL, salva una copia nel tuo Drive ed esegui la preparazione. Una verifica locale o CI non sostituisce questa prima prova con l’account Google della scuola.
