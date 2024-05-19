import streamlit as st
import math
import smtplib, ssl
from email.mime.text import MIMEText


# Custom styles for the app
st.markdown("""
<style>
    /* Base styles */
    .dollar {
        font-weight: bold;
    }
    .dollar-total {
        font-size: 24px; 
    }
    text-sml {
        font-size: 2px;
        color: red;       
    }
    .pl10 {
        padding-left: 10px;
    }            
    .pt10 {
        padding-top: 10px;
    }          
    .pt20 {
        padding-top: 20px;
    }
    .pt40 {
        padding-top: 40px;
    }
    .pb10 {
        padding-bottom: 10px;
    }                 
    .pb20 {
        padding-bottom: 20px;
    }
    .pb40 {
        padding-bottom: 40px;
    }
    .results-title {
        color: #02006c;
        font-size: 140%;           
    }
    .results-total {
        color: #02006c;
        font-weight: bold;
        background-color: #ccd6f6
    }
</style>
""", unsafe_allow_html=True)

# Function to format the slider value with commas and dollar sign
def format_dollar_value(value):
    return f"${value:,}"

# Title of the app
st.title('Contract Manager Pricing Estimator')
st.caption('v003')

# Blurb at the top of the page
st.markdown("""
Are you interested in hiring a Contract Manager for your organization? Just move the sliders below to best reflect your organization's revenue and contract demands, and we'll give you some ballpark pricing.""")
st.caption("""
**NOTE:** All estimates are purely for informational purposes; customized pricing will likely vary once we understand the nuances of your specific situation.           
""")
st.markdown(f'<div class="pb40"></div>', unsafe_allow_html=True)

# User inputs using sliders
annual_revenue = st.slider('Select your annual revenue (USD):', min_value=10000000, max_value=1000000000, step=10000000)

# Display formatted annual revenue
st.markdown(f"**Annual Revenue (USD):** {format_dollar_value(annual_revenue)}")

annual_contract_volume = st.slider('Select your annual number of contracts:', min_value=10, max_value=500, step=20)
average_pages_per_contract = st.slider('Select average pages per contract:', min_value=10, max_value=250, step=25)

# Button to calculate pricing
if st.button('Calculate Pricing'):
    price_max = 2000000000
    fee_percent = -0.0000194472 * math.log(annual_revenue) + 0.0004408921
    discount = .10
    setup_costs = 8500

    # Base Fee
    if annual_revenue > price_max:
	    base_fee = annual_revenue * price_max
    else:
        base_fee = max(9500, annual_revenue * fee_percent)

    base_fee = math.trunc(base_fee)

    # Variable Costs

    # Litera License
    if base_fee < 21000:
	    litera_license = 500
    elif base_fee in range(21001, 50000):
	    litera_license = 2000
    else:
	    litera_license = 4000
         
    litera_license = math.trunc(litera_license)

    #CIDA MS Azure
    cida_ms_azure = (annual_contract_volume * average_pages_per_contract * .15)

    #first_rule
    first_rule = (base_fee * .20)

    #Variable Costs Total
    variable_costs = round(math.trunc(litera_license + cida_ms_azure + first_rule), -1) 

    #Total Discount
    total_discount = math.trunc(base_fee * .10 + first_rule * discount)


    # Caculate Teir Base 
    foundation_base = round(math.trunc(base_fee + variable_costs - total_discount))
    framework_base = round(math.trunc(foundation_base * 1.49))
    pinnacle_base = round(math.trunc(foundation_base * 1.95) -4) #FIGURE A BETTER WAY TO ROUND THIS


    # PLL Costs
    if base_fee < 7500:
        pll_costs = 1650 #CHANGE TO 1650
    elif base_fee in range(7501, 20000):
        pll_costs = base_fee * .20
    elif base_fee in range(20001, 45000):
        pll_costs = base_fee * .175
    elif base_fee in range(45001, 150000):
        pll_costs = base_fee * .15
    else:
        pll_costs = base_fee * .125
        
    pll_costs = math.trunc(pll_costs - pll_costs * discount)

    # PLL Costs Framework
    if framework_base < 7500:
        pll_costs_framework = 1500 #CHANGE TO 1650
    elif framework_base in range(7501, 20000):
        pll_costs_framework = framework_base * .20
    elif framework_base in range(20001, 45000):
        pll_costs_framework = framework_base * .175
    elif framework_base in range(45001, 150000):
        pll_costs_framework = framework_base * .15
    else:
        pll_costs_framework = framework_base * .125

    pll_costs_framework = math.trunc(pll_costs_framework)

    # PLL Costs Pinnacle
    if pinnacle_base < 7500:
        pll_costs_pinnacle = 1500 #CHANGE TO 1650
    elif pinnacle_base in range(7501, 20000):
        pll_costs_pinnacle = pinnacle_base * .20
    elif pinnacle_base in range(20001, 45000):
        pll_costs_pinnacle = pinnacle_base * .175
    elif pinnacle_base in range(45001, 150000):
        pll_costs_pinnacle = pinnacle_base * .15
    else:
        pll_costs_pinnacle = pinnacle_base * .125
        
    pll_costs_pinnacle = math.trunc(pll_costs_pinnacle)

    # Teir Total calculation
    foundation_total = round(foundation_base + pll_costs, -1) #removed " + setup_costs"
    framework_total = round(framework_base + pll_costs_framework, -1)
    pinnacle_total = round(pinnacle_base + pll_costs_pinnacle, -1)

    st.markdown(f'<div class="pb40"></div>', unsafe_allow_html=True)

    # Display the formatted results
    st.markdown(f'<div class="pt40 pb40">Thank you for your interest in Contract Manager. Based on the inputs you\'ve provided, a ballpark estimate for your organization is:</div>', unsafe_allow_html=True)

    # Taking inputs
    cmcc_user = st.text_input('Full Name')
    cmcc_company = st.text_input('Company')
    st.markdown(f'<div class="pb20"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output results-title">Foundation Tier Annual Pricing</div>', unsafe_allow_html=True)   
    st.markdown(f'<div class="pricing-output">Base License: <span class="dollar">${foundation_base:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output">Preferred Language Library: <span class="dollar">${pll_costs:,.2f}</span></div>', unsafe_allow_html=True)
    #st.markdown(f'<div class="pricing-output pb10">Implementation Costs: <span class="dollar">${setup_costs:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output results-total pl10">Total: <span class="dollar-total">${foundation_total:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pb20"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output results-title">Framework Tier Annual Pricing </div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output">Base License: <span class="dollar">${framework_base:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output">Preferred Language Library: <span class="dollar">${pll_costs_framework:,.2f}</span></div>', unsafe_allow_html=True)
    #st.markdown(f'<div class="pricing-output pb10">Implementation Costs: <span class="dollar">${setup_costs:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output results-total pl10">Total: <span class="dollar-total">${framework_total:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pb20"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output results-title">Pinnacle Tier Annual Pricing </div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output">Base License: <span class="dollar">${pinnacle_base:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output">Preferred Language Library: <span class="dollar">${pll_costs_pinnacle:,.2f}</span></div>', unsafe_allow_html=True)
    #st.markdown(f'<div class="pricing-output pb10">Implementation Costs: <span class="dollar">${setup_costs:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pricing-output results-total pl10">Total: <span class="dollar-total">${pinnacle_total:,.2f}</span></div>', unsafe_allow_html=True)

    st.balloons()

    email_sender = "cmcc@webclops.com"
    email_receiver = "cmcc@webclops.com"
    subject = "CMCC Project Estimator"
    body = "Hello"
    password = "rewards26rg"

    try:
        msg = MIMEText(body)
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject

        server = smtplib.SMTP('mail.webclops.com', 465)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()
        st.success('Email sent successfully! 🚀')
    except Exception as e:
        st.error(f"Failed to send email: {e}")  


# Run this with `streamlit run this_script.py`