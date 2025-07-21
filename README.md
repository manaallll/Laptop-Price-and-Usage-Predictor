# Machine Learning Report: Laptop Price Estimation & Use-Case Classification

## 1. Project Overview

This project delivers a dual-function analysis of laptop specifications. It predicts the market price (a regression task) and recommends the ideal usage environment, such as Programming, School/University, or Business (a classification task). The entire system is deployed as a user-friendly web application using the **Streamlit** framework.

---

## 2. Models & Methodology

Two distinct machine learning models were trained and implemented:

### a. Regression Model: Laptop Price Prediction

*   **Model Used:** `Random Forest Regressor`
*   **Objective:** To predict the `Price (in Euros)` based on hardware specifications.
*   **Evaluation Metrics:** Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R² Score.

### b. Classification Model: Laptop Use-Case Prediction

*   **Model Used:** `Random Forest Classifier`
*   **Objective:** To classify a laptop into a predefined usage category.
*   **Target Classes:**
    *   `0`: Programming
    *   `1`: School/University
    *   `2`: Business
*   **Evaluation Metrics:** Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.

---

## 3. Data & Features

### Input Features

The models utilize a comprehensive set of features to ensure accurate predictions, including:
`Company`, `Type Name`, `Inches`, `RAM`, `Operating System`, `Weight`, `Screen Resolution`, `Touchscreen`, `IPS Panel`, `Retina Display`, `CPU Brand`, `Model`, `Clock Speed`, `Primary & Secondary Storage`, `GPU Company` and `Model`.

### Data Preprocessing

A robust preprocessing pipeline was implemented to prepare the data for training:

*   **Label Encoding:** Converted categorical features (e.g., Company, OS) into numerical values.
*   **Feature Engineering:** Created new, informative features from existing ones (e.g., from screen resolution and CPU details).
*   **Handling Missing Values:** Addressed null values through imputation or row removal to maintain data quality.

---

## 4. Deployment & User Interaction

The final models are deployed in a Streamlit application that allows for seamless user interaction:

1.  **Input:** The user enters laptop specifications into a simple form.
2.  **Prediction:** Upon clicking "Submit," the application processes the data and feeds it to the models.
3.  **Output:** The predicted price and recommended use-case are displayed clearly to the user.
4.  **Reset:** A "Reset" button clears the form for a new analysis.

---

## 5. Conclusion

This system successfully combines regression and classification to provide valuable pricing insights and practical usage guidance. The use of **Random Forest**, a powerful ensemble learning method, ensures model accuracy and reliability, while the Streamlit interface makes the complex analysis accessible and user-friendly.
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
