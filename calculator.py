import streamlit as st
import math

# Custom styles for the app
st.markdown("""
<style>
    /* Base styles */
    .css-1xi51a1 {
        font-size: 18px;
    }
    .css-1cpxqw2 {
        font-size: 20px;  /* Bigger text on slider labels */
    }
    .stSlider .css-14f6t7n {
        height: 1.5rem !important;  /* Increase size of slider track */
    }
    .stSlider .css-1cpxqw2 {
        font-size: 22px !important;  /* Larger font for slider labels */
    }
    .stSlider .st-ae .css-1xgk5py {  /* Increase size of slider handle */
        height: 1.5rem !important;
        width: 1.5rem !important;
    }
    .st-de {
        background-color: #02006c !important;  /* Change slider handle to blue */
    }
    .st-dh {
        background-color: #ccd6f6 !important;  /* Change slider track to blue */
    }
</style>
""", unsafe_allow_html=True)

# Function to format the slider value with commas and dollar sign
def format_dollar_value(value):
    return f"${value:,}"

# Title of the app
st.title('Contract Manager Pricing Estimator')

# Blurb at the top of the page
st.markdown("""
Interested in Contract Manager for your organization? Just move the sliders below to best reflect the revenue and contract demands of your organization, and we'll give you some ballpark pricing. **NOTE:** All estimates are purely for informational purposes; actual customized pricing will likely vary once we understand the nuances of your specific situation.
""")

# User inputs using sliders
annual_revenue = st.slider('Select your annual revenue (USD):', min_value=10000000, max_value=1000000000, step=10000000)

# Display formatted annual revenue
st.markdown(f"**Annual Revenue (USD):** {format_dollar_value(annual_revenue)}")

annual_contract_volume = st.slider('Select your annual number of contracts:', min_value=10, max_value=500, step=20)
average_pages_per_contract = st.slider('Select average pages per contract:', min_value=10, max_value=250, step=25)

# Button to calculate pricing
if st.button('Calculate Pricing'):
    # Calculation of Base Fee using log regression
    fee_percent = -0.0000194472 * math.log(annual_revenue) + 0.0004408921
    base_fee = annual_revenue * fee_percent
    
    # PLL Costs and Variable Costs
    pll_costs = base_fee * 0.20
    variable_costs = base_fee * 0.39 * (annual_contract_volume * average_pages_per_contract * 0.001)

    # Foundation Fee calculation
    foundation_fee = base_fee + pll_costs + variable_costs

    # Calculating further tiers
    framework_fee = foundation_fee * 1.4
    pinnacle_fee = framework_fee * 1.4

    # Display the formatted results
    st.markdown(f'Thank you for your interest in Contract Manager. Based on the inputs you\'ve provided, a ballpark estimate for your organization is:', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output">Foundation Tier annual pricing is: <span class="dollar">${foundation_fee:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output">Framework Tier annual pricing is: <span class="dollar">${framework_fee:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output">Pinnacle Tier annual pricing is: <span class="dollar">${pinnacle_fee:,.2f}</span></div>', unsafe_allow_html=True)

# Run this with `streamlit run this_script.py`
