# RetailAI Copilot — Démonstrateur Data & IA e-commerce

**Prototype indépendant, non affilié à Hoortrade/Casanoov.** Il exploite deux jeux de données :
1. `data/ventes_synthetiques.csv` (2 000 commandes commerciales fictives, marques Casanoov/Cazeboo/Sicaan)
2. `data/Gestion_Stock_Maroc.xlsx` et `data/stock_nettoye.csv` (177 mouvements de stock marocains, sans lien avec Hoortrade)

## Démarrage rapide — Docker
Prérequis : Docker Desktop.
```bash
docker compose up --build
```
- Interface : http://localhost:8502
- API : http://localhost:8000/docs
- Health : http://localhost:8000/health

## Démarrage sans Docker (Python 3.11)
```bash
python -m venv .venv
# Windows PowerShell : .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/seed.py
uvicorn app.main:app --reload
# Deuxième terminal :
streamlit run dashboard/streamlit_app.py --server.port 8502
```

## Modules réellement fonctionnels
- API FastAPI `/sales`, `/stocks/low`, `/stocks/movements`, `/ask`.
- Tableau de bord Streamlit (ventes, mouvements de stock, assistant documentaire).
- Stockage SQLite local, initialisé à partir des CSV (démarrage sans serveur Oracle).
- RAG **TF-IDF lexical** sur deux documents fictifs avec références de fichiers. Un LLM OpenAI-compatible est facultatif (clé API + `pip install openai`). **Ce n'est pas encore un RAG vectoriel avec embeddings.**
- Serveur MCP optionnel avec outils de lecture seule (`pip install mcp`, `python -m app.mcp_server`).
- Tests Pytest et workflow GitHub Actions.

## Connecteurs / modules fournis mais non activés automatiquement
- `sql/stock_oracle.sql` : schéma Oracle et requêtes; `scripts/oracle_connect.py` : test de connexion Oracle (`pip install oracledb`). Le moteur de l'application est SQLite par défaut.
- `scripts/upload_bigquery.py` : import manuel du CSV commercial vers BigQuery (`pip install google-cloud-bigquery`, identifiants GCP nécessaires).
- `dbt/` : exemple de modèle BigQuery; nécessite dbt-bigquery et configuration du profil.
- `airflow/` : exemple de DAG de validation, nécessite un environnement Airflow distinct.
- Cloud Run, IAM, RLS et authentification : **non implémentés**. Voir `docs/SECURITY.md`.

## Données et qualité
`data/rapport_qualite_stock.csv` contient les contrôles sur le fichier de stock. Les identifiants répétés et valeurs manquantes ne sont pas supprimés automatiquement. Les variations nettes ne sont pas des stocks disponibles sans stock initial.

## Tests
```bash
python scripts/validate_data.py
python -m pytest -q
```

## Architecture
Streamlit → FastAPI → SQLite (ventes/mouvements) ou recherche documentaire TF-IDF. Des adaptateurs Oracle et BigQuery sont fournis comme points de départ; leur branchement à l'API nécessite une phase supplémentaire.

## Feuille de route
1. Sécuriser les accès et implémenter rôles / restrictions.
2. Remplacer TF-IDF par embeddings et base vectorielle, évaluer les citations.
3. Connecter Oracle à l'API en lecture seule, puis BigQuery avec IAM/RLS.
4. Industrialiser dbt, Airflow, CI/CD et Cloud Run.
5. Mesurer latence, fidélité, coût et qualité des réponses.


## Extension RAG vectoriel / IAM / RLS / Cloud (v0.2)
- `app/vector_rag.py` : Chroma persistant + embeddings multilingues, découpage chevauchant, sources, seuil de pertinence, abstention; corpus de démo uniquement.
- `app/security.py` : jeton de démo, rôle et périmètres configurés **côté serveur**.
- `app/analytics.py` : filtres pays et marque appliqués dans SQL avant agrégation; rôle admin requis pour les mouvements.
- `cloud/bigquery_rls_example.sql` : modèle de row access policy BigQuery (non appliqué).
- `cloud/deploy-cloud-run.sh` : modèle de déploiement Cloud Run privé (non exécuté).
- `docs/SECURITY.md` : voir aussi `cloud/README.md` pour les limites.

### Lancer en local
1. `cp .env.example .env` (PowerShell : `Copy-Item .env.example .env`).
2. Remplacer `DEMO_API_TOKEN` par un secret aléatoire et long.
3. `docker compose up --build` puis ouvrir `http://localhost:8502`.
4. Saisir le jeton dans la barre latérale de Streamlit.

### Activer le RAG vectoriel
1. Dans `.env`, définir `INSTALL_VECTOR=true` et `RAG_BACKEND=vector`.
2. Relancer `docker compose up --build`.
3. Au premier appel `/ask`, téléchargement du modèle d'embeddings, puis indexation locale.
4. Ajouter `OPENAI_API_KEY` uniquement si génération LLM souhaitée (sinon réponse par extrait).

### Sécurité et limites
**IAM/RLS GCP sont des exemples d'infrastructure, non une configuration déployée.**
L'authentification par jeton partagé n'est **pas adaptée à la production**. Le RAG ne contient que des documents fictifs de démonstration et ne fournit pas de séparation multi-tenant de documents. Les données de ventes restent synthétiques. Les services Cloud nécessitent des identifiants et des ressources GCP que ce ZIP ne peut pas créer.


## Nouvelle interface Next.js / React / TypeScript
- `frontend/` : tableau de bord moderne, graphiques Recharts, ventes, stocks, chat RAG, page agents et sécurité.
- Route serveur `/api/proxy/[...path]` : proxy de routes FastAPI explicitement autorisées; le jeton saisi reste en mémoire navigateur et est envoyé en en-tête.
- Docker Compose : **http://localhost:3000** (nouvelle interface), **http://localhost:8502** (ancien Streamlit), **http://localhost:8000/docs** (API).
- Démarrage : copier `.env.example` en `.env`, changer `DEMO_API_TOKEN`, puis `docker compose up --build`.
- Sans Docker : `cd frontend && npm install && npm run dev` (nécessite une API locale et `API_INTERNAL_URL=http://127.0.0.1:8000`).
- Le design n'implémente pas encore une authentification de production. Ne pas exposer le jeton partagé sur Internet.
- La page Agents indique les intégrations disponibles/prévues; elle n'invente pas de journaux MCP.


## V3 — assistant SQL métier, prévisions et observabilité
- `/ask` reconnaît des questions de ventes/commandes/stocks et exécute des requêtes SQL **paramétrées et prédéfinies**, jamais du SQL généré par un LLM. Les filtres pays/marque sont imposés côté serveur.
- `/forecast?horizon=3` calcule une baseline de moyenne mobile 3 mois et une MAE walk-forward, sur données **synthétiques**. Ce n'est pas un modèle de Machine Learning entraîné.
- `/observability` expose, pour le rôle `admin` uniquement, des compteurs en mémoire et latences des requêtes `/ask`. Les prompts et secrets ne sont pas journalisés. Les compteurs sont perdus au redémarrage.
- Next.js propose une page « Prévisions ». Le proxy Next.js autorise explicitement les deux nouvelles routes.
- Aucun déploiement GCP, connexion Oracle distante ou modèle LLM réel n'est implicitement activé.
