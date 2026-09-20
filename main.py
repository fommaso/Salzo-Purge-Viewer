from pypdf import PdfReader
import customtkinter
import re

def get_data(file):
    reader = PdfReader(file)
    page = reader.pages[0]
    text = page.extract_text()
    
    bocciatiPreTest = list(re.finditer(r'\b\d{7}\s[INS]+.[P]', text))
    NbocciatiPreTest = len(bocciatiPreTest)
    promossi = list(re.finditer(r'\b\d{7}\s\d{2}', text))
    Npromossi = len(promossi)
    totali = list(re.finditer(r'\b\d{7}', text))
    Ntotali = len(totali)
    return [NbocciatiPreTest, Npromossi, Ntotali]

def get_mean(file):
    reader = PdfReader(file)
    page = reader.pages[0]
    text = page.extract_text()

    voti = []
    promossi = list(re.finditer(r'\b\d{7}\s\d{2}', text))
    for student in promossi:
        voti.append(int(student.group()[-2:]))
    return round(sum(voti)/len(voti), ndigits=2)

# tkinter functions
def button_callback():
    given = False
    file = entry.get()
    if '.pdf' not in file:
        results = customtkinter.CTkLabel(app, text='Estensione errata, controllare che sia un file .pdf')
        results.pack(padx=20, pady=0)
        given = True
        return
    diagnostics = get_data(file)

    try:
        bocciati = diagnostics[2]-diagnostics[1]
        promossi = diagnostics[1]
        bocciati_pretest = diagnostics[0]
        totali = diagnostics[2]
        output = f"Matricole che hanno sostenuto l'esame: {totali}\nBocciati al Pretest: {round(round(bocciati_pretest/totali, 2)*100, 2)}% ({bocciati_pretest} studenti)\nBocciati dopo: {round(round((bocciati-bocciati_pretest)/totali, 2)*100, 2)}% ({bocciati-bocciati_pretest} studenti)\nTotale bocciati: {round(round(bocciati/totali, 2)*100, 2)}% ({bocciati} studenti)\nPromossi: {round(round(promossi/totali, 2)*100, 2)}% ({promossi} studenti) con un voto medio pari a: {get_mean(file)}"
        results = customtkinter.CTkLabel(app, text=output)
        results.pack(padx=20, pady=0)
    except:
        results = customtkinter.CTkLabel(app, text="C'è stato un errore con il calcolo dei dati,\ncontrollare di aver inserito il percorso giusto")
        results.pack(padx=20, pady=0)

customtkinter.set_appearance_mode("system")
app = customtkinter.CTk()
app.geometry("400x200")
app.title('Salzo Purge Viewer')

entry = customtkinter.CTkEntry(app, placeholder_text="Insert file path")
entry.pack(padx=20, pady=0)

button = customtkinter.CTkButton(app, text="Run", command=button_callback)
button.pack(padx=20, pady=20)


app.mainloop()