import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import time
from plyer import notification
import schedule
class CSV:
    CSV_FILE = 'finance_tracker.csv'
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initial_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            dataFile = pd.DataFrame(columns=cls.COLUMNS)
            dataFile.to_csv(cls.CSV_FILE, index=False)
            print("CSV file initialized with headers.")
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")
    
    @classmethod
    def view_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the specified date range.")
            return None
        else:
            print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}))
            total_income = filtered_df[filtered_df["category"] == 'Credit']["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Debit"]["amount"].sum()
            total_savings = total_income - total_expense
            print("Summary:\n")
            print(f"Total Income: Rs.{total_income}")
            print(f"Total Expense: Rs.{total_expense}")
            print(f"Total Savings: Rs.{total_savings}")

            return filtered_df

def add_me():
    CSV.initial_csv()
    date = input("Enter a date in (dd-mm-yyyy) format or select today's date: ")
    amount = input("Enter the amount: ")
    category = input("Enter the category (Credit/Debit): ")
    description = input("Enter the description: ")

    CSV.add_entry(date, amount, category, description)

def plot_transaction(df):
    df.set_index("date", inplace=True)
    income_df = df[df["category"] == "Credit"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Debit"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color='b')
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color='r')
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income V/S Expense")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"income_vs_expense_{datetime.today().strftime('%d-%m-%Y')}.png")
    print("Plot saved.")

def export_csv_to_excel(csv_file, excel_file):
    try:
        readfile=pd.read_csv(csv_file)
        readfile.to_excel(excel_file,index=False,header=True)
    except Exception as e:
        print(f"An error occurred: {e}")
def enable_reminder():
    notification.notify(
        title="Time to record your spendings!",
        message="Enter all your spendings from the day to keep a track",
        app_icon="/home/soham/python-learning/Personal finance tracker/bagofmoney_dollar_4399.png",
        timeout=10
    )

def main():
    welcome_string = "Welcome to personal finance tracker"
    print(welcome_string.center(2 * len(welcome_string), "-"))
    while True:
        print("\nSelect:\n1) Add transaction\n2) View past transactions\n3) Delete all data\n4) Export data to Excel\n5)Set reminder\n6) Exit")
        try:
            x = int(input())
            match x:
                case 1:
                    add_me()
                case 2:
                    start_date = input("Enter start date in dd-mm-yyyy format: ")
                    end_date = input("Enter end date in dd-mm-yyyy format: ")
                    df = CSV.view_transactions(start_date, end_date)
                    if df is not None and input("\nDo you want to see a plot of income vs expense (y/n)? ").lower() == 'y':
                        plot_transaction(df)
                case 3:
                    print("Warning!!! All previous data will be deleted.")
                    if input("Do you want to continue (y/n)? ").lower() == 'y':
                        header = "date,amount,category,description\n"
                        try:
                            with open(CSV.CSV_FILE, 'w') as file:
                                file.write(header)
                            print("All previous records have been deleted.")
                        except Exception as e:
                            print(f"An error occurred: {e}")
                case 4:
                    export_csv_to_excel('/home/soham/python-learning/Personal finance tracker/finance_tracker.csv','/home/soham/python-learning/Personal finance tracker/finance_tracker.xlsx')
                
                case 5:
                    default_time='10:00'
                    if input("Do you want to enable the notification on daily basis (y/n)?")=='y':
                        schedule_time=input("Enter time that you want to schedule the notification[hour:minute] format")
                        print(f"Reminde set for {schedule_time}")
                        schedule.every().day.at(schedule_time).do(enable_reminder)
                        while True:
                            schedule.run_pending()
                            time.sleep(1)
                    elif(input =='n'):
                        try:
                            days=int(input('Enter number of days after which you want to schedule the notification:'))
                            schedule.every(days).at('10:00').do(enable_reminder)
                            while True:
                                schedule.run_pending()
                                time.sleep(1)
                        except TypeError as e:
                            print(f"Invalid format. Error occured{e}")
                case 6:
                    break
                case _:
                    print("Make a valid selection.")
        except ValueError as e:
            print(e)
            print("Enter an integer value.")

if __name__ == "__main__":
    main()
'''To send the notification we must schedule it using time scheduler and the desktop notification must be scheduled using the winnotify notation'''