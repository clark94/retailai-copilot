# Sécurité et limites
- Données commerciales : synthétiques; stock marocain : source utilisateur, à ne pas confondre avec Hoortrade.
- Les routes API ne sont PAS authentifiées. Ne pas exposer cette démo sur Internet sans authentification, quotas et contrôle des accès.
- Les outils MCP sont en lecture seule et reposent sur des requêtes prédéfinies.
- Aucune requête SQL libre générée par LLM n'est exécutée.
- IAM/RLS BigQuery : **non implémentés**; à configurer avant usage réel.
- Les clés API restent dans `.env` non versionné.
- Les documents RAG sont fictifs. Ne pas les présenter comme politiques commerciales officielles.
- Vérifier les droits d'usage avant d'ajouter des documents tiers.
