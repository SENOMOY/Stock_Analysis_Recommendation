from tkinter import *
from tkinter import messagebox
import pandas as pd
import tkinter as tk
from data.Company_Data import getCompanyData
from report.GenerateReport import generateReport
import string

root = Tk()
root.title("Stock Analysis & Prediction")

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.pack(pady=100, padx=200)

# Create country tkinter variable
country_tnktr = StringVar(root)
# Set the default option
country_tnktr.set('Select Country')
# Country options
country = getCompanyData([], []).sort_values('Country',ascending=True)['Country'].dropna().unique()
# Create country option menu
popupMenu1 = OptionMenu(mainframe, country_tnktr, *country)
popupMenu1.config(width=13, indicatoron=0, padx=10)
Label(mainframe, text="Country").grid(row=1, column=1)
popupMenu1.grid(row=2, column=1)

# Create exchange tkinter variable
exchange_tnktr = StringVar(root)
# Set the default option
exchange_tnktr.set('Select Exchange')
# Create exchange option menu
popupMenu2 = OptionMenu(mainframe, exchange_tnktr, '')
popupMenu2.config(width=13, indicatoron=0, padx=10, state=DISABLED)
Label(mainframe, text="Exchange").grid(row=1, column=2)
popupMenu2.grid(row=2, column=2)

# Create alphabet tkinter variable
alphabet_tnktr = StringVar(root)
# Set the default option
alphabet_tnktr.set('A-Z')
# Create alphabet option menu
popupMenu3 = OptionMenu(mainframe, alphabet_tnktr, '')
popupMenu3.config(width=3, indicatoron=0, padx=10, state=DISABLED)
Label(mainframe, text="A-Z").grid(row=1, column=3)
popupMenu3.grid(row=2, column=3)


# Create company tkinter variable
company_tnktr = StringVar(root)
# Set the default option
company_tnktr.set('Select Company')
# Create exchange option menu
popupMenu4 = OptionMenu(mainframe, company_tnktr, '')
popupMenu4.config(width=20, indicatoron=0, padx=10, state=DISABLED)
Label(mainframe, text="Company").grid(row=1, column=4)
popupMenu4.grid(row=2, column=4)


def resetOptions(menu, tnktr, msg):
    menu['menu'].delete(0, 'end')
    tnktr.set(msg)

def getAdvisory():
    company_list = getCompanyData([country_tnktr.get()],[exchange_tnktr.get()]).sort_values('Country',ascending=True)
    company_ticker = company_list.loc[(company_list['Name'].isin([company_tnktr.get()]))]['Ticker'] \
        .dropna().unique()[0]
    messagebox.showinfo('','Running Stock Advisory for '+company_tnktr.get()+' from ' + exchange_tnktr.get()
                        + ' exchange of ' + country_tnktr.get())
    generateReport(company_ticker, company_tnktr.get())
    resetOptions(popupMenu2, exchange_tnktr, 'Select Exchange')
    resetOptions(popupMenu3, alphabet_tnktr, 'A-Z')
    resetOptions(popupMenu4, company_tnktr, 'Select Company')
    popupMenu2.config(state=DISABLED)
    popupMenu3.config(state=DISABLED)
    popupMenu4.config(state=DISABLED)
    advisory_button.config(state=DISABLED)

advisory_button = Button(mainframe, text="Get Advisory", state=DISABLED, command=getAdvisory, bg="black", fg="white")
advisory_button.grid(row=5, column=2)

# on change dropdown value
def enableExchange(*args):
    resetOptions(popupMenu2, exchange_tnktr, 'Select Exchange')
    exchange_tnktr.set('Select Exchange')
    exchange = getCompanyData([country_tnktr.get()],[]).sort_values('Exchange',ascending=True)['Exchange'] \
        .dropna().unique()
    popupMenu2.config(state=NORMAL)
    popupMenu3.config(state=DISABLED)
    popupMenu4.config(state=DISABLED)
    advisory_button.config(state=DISABLED)
    for value in exchange:
        popupMenu2['menu'].add_command(label=value, command=tk._setit(exchange_tnktr, value))

def enableAlphabetOptions(*args):
    resetOptions(popupMenu3, alphabet_tnktr, 'A-Z')
    alphabet_tnktr.set('A-Z')
    alphabets = list(string.ascii_uppercase)
    popupMenu3.config(state=NORMAL)
    popupMenu4.config(state=DISABLED)
    for value in alphabets:
        popupMenu3['menu'].add_command(label=value, command=tk._setit(alphabet_tnktr, value))

# on change dropdown value
def enableCompany(*args):
    resetOptions(popupMenu4, company_tnktr, 'Select Company')
    company_tnktr.set('Select Company')
    company = getCompanyData([country_tnktr.get()],[exchange_tnktr.get()]).sort_values('Name',ascending=True)['Name'] \
        .dropna().unique()
    company_srs = pd.Series(company)
    company_srs = company_srs.loc[company_srs.str.startswith(alphabet_tnktr.get(), na=False)]
    popupMenu4.config(state=NORMAL)
    advisory_button.config(state=DISABLED)
    for value in company_srs:
        popupMenu4['menu'].add_command(label=value, command=tk._setit(company_tnktr, value))

def enableButton(*args):
    advisory_button.config(state=NORMAL)

# link function to change country dropdown
country_tnktr.trace('w', enableExchange)
exchange_tnktr.trace('w', enableAlphabetOptions)
alphabet_tnktr.trace('w',enableCompany)
company_tnktr.trace('w', enableButton)

root.mainloop()
