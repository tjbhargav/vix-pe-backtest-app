import streamlit as st

st.title("📈 Compound Interest Calculator")

# Inputs
principal = st.number_input("Enter Initial Investment Amount (₹)", min_value=0.0, value=100000.0, step=1000.0, format="%.2f")
rate = st.number_input("Enter Annual Interest Rate (%)", min_value=0.0, value=8.0, step=0.1, format="%.2f")
years = st.number_input("Enter Investment Duration (Years)", min_value=1, value=10, step=1)
frequency = st.selectbox("Compounding Frequency", ["Yearly", "Half-Yearly", "Quarterly", "Monthly"])

# Frequency to n (compounding periods per year)
frequency_map = {
    "Yearly": 1,
    "Half-Yearly": 2,
    "Quarterly": 4,
    "Monthly": 12
}
n = frequency_map[frequency]

# Compound Interest Formula: A = P * (1 + r/n)^(nt)
r_decimal = rate / 100
amount = principal * (1 + r_decimal / n) ** (n * years)
interest_earned = amount - principal

# Results
st.subheader("💡 Investment Summary")
st.write(f"Future Value (Maturity Amount): ₹{amount:,.2f}")
st.write(f"Total Interest Earned: ₹{interest_earned:,.2f}")

# Optional: Visualize
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

years_list = np.arange(0, years + 1)
balance = [principal * (1 + r_decimal / n) ** (n * t) for t in years_list]

fig, ax = plt.subplots()
ax.plot(years_list, balance, marker='o', linestyle='-', color='green')
ax.set_title("Growth Over Time")
ax.set_xlabel("Years")
ax.set_ylabel("Amount (₹)")
ax.grid(True)
st.pyplot(fig)

# Show yearly gains in a table
st.subheader("📅 Yearly Growth Table")
yearly_data = pd.DataFrame({
    "Year": years_list,
    "Year-End Balance (₹)": balance,
    "Yearly Gain (₹)": np.append([0], np.diff(balance))
})
st.dataframe(yearly_data.style.format({"Year-End Balance (₹)": "₹{:,.2f}", "Yearly Gain (₹)": "₹{:,.2f}"}))

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
