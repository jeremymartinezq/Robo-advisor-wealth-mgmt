# Summary: Robo-Advisor Python Code

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np


# Function to calculate life expectancy
def calculate_life_expectancy(age, gender):
    life_expectancy_table = {
        "male": {35: 79.2, 40: 78.0, 45: 76.8, 50: 75.4},
        "female": {35: 82.0, 40: 81.0, 45: 79.8, 50: 78.4}
    }
    if gender.lower() not in life_expectancy_table:
        return None
    nearest_age = min(life_expectancy_table[gender.lower()].keys(), key=lambda x: abs(x - age))
    return life_expectancy_table[gender.lower()][nearest_age]


# Function to calculate years left
def calculate_years_left(age, gender):
    life_expectancy = calculate_life_expectancy(age, gender)
    if life_expectancy:
        return life_expectancy - age
    return None


# Function to get asset allocation based on years left
def get_asset_allocation(years_left):
    if years_left >= 30:
        return {"Stocks": 80, "Bonds": 10, "Real Estate": 5, "Cash": 5}
    elif 20 <= years_left < 30:
        return {"Stocks": 70, "Bonds": 20, "Real Estate": 5, "Cash": 5}
    elif 10 <= years_left < 20:
        return {"Stocks": 60, "Bonds": 30, "Real Estate": 5, "Cash": 5}
    elif 5 <= years_left < 10:
        return {"Stocks": 50, "Bonds": 40, "Real Estate": 5, "Cash": 5}
    else:
        return {"Stocks": 30, "Bonds": 50, "Real Estate": 10, "Cash": 10}


# Function to fetch top performing stocks, bonds, and real estate from Yahoo Finance
def get_investment_recommendations():
    recommended_stocks = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN"]
    recommended_bonds = ["BND", "LQD", "GOVT", "JNK"]
    recommended_real_estate = ["O", "AMT", "PLD", "PSA"]

    stocks_data = yf.download(recommended_stocks, period="1y")['Adj Close']
    bonds_data = yf.download(recommended_bonds, period="1y")['Adj Close']
    real_estate_data = yf.download(recommended_real_estate, period="1y")['Adj Close']

    # Example of processing data to get top performers
    stock_performance = stocks_data.pct_change().mean().nlargest(3)
    bond_performance = bonds_data.pct_change().mean().nlargest(3)
    real_estate_performance = real_estate_data.pct_change().mean().nlargest(3)

    return stock_performance.index.tolist(), bond_performance.index.tolist(), real_estate_performance.index.tolist()


# Function to visualize asset allocation
def visualize_asset_allocation(asset_allocation):
    labels = list(asset_allocation.keys())
    sizes = list(asset_allocation.values())
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']
    explode = (0.1, 0, 0, 0)  # explode the 1st slice (Stocks)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Asset Allocation Strategy')
    plt.show()


def visualize_glide_path():
    years_before_retirement = np.arange(-40, 30, 1)  # -40 years to 30 years
    equity = np.clip(100 - (2 * (years_before_retirement + 40)), 25, 95)  # Equity allocation
    fixed_income = 100 - equity  # Fixed income allocation

    plt.figure(figsize=(10, 6))

    # Plot the equity and fixed income allocations as filled areas
    plt.fill_between(years_before_retirement, equity, color="lightblue", label="Equity (Stocks)", alpha=0.6)
    plt.fill_between(years_before_retirement, 0, fixed_income, color="lightcoral", label="Fixed Income (Bonds)",
                     alpha=0.6)

    # Add dashed trend lines for equity and fixed income allocations
    plt.plot(years_before_retirement, equity, color="darkblue", linestyle='--', linewidth=2, label="Equity Trend Line")
    plt.plot(years_before_retirement, fixed_income, color="red", linestyle='--', linewidth=2,
             label="Fixed Income Trend Line")

    # Add a vertical line to indicate the retirement target date
    plt.axvline(x=0, color="black", linestyle="--", label="Retirement Target Date")

    # Add chart labels and title
    plt.title('Glide Path Asset Allocation Over Time')
    plt.xlabel('Years Relative to Retirement')
    plt.ylabel('Asset Allocation (%)')

    # Annotate key points on the glide path
    plt.text(-40, 95, "95% Equity", va='center', ha='right', fontsize=10, color='blue')
    plt.text(-40, 25, "5% Bonds", va='center', ha='right', fontsize=10, color='red')
    plt.text(30, 30, "30% Equity", va='center', ha='left', fontsize=10, color='blue')
    plt.text(30, 70, "70% Bonds", va='center', ha='left', fontsize=10, color='red')

    # Calculate intersection point (where equity and fixed income are both 50%)
    intersection_x = -20  # At 20 years before retirement
    intersection_y = 50  # 50% allocation for both

    # Annotate the intersection point with stacked labels
    label_text = "50%\nBonds\n50%\nEquity"
    plt.text(intersection_x, intersection_y, label_text,
             va='center', ha='center', fontsize=10, color='black')

    # Plot grid and show the legend
    plt.grid(True)
    plt.legend(loc='upper right')

    # Display the glide path plot
    plt.show()


# Function to handle the submission of the quiz
def submit():
    try:
        age = int(age_entry.get())
        gender = gender_entry.get().strip().lower()
        current_income = float(income_entry.get())
        retirement_age = int(retirement_age_entry.get())
        married = married_var.get()
        spouse_income = float(spouse_income_entry.get()) if married == "Yes" else 0
        kids = int(kids_entry.get())
        target_savings = float(target_savings_entry.get())
        owns_house = house_var.get()

        if gender not in ['male', 'female']:
            raise ValueError("Invalid gender")

        years_left = calculate_years_left(age, gender)

        if years_left is None:
            messagebox.showerror("Error", "Invalid age or gender")
            return

        asset_allocation = get_asset_allocation(years_left)

        # Get investment recommendations
        recommended_stocks, recommended_bonds, recommended_real_estate = get_investment_recommendations()

        result_text = (f"You have approximately {years_left:.1f} years left to live.\n\n"
                       f"Current Income: ${current_income:,.2f}\n"
                       f"Retirement Age: {retirement_age}\n"
                       f"Married: {married}\n"
                       f"Spouse's Income: ${spouse_income:,.2f}\n"
                       f"Number of Kids: {kids}\n"
                       f"Target Retirement Savings: ${target_savings:,.2f}\n"
                       f"Owns/Plans to Buy a House: {owns_house}\n\n"
                       "Suggested Asset Allocation:\n")

        for asset, percentage in asset_allocation.items():
            result_text += f"{asset}: {percentage}%\n"

        result_text += "\nRecommended Stocks:\n" + "\n".join(recommended_stocks) + "\n"
        result_text += "\nRecommended Bonds:\n" + "\n".join(recommended_bonds) + "\n"
        result_text += "\nRecommended Real Estate Investments:\n" + "\n".join(recommended_real_estate) + "\n"

        messagebox.showinfo("Results", result_text)

        # Visualize the asset allocation
        visualize_asset_allocation(asset_allocation)

        # Visualize the glide path allocation
        visualize_glide_path()

    except ValueError as e:
        messagebox.showerror("Input Error", "Please enter valid inputs for all fields.")


# Initialize the main Tkinter window
root = tk.Tk()
root.title("Retirement Planning Robo-advisor")
root.geometry("500x600")

# Create labels and entry fields for all questions
tk.Label(root, text="Enter your age:").pack(pady=5)
age_entry = tk.Entry(root)
age_entry.pack(pady=5)

tk.Label(root, text="Enter your gender (male/female):").pack(pady=5)
gender_entry = tk.Entry(root)
gender_entry.pack(pady=5)

tk.Label(root, text="What is your current income?").pack(pady=5)
income_entry = tk.Entry(root)
income_entry.pack(pady=5)

tk.Label(root, text="At what age do you want to retire?").pack(pady=5)
retirement_age_entry = tk.Entry(root)
retirement_age_entry.pack(pady=5)

tk.Label(root, text="Are you married?").pack(pady=5)
married_var = tk.StringVar(value="No")
tk.Radiobutton(root, text="Yes", variable=married_var, value="Yes").pack()
tk.Radiobutton(root, text="No", variable=married_var, value="No").pack()

tk.Label(root, text="If married, what is your spouse's income?").pack(pady=5)
spouse_income_entry = tk.Entry(root)
spouse_income_entry.pack(pady=5)

tk.Label(root, text="How many kids do you (or plan to) have?").pack(pady=5)
kids_entry = tk.Entry(root)
kids_entry.pack(pady=5)

tk.Label(root, text="What is your target retirement savings amount?").pack(pady=5)
target_savings_entry = tk.Entry(root)
target_savings_entry.pack(pady=5)

tk.Label(root, text="Do you own a house (or plan to buy one)?").pack(pady=5)
house_var = tk.StringVar(value="No")
tk.Radiobutton(root, text="Yes", variable=house_var, value="Yes").pack()
tk.Radiobutton(root, text="No", variable=house_var, value="No").pack()

# Submit button to trigger the quiz calculation
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
