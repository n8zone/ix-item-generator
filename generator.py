import tkinter as tk
import re

window = tk.Tk()
window.geometry("700x480")

variable_fields = []
numeric_fields = []
raw_variables = []
numeric_variables = []
content = ""

VARIABLE_PATTERN = r"ITEM\.\w+\s*="
NUMERIC_VARIABLE_PATTERN = r"ITEM\.\w+\s*#="
def stripToVariables(strings, pattern):
    return re.findall(pattern, strings)

def GetTemplate():
    with open("template_clothes.txt", "r") as template_file:
        template = template_file.read()
        return template
    

def clean_fields():
    for entry in variable_fields:
        entry.delete(0,tk.END)
    
    for entry in numeric_fields:
        entry.delete(0,tk.END)

def clean_content():
    global content
    content = GetTemplate()

def button_click():
    global ingredients
    global results
    global content
    print("Button clicked!")
    i = 0
    for entry in variable_fields:
        content = content.replace(raw_variables[i], raw_variables[i] + " " + "'" + entry.get() + "'")
        i += 1
    print(content)

    i = 0
    for entry in numeric_fields:
        content = content.replace(numeric_variables[i], numeric_variables[i].replace("#","") + " " + entry.get())
        i += 1
    print(content)


    with open(f"sh_{variable_fields[0].get().lower().replace(' ', '_')}.lua", "w") as new_file:
        new_file.write(content)

    clean_fields()
    clean_content()



def generateFields():
    global content
    global variable_fields
    global raw_variables
    global numeric_variables
    template = GetTemplate()
    content = template
    raw_variables = stripToVariables(template, VARIABLE_PATTERN)
    numeric_variables = stripToVariables(template, NUMERIC_VARIABLE_PATTERN)
    variables = []


    
    for s in raw_variables:
        s = s.replace("ITEM.", "")
        s = s.replace("=", "")
        s = s.strip()
        variables.append(s)


    for s in variables:
        label = nameLabel = tk.Label(window, text=s)
        label.pack()
        entry = tk.Entry(window, width=40)
        entry.pack()
        variable_fields.append(entry)
    

    for s in numeric_variables:
        label = tk.Label(window, text=s.replace("ITEM.","").replace("=","").strip())
        label.pack()
        entry = tk.Entry(window, width=40)
        entry.pack()
        numeric_fields.append(entry)


generateFields()

button = tk.Button(window, text="Create", command=button_click)
button.pack()

window.mainloop()