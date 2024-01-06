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
    # izmantojam "jsname", jo nav id un "aria-label" var atšķirties skatoties pēc pārlūkprogrammas valodas
    btn = driver.find_elements(By.CSS_SELECTOR, "[jsname='b3VHJd']")
    if len(btn) > 0:
        btn[0].click()
    else:
        print("Neatradam Cookie brīdinājumu. Izlaišam...")

    # izmantojam "data-tooltip-id", jo nav id un "aria-label" var atšķirties skatoties pēc pārlūkprogrammas valodas
    play_btn = driver.find_element(By.CSS_SELECTOR, "[data-tooltip-id='ucj-10']")
    input_field = driver.find_element(By.CLASS_NAME, "er8xn")

    tryToReadPage(0, pdf, play_btn, input_field)

def tryToReadPage(i, pdf, play_btn, input_field):
    print("Try " + str(i))
    # pārbaudam vai teksts vēl tiek atskaņots. Ja jā, tad "label-on" sakritīs ar esošo "label", un mēs pārbaudam atkal pēc sekundes
    if play_btn.get_attribute("data-aria-label-on") == play_btn.get_attribute("aria-label"):
        print("Wait " + str(i))
        app.after(1000, tryToReadPage, i, pdf, play_btn, input_field)
    elif i<len(pdf.pages):
        print("Read " + str(i))
        input_field.clear()
        text = pdf.pages[i].extract_text()
        # mēs pieņemam ka lapā parasti nav vairāk nekā 5000 simboli
        input_field.send_keys(text)
        # šis dod laiku googlai saprast ierakstītot tekstu, ja teksts ir mazs
        app.after(500, play_btn.click)
        print(play_btn.get_attribute("data-aria-label-on") == play_btn.get_attribute("aria-label"))
        app.after(5000, tryToReadPage, i+1, pdf, play_btn, input_field)

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
