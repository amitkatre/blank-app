import streamlit as st

# Title
st.title("UK Property Investment Calculator (BTL Company)")

# Input section
property_price = st.number_input("Property Purchase Price (£)", value=375000)
property_type = st.selectbox("Property Type", ["Regular Buy-to-Let", "HMO"])
num_beds = st.number_input("Number of Bedrooms", min_value=1, max_value=12, value=5 if property_type == "HMO" else 1)
monthly_rent_per_room = st.number_input("Monthly Rent per Room (£)", value=750)
ltv = st.slider("Loan-to-Value (%)", min_value=50, max_value=90, value=75)
interest_rate = st.number_input("Mortgage Interest Rate (%)", value=5.0)
renovation_cost = st.number_input("HMO Renovation Cost (£)", value=25000 if property_type == "HMO" else 0)
self_managed = st.checkbox("Self-Managed?", value=True)

# Calculations
deposit = property_price * (100 - ltv) / 100
mortgage = property_price * ltv / 100
annual_interest = mortgage * interest_rate / 100

# Stamp Duty (Ltd Co surcharge)
def calculate_sdlt(price):
    brackets = [
        (1500000, 0.17),
        (925000, 0.15),
        (250000, 0.10),
        (0, 0.05),
    ]
    sdlt = 0
    for threshold, rate in brackets:
        if price > threshold:
            sdlt += (price - threshold) * rate
            price = threshold
    return sdlt

stamp_duty = calculate_sdlt(property_price)
annual_rent = monthly_rent_per_room * num_beds * 12
management_fee = 0 if self_managed else annual_rent * 0.10

# Other fixed costs
utilities = 4000 if property_type == "HMO" else 0
insurance = 500
maintenance = 1000
accounting = 750
misc = 1000

total_operating_costs = sum([management_fee, utilities, insurance, maintenance, accounting, misc])
total_upfront = deposit + stamp_duty + renovation_cost + 2000 + 1500  # mortgage/legal fees
net_profit_before_tax = annual_rent - annual_interest - total_operating_costs
corp_tax = net_profit_before_tax * 0.19 if net_profit_before_tax > 0 else 0
net_profit_after_tax = net_profit_before_tax - corp_tax
gross_yield = (annual_rent / property_price) * 100
net_yield = (net_profit_after_tax / total_upfront) * 100

# Results
st.subheader("Results")
st.write(f"**Stamp Duty:** £{stamp_duty:,.2f}")
st.write(f"**Deposit:** £{deposit:,.2f}")
st.write(f"**Mortgage Amount:** £{mortgage:,.2f}")
st.write(f"**Annual Rent:** £{annual_rent:,.2f}")
st.write(f"**Total Operating Costs:** £{total_operating_costs:,.2f}")
st.write(f"**Net Profit (Before Tax):** £{net_profit_before_tax:,.2f}")
st.write(f"**Corporation Tax (19%):** £{corp_tax:,.2f}")
st.write(f"**Net Profit (After Tax):** £{net_profit_after_tax:,.2f}")
st.write(f"**Gross Yield:** {gross_yield:.2f}%")
st.write(f"**Net Yield (After Tax):** {net_yield:.2f}%")