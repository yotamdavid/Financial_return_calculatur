import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def calculate_investment_return(index_data, monthly_investment, start_date, end_date):

    # בחירת נתוני המדד הרלוונטיים
    index_data = index_data[['Adj Close']]

    # הגדרת 'Date' כאינדקס (אם קיים)
    if 'Date' in index_data.columns:
        index_data.set_index('Date', inplace=True)

    # בחירת נתונים לתקופה הרצויה
    index_data = index_data[(index_data.index >= start_date) & (index_data.index <= end_date)]

    # חישוב מספר החודשים
    num_months = len(index_data)

    # יצירת רשימות לאחסון נתונים
    total_shares = 0
    total_invested = 0
    transactions = []

    # ביצוע השקעה חודשית ביחס למחיר המדד בתחילת כל חודש
    for i in range(num_months):
        # בדיקה אם היום הוא היום הראשון בחודש
        if index_data.index[i].day == 1:
            # חישוב מספר המניות שנרכשו בחודש זה ביחס למחיר המדד
            shares_purchased = monthly_investment / index_data['Adj Close'].iloc[i]
            total_shares += shares_purchased
            total_invested += monthly_investment
            transactions.append((index_data.index[i], shares_purchased, index_data['Adj Close'].iloc[i]))

    # חישוב ערך תיק ההשקעות בסוף התקופה
    portfolio_value = total_shares * index_data['Adj Close'].iloc[-1]

    # חישוב התשואה
    total_return = portfolio_value - total_invested
    total_return_percentage = (total_return / total_invested) * 100

    # הדפסת תוצאות
    print(f"השקעה חודשית: {monthly_investment}")
    print(f"תקופה: {start_date} - {end_date}")
    print(f"סכום כולל שהושקע: {total_invested}")
    print(f"ערך תיק ההשקעות: {portfolio_value}")
    print(f"תשואה בכסף: {total_return}")
    print(f"תשואה באחוזים: {total_return_percentage:.2f}%")

    # יצירת גרף
    plt.plot(index_data.index, total_invested + (total_shares * index_data['Adj Close'] - total_invested).values, label="Portfolio Value")
    plt.xlabel("Date")
    plt.ylabel("Value (USD)")
    plt.legend()
    plt.show()

    # הדפסת היסטוריית עסקאות
    print("\nהיסטוריית עסקאות:")
    print("תאריך\t\t\tמספר מניות\tמחיר מנייה")
    for transaction in transactions:
        print(f"{transaction[0].strftime('%Y-%m-%d')}\t{transaction[1]:.2f}\t\t{transaction[2]:.2f}")

# הגדרת פרמטרים
monthly_investment = 2000  # השקעה חודשית
start_date = "1988-01-01"  # תאריך התחלה
end_date = "2024-3-31"  # תאריך סיום

# הורדת נתוני מדד S&P 500 (הסתרת הודעות התקדמות)
index_data = yf.download("^GSPC", start=start_date, end=end_date, progress=False)

# חישוב התשואה
calculate_investment_return(index_data, monthly_investment, start_date, end_date)
