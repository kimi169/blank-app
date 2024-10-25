import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="FIRE Calculator", page_icon=":fire:")

# Title
st.title('FIREUK Simulator')
st.write("Calculate the funds required to sustain early retirement based on various growth rates and annual expenses.")

# User Inputs
age = st.number_input('Current Age', min_value=18, max_value=100, value=40)
retirement_age = st.number_input('SIPP Access Age', min_value=18, max_value=100, value=58)
DB_pension_age = st.number_input('DB Pension Start Age', min_value=18, max_value=100, value=65)
liquid_assets = st.number_input('Liquid Assets Before Age 58 (£)', min_value=10000, value=800000)
SIPP_assets = st.number_input('SIPP Assets (£)', min_value=10000, value=350000)
DB_pension = st.number_input('Annual DB Pension (£)', min_value=0, value=12000)
annual_expenses = st.number_input('Annual Expenses (£)', min_value=0, value=32000)

# Growth Rate Range
growth_rate_min = st.slider('Minimum Real Growth Rate (%)', 0, 10, 1)
growth_rate_max = st.slider('Maximum Real Growth Rate (%)', 0, 10, 7)

# Calculation function
def calculate_fire(liquid_assets, SIPP_assets, DB_pension, annual_expenses, growth_rate_min, growth_rate_max):
    # Define range of growth rates directly as decimals
    growth_rates = [r / 100 for r in range(growth_rate_min, growth_rate_max + 1)]
    results = []
    n_pre58 = retirement_age - age
    n_58_to_65 = DB_pension_age - retirement_age
    n_65_to_88 = 88 - DB_pension_age
    remaining_expenses_post65 = annual_expenses - DB_pension
    
    for r in growth_rates:
        # Pre-58 requirement
        PV_pre58 = annual_expenses * ((1 - (1 + r)**-n_pre58) / r) if r != 0 else annual_expenses * n_pre58
        
        # Post-58 SIPP requirement
        PV_58_to_65 = annual_expenses * ((1 - (1 + r)**-n_58_to_65) / r) if r != 0 else annual_expenses * n_58_to_65
        PV_65_to_88 = remaining_expenses_post65 * ((1 - (1 + r)**-n_65_to_88) / r) if r != 0 else remaining_expenses_post65 * n_65_to_88
        total_SIPP = PV_58_to_65 + PV_65_to_88
        total_FIRE = PV_pre58 + total_SIPP
        results.append([r * 100, round(PV_pre58), round(total_SIPP), round(total_FIRE)])

    return pd.DataFrame(results, columns=["Growth Rate (%)", "Pre-58 Liquid (£)", "Post-58 SIPP (£)", "Total FIRE (£)"])

# Run calculation
if st.button("Calculate FIRE Requirements"):
    df = calculate_fire(liquid_assets, SIPP_assets, DB_pension, annual_expenses, growth_rate_min, growth_rate_max)
    st.write(df)

    # Display total FIRE chart
    st.line_chart(df.set_index("Growth Rate (%)")["Total FIRE (£)"], width=700, height=400)

    # Summary message
    st.write("Results show required funds at various growth rates for sustaining early retirement.")

    # Download results as CSV
    st.download_button(label='Download Results as CSV', data=df.to_csv(index=False), file_name='fire_calculator_results.csv')
