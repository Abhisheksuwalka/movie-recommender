# Movie Recommender System

A movie recommendation system that suggests five similar movies based on a database of around 5000 top movies.

## Live Demo
Check out the live demo: [Movie Recommender](https://movie-rec-1j40.onrender.com)

## Data Source
The dataset is sourced from [TMDB Movie Metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).

## Installation
To set up the environment and install dependencies, use the following commands:

```bash
$envName=movieRecEnv OR envName=movieRecEnv
conda create --name $envName -y

conda activate $envName
pip install -r requirements.txt
```

## Project Structure

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- Overview of the project
├── data               <- Movie dataset files
│   ├── raw            <- Original dataset
│   ├── processed      <- Cleaned and transformed data
│
├── models             <- Trained recommendation models
│
├── notebooks          <- Jupyter notebooks for experimentation and exploration
│
├── requirements.txt   <- Dependencies for the project
│
└── src                         <- Source code for the recommendation system
    │
    ├── dataset.py              <- Scripts to load and process the dataset
    ├── recommender.py          <- Movie recommendation logic
    ├── app.py                  <- Web application script (Flask or similar framework)
    └── config.py               <- Configuration settings
```

## Usage
1. Run the web application locally:
   ```bash
   python src/app.py
   ```
2. Open the browser and navigate to `http://localhost:5000`
3. Search for a movie to get recommendations.

## License
This project is released under an open-source license. Feel free to modify and contribute!