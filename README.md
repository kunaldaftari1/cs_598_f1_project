# CS 598 F1 Race Winner Prediction Project

A semester-long data curation project for predicting Formula 1 race winners using data from multiple sources including FastF1, OpenF1, and weather APIs.

## Project Overview

This project demonstrates an end-to-end data curation workflow for predicting F1 race winners using pre-race information. The goal is to answer:

> **How accurately can we model pre-race win probabilities for each driver using available historical race, weather, and tire data?**

## Project Structure

```
cs_598_f1_project/
│   .gitignore
│   README.md
│
├───data
│   ├───cleaned
│           circuits.csv
│           drivers.csv
│           overtakes.csv
│           pirelli_tyre.csv
│           race_result.csv
│           sessions.csv
│           starting_grid.csv
│           stints.csv
│           weather.csv
├───deliverables
│       metadata_and_data_dictionary.pdf
│       schema.sql
├───documentation
│       Proposal Draft_ Predicting F1 Race Winners through Data Curation.pdf
│       readme.md
├───history
│   ├───data
│   │   │   f1_database.db
│   │   │   readme.md
│   │   │
│   │   ├───fastf1_testdata
│   │   ├───openf1_samples
│   │   └───openmeteo_testdata
│   └───scripts
│           fastf1_api.py
│           openf1_api.py
│           openf1_api_all.py
│           openmeteo_api.py
│           pirelli_tire_data.py
│           testing.ipynb
└───scripts
    └───data_cleaning
            factory.py
            main.py
            retrieve_data.ipynb
```

## Quick Start

### 1. Create the Database Schema

```bash
# Option 1: Using the Python test script
python scripts/test_schema.py

# Option 2: Using SQLite directly
sqlite3 data/f1_database.db < scripts/create_schema.sql
```

### 2. Test Data Collection

```bash
# Test OpenF1 API (samples saved to data/openf1_samples/)
python scripts/openf1_api_all.py

# Test FastF1 (caches to data/fastf1_testdata/)
python scripts/fastf1_api.py

# Test weather API
python scripts/openmeteo_api.py
```

## Database Schema

The project uses a normalized relational database schema with 8 main tables:

1. **meetings** - Grand Prix information
2. **sessions** - Individual race/practice sessions
3. **drivers** - Driver information per session
4. **weather** - Weather conditions during sessions
5. **session_results** - Race results and outcomes
6. **stints** - Tire stint information
7. **tire_allocations** - Pre-race tire allocations (manual from Pirelli)
8. **pit_stops** - Pit stop timing data

Plus 2 analytical views:
- **pre_race_features** - Aggregated pre-race features for prediction
- **race_outcomes** - Race results with outcome flags

See `documentation/schema.md` for the complete ER diagram and table definitions.

## Data Sources

- **OpenF1 API**: Live race data (https://openf1.org/)
- **FastF1**: Historical F1 timing data (https://github.com/theOehrly/Fast-F1)
- **OpenWeather**: Weather conditions (https://openweathermap.org/api)
- **Pirelli**: Tire compound allocations (manual extraction)

## Key Features

- **Data Curation**: End-to-end workflow from raw API data to analysis-ready datasets
- **Database Design**: Normalized relational schema following 3NF principles
- **Metadata Management**: Comprehensive data documentation and lineage tracking
- **Reproducibility**: Automated scripts for data acquisition and processing
- **Predictive Modeling**: Framework for pre-race win probability predictions

## Team

- Fatih Atlamaz
- Navtej Kathuria  
- Kunal Daftari

## License

This project is for educational purposes as part of CS 598 (Data Curation) at the University of Illinois.

## References

See the proposal document in `documentation/` for complete references and project scope. 
