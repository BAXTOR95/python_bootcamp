import tkinter as tk

window = tk.Tk()
window.title("Mile to Km Converter")
window.minsize(200, 110)
window.config(padx=20, pady=20)


def miles_to_km():
    km_value_label.config(text=f"{round(float(miles_entry.get()) * 1.609, 2)}")


# Miles Entry

miles_entry = tk.Entry(width=10)
miles_entry.insert(tk.END, "0")
miles_entry.grid(column=1, row=0)

# Labels

miles_label = tk.Label(text="Miles")
miles_label.grid(column=2, row=0)

equal_to_label = tk.Label(text="is equal to")
equal_to_label.grid(column=0, row=1)

km_value_label = tk.Label(text="0")
km_value_label.grid(column=1, row=1)

km_label = tk.Label(text="Km")
km_label.grid(column=2, row=1)

# Calculate Button

calculate_btn = tk.Button(text="Calculate", command=miles_to_km)
calculate_btn.grid(column=1, row=2)

window.mainloop()
