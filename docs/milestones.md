# Suggested Milestones

1. **Milestone 1 - Environment Up**
   - Containers run locally.
   - Frontend can hit API health endpoint.

2. **Milestone 2 - End-to-End Request Flow**
   - Frontend form calls `POST /api/v1/analyze`.
   - API returns baseline result with anomaly label.

3. **Milestone 3 - Baseline Analytics v1**
   - Pricing baseline calibrated from `data/sample_properties.csv`.
   - Add at least 3 unit tests for pricing/anomaly logic.

4. **Milestone 4 - Persistence**
   - Save property + analysis records in PostgreSQL.
   - Add read endpoint for recent analyses.

5. **Milestone 5 - Explainability + UX**
   - Better risk explanation in API.
   - Streamlit uses charts / comparison visuals.

6. **Milestone 6 - Demo Readiness**
   - Team dry-run demo script.
   - Final bug fixes and documentation polish.
