# Nota: Este entorno no soporta Tkinter directamente.
# Para ejecutar este script, usá un entorno local de Python (como IDLE o VS Code) donde esté disponible Tkinter.

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ModuleNotFoundError:
    print("Error: Tkinter no está disponible en este entorno. Usá un entorno local con soporte gráfico.")
    exit()

from datetime import datetime

# Asegurarse de que el módulo 'calculos.py' esté disponible
try:
    from calculos import calcular_tmb, calcular_tdee, calcular_macros
except ImportError as e:
    print(f"Error al importar funciones desde 'calculos.py': {e}\nAsegúrate de que el archivo 'calculos.py' esté en el mismo directorio y contenga las funciones necesarias.")
    exit()

# --- Función principal que procesa todos los cálculos ---
def procesar():
    try:
        nombre = nombre_entry.get().strip().title()
        apellido = apellido_entry.get().strip().title()
        genero = genero_var.get()
        edad = int(edad_entry.get())
        peso = float(peso_entry.get())
        estatura = float(estatura_entry.get())
        dias = int(ejercicio_entry.get())
        objetivo = objetivo_var.get()

        tmb = calcular_tmb(genero, peso, estatura, edad)
        tdee = calcular_tdee(tmb, dias)

        if objetivo == "Pérdida de Peso":
            kilos = float(kilos_obj_entry.get())
            meses = int(meses_entry.get())
            total_dias = meses * 30.437
            total_calorias = kilos * 7700
            deficit_diario = total_calorias / total_dias
            calorias = tdee - deficit_diario
            ritmo_mensual = (deficit_diario * 30.437) / 7700
            min_cal = 1500 if genero == 'm' else 1200
            if calorias < min_cal:
                calorias = min_cal
                deficit_diario = tdee - calorias
                ritmo_mensual = (deficit_diario * 30.437) / 7700
        elif objetivo == "Ganancia de Masa Muscular":
            superavit = 250
            calorias = tdee + superavit
            kilos = float(kilos_obj_entry.get())
            deficit_diario = 0
            ritmo_mensual = 0
        else:
            calorias = tdee
            kilos = 0
            deficit_diario = 0
            ritmo_mensual = 0

        plan = macros_var.get()
        plan_key = {'Balanceada': '1', 'Baja en Carbohidratos': '2', 'Alta en Carbohidratos': '3'}[plan]
        p, c, g, plan_nombre = calcular_macros(calorias, plan_key)

        # Resultados
        resumen = (
            f"\n👤 {nombre} {apellido}\n"
            f"TMB: {tmb:.0f} kcal\n"
            f"TDEE: {tdee:.0f} kcal\n"
            f"Objetivo: {objetivo}\n"
            f"Calorías Objetivo: {calorias:.0f} kcal\n"
            f"Plan: {plan_nombre}\n"
            f"Proteínas: {p:.0f}g | Carbs: {c:.0f}g | Grasas: {g:.0f}g\n"
        )

        if objetivo == "Pérdida de Peso":
            resumen += (
                f"Déficit diario: {deficit_diario:.0f} kcal\n"
                f"Pérdida mensual estimada: {ritmo_mensual:.2f} kg\n"
            )
        elif objetivo == "Ganancia de Masa Muscular":
            resumen += f"Ganancia esperada: {kilos:.1f} kg\n"

        resultado_text.set(resumen)

    except Exception as e:
        messagebox.showerror("Error", f"Verifica tus datos:\n{e}")

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Calculadora Nutricional Personalizada")
ventana.geometry("480x650")
ventana.configure(bg="#f0f4f8")

estilo = ttk.Style()
estilo.configure("TLabel", font=("Segoe UI", 11))
estilo.configure("TEntry", font=("Segoe UI", 11))
estilo.configure("TButton", font=("Segoe UI", 11))

frame = ttk.Frame(ventana, padding=20)
frame.pack(fill="both", expand=True)

# --- Campos de entrada ---
campos = [
    ("Nombre", "nombre_entry"),
    ("Apellido", "apellido_entry"),
    ("Edad", "edad_entry"),
    ("Peso (kg)", "peso_entry"),
    ("Estatura (cm)", "estatura_entry"),
    ("Días de ejercicio/semana", "ejercicio_entry")
]

vars_globales = globals()
for texto, var in campos:
    ttk.Label(frame, text=texto).pack()
    entry = ttk.Entry(frame)
    entry.pack()
    vars_globales[var] = entry

# --- Género ---
ttk.Label(frame, text="Género (m/f)").pack()
genero_var = tk.StringVar()
ttk.Combobox(frame, textvariable=genero_var, values=["m", "f"]).pack()

# --- Objetivo ---
def actualizar_objetivo(*args):
    if objetivo_var.get() in ["Pérdida de Peso", "Ganancia de Masa Muscular"]:
        kilos_obj_entry.pack()
        if objetivo_var.get() == "Pérdida de Peso":
            meses_entry.pack()
        else:
            meses_entry.pack_forget()
    else:
        kilos_obj_entry.pack_forget()
        meses_entry.pack_forget()

objetivo_var = tk.StringVar()
ttk.Label(frame, text="Objetivo").pack()
ttk.Combobox(frame, textvariable=objetivo_var, values=["Pérdida de Peso", "Mantenimiento de Peso", "Ganancia de Masa Muscular"]).pack()
objetivo_var.trace("w", actualizar_objetivo)

kilos_obj_entry = ttk.Entry(frame)
kilos_obj_entry.insert(0, "Kilos objetivo")
meses_entry = ttk.Entry(frame)
meses_entry.insert(0, "Meses (solo si es pérdida de peso)")

# --- Macronutrientes ---
ttk.Label(frame, text="Distribución de Macronutrientes").pack()
macros_var = tk.StringVar()
ttk.Combobox(frame, textvariable=macros_var,
             values=["Balanceada", "Baja en Carbohidratos", "Alta en Carbohidratos"]).pack()

# --- Botón Calcular ---
ttk.Button(frame, text="Calcular Plan", command=procesar).pack(pady=15)

# --- Resultado ---
resultado_text = tk.StringVar()
tk.Label(frame, textvariable=resultado_text, justify="left", bg="#f0f4f8", font=("Segoe UI", 10)).pack()

ventana.mainloop()
