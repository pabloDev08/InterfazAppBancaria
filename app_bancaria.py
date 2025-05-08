import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
import time
import random
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AyQueTeGuardoLosOros S.L. - Sistema Bancario Avanzado")
        self.root.geometry("900x700")
        self.root.configure(bg="#2c3e50")
        
        # Configuración inicial
        self.saldo = 780000.00  # Saldo inicial en euros
        self.moneda_actual = "EUR"
        self.usuarios = {"admin": "admin123"}  # Usuario y contraseña
        self.usuario_actual = None
        self.tasa_cambio = self.obtener_tasas_cambio()
        
        # Cargar imágenes e iconos
        self.load_images()
        
        # Estilos
        self.setup_styles()
        
        # Pantalla de inicio de sesión
        self.show_login_screen()
    
    def load_images(self):
        try:
            # Iconos para los botones (usando emoji como alternativa)
            self.icons = {
                "login": "🔑",
                "logout": "🚪",
                "user": "👤",
                "money": "💰",
                "exchange": "💱",
                "graph": "📊",
                "deposit": "⬆️",
                "withdraw": "⬇️",
                "delete": "❌"
            }
            
            # Logo del banco (usando un label con texto como alternativa)
            self.logo_text = "🏦 AyQueTeGuardoLosOros S.L."
        except Exception as e:
            print(f"Error cargando imágenes: {e}")
            # Si hay error, usar texto simple
            self.icons = {k: "" for k in ["login", "logout", "user", "money", "exchange", "graph", "deposit", "withdraw", "delete"]}
            self.logo_text = "AyQueTeGuardoLosOros S.L."
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TLabel', background='#2c3e50', foreground='white', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Title.TLabel', font=('Helvetica', 20, 'bold'))
        self.style.configure('Saldo.TLabel', font=('Helvetica', 16, 'bold'), foreground='#f39c12')
        
        self.style.map('TButton',
                      foreground=[('active', 'white'), ('!disabled', 'white')],
                      background=[('active', '#3498db'), ('!disabled', '#2980b9')])
        
        self.style.configure('Currency.TCombobox', fieldbackground='white', background='white')
    
    def obtener_tasas_cambio(self):
        # Tasas de cambio de ejemplo (en un sistema real se obtendrían de una API)
        return {
            "EUR": 1.0,      # Euro (base)
            "USD": 1.05,     # Dólar estadounidense
            "GBP": 0.86,    # Libra esterlina
            "JPY": 157.47,   # Yen japonés
            "AUD": 1.62,    # Dólar australiano
            "CAD": 1.42,     # Dólar canadiense
            "CHF": 0.95,    # Franco suizo
            "CNY": 7.61      # Yuan chino
        }
    
    def actualizar_tasas_cambio(self):
        try:
            # En un sistema real, aquí se haría una petición a una API de tasas de cambio
            # Ejemplo con API ficticia (descomentar para implementación real)
            # response = requests.get("https://api.exchangerate-api.com/v4/latest/EUR")
            # self.tasa_cambio = response.json()["rates"]
            
            # Simular actualización con pequeñas variaciones aleatorias
            for currency in self.tasa_cambio:
                if currency != "EUR":
                    variation = random.uniform(-0.02, 0.02)
                    self.tasa_cambio[currency] = max(0.5, min(2.0, self.tasa_cambio[currency] * (1 + variation)))
            
            messagebox.showinfo("Tasas de Cambio", "Las tasas de cambio se han actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron actualizar las tasas de cambio: {str(e)}")
    
    def convertir_moneda(self, cantidad, de_moneda, a_moneda):
        if de_moneda == a_moneda:
            return cantidad
        
        if de_moneda == "EUR":
            return cantidad * self.tasa_cambio.get(a_moneda, 1)
        elif a_moneda == "EUR":
            return cantidad / self.tasa_cambio.get(de_moneda, 1)
        else:
            # Convertir primero a EUR y luego a la moneda destino
            en_euros = cantidad / self.tasa_cambio.get(de_moneda, 1)
            return en_euros * self.tasa_cambio.get(a_moneda, 1)
    
    def show_login_screen(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Marco principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        # Logo/título
        ttk.Label(main_frame, text=self.logo_text, style='Title.TLabel').pack(pady=20)
        
        # Formulario de login
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(pady=20)
        
        ttk.Label(login_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.user_entry = ttk.Entry(login_frame)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.pass_entry = ttk.Entry(login_frame, show="*")
        self.pass_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=f"{self.icons['login']} Iniciar Sesión", 
                  command=self.login).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text=f"{self.icons['user']} Crear Usuario", 
                  command=self.crear_usuario).pack(side=tk.LEFT, padx=10)
    
    def login(self):
        usuario = self.user_entry.get()
        contraseña = self.pass_entry.get()
        
        if usuario in self.usuarios and self.usuarios[usuario] == contraseña:
            self.usuario_actual = usuario
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def crear_usuario(self):
        usuario = simpledialog.askstring("Crear Usuario", "Ingrese un nombre de usuario:")
        if not usuario:
            return
            
        if usuario in self.usuarios:
            messagebox.showerror("Error", "El usuario ya existe")
            return
            
        contraseña = simpledialog.askstring("Crear Usuario", "Ingrese una contraseña:", show="*")
        if not contraseña:
            return
            
        self.usuarios[usuario] = contraseña
        messagebox.showinfo("Éxito", "Usuario creado correctamente")
    
    def show_main_menu(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Marco principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Barra superior
        top_bar = ttk.Frame(main_frame)
        top_bar.pack(fill=tk.X, pady=10)
        
        ttk.Label(top_bar, text=f"Bienvenido, {self.usuario_actual}", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Selector de moneda
        self.currency_var = tk.StringVar(value=self.moneda_actual)
        currency_box = ttk.Combobox(top_bar, textvariable=self.currency_var, 
                                  values=list(self.tasa_cambio.keys()), 
                                  state="readonly", width=5, style='Currency.TCombobox')
        currency_box.pack(side=tk.RIGHT, padx=10)
        currency_box.bind("<<ComboboxSelected>>", self.cambiar_moneda)
        
        # Botón de logout
        ttk.Button(top_bar, text=f"{self.icons['logout']} Salir", 
                  command=self.logout).pack(side=tk.RIGHT, padx=10)
        
        # Mostrar saldo actual
        self.saldo_label = ttk.Label(main_frame, text="", style='Saldo.TLabel')
        self.saldo_label.pack(pady=20)
        self.actualizar_saldo_display()
        
        # Botones de operaciones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=30)
        
        button_data = [
            (f"{self.icons['deposit']} Depositar", self.depositar),
            (f"{self.icons['withdraw']} Retirar", self.retirar),
            (f"{self.icons['exchange']} Cambio de Moneda", self.mostrar_cambio_moneda),
            (f"{self.icons['graph']} Gráfico de Movimientos", self.mostrar_grafico),
            (f"{self.icons['user']} Eliminar Usuario", self.eliminar_usuario),
            (f"{self.icons['money']} Actualizar Tasas", self.actualizar_tasas_cambio)
        ]
        
        for text, command in button_data:
            btn = ttk.Button(buttons_frame, text=text, command=command)
            btn.pack(fill=tk.X, pady=5, padx=50)
    
    def cambiar_moneda(self, event=None):
        nueva_moneda = self.currency_var.get()
        if nueva_moneda != self.moneda_actual:
            self.moneda_actual = nueva_moneda
            self.actualizar_saldo_display()
    
    def actualizar_saldo_display(self):
        saldo_convertido = self.convertir_moneda(self.saldo, "EUR", self.moneda_actual)
        self.saldo_label.config(text=f"Saldo actual: {saldo_convertido:.2f} {self.moneda_actual}")
    
    def depositar(self):
        cantidad = simpledialog.askfloat("Depositar", f"Ingrese cantidad a depositar ({self.moneda_actual}):")
        if cantidad is None or cantidad <= 0:
            messagebox.showerror("Error", "Debe ingresar una cantidad positiva")
            return
        
        # Verificación adicional para grandes depósitos (equivalente a 95,000 USD)
        umbral_grande = self.convertir_moneda(95000, "USD", self.moneda_actual)
        if cantidad > umbral_grande:
            if not messagebox.askyesno("Verificación Requerida", 
                                     f"Está intentando depositar {cantidad:.2f} {self.moneda_actual}\n"
                                     "¿Desea continuar con esta operación?"):
                return
        
        # Convertir a euros para almacenamiento interno
        cantidad_eur = self.convertir_moneda(cantidad, self.moneda_actual, "EUR")
        self.saldo += cantidad_eur
        
        # Animación de depósito
        self.animate_transaction("deposit")
        
        messagebox.showinfo("Éxito", f"Has depositado {cantidad:.2f} {self.moneda_actual} correctamente")
        self.actualizar_saldo_display()
    
    def retirar(self):
        saldo_actual = self.convertir_moneda(self.saldo, "EUR", self.moneda_actual)
        max_retiro = saldo_actual * 0.5  # Máximo 50% del saldo
        
        cantidad = simpledialog.askfloat("Retirar", 
                                       f"Ingrese cantidad a retirar ({self.moneda_actual}):\n"
                                       f"Máximo disponible: {max_retiro:.2f} {self.moneda_actual}")
        if cantidad is None or cantidad <= 0:
            messagebox.showerror("Error", "Debe ingresar una cantidad positiva")
            return
        
        if cantidad > max_retiro:
            messagebox.showerror("Error", f"No puede retirar más del 50% de su saldo ({max_retiro:.2f} {self.moneda_actual})")
            return
        
        # Convertir a euros para verificación
        cantidad_eur = self.convertir_moneda(cantidad, self.moneda_actual, "EUR")
        if cantidad_eur > self.saldo:
            messagebox.showerror("Error", "Saldo insuficiente")
            return
        
        # Confirmación adicional
        if not messagebox.askyesno("Confirmar Retiro", 
                                 f"¿Está seguro que desea retirar {cantidad:.2f} {self.moneda_actual}?"):
            return
        
        self.saldo -= cantidad_eur
        
        # Animación de retiro
        self.animate_transaction("withdraw")
        
        messagebox.showinfo("Éxito", f"Has retirado {cantidad:.2f} {self.moneda_actual} correctamente")
        self.actualizar_saldo_display()
    
    def animate_transaction(self, transaction_type):
        # Crear una ventana emergente para la animación
        popup = tk.Toplevel(self.root)
        popup.title("Procesando transacción..." if transaction_type == "deposit" else "Retirando fondos...")
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        # Centrar la ventana emergente
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Configurar contenido de la animación
        if transaction_type == "deposit":
            emoji_sequence = ["💰", "💵", "💶", "💷", "💴"]
            message = "Depositando fondos..."
        else:
            emoji_sequence = ["💸", "💳", "🧾", "📉", "📤"]
            message = "Retirando fondos..."
        
        label = ttk.Label(popup, text=emoji_sequence[0], font=("Arial", 24))
        label.pack(pady=20)
        
        ttk.Label(popup, text=message).pack()
        
        # Función para animar los emojis
        def animate(frame=0):
            if frame < len(emoji_sequence):
                label.config(text=emoji_sequence[frame])
                popup.after(200, animate, frame + 1)
            else:
                popup.destroy()
        
        # Iniciar animación
        popup.after(100, animate)
        
        # Hacer que la ventana sea modal
        popup.grab_set()
        self.root.wait_window(popup)
    
    def mostrar_cambio_moneda(self):
        # Crear ventana de cambio de moneda
        exchange_win = tk.Toplevel(self.root)
        exchange_win.title("Cambio de Moneda")
        exchange_win.geometry("400x300")
        
        # Marco principal
        main_frame = ttk.Frame(exchange_win)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Configurar tasas de cambio
        ttk.Label(main_frame, text="Tasas de cambio (1 EUR = )", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        for currency, rate in self.tasa_cambio.items():
            if currency != "EUR":
                ttk.Label(main_frame, text=f"{currency}: {rate:.4f}").pack()
        
        # Separador
        ttk.Separator(main_frame).pack(fill=tk.X, pady=10)
        
        # Conversor de moneda
        ttk.Label(main_frame, text="Conversor de moneda", font=("Helvetica", 12, "bold")).pack(pady=5)
        
        converter_frame = ttk.Frame(main_frame)
        converter_frame.pack(pady=10)
        
        # Entrada de cantidad
        ttk.Label(converter_frame, text="Cantidad:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(converter_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Monedas de origen y destino
        ttk.Label(converter_frame, text="De:").grid(row=1, column=0, padx=5, pady=5)
        self.from_currency = ttk.Combobox(converter_frame, values=list(self.tasa_cambio.keys()), state="readonly")
        self.from_currency.current(0)
        self.from_currency.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(converter_frame, text="A:").grid(row=2, column=0, padx=5, pady=5)
        self.to_currency = ttk.Combobox(converter_frame, values=list(self.tasa_cambio.keys()), state="readonly")
        self.to_currency.current(1)
        self.to_currency.grid(row=2, column=1, padx=5, pady=5)
        
        # Botón de conversión
        ttk.Button(converter_frame, text="Convertir", command=self.convertir).grid(row=3, columnspan=2, pady=10)
        
        # Resultado
        self.result_label = ttk.Label(main_frame, text="", style='Saldo.TLabel')
        self.result_label.pack(pady=10)
    
    def convertir(self):
        try:
            cantidad = float(self.amount_entry.get())
            de_moneda = self.from_currency.get()
            a_moneda = self.to_currency.get()
            
            resultado = self.convertir_moneda(cantidad, de_moneda, a_moneda)
            self.result_label.config(text=f"{cantidad:.2f} {de_moneda} = {resultado:.2f} {a_moneda}")
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida")
    
    def mostrar_grafico(self):
        # Datos de ejemplo para el gráfico (en un sistema real serían los movimientos históricos)
        movimientos = {
            "Depósitos": random.randint(5, 20),
            "Retiros": random.randint(3, 15),
            "Transferencias": random.randint(2, 10)
        }
        
        # Crear ventana para el gráfico
        graph_win = tk.Toplevel(self.root)
        graph_win.title("Gráfico de Movimientos")
        graph_win.geometry("600x500")
        
        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.bar(movimientos.keys(), movimientos.values(), color=['#2ecc71', '#e74c3c', '#3498db'])
        ax.set_title("Movimientos Bancarios")
        ax.set_ylabel("Cantidad")
        
        # Mostrar el gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Botón para cerrar
        ttk.Button(graph_win, text="Cerrar", command=graph_win.destroy).pack(pady=10)
    
    def eliminar_usuario(self):
        if self.usuario_actual == "admin":
            messagebox.showerror("Error", "No se puede eliminar el usuario admin")
            return
            
        confirmacion = messagebox.askyesno("Confirmar", 
                                         "¿Está seguro que desea eliminar su usuario?\n"
                                         "Esta acción no se puede deshacer.")
        if confirmacion:
            del self.usuarios[self.usuario_actual]
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            self.logout()
    
    def logout(self):
        self.usuario_actual = None
        self.show_login_screen()

if __name__ == '__main__':
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()