import tkinter as tk
from tkinter import filedialog
import PyPDF2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

app = tk.Tk()
app.title('File Explorer')
app.geometry("500x500")
app.config(background = "white")
# Settings
wait_for_page = 1
reading_languag = "lv"

def browseFiles():
    filename = filedialog.askopenfilename(
        initialdir = "/",
        title = "Select a PDF",
        filetypes = (("PDF files","*.pdf*"),("All files","*.*"))
    )
    label_file_explorer.configure(text="Reading: " + filename)
    readPDF(PyPDF2.PdfReader(open(filename,"rb")))

def readPDF(pdf):
    service = Service()
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=option)
    driver.get("https://translate.google.com/?sl=" + reading_languag)
    time.sleep(wait_for_page)

    # Cookie brīdinājuma
    btn = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Accept all']")
    if len(btn) > 0:
        btn[0].click()
    else:
        print("Neatradam Cookie brīdinājumu. Izlaišam...")

    time.sleep(2)

    page_count = len(pdf.pages)

    for i in range(0, page_count):
        text = pdf.pages[i].extract_text()
        #print(text)



label_file_explorer = tk.Label(
    app, 
    text = "Pick a file...",
    width = 71, height = 4, 
    fg = "blue"
)
  
button_explore = tk.Button(
    app, 
    text = "Browse Files",
    command = browseFiles
) 
  
label_file_explorer.grid(column = 1, row = 1)
button_explore.grid(column = 1, row = 2)

app.mainloop()
