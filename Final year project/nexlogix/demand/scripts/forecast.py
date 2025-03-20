# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # ✅ Force Matplotlib to use non-GUI backend

import matplotlib.pyplot as plt
import os
import django
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexlogix.settings")  # Replace 'nexlogix' with your project name
django.setup()

def run_forecasting():
    from django.conf import settings
    # Load dataset
    dataset_path = os.path.join(settings.BASE_DIR, "demand", "data", "data.csv")
    df = pd.read_csv(dataset_path)

    # Convert Date column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    # Encode categorical variables
    le_product = LabelEncoder()
    df["Product_Encoded"] = le_product.fit_transform(df["Product"])

    le_weather = LabelEncoder()
    df["Weather_Encoded"] = le_weather.fit_transform(df["Weather"])

    le_economic = LabelEncoder()
    df["Economic_Encoded"] = le_economic.fit_transform(df["Economic_Condition"])

    le_holiday = LabelEncoder()
    df["Holiday_Encoded"] = le_holiday.fit_transform(df["Holiday_Season"])

    # Define features and target variable
    X = df[["Year", "Month", "Product_Encoded", "Weather_Encoded", "Economic_Encoded", "Holiday_Encoded", "Final_Price"]]
    y = df["Units_Sold"]

    # Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Generate predictions for 2025
    future_dates = [f"2025-{month:02d}" for month in range(1, 13)]
    predictions = []

    for product in df["Product"].unique():
        for date in future_dates:
            year, month = map(int, date.split('-'))
            product_encoded = le_product.transform([product])[0]
            weather_encoded = np.random.randint(0, len(le_weather.classes_))
            economic_encoded = np.random.randint(0, len(le_economic.classes_))
            holiday_encoded = np.random.randint(0, len(le_holiday.classes_))
            avg_price = df[df["Product"] == product]["Final_Price"].mean()

            # Fix feature names issue
            feature_names = ["Year", "Month", "Product_Encoded", "Weather_Encoded", "Economic_Encoded", "Holiday_Encoded", "Final_Price"]
            input_data = pd.DataFrame([[year, month, product_encoded, weather_encoded, economic_encoded, holiday_encoded, avg_price]], columns=feature_names)

            predicted_sales = model.predict(input_data)[0]
            predictions.append([date, product, int(predicted_sales)])

    # Save predictions to CSV
    df_predictions = pd.DataFrame(predictions, columns=["Date", "Product", "Predicted_Units_Sold"])
    predictions_path = os.path.join(settings.MEDIA_ROOT, "demand_forecasting_predictions_2025.csv")
    df_predictions.to_csv(predictions_path, index=False)

    # Generate and save graphs
    image_files = []
    for product in df["Product"].unique():
        df_actual = df[df["Product"] == product].copy()
        df_predicted = df_predictions[df_predictions["Product"] == product].copy()

        df_actual.loc[:, "Date"] = pd.to_datetime(df_actual["Date"])
        df_predicted.loc[:, "Date"] = pd.to_datetime(df_predicted["Date"])

        plt.figure(figsize=(12, 6))
        plt.plot(df_actual["Date"], df_actual["Units_Sold"], marker='o', linestyle='-', label="Actual Sales", color="blue")
        plt.plot(df_predicted["Date"], df_predicted["Predicted_Units_Sold"], marker='s', linestyle='--', label="Predicted Sales (2025)", color="red")

        plt.xlabel("Date")
        plt.ylabel("Units Sold")
        plt.title(f"Actual vs. Predicted Sales for {product}")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()

        # Save image properly
        image_filename = f"sales_forecast_{product.replace(' ', '_').lower()}.png"
        plt.savefig(os.path.join(settings.MEDIA_ROOT, image_filename), bbox_inches="tight")
        plt.close()

        # Add to list
        image_files.append(image_filename)

    print("Demand forecasting completed. Predictions and graphs saved.")
    return image_files  # Return image filenames
