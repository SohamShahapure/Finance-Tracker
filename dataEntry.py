from datetime import datetime
date_format=("%d-%m-%Y")
CATEGORIES={'C':'Credit',"D":'Debit'}
def get_date(prompt,allowed_default=False):
    date_str=input(prompt)
     
    if allowed_default and not date_str:
       return datetime.today().strftime(date_format)
    try:
        #This method validates the date
        valid_date=datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. please input in the format dd-mm--yyyy")
        #using recursion
        return get_date(prompt,allowed_default)
def get_amount():
    try:
        amount=float(input("Enter the amount: "))
        if amount<=0:
            raise ValueError("Amount must be non-negative , non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    
def get_category():
    cat_input=input("Enter category: (C) for Credit & (D) for Debit: ").upper()
    if cat_input in CATEGORIES:
        return CATEGORIES[cat_input]
    else:
        print("Invalid category. Enter (C) for credit and (D) for debit")
        return get_category()
def get_description():
    return input("Enter a description(optional)")


