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
There are multiple ways to access and reproduce the data described in this document. However, regardless of the method used, the initial steps are:
```bash
git clone https://github.com/kunaldaftari1/cs_598_f1_project.git
cd scripts/data_cleaning
```

### 1. Pre-Generated Dataset Method
Because the OpenF1 API enforces strict rate limits, retrieving the full dataset directly from the API can be slow. Given these constraints, the quickest way to explore the data is to use the sample dataset provided in the repository. This sample contains sessions from 2025-11-28 to 2025-12-07, including two full race weekends.

All pre-generated files are available under:

```bash
cs_598_f1_project/data/cleaned
```

This method is connected directly into the command-line interface and can be launched with:

```bash
python main.py pre-generated  # within the ../scripts/data_cleaning directory
                              # or simply run with python main.py p
```

Once launched, this mode loads the cleaned CSVs from the repository rather than sending live API requests. As a result, it completely avoids rate limiting and provides an immediate, stable environment for exploring circuits, drivers, sessions, stints, overtakes, weather, tyre data, and more. It is the recommended entry point for quickly inspecting the dataset, validating schemas, and experimenting.
The method also allows for simple customization, such as selecting the number of rows displayed in the terminal:

```bash
rows [int]         # sets the preferred number of rows to display in the output
```

### 2. Jupyter Notebook
The most reliable way to retrieve new, updated data is by using the Jupyter Notebook located at  scripts/data_cleaning/retrieve_data.ipynb. This approach does require an IDE or environment that supports Jupyter Notebooks, along with a Python kernel installed on the system. Numerous resources and installation guides for these tools are widely available online. 

The first code block in the Jupyter Notebook includes all necessary imports and provides an option to specify the earliest date from which data should be retrieved. Nearly every other code block includes a function that makes a call to the OpenF1 API, followed by a block that invokes the function and performs the actual data retrieval. Because the API’s rate-limiting behavior can be inconsistent, any block that fails due to rate limiting can typically be rerun after increasing the delay specified in the time.sleep() statements as well as after waiting 5-10 minutes. All code blocks are extensively commented for the user’s convenience.

It is important to note that, unlike the other methods described below, the Jupyter Notebook is intended to be executed sequentially. Several later blocks depend on variables and data structures created earlier. For instance, the first three code blocks must be executed initially, and the helper functions that interact with the API must be run before the large code blocks that utilize them.

### 3. Assisted UI Method
Provided that retrying due to rate limiting isn’t an issue or the user wants very recent data (by specifying the date to be within the month), we provide a simple, in-terminal interface that guides users step-by-step through producing and accessing the data. This interface can be launched with:

```bash
python main.py assisted  # within the ../scripts/data_cleaning directory
```

Once launched, the user is presented with a list of available functions and can choose to run a function, modify the date or number of rows, or exit the process. If the user chooses to run a function, they are then given the option either to save the resulting data locally as a CSV file or to display a selected number of rows directly in the terminal. To be clear, the number of rows can be selected using the rows option. The date option allows the user to specify the earliest date from which data should be retrieved. Finally, exiting the process will result in these settings being reset, however, the data saved locally will remain.

An example sequence of user inputs might look like:

```bash
python main.py assisted
date 
2025-12-01
rows
30
circuits
yes
drivers
no
exit
```

### 4. Manual UI Method
Similar to the previous method, assuming rate-limiting retries are not an issue, the user also has the option to run commands directly in a single line. This approach avoids the step-by-step prompts of the assisted method and allows for faster, straightforward execution. 

To launch the process:

```bash
python main.py manual # within the ../scripts/data_cleaning directory
```

The available commands are provided below:

```bash
exit               # exits the process

rows [int]         # sets the preferred number of rows to display in the output

date [YYYY-MM-DD]  # specifies the earliest date the data should be retrieved

function [bool]    # runs the specified function
                   # bool determines whether to save the output locally
                   # valid functions: races, starting_grid, race_result, 
                   # circuits, drivers, stints, 
                   # overtakes, weather, pirelli_tyre
```

## Schema & Tables

The project uses a normalized relational database schema with the following main tables:

- **sessions** — Contains information about each F1 session (race, qualifying, practice), including session type, circuit, and dates.

- **circuits** — Stores circuit identifiers and associated country information.

- **teams** — Lists F1 team names used for driver-team relationships.

- **drivers** — Stores driver information for each session, including driver number, name, and team.

- **starting_grid** — Contains qualifying results for each session, including starting position and lap duration.

- **race_result** — Contains final race classifications and driver status (e.g., finished, DNF, DSQ).

- **race_stints** — Records tire stint information per driver, including compound choice and stint length.

- **overtakes** — Stores average overtaking statistics per driver and circuit.

- **weather** — Contains session-level weather data such as temperature, rainfall, and wind conditions.

- **pirelli_tyres** — Lists official Pirelli tire compound allocations per circuit and year.

A full schema diagram and detailed field definitions are available in  
`documentation/schema.md`.

## Data Sources

- **OpenF1 API**: Live race data (https://openf1.org/)
- **OpenWeather**: Weather conditions (https://openweathermap.org/api)
- **Pirelli**: Tire compound allocations (manual extraction)

## Key Features

- **Data Curation**: End-to-end workflow from raw API data to analysis-ready datasets
- **Database Design**: Normalized relational schema following 3NF principles
- **Metadata Management**: Comprehensive data documentation and lineage tracking
- **Reproducibility**: Automated scripts for data acquisition and processing

## Team

- Fatih Atlamaz
- Navtej Kathuria  
- Kunal Daftari

## License

This project is for educational purposes as part of CS 598 (Data Curation) at the University of Illinois.

## References

See the proposal document in `documentation/` for complete references and project scope. 
