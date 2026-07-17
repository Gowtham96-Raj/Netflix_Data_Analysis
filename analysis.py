"""
Netflix Data Analysis
Author: Gowtham Raj S

This script performs data cleaning and exploratory data analysis
on the Netflix Titles dataset.
"""

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = "netflix_titles.csv"
OUTPUT_FOLDER = "output"


def load_data(file_path: str) -> pd.DataFrame:
    """Load the Netflix dataset."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found: {file_path}. "
            "Place netflix_titles.csv in the same folder as analysis.py."
        )

    return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the dataset for analysis."""
    cleaned = df.copy()

    cleaned.drop_duplicates(inplace=True)

    text_columns = [
        "title",
        "director",
        "cast",
        "country",
        "rating",
        "duration",
        "listed_in",
        "description",
    ]

    for column in text_columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].fillna("Unknown").astype(str).str.strip()

    if "date_added" in cleaned.columns:
        cleaned["date_added"] = pd.to_datetime(
            cleaned["date_added"].astype(str).str.strip(),
            errors="coerce",
        )
        cleaned["year_added"] = cleaned["date_added"].dt.year

    if "release_year" in cleaned.columns:
        cleaned["release_year"] = pd.to_numeric(
            cleaned["release_year"],
            errors="coerce",
        )

    return cleaned


def print_summary(df: pd.DataFrame) -> None:
    """Print general information and key findings."""
    print("\nNETFLIX DATA ANALYSIS")
    print("=" * 50)
    print(f"Total titles: {len(df):,}")

    if "type" in df.columns:
        print("\nMovies vs TV Shows:")
        print(df["type"].value_counts())

    if "country" in df.columns:
        country_data = (
            df["country"]
            .str.split(",")
            .explode()
            .str.strip()
        )
        country_data = country_data[country_data != "Unknown"]

        print("\nTop 10 countries by number of titles:")
        print(country_data.value_counts().head(10))

    if "rating" in df.columns:
        print("\nTop content ratings:")
        print(df["rating"].value_counts().head(10))

    if "listed_in" in df.columns:
        genres = (
            df["listed_in"]
            .str.split(",")
            .explode()
            .str.strip()
        )
        print("\nTop 10 genres:")
        print(genres.value_counts().head(10))

    if "director" in df.columns:
        directors = (
            df.loc[df["director"] != "Unknown", "director"]
            .str.split(",")
            .explode()
            .str.strip()
        )
        print("\nTop 10 directors:")
        print(directors.value_counts().head(10))

    if "duration" in df.columns and "type" in df.columns:
        movies = df[df["type"] == "Movie"].copy()
        movies["duration_minutes"] = pd.to_numeric(
            movies["duration"].str.extract(r"(\d+)")[0],
            errors="coerce",
        )

        longest_movies = movies.nlargest(
            10,
            "duration_minutes",
        )[["title", "duration_minutes"]]

        print("\nTop 10 longest movies:")
        print(longest_movies.to_string(index=False))


def save_chart(file_name: str) -> None:
    """Save the active chart and close it."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, file_name)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved chart: {output_path}")


def create_visualizations(df: pd.DataFrame) -> None:
    """Create and save charts for the project."""
    if "type" in df.columns:
        df["type"].value_counts().plot(
            kind="bar",
            title="Netflix Movies vs TV Shows",
        )
        plt.xlabel("Content Type")
        plt.ylabel("Number of Titles")
        save_chart("movies_vs_tv_shows.png")

    if "year_added" in df.columns:
        yearly_titles = (
            df.dropna(subset=["year_added"])
            .groupby("year_added")
            .size()
            .sort_index()
        )

        yearly_titles.plot(
            kind="line",
            marker="o",
            title="Netflix Titles Added by Year",
        )
        plt.xlabel("Year Added")
        plt.ylabel("Number of Titles")
        save_chart("titles_added_by_year.png")

    if "country" in df.columns:
        top_countries = (
            df["country"]
            .str.split(",")
            .explode()
            .str.strip()
        )
        top_countries = top_countries[top_countries != "Unknown"]
        top_countries = top_countries.value_counts().head(10)

        top_countries.sort_values().plot(
            kind="barh",
            title="Top 10 Countries by Netflix Titles",
        )
        plt.xlabel("Number of Titles")
        plt.ylabel("Country")
        save_chart("top_countries.png")

    if "rating" in df.columns:
        top_ratings = df["rating"].value_counts().head(10)

        top_ratings.plot(
            kind="bar",
            title="Top Netflix Content Ratings",
        )
        plt.xlabel("Rating")
        plt.ylabel("Number of Titles")
        save_chart("ratings_distribution.png")

    if "listed_in" in df.columns:
        top_genres = (
            df["listed_in"]
            .str.split(",")
            .explode()
            .str.strip()
            .value_counts()
            .head(10)
        )

        top_genres.sort_values().plot(
            kind="barh",
            title="Top 10 Netflix Genres",
        )
        plt.xlabel("Number of Titles")
        plt.ylabel("Genre")
        save_chart("top_genres.png")


def export_cleaned_data(df: pd.DataFrame) -> None:
    """Save the cleaned dataset."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, "netflix_titles_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned dataset: {output_path}")


def main() -> None:
    """Run the complete Netflix analysis."""
    try:
        netflix_df = load_data(DATA_FILE)
        netflix_df = clean_data(netflix_df)

        print_summary(netflix_df)
        create_visualizations(netflix_df)
        export_cleaned_data(netflix_df)

        print("\nAnalysis completed successfully.")

    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)

    except pd.errors.EmptyDataError:
        print("Error: The dataset file is empty.")
        sys.exit(1)

    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
