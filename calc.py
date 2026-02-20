import customtkinter as ctk
import math
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Calculator")
app.geometry("520x740")

tabview = ctk.CTkTabview(app, width=500, height=650)
tabview.pack(padx=10, pady=(10, 0))

tab_standard = tabview.add("Standard")
tab_scientific = tabview.add("Scientific")
tab_converter = tabview.add("Converter")


def update_status(message=""):
    """Update the status bar with current mode and optional message."""
    mode_text = ""
    if tabview.get() == "Scientific":
        mode_text = f"Mode: {mode_var.get()}"
    status_text = mode_text + (f" | {message}" if message else "")
    status_label.configure(text=status_text)

def safe_eval(expr):
    """Evaluate expression in a restricted environment with math available."""
    allowed_globals = {"math": math}
    return eval(expr, {"__builtins__": {}}, allowed_globals)

# ---------- STANDARD TAB ----------
entry_std = ctk.CTkEntry(tab_standard, width=460, height=50, font=("Arial", 20), justify="right")
entry_std.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

def click_std(value):
    entry_std.insert("end", value)
    update_status()

def clear_std():
    entry_std.delete(0, "end")
    update_status()

def evaluate_std():
    expr = entry_std.get().strip()
    if not expr:
        update_status("Nothing to evaluate")
        return
    try:
        
        expr_eval = expr.replace("^", "**")
        result = safe_eval(expr_eval)
        entry_std.delete(0, "end")
        entry_std.insert(0, str(result))
        update_status("OK")
    except SyntaxError:
        entry_std.delete(0, "end"); entry_std.insert(0, "Invalid Expression")
        update_status("Invalid Expression")
    except NameError:
        entry_std.delete(0, "end"); entry_std.insert(0, "Unknown Name")
        update_status("Unknown Name")
    except ZeroDivisionError:
        entry_std.delete(0, "end"); entry_std.insert(0, "Division by Zero")
        update_status("Division by Zero")
    except Exception:
        entry_std.delete(0, "end"); entry_std.insert(0, "Error")
        update_status("Error")

buttons_std = [
    ("7",1,0),("8",1,1),("9",1,2),("/" ,1,3),
    ("4",2,0),("5",2,1),("6",2,2),("*" ,2,3),
    ("1",3,0),("2",3,1),("3",3,2),("-" ,3,3),
    ("0",4,0),("." ,4,1),("=" ,4,2),("+" ,4,3),
]
for (text,row,col) in buttons_std:
    cmd = evaluate_std if text=="=" else lambda t=text: click_std(t)
    ctk.CTkButton(tab_standard, text=text, width=100, height=60, command=cmd).grid(row=row, column=col, padx=5, pady=5)

ctk.CTkButton(tab_standard, text="Clear", width=460, height=50, fg_color="#ff6666", command=clear_std).grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# ---------- SCIENTIFIC TAB ----------
entry_sci = ctk.CTkEntry(tab_scientific, width=460, height=50, font=("Arial", 20), justify="right")
entry_sci.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

mode_var = ctk.StringVar(value="Degrees")
mode_switch = ctk.CTkOptionMenu(tab_scientific, values=["Degrees", "Radians"], variable=mode_var, width=200)
mode_switch.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

def on_mode_change(*args):
    update_status()
mode_var.trace_add("write", on_mode_change)

def click_sci(value):
    entry_sci.insert("end", value)
    update_status()

def clear_sci():
    entry_sci.delete(0, "end")
    update_status()

def backspace_sci():
    current = entry_sci.get()
    if current:
        entry_sci.delete(len(current)-1, "end")
    update_status()

def evaluate_sci():
    expr = entry_sci.get().strip()
    if not expr:
        update_status("Nothing to evaluate")
        return
    try:
        expr = expr.replace("√", "math.sqrt")
        expr = expr.replace("^", "**")
        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("x²", "**2")
        expr = expr.replace("exp", "math.exp")
        expr = expr.replace("ln", "math.log")
        expr = expr.replace("log", "math.log10")

        if mode_var.get() == "Degrees":
            expr = re.sub(r'sin\((.*?)\)', r'math.sin(math.radians(\1))', expr)
            expr = re.sub(r'cos\((.*?)\)', r'math.cos(math.radians(\1))', expr)
            expr = re.sub(r'tan\((.*?)\)', r'math.tan(math.radians(\1))', expr)
        else:
            expr = expr.replace("sin(", "math.sin(").replace("cos(", "math.cos(").replace("tan(", "math.tan(")

        result = safe_eval(expr)
        entry_sci.delete(0, "end")
        
        if isinstance(result, float):
            entry_sci.insert(0, str(round(result, 8)).rstrip('0').rstrip('.') if '.' in str(round(result,8)) else str(round(result,8)))
        else:
            entry_sci.insert(0, str(result))
        update_status("OK")
    except SyntaxError:
        entry_sci.delete(0, "end"); entry_sci.insert(0, "Invalid Expression")
        update_status("Invalid Expression")
    except NameError:
        entry_sci.delete(0, "end"); entry_sci.insert(0, "Unknown Function")
        update_status("Unknown Function")
    except ZeroDivisionError:
        entry_sci.delete(0, "end"); entry_sci.insert(0, "Division by Zero")
        update_status("Division by Zero")
    except Exception:
        entry_sci.delete(0, "end"); entry_sci.insert(0, "Error")
        update_status("Error")

buttons_sci = [
    ("sin",2,0),("cos",2,1),("tan",2,2),("√",2,3),
    ("log",3,0),("ln",3,1),("π",3,2),("^",3,3),
    ("(",4,0),(")",4,1),("/" ,4,2),("*" ,4,3),
    ("7",5,0),("8",5,1),("9",5,2),("-" ,5,3),
    ("4",6,0),("5",6,1),("6",6,2),("+" ,6,3),
    ("1",7,0),("2",7,1),("3",7,2),("=" ,7,3),
    ("0",8,0),("." ,8,1),("⌫",8,2)
]
for (text,row,col) in buttons_sci:
    if text == "=":
        cmd = evaluate_sci
    elif text == "⌫":
        cmd = backspace_sci
    else:
        if text in ("sin","cos","tan","log","ln"):
            cmd = lambda t=text: click_sci(f"{t}(")
        elif text == "√":
            cmd = lambda t=text: click_sci("√(")
        else:
            cmd = lambda t=text: click_sci(t)
    ctk.CTkButton(tab_scientific, text=text, width=100, height=60, command=cmd).grid(row=row, column=col, padx=5, pady=5)

ctk.CTkButton(tab_scientific, text="Clear", width=460, height=50, fg_color="#ff6666", command=clear_sci).grid(row=9, column=0, columnspan=4, padx=10, pady=10)

# ---------- CONVERTER TAB ----------
entry_conv = ctk.CTkEntry(tab_converter, width=460, height=50, font=("Arial", 20), justify="right")
entry_conv.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

def convert(choice):
    try:
        val = float(entry_conv.get())
        if choice == "Meters → Centimeters": result = val * 100
        elif choice == "Kilograms → Pounds": result = val * 2.20462
        elif choice == "Celsius → Fahrenheit": result = (val * 9/5) + 32
        elif choice == "USD → INR": result = val * 83.0
        else: result = "Error"
        entry_conv.delete(0, "end"); entry_conv.insert(0, str(round(result,2)))
        update_status("Converted")
    except ValueError:
        entry_conv.delete(0, "end"); entry_conv.insert(0, "Invalid Number")
        update_status("Invalid Number")
    except Exception:
        entry_conv.delete(0, "end"); entry_conv.insert(0, "Error")
        update_status("Error")

converter_options = ["Meters → Centimeters","Kilograms → Pounds","Celsius → Fahrenheit","USD → INR"]
converter_var = ctk.StringVar(value="Select Conversion")
converter_menu = ctk.CTkOptionMenu(tab_converter, values=converter_options, variable=converter_var, width=250)
converter_menu.grid(row=1, column=0, columnspan=2, padx=10, pady=20)

ctk.CTkButton(tab_converter, text="Convert", width=180, height=40, fg_color="#3399cc",
              command=lambda: convert(converter_var.get())).grid(row=1, column=2, columnspan=2, padx=10, pady=20)

ctk.CTkButton(tab_converter, text="Clear", width=460, height=50, fg_color="#ff6666",
              command=lambda: (entry_conv.delete(0,"end"), update_status())).grid(row=2, column=0, columnspan=4, padx=10, pady=10)

# ---------- Status bar ----------
status_label = ctk.CTkLabel(app, text="", anchor="w", width=500)
status_label.pack(fill="x", padx=10, pady=(6,10))
update_status()

# ---------- Keyboard bindings ----------
def handle_key(event):
    """Route keyboard input to the active tab's entry and actions."""
    key = event.keysym
    char = event.char

    current_tab = tabview.get()

    # Tab switching: Ctrl+1/2/3
    if event.state & 0x4:  # Control pressed (platform dependent but works commonly)
        if key == "1":
            tabview.set("Standard"); update_status(); return
        if key == "2":
            tabview.set("Scientific"); update_status(); return
        if key == "3":
            tabview.set("Converter"); update_status(); return

    # Common keys
    if key == "Return":
        if current_tab == "Standard": evaluate_std()
        elif current_tab == "Scientific": evaluate_sci()
        elif current_tab == "Converter": convert(converter_var.get())
        return
    if key == "Escape":
        if current_tab == "Standard": clear_std()
        elif current_tab == "Scientific": clear_sci()
        elif current_tab == "Converter": entry_conv.delete(0, "end"); update_status()
        return
    if key == "BackSpace":
        if current_tab == "Standard":
            cur = entry_std.get(); entry_std.delete(len(cur)-1, "end") if cur else None
        elif current_tab == "Scientific":
            backspace_sci()
        elif current_tab == "Converter":
            cur = entry_conv.get(); entry_conv.delete(len(cur)-1, "end") if cur else None
        return

    # Printable characters: route to the active entry
    if char and char in "0123456789.+-*/()^":
        if current_tab == "Standard":
            entry_std.insert("end", char); update_status()
        elif current_tab == "Scientific":
            entry_sci.insert("end", char); update_status()
        elif current_tab == "Converter":
            entry_conv.insert("end", char); update_status()
        return

    # Scientific shortcuts (letters) only when Scientific tab active
    if current_tab == "Scientific" and char:
        lower = char.lower()
        if lower == "s":
            entry_sci.insert("end", "sin("); update_status(); return
        if lower == "c":
            entry_sci.insert("end", "cos("); update_status(); return
        if lower == "t":
            entry_sci.insert("end", "tan("); update_status(); return
        if lower == "l":
            entry_sci.insert("end", "log("); update_status(); return
        if lower == "n":
            entry_sci.insert("end", "ln("); update_status(); return
        if lower == "p":
            entry_sci.insert("end", "π"); update_status(); return
        if lower == "r":
            entry_sci.insert("end", "√("); update_status(); return

app.bind_all("<Key>", handle_key)
app.mainloop()
