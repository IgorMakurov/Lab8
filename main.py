#Требуется написать ООП с графическим интерфейсом в соответствии со своим вариантом.
#Должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
#Ввод данных из файла с контролем правильности ввода. Базы данных не использовать.
#При необходимости сохранять информацию в файлах, разделяя значения запятыми (CSV файлы) или пробелами.
#Для GUI и визуализации использовать библиотеку tkinter.
#Вариант 13
#Объекты – торговые сделки
#Функции:
#сегментация полного списка сделок по видам товаров;
#визуализация предыдущей функции в форме круговой диаграммы;
#сегментация полного списка договоров по продавцам;
#визуализация предыдущей функции в форме круговой диаграммы

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Contract:
    def __init__(self, contract_id, computer_type, supplier, quantity):
        self.contract_id = contract_id
        self.computer_type = computer_type
        self.supplier = supplier
        self.quantity = quantity

    def __str__(self):
        return f"ID: {self.contract_id}, Тип: {self.computer_type}, Продавец: {self.supplier}, Количество: {self.quantity}"

    def to_csv(self):
        return f"{self.contract_id},{self.computer_type},{self.supplier},{self.quantity}"

    @staticmethod
    def from_csv(csv_string):
        try:
            contract_id, computer_type, supplier, quantity = csv_string.strip().split(',')
            # Валидация данных
            if not isinstance(contract_id, str) or not contract_id:
                raise ValueError("ID контракта должен быть не пустой строкой")
            if not isinstance(computer_type, str) or not computer_type:
                raise ValueError("Тип товара должен быть не пустой строкой")
            if not isinstance(supplier, str) or not supplier:
                raise ValueError("Продавец должен быть не пустой строкой")
            quantity = int(quantity)
            if quantity <= 0:
              raise ValueError("Количество должно быть целым числом больше 0")
            
            return Contract(contract_id, computer_type, supplier, quantity)
        except (ValueError, Exception):
            return None

def load_contracts_from_csv(filename):
    contracts = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                contract = Contract.from_csv(line)
                if contract:
                    contracts.append(contract)
                else:
                    messagebox.showwarning("Предупреждение", f"Некорректная строка в файле: {line.strip()}")
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден.")
    return contracts

def segment_by_computer_type(contracts):
    types = {}
    for contract in contracts:
      if contract.computer_type in types:
        types[contract.computer_type] += contract.quantity
      else:
        types[contract.computer_type] = contract.quantity
    return types

def segment_by_supplier(contracts):
    suppliers = {}
    for contract in contracts:
      if contract.supplier in suppliers:
        suppliers[contract.supplier] += contract.quantity
      else:
        suppliers[contract.supplier] = contract.quantity
    return suppliers

class ContractApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Торговые сделки")
        self.contracts = []
        self.plot_frame = None # Для хранения фрейма с графиком и кнопкой
        self.current_plot = None # Для хранения текущего графика

        # Меню
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть CSV", command=self.load_from_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        root.config(menu=menu_bar)

        # Кнопки
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        btn_type_segmentation = tk.Button(frame_buttons, text="Сегментация по типу", command=self.show_type_pie)
        btn_type_segmentation.pack(side=tk.LEFT, padx=5)

        btn_supplier_segmentation = tk.Button(frame_buttons, text="Сегментация по продавцам", command=self.show_supplier_pie)
        btn_supplier_segmentation.pack(side=tk.LEFT, padx=5)

        # Текстовое поле
        self.text_area = tk.Text(root, height=15, width=80)
        self.text_area.pack(padx=10, pady=10)


    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.contracts = load_contracts_from_csv(filename)
            if self.contracts:
              self.update_text_area()
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить данные из файла.")

    def update_text_area(self):
        self.text_area.delete("1.0", tk.END)
        for contract in self.contracts:
            self.text_area.insert(tk.END, str(contract) + "\n")


    def show_type_pie(self):
        if not self.contracts:
            messagebox.showwarning("Предупреждение", "Нет данных для построения диаграммы.")
            return
        segmented_data = segment_by_computer_type(self.contracts)
        self.plot_pie_chart(segmented_data, "Распределение товаров по типам")

    def show_supplier_pie(self):
        if not self.contracts:
            messagebox.showwarning("Предупреждение", "Нет данных для построения диаграммы.")
            return
        segmented_data = segment_by_supplier(self.contracts)
        self.plot_pie_chart(segmented_data, "Распределение товаров по продавцам")

    def plot_pie_chart(self, data, title):
        if not data:
            messagebox.showwarning("Предупреждение", "Нет данных для диаграммы.")
            return
        
        if self.plot_frame: # Удаляет предыдущий фрейм
            self.plot_frame.destroy()
            self.plot_frame = None

        if self.current_plot: # Закрывает предыдущий график если он есть
            plt.close(self.current_plot)
            self.current_plot = None

        self.plot_frame = tk.Frame(self.root)  # Создает фрейм для графика и кнопки
        self.plot_frame.pack()

        labels = list(data.keys())
        values = list(data.values())

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Равные оси для круга
        ax.set_title(title)

        self.current_plot = fig # Сохраняет ссылку на график

        # Создает виджет для отображения графика в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()


        def destroy_plot():
            if self.plot_frame:
               self.plot_frame.destroy()  # Удаляет фрейм с графиком и кнопкой
               self.plot_frame = None # Сбрасывает ссылку
            if self.current_plot:
               plt.close(self.current_plot)
               self.current_plot = None


        destroy_button = tk.Button(self.plot_frame, text="Закрыть график", command=destroy_plot)
        destroy_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContractApp(root)
    root.mainloop()