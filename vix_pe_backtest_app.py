# Streamlit Web App for VIX + PE Backtest Strategy

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Backtest Strategy Function
def backtest_strategy(df):
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
    except Exception as e:
        st.error("Date conversion failed. Make sure 'Date' column is in YYYY-MM-DD format.")
        return pd.DataFrame(), 0, 0

    required_columns = {'Date', 'Nifty_Close', 'VIX', 'Nifty_PE'}
    if not required_columns.issubset(df.columns):
        st.error(f"Missing columns in CSV. Required columns: {', '.join(required_columns)}")
        return pd.DataFrame(), 0, 0

    trades = []
    holding = False
    entry_price, entry_date = None, None

    for i in range(len(df)):
        row = df.iloc[i]

        try:
            if not holding and row['VIX'] <= 14 or row['Nifty_PE'] <= 23:
                entry_price = row['Nifty_Close']
                entry_date = row['Date']
                holding = True

            elif holding:
                holding_period = (row['Date'] - entry_date).days
                exit_conditions = (
                    row['VIX'] >= 19 or 
                    row['Nifty_PE'] >= 23 or 
                    #holding_period >= 15
                )

                if exit_conditions:
                    exit_price = row['Nifty_Close']
                    exit_date = row['Date']
                    return_pct = ((exit_price - entry_price) / entry_price) * 100

                    trades.append({
                        'Entry Date': entry_date,
                        'Exit Date': exit_date,
                        'Entry Price': entry_price,
                        'Exit Price': exit_price,
                        'Return (%)': return_pct
                    })

                    holding = False
        except Exception as e:
            st.warning(f"Error processing row {i}: {e}")
            continue

    results = pd.DataFrame(trades)
    win_rate = (results['Return (%)'] > 0).mean() * 100 if not results.empty else 0
    avg_return = results['Return (%)'].mean() if not results.empty else 0

    return results, win_rate, avg_return

# Plotting Function
def plot_trades(df, trades):
    try:
        plt.figure(figsize=(14, 6))
        plt.plot(df['Date'], df['Nifty_Close'], label='Nifty Close', color='blue')

        for _, trade in trades.iterrows():
            plt.axvline(trade['Entry Date'], color='green', linestyle='--', alpha=0.6, label='Entry' if _ == 0 else '')
            plt.axvline(trade['Exit Date'], color='red', linestyle='--', alpha=0.6, label='Exit' if _ == 0 else '')

        plt.title('Nifty Trades Based on VIX + PE Strategy')
        plt.xlabel('Date')
        plt.ylabel('Nifty Close Price')
        plt.legend()
        plt.tight_layout()
        plt.grid(True)
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Plotting failed: {e}")

# Streamlit App
st.title("VIX + Nifty PE Based Backtest Strategy")

uploaded_file = st.file_uploader("Upload CSV File with columns: Date, Nifty_Close, VIX, Nifty_PE", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview:")
        st.dataframe(df.head())

        results, win_rate, avg_return = backtest_strategy(df)

        if not results.empty:
            st.subheader("Trade Results")
            st.dataframe(results)

            st.markdown(f"**Win Rate:** {win_rate:.2f}%")
            st.markdown(f"**Average Return per Trade:** {avg_return:.2f}%")

            st.subheader("Nifty Chart with Entry/Exit Points")
            plot_trades(df, results)
        else:
            st.warning("No trades were triggered based on current strategy and uploaded data.")

    except Exception as e:
        st.error(f"Failed to process the uploaded file: {e}")
else:
    st.info("Please upload a properly formatted CSV file to run the strategy.")
