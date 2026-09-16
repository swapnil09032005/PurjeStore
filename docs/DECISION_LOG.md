# PurjeStore Decision Log

| Date | Decision | Reason | Evidence | Status |
|---|---|---|---|---|
| 2026-09-16 | Use VS Code + Jupyter | VS Code for engineering/application work; Jupyter for exploration and experiments | Project workflow decision | Confirmed |
| 2026-09-16 | Use 177 CSV files for development | Provides a controlled and reproducible development data source | Project architecture decision | Confirmed |
| 2026-09-16 | Maintain separate live database connection | Required for current data, dashboard refresh and ML inference | Project architecture decision | Confirmed |
| 2026-09-16 | Keep development and live data logically separated | Prevent accidental modification of live data and preserve reproducibility | Architecture principle | Confirmed |
| 2026-09-16 | Store database credentials through environment configuration | Prevent credentials from entering source control | Security principle | Confirmed |
| 2026-09-16 | Train ML models through validated development pipelines before live inference | Separates model development from production inference | ML architecture principle | Confirmed |
