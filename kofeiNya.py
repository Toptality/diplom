import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sqlite3
from datetime import datetime
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CoffeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Hub")
        self.root.geometry("1200x800")
        self.root.state("zoomed")
        
        #  Цветовая схема
        self.colors = {
            "background": "#1A1A1D",
            "primary": "#4E4E50",
            "secondary": "#6F2232",
            "accent": "#950740",
            "text": "#FFFFFF",
            "light_text": "#C5C6C7",
            "card_bg": "#2D2D30",
            "highlight": "#C3073F",
            "border": "#4E4E50"
        }

        self.setup_styles()
        
        # Инициализация базы данных
        self.init_db()

        self.root.configure(bg=self.colors["background"])
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=10)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        # Заголовок и категории
        self.create_header()
        
        # Основная область выбора напитков
        self.create_drinks_area()
        
        # Корзина
        self.create_cart_area()

        # Напитки
        self.all_drinks = [
            # Кофе 
            {"name": "Эспрессо", "price": 100, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "eKspresso.png"), "ingredients": "Крепкий кофе"},
            {"name": "Капучино", "price": 150, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "capp.png"), "ingredients": "Эспрессо, молоко"},
            {"name": "Латте", "price": 170, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "lattE.png"), "ingredients": "Эспрессо, молоко"},
            {"name": "Флэт Уайт", "price": 130, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "fw.png"), "ingredients": "Двойной эспрессо, молоко"},
            {"name": "Американо", "price": 110, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "Amer.png"), "ingredients": "Двойной эспрессо, вода"},
            {"name": "Фрапучино", "price": 210, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "fappuccino.png"), "ingredients": "Кофе, молоко, лёд"},
            {"name": "Айс Латте", "price": 180, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "IL.png"), "ingredients": "Эспрессо, молоко, лёд"},
            {"name": "Раф", "price": 190, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "gaf-gaf.png"), "ingredients": "Эспрессо, сливки, ванильный сахар"},
            {"name": "Моккачино", "price": 200, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "mok.png"), "ingredients": "Эспрессо, шоколад, молоко"},
            {"name": "Глясе", "price": 160, "category": "Кофе", "image": os.path.join(BASE_DIR, "карточки", "mlem-mlem.png"), "ingredients": "Эспрессо, мороженое"},
            
            # Шоколад 
            {"name": "Горячий шоколад", "price": 200, "category": "Шоколад", "image": os.path.join(BASE_DIR, "карточки", "HotChocolat.png"), "ingredients": "Тёмный шоколад, молоко"},
            {"name": "Белый шоколад", "price": 210, "category": "Шоколад", "image": os.path.join(BASE_DIR, "карточки", "kkk.png"), "ingredients": "Белый шоколад, молоко"},
            
            # Чай 
            {"name": "Зеленый чай", "price": 90, "category": "Чай", "image": os.path.join(BASE_DIR, "карточки", "green_tea_neko.png"), "ingredients": "Зелёный чай"},
            {"name": "Черный чай", "price": 80, "category": "Чай", "image": os.path.join(BASE_DIR, "карточки", "red(nigger)_tea.png"), "ingredients": "Чёрный чай"},
            {"name": "Чефир", "price": 150, "category": "Чай", "image": os.path.join(BASE_DIR, "карточки", "oshalet_ne_vstatb.png"), "ingredients": "Очень крепкий чай"},
        ]

        self.filtered_drinks = self.all_drinks
        self.create_drink_buttons()
        self.total_cost = 0
        self.cart_items = []

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка стилей для кнопок
        style.configure('Primary.TButton', 
                       foreground=self.colors["text"],
                       background=self.colors["secondary"],
                       font=('Helvetica', 10, 'bold'),
                       padding=10,
                       borderwidth=0)
        
        style.map('Primary.TButton',
                 background=[('active', self.colors["accent"])])
        
        style.configure('Secondary.TButton',
                      foreground=self.colors["text"],
                      background=self.colors["primary"],
                      font=('Helvetica', 9),
                      padding=8)
        
        style.configure('TFrame', background=self.colors["background"])
        style.configure('TLabel', background=self.colors["background"], foreground=self.colors["text"])
        style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'), foreground=self.colors["highlight"])
        style.configure('Card.TFrame', background=self.colors["card_bg"], relief=tk.RAISED, borderwidth=1, bordercolor=self.colors["border"])
        style.configure('TEntry', fieldbackground=self.colors["card_bg"], foreground=self.colors["text"])
        style.configure('Vertical.TScrollbar', background=self.colors["primary"], troughcolor=self.colors["background"])

    def create_header(self):
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        
        # Логотип и название
        logo_frame = ttk.Frame(header_frame, style='TFrame')
        logo_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        
        ttk.Label(logo_frame, text="Coffee Hub", style='Header.TLabel').pack(side=tk.LEFT, padx=10)
        
        # Категории
        category_frame = ttk.Frame(header_frame, style='TFrame')
        category_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20)
        
        self.categories = ["Все напитки", "Кофе", "Шоколад", "Чай"]
        self.selected_category = tk.StringVar(value=self.categories[0])
        
        for category in self.categories:
            btn = ttk.Button(category_frame, text=category, style='Secondary.TButton',
                            command=lambda c=category: self.select_category(c))
            btn.pack(side=tk.LEFT, padx=5)
        
        
        random_btn = ttk.Button(category_frame, text="🎲 Случайный напиток", style='Secondary.TButton',
                              command=self.random_drink)
        random_btn.pack(side=tk.LEFT, padx=5)
        
        # Поиск
        search_frame = ttk.Frame(header_frame, style='TFrame')
        search_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_search_results())
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25, style='TEntry')
        search_entry.pack(side=tk.RIGHT)

    def random_drink(self):
        
        random_drink = random.choice(self.all_drinks)
        self.show_modifiers(random_drink)

    def create_drinks_area(self):
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        ttk.Label(main_frame, text="Меню напитков", style='Header.TLabel').pack(pady=10)
        
        # Вертикальный ползунок
        self.drink_canvas = tk.Canvas(main_frame, bg=self.colors["background"], highlightthickness=0)
        self.drink_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.drink_frame = ttk.Frame(self.drink_canvas, style='TFrame')
        self.drink_canvas.create_window((0, 0), window=self.drink_frame, anchor="nw")
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.drink_canvas.yview, style='Vertical.TScrollbar')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.drink_canvas.configure(yscrollcommand=scrollbar.set)
        self.drink_canvas.bind("<Configure>", lambda e: self.drink_canvas.configure(scrollregion=self.drink_canvas.bbox("all")))
        
        # Сетка для напитков
        for i in range(5):
            self.drink_frame.grid_columnconfigure(i, weight=1, uniform="drinks")

    def create_cart_area(self):
        cart_frame = ttk.Frame(self.root, style='TFrame')
        cart_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=5)
        
        ttk.Label(cart_frame, text="Ваш заказ", style='Header.TLabel').pack(pady=10)
        
        self.cart_canvas = tk.Canvas(cart_frame, bg=self.colors["background"], highlightthickness=0)
        self.cart_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.cart_items_frame = ttk.Frame(self.cart_canvas, style='TFrame')
        self.cart_canvas.create_window((0, 0), window=self.cart_items_frame, anchor="nw")
        
        scrollbar = ttk.Scrollbar(cart_frame, orient=tk.VERTICAL, command=self.cart_canvas.yview, style='Vertical.TScrollbar')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cart_canvas.configure(yscrollcommand=scrollbar.set)
        self.cart_canvas.bind("<Configure>", lambda e: self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all")))
        
        # Итоговая сумма
        self.total_frame = ttk.Frame(cart_frame, style='TFrame')
        self.total_frame.pack(fill=tk.X, pady=10)
        
        self.total_label = ttk.Label(self.total_frame, text="Общая стоимость: 0 руб.", 
                                   font=('Helvetica', 12, 'bold'), style='TLabel')
        self.total_label.pack()
        
        # Кнопки корзины
        button_frame = ttk.Frame(cart_frame, style='TFrame')
        button_frame.pack(fill=tk.X, pady=5)
        
        self.pay_button = ttk.Button(button_frame, text="Оплатить", style='Primary.TButton', command=self.pay)
        self.pay_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.clear_button = ttk.Button(button_frame, text="Очистить", style='Secondary.TButton', command=self.clear_cart)
        self.clear_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.history_button = ttk.Button(button_frame, text="История", style='Secondary.TButton', command=self.show_history)
        self.history_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    def init_db(self):
        self.conn = sqlite3.connect('orders.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              order_date TEXT,
                              items TEXT,
                              total REAL)''')
        self.conn.commit()

    def save_order(self, items, total):
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items_text = "\n".join([f"{item['name']} ({item['modifiers']}) - {item['price']} руб." for item in items])
        self.cursor.execute("INSERT INTO orders (order_date, items, total) VALUES (?, ?, ?)",
                           (order_date, items_text, total))
        self.conn.commit()

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("История заказов")
        history_window.geometry("800x600")
        history_window.configure(bg=self.colors["background"])
        
        ttk.Label(history_window, text="История заказов", style='Header.TLabel').pack(pady=10)

        canvas = tk.Canvas(history_window, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=canvas.yview, style='Vertical.TScrollbar')
        scrollable_frame = ttk.Frame(canvas, style='TFrame')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.cursor.execute("SELECT * FROM orders ORDER BY order_date DESC")
        orders = self.cursor.fetchall()

        if not orders:
            ttk.Label(scrollable_frame, text="Нет сохранённых заказов", style='TLabel').pack(pady=10)
        else:
            for order in orders:
                order_frame = ttk.Frame(scrollable_frame, style='Card.TFrame', padding=10)
                order_frame.pack(fill=tk.X, padx=5, pady=5)

                ttk.Label(order_frame, 
                         text=f"Заказ №{order[0]} - {order[1]}", 
                         font=('Helvetica', 12, 'bold'),
                         style='TLabel').pack(anchor="w")
                
                ttk.Label(order_frame, 
                         text=order[2], 
                         justify=tk.LEFT,
                         style='TLabel').pack(anchor="w")
                
                ttk.Label(order_frame, 
                         text=f"Итого: {order[3]} руб.", 
                         font=('Helvetica', 10, 'bold'),
                         style='TLabel').pack(anchor="w")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_search_results(self):
        query = self.search_var.get().lower()
        self.filtered_drinks = [d for d in self.all_drinks if query in d['name'].lower()]
        self.create_drink_buttons()

    def select_category(self, category):
        self.selected_category.set(category)
        self.search_var.set("")
        self.filtered_drinks = self.all_drinks if category == "Все напитки" else [d for d in self.all_drinks if d['category'] == category]
        self.create_drink_buttons()

    def create_drink_buttons(self):
        for widget in self.drink_frame.winfo_children():
            widget.destroy()
            
        if not self.filtered_drinks:
            ttk.Label(self.drink_frame, 
                     text="Данного напитка нет в ассортименте", 
                     style='TLabel').grid(row=0, column=0, padx=10, pady=10)
            return

        for i, drink in enumerate(self.filtered_drinks):
            row = i // 5
            col = i % 5

            card_frame = ttk.Frame(self.drink_frame, style='Card.TFrame', padding=10)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            try:
                img = Image.open(drink['image']).resize((140, 140))
                img = ImageTk.PhotoImage(img)
            except:
                img = ImageTk.PhotoImage(Image.new('RGB', (140, 140), color='gray'))

            img_label = tk.Label(card_frame, image=img, bg=self.colors["card_bg"])
            img_label.image = img
            img_label.pack()
            img_label.bind("<Button-1>", lambda e, d=drink: self.show_modifiers(d))

            name_label = ttk.Label(card_frame, 
                                 text=drink['name'], 
                                 font=('Helvetica', 10, 'bold'),
                                 style='TLabel')
            name_label.pack()

            price_label = ttk.Label(card_frame, 
                                  text=f"{drink['price']} руб.", 
                                  font=('Helvetica', 9),
                                  style='TLabel')
            price_label.pack()

            btn = ttk.Button(card_frame, 
                            text="Добавить", 
                            style='Secondary.TButton',
                            command=lambda d=drink: self.add_to_cart(d, []))
            btn.pack(pady=5)

    def show_modifiers(self, drink):
        modifier_window = tk.Toplevel(self.root)
        modifier_window.title(f"Модификаторы — {drink['name']}")
        modifier_window.geometry("450x550")
        modifier_window.configure(bg=self.colors["background"])
        modifier_window.grab_set()

        card_frame = ttk.Frame(modifier_window, style='Card.TFrame', padding=10)
        card_frame.pack(pady=10)
        
        try:
            img = Image.open(drink['image']).resize((140, 140))
            img = ImageTk.PhotoImage(img)
        except:
            img = ImageTk.PhotoImage(Image.new('RGB', (140, 140), color='gray'))

        ttk.Label(card_frame, image=img, style='TLabel').pack()
        ttk.Label(card_frame, 
                 text=f"{drink['name']} - {drink['price']} руб.", 
                 font=('Helvetica', 14, 'bold'),
                 style='TLabel').pack(pady=5)
        
        ttk.Label(card_frame, 
                 text=f"Состав: {drink.get('ingredients', 'не указан')}", 
                 font=('Helvetica', 10),
                 style='TLabel').pack()
        card_frame.image = img

        selected_mods = []
        milk_var = tk.StringVar(value="Обычное")
        syrup_var = tk.StringVar(value="Без сиропа")
        strength_var = tk.StringVar(value="1")
        sugar_entry_var = tk.StringVar()
        ice_var = tk.BooleanVar()

        is_espresso = drink["name"].lower() == "эспрессо"
        category = drink["category"]

        def add_option(label, var, options):
            frame = ttk.Frame(modifier_window, style='TFrame')
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label, style='TLabel').pack(side=tk.LEFT, padx=5)
            
            menu = ttk.OptionMenu(frame, var, *options, style='Secondary.TButton')
            menu.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        if is_espresso:
            add_option("Крепость (шоты):", strength_var, [str(i) for i in range(1, 6)])
        elif category == "Кофе":
            add_option("Молоко:", milk_var, ["Обычное", "Банановое (+60)", "Ванильное (+60)", "Миндальное (+60)", "Фундучное (+60)", "Овсяное (+60)"])
            add_option("Сироп:", syrup_var, ["Без сиропа", "Ванильный (+15)", "Карамельный (+15)"])
            
            sugar_frame = ttk.Frame(modifier_window, style='TFrame')
            sugar_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(sugar_frame, text="Сахар (в кубиках, до 10):", style='TLabel').pack(side=tk.LEFT, padx=5)
            ttk.Entry(sugar_frame, textvariable=sugar_entry_var, style='TEntry').pack(side=tk.RIGHT, expand=True, fill=tk.X)
            
            ttk.Checkbutton(modifier_window, 
                          text="Добавить лёд", 
                          variable=ice_var, 
                          style='TLabel').pack(pady=5)
        elif category == "Чай":
            add_option("Крепость:", strength_var, ["1", "2", "3"])
            
            sugar_frame = ttk.Frame(modifier_window, style='TFrame')
            sugar_frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(sugar_frame, text="Сахар (в кубиках, до 10):", style='TLabel').pack(side=tk.LEFT, padx=5)
            ttk.Entry(sugar_frame, textvariable=sugar_entry_var, style='TEntry').pack(side=tk.RIGHT, expand=True, fill=tk.X)
        elif category == "Шоколад":
            add_option("Молоко:", milk_var, ["Обычное", "Банановое (+60)", "Ванильное (+60)", "Миндальное (+60)", "Фундучное (+60)", "Овсяное (+60)"])

        def confirm():
            price = drink['price']
            mods = []

            if is_espresso:
                shots = int(strength_var.get())
                if shots > 2:
                    extra = (shots - 2) * 40
                    price += extra
                mods.append(f"{shots} шот(а)")
            else:
                if milk_var.get() != "Обычное":
                    mods.append(milk_var.get())
                    price += 60

                if syrup_var.get() != "Без сиропа":
                    mods.append(syrup_var.get())
                    price += 15

                sugar = sugar_entry_var.get().strip()
                if sugar.isdigit():
                    sugar = int(sugar)
                    if 0 <= sugar <= 10:
                        if sugar > 0:
                            mods.append(f"Сахар: {sugar} куб.")
                        else:
                            mods.append("Без сахара")
                    else:
                        messagebox.showwarning("Ошибка", "Можно выбрать от 0 до 10 кубиков сахара.")
                        return
                else:
                    mods.append("Без сахара")

                if strength_var.get() != "1" and category == "Чай":
                    mods.append(f"Крепость: {strength_var.get()}")

                if ice_var.get():
                    mods.append("Лёд")

            self.add_to_cart(drink, mods, price)
            modifier_window.destroy()

        btn_frame = ttk.Frame(modifier_window, style='TFrame')
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, 
                 text="Добавить в корзину", 
                 style='Primary.TButton', 
                 command=confirm).pack(side=tk.LEFT, expand=True, padx=5)
        
        ttk.Button(btn_frame, 
                 text="Отмена", 
                 style='Secondary.TButton', 
                 command=modifier_window.destroy).pack(side=tk.LEFT, expand=True, padx=5)

    def add_to_cart(self, drink, modifiers, custom_price=None):
        price = custom_price if custom_price is not None else drink['price']
        mods_text = ", ".join(modifiers) if modifiers else "без модификаторов"

        item_frame = ttk.Frame(self.cart_items_frame, style='Card.TFrame', padding=5)
        item_frame.pack(fill=tk.X, padx=5, pady=2)

        try:
            img = Image.open(drink['image']).resize((40, 40))
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(item_frame, image=img, bg=self.colors["card_bg"])
            img_label.image = img
            img_label.pack(side=tk.LEFT, padx=5)
        except:
            pass

        item_text = f"{drink['name']} ({mods_text}) - {price} руб."
        ttk.Label(item_frame, 
                 text=item_text, 
                 style='TLabel').pack(side=tk.LEFT, fill=tk.X, expand=True)

        remove_btn = ttk.Button(item_frame, 
                              text="×", 
                              style='Secondary.TButton',
                              command=lambda f=item_frame, p=price: self.remove_cart_item(f, p))
        remove_btn.pack(side=tk.RIGHT)

        self.cart_items.append({
            "frame": item_frame,
            "price": price,
            "name": drink['name'],
            "modifiers": mods_text
        })
        self.total_cost += price
        self.update_total()

    def remove_cart_item(self, item_frame, price):
        item_frame.destroy()
        self.cart_items = [item for item in self.cart_items if item["frame"] != item_frame]
        self.total_cost -= price
        self.update_total()

    def update_total(self):
        self.total_label.config(text=f"Общая стоимость: {self.total_cost} руб.")

    def pay(self):
        if self.total_cost == 0:
            messagebox.showinfo("Корзина пуста", "Добавьте напитки перед оплатой.")
        else:
            self.save_order(self.cart_items, self.total_cost)
            messagebox.showinfo("Оплата", f"Вы оплатили {self.total_cost} руб. Заказ сохранён в истории.")
            self.clear_cart()

    def clear_cart(self):
        for item in self.cart_items:
            item["frame"].destroy()
        self.cart_items.clear()
        self.total_cost = 0
        self.update_total()

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeApp(root)
    root.mainloop()
