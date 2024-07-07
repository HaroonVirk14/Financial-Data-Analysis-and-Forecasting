from google.colab import files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing

uploaded = files.upload()

uploaded_filenames = list(uploaded.keys())
if 'cdp_financial_data.csv' in uploaded_filenames:
    import io
    df2 = pd.read_csv(io.BytesIO(uploaded['cdp_financial_data.csv']))

    missing_values_summary = df2.isnull().sum()
    columns_to_drop = missing_values_summary[missing_values_summary > (0.80 * len(df2))].index
    cleaned_financial_data = df2.drop(columns=columns_to_drop)

    key_columns = ['Revenue', 'Cost of Revenue', 'Operating Income (Loss)', 'Operating Expenses', 'Depreciation & Amortization']
    for column in key_columns:
        cleaned_financial_data[column] = cleaned_financial_data[column].fillna(cleaned_financial_data[column].median())

    cleaned_financial_data['Report Date'] = pd.to_datetime(cleaned_financial_data['Report Date'])

    descriptive_stats = cleaned_financial_data[key_columns].describe()
    print(descriptive_stats)

    cleaned_financial_data['Gross Profit'] = cleaned_financial_data['Revenue'] - cleaned_financial_data['Cost of Revenue']
    cleaned_financial_data['Operating Profit'] = cleaned_financial_data['Operating Income (Loss)']
    cleaned_financial_data['Net Profit'] = cleaned_financial_data['Operating Profit'] - cleaned_financial_data['Operating Expenses']

    cleaned_financial_data['EBITDA'] = cleaned_financial_data['Operating Profit'] + cleaned_financial_data['Depreciation & Amortization']

    cleaned_financial_data['Gross Profit Margin'] = cleaned_financial_data['Gross Profit'] / cleaned_financial_data['Revenue']
    cleaned_financial_data['Operating Profit Margin'] = cleaned_financial_data['Operating Profit'] / cleaned_financial_data['Revenue']
    cleaned_financial_data['Net Profit Margin'] = cleaned_financial_data['Net Profit'] / cleaned_financial_data['Revenue']

    cleaned_financial_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    cleaned_financial_data.fillna(0, inplace=True)

    kpi_columns = ['Gross Profit', 'Operating Profit', 'Net Profit', 'EBITDA', 'Gross Profit Margin', 'Operating Profit Margin', 'Net Profit Margin']
    kpi_stats = cleaned_financial_data[kpi_columns].describe()
    print(kpi_stats)

    cleaned_financial_data['Fiscal Year'] = pd.to_numeric(cleaned_financial_data['Fiscal Year'], errors='coerce') 

    plt.figure(figsize=(14, 7))
    for column in key_columns:
        plt.plot(annual_data.index, annual_data[column], label=column)
    plt.title('Trends in Key Financial Metrics Over Time')
    plt.xlabel('Fiscal Year')
    plt.ylabel('Values')
    plt.legend()
    plt.show()

    model = ExponentialSmoothing(annual_data['Revenue'], trend='add', seasonal=None, seasonal_periods=12)
    fit = model.fit()
    forecast = fit.forecast(steps=5)

    plt.plot(annual_data.index, annual_data['Revenue'], label='Historical Revenue')
    plt.plot(forecast.index, forecast, label='Forecasted Revenue', linestyle='--')
    plt.title('Historical Revenue and Forecast')
    plt.xlabel('Fiscal Year')
    plt.ylabel('Revenue')
    plt.legend()
    plt.show()
