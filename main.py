import tkinter as tk
from tkinter import filedialog
import PyPDF2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

app = tk.Tk()
app.title('PDF Reader')
app.geometry("500x180")
app.config(background = "white")
lang_options = [
    "Auto","Latviski","English","Русский"
]
name_to_lang_code = {
    "Latviski":"lv",
    "English":"en",
    "Русский":"ru",
    "Auto":"auto"
}
# Settings
reading_languag = tk.StringVar() 
reading_languag.set(lang_options[0])

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
    driver.get("https://translate.google.com/?sl=" + name_to_lang_code[reading_languag.get()] + "&tl=ja")
    time.sleep(2)

    btn = driver.find_elements(By.CSS_SELECTOR, "[jsname='b3VHJd']")
    if len(btn) > 0:
        btn[0].click()
    else:
        print("Neatradam Cookie brīdinājumu. Izlaišam...")

    play_btn = driver.find_element(By.CSS_SELECTOR, "[data-tooltip-id='ucj-10']")
    input_field = driver.find_element(By.CLASS_NAME, "er8xn")

    tryToReadPage(0, pdf, play_btn, input_field)

def tryToReadPage(i, pdf, play_btn, input_field):
    print("Try " + str(i))
    if play_btn.get_attribute("data-aria-label-on") == play_btn.get_attribute("aria-label"):
        print("Wait " + str(i))
        app.after(1000, tryToReadPage, i, pdf, play_btn, input_field)
    elif i<len(pdf.pages):
        print("Read " + str(i))
        input_field.clear()
        text = pdf.pages[i].extract_text()
        input_field.send_keys(text)
        app.after(500, play_btn.click)
        print(play_btn.get_attribute("data-aria-label-on") == play_btn.get_attribute("aria-label"))
        app.after(1000, tryToReadPage, i+1, pdf, play_btn, input_field)

label_file_explorer = tk.Label(app,text = "...", width = 60, height = 3, fg = "blue") 
button_explore = tk.Button(app, text = "PDF",command = browseFiles, pady=2) 
drop_box = tk.OptionMenu(app, reading_languag, *lang_options) 
credit = tk.Label(app, text="Programmētājs: Ralfs Aizsils 231RDB026")
  
app.grid_rowconfigure([1,5], minsize=20)
app.grid_columnconfigure(1, minsize=40)
label_file_explorer.grid(column = 2, row = 2)
drop_box.grid(column=2, row=3)
button_explore.grid(column = 2, row = 4)
credit.grid(column=2, row=6)

app.mainloop()
