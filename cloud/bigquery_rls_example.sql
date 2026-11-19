-- TEMPLATE ONLY: replace PROJECT_ID, DATASET_ID and group email.
-- Execute as BigQuery administrator; requires row access policy permissions.
-- This policy filters the France slice; create corresponding policies for other authorized groups.
CREATE ROW ACCESS POLICY france_sales
ON `PROJECT_ID.DATASET_ID.ventes`
GRANT TO ("group:analystes-france@example.org")
FILTER USING (pays = 'France');

-- Grant minimum table access separately. Test with impersonated authorized identities.
-- BigQuery IAM/RLS is distinct from the demo API's application-level filtering.
