# Laptop Price and Usage Predictor

This project delivers a dual-function analysis of laptop specifications through two distinct machine learning models. A regression model forecasts market price, while a classification model recommends the ideal usage type. The development process covered end-to-end data preprocessing, including label encoding and feature engineering, and culminated in an interactive web application deployed with Streamlit.

<!-- You can add a screenshot of your app working here! -->
<!-- ![App Screenshot](app_screenshot.png) -->

##  Key Features

-   **Price Prediction:** Utilizes a Random Forest Regressor to estimate the price of a laptop based on its hardware specifications.
-   **Use-Case Classification:** Employs a classification model to categorize a laptop for its optimal environment (e.g., Programming, Gaming, Business).
-   **Intelligent Validation:** Includes a custom logic layer to provide warnings about unusual or inconsistent specification combinations.
-   **Interactive UI:** A user-friendly interface built with Streamlit allows for easy input and clear presentation of results.

## Technologies & Skills

-   **Language:** Python
-   **Data Science Stack:** Pandas, NumPy, Scikit-Learn, Matplotlib
-   **Machine Learning:** Regression, Classification, Ensemble Models (Random Forest), Feature Engineering
-   **Deployment & Tools:** Streamlit, Jupyter Notebook, Git, Virtual Environments

## Performance

The models were trained on a dataset of over 1100 laptops and achieved strong performance metrics:
-   **Classification Accuracy:** 90%
-   **Regression R² Score:** 86%

## How to Run

1.  Clone the repository:
    ```bash
    git clone https://github.com/manaallll/Laptop-Price-and-Usage-Predictor.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd Laptop-Price-and-Usage-Predictor
    ```
3.  Create and activate a Python virtual environment.
4.  Install the required packages:
    *(Note: You would first need to create a requirements.txt file with `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```
5.  Run the Streamlit application:
    ```bash
    streamlit run MyApp.py
    ```
