import sys
from typing import Optional, List, Dict
from dataclasses import dataclass
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import mysql.connector


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Lbhtrnjh_4231',
    'database': 'cafeteria_db',
    'port': 3305
}


@dataclass
class ProductData:
    id: int
    name: str
    price: float
    description: str = ""
    weight: str = ""
    category_name: str = ""


@dataclass
class CartItem:
    product: ProductData
    quantity: int


class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.connect_to_database()
    
    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(**db_config)
        except mysql.connector.Error:
            self.connection = None
    
    def execute_select(self, query: str, params: tuple = ()) -> List[Dict]:
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except:
            return []
    
    def execute_insert(self, query: str, params: tuple = ()) -> Optional[int]:
        if not self.connection:
            return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except:
            return None


class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(400, 250)
        LoginDialog.setWindowTitle("Авторизация")
        
        self.verticalLayout = QVBoxLayout(LoginDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.label_title = QLabel(LoginDialog)
        self.label_title.setObjectName("label_title")
        self.label_title.setText("Система учета кафетерия")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_title)
        
        self.label_username = QLabel(LoginDialog)
        self.label_username.setObjectName("label_username")
        self.label_username.setText("Логин:")
        self.verticalLayout.addWidget(self.label_username)
        
        self.lineEdit_username = QLineEdit(LoginDialog)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_username.setPlaceholderText("Введите имя пользователя")
        self.verticalLayout.addWidget(self.lineEdit_username)
        
        self.label_password = QLabel(LoginDialog)
        self.label_password.setObjectName("label_password")
        self.label_password.setText("Пароль:")
        self.verticalLayout.addWidget(self.label_password)
        
        self.lineEdit_password = QLineEdit(LoginDialog)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setPlaceholderText("Введите пароль")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.verticalLayout.addWidget(self.lineEdit_password)
        
        self.pushButton_login = QPushButton(LoginDialog)
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_login.setText("Войти в систему")
        self.pushButton_login.setMinimumSize(0, 40)
        self.verticalLayout.addWidget(self.pushButton_login)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
    
    def retranslateUi(self, LoginDialog):
        pass


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.setup_connections()
        self.apply_stylesheet()
    
    def setup_connections(self):
        self.ui.pushButton_login.clicked.connect(self.handle_login)
    
    def apply_stylesheet(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #212529;
                font-size: 13px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
            }
            QPushButton {
                background-color: #FF5722;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
    
    def handle_login(self):
        username = self.ui.lineEdit_username.text().strip()
        password = self.ui.lineEdit_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Ошибка ввода", "Заполните все поля")
            return
        
        if username == "admin" and password == "123":
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка авторизации", "Неверный логин или пароль")


class Ui_ProductCardWidget(object):
    def setupUi(self, ProductCardWidget):
        if not ProductCardWidget.objectName():
            ProductCardWidget.setObjectName("ProductCardWidget")
        ProductCardWidget.resize(240, 300)
        
        self.verticalLayout = QVBoxLayout(ProductCardWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        
        self.label_image = QLabel(ProductCardWidget)
        self.label_image.setObjectName("label_image")
        self.label_image.setMinimumSize(0, 120)
        self.label_image.setMaximumSize(16777215, 120)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_image)
        
        self.label_name = QLabel(ProductCardWidget)
        self.label_name.setObjectName("label_name")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_name.setFont(font)
        self.label_name.setWordWrap(True)
        self.label_name.setMaximumHeight(40)
        self.verticalLayout.addWidget(self.label_name)
        
        self.label_description = QLabel(ProductCardWidget)
        self.label_description.setObjectName("label_description")
        self.label_description.setWordWrap(True)
        self.label_description.setMaximumHeight(45)
        self.verticalLayout.addWidget(self.label_description)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        self.horizontalLayout_bottom = QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        
        self.label_price = QLabel(ProductCardWidget)
        self.label_price.setObjectName("label_price")
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(True)
        self.label_price.setFont(font2)
        self.horizontalLayout_bottom.addWidget(self.label_price)
        
        self.label_weight = QLabel(ProductCardWidget)
        self.label_weight.setObjectName("label_weight")
        self.horizontalLayout_bottom.addWidget(self.label_weight)
        
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_bottom.addItem(spacerItem2)
        
        self.pushButton_add = QPushButton(ProductCardWidget)
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton_add.setText("Добавить")
        self.pushButton_add.setMinimumSize(85, 32)
        self.pushButton_add.setMaximumSize(85, 32)
        self.horizontalLayout_bottom.addWidget(self.pushButton_add)
        
        self.verticalLayout.addLayout(self.horizontalLayout_bottom)
    
    def retranslateUi(self, ProductCardWidget):
        pass


class ProductCardWidget(QFrame):
    def __init__(self, product_data: ProductData, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.ui = Ui_ProductCardWidget()
        self.ui.setupUi(self)
        self.setup_product_data()
        self.setup_connections()
        self.apply_stylesheet()
        self.setCursor(Qt.PointingHandCursor)
    
    def setup_product_data(self):
        self.ui.label_name.setText(self.product_data.name)
        
        desc = self.product_data.description
        if len(desc) > 50:
            desc = desc[:50] + "..."
        self.ui.label_description.setText(desc)
        self.ui.label_description.setStyleSheet("color: #6c757d; font-size: 11px;")
        
        self.ui.label_price.setText(f"{self.product_data.price:.2f} руб.")
        self.ui.label_price.setStyleSheet("color: #FF5722;")
        
        self.ui.label_weight.setText(self.product_data.weight)
        self.ui.label_weight.setStyleSheet("color: #6c757d; font-size: 11px;")
        
        self.ui.label_image.setStyleSheet("""
            background-color: #e9ecef;
            border: 2px dashed #adb5bd;
            border-radius: 8px;
            color: #6c757d;
            font-size: 12px;
        """)
    
    def setup_connections(self):
        self.ui.pushButton_add.clicked.connect(self.handle_add_to_cart)
    
    def apply_stylesheet(self):
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
            }
        """)
    
    def handle_add_to_cart(self):
        main_window = self.window()
        if hasattr(main_window, 'add_product_to_cart'):
            main_window.add_product_to_cart(self.product_data)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.show_product_info()
    
    def show_product_info(self):
        main_window = self.window()
        if hasattr(main_window, 'show_product_details_dialog'):
            main_window.show_product_details_dialog(self.product_data)


class Ui_CatalogWidget(object):
    def setupUi(self, CatalogWidget):
        if not CatalogWidget.objectName():
            CatalogWidget.setObjectName("CatalogWidget")
        
        self.verticalLayout = QVBoxLayout(CatalogWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.horizontalLayout_header = QHBoxLayout()
        self.horizontalLayout_header.setObjectName("horizontalLayout_header")
        
        self.label_header = QLabel(CatalogWidget)
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Каталог продуктов")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_header.setFont(font)
        self.horizontalLayout_header.addWidget(self.label_header)
        
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_header.addItem(spacerItem)
        
        self.pushButton_goto_cart = QPushButton(CatalogWidget)
        self.pushButton_goto_cart.setObjectName("pushButton_goto_cart")
        self.pushButton_goto_cart.setText("Корзина")
        self.horizontalLayout_header.addWidget(self.pushButton_goto_cart)
        
        self.verticalLayout.addLayout(self.horizontalLayout_header)
        
        self.horizontalLayout_filters = QHBoxLayout()
        self.horizontalLayout_filters.setObjectName("horizontalLayout_filters")
        
        self.lineEdit_search = QLineEdit(CatalogWidget)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.lineEdit_search.setPlaceholderText("Поиск...")
        self.horizontalLayout_filters.addWidget(self.lineEdit_search)
        
        self.comboBox_category = QComboBox(CatalogWidget)
        self.comboBox_category.setObjectName("comboBox_category")
        self.horizontalLayout_filters.addWidget(self.comboBox_category)
        
        self.pushButton_sort_asc = QPushButton(CatalogWidget)
        self.pushButton_sort_asc.setObjectName("pushButton_sort_asc")
        self.pushButton_sort_asc.setText("Цена (возр.)")
        self.horizontalLayout_filters.addWidget(self.pushButton_sort_asc)
        
        self.pushButton_sort_desc = QPushButton(CatalogWidget)
        self.pushButton_sort_desc.setObjectName("pushButton_sort_desc")
        self.pushButton_sort_desc.setText("Цена (убыв.)")
        self.horizontalLayout_filters.addWidget(self.pushButton_sort_desc)
        
        self.verticalLayout.addLayout(self.horizontalLayout_filters)
        
        self.scrollArea = QScrollArea(CatalogWidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.gridLayout_products = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_products.setObjectName("gridLayout_products")
        self.gridLayout_products.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
    
    def retranslateUi(self, CatalogWidget):
        pass


class CatalogWidget(QWidget):
    def __init__(self, db_connection: DatabaseConnection, parent=None):
        super().__init__(parent)
        self.db_connection = db_connection
        self.current_sort_order = "ASC"
        self.ui = Ui_CatalogWidget()
        self.ui.setupUi(self)
        self.setup_connections()
        self.apply_stylesheet()
        self.load_categories()
        self.refresh_product_list()
    
    def setup_connections(self):
        self.ui.pushButton_goto_cart.clicked.connect(self.handle_goto_cart)
        self.ui.lineEdit_search.textChanged.connect(self.refresh_product_list)
        self.ui.comboBox_category.currentIndexChanged.connect(self.refresh_product_list)
        self.ui.pushButton_sort_asc.clicked.connect(lambda: self.change_sort_order("ASC"))
        self.ui.pushButton_sort_desc.clicked.connect(lambda: self.change_sort_order("DESC"))
    
    def apply_stylesheet(self):
        self.ui.scrollArea.setStyleSheet("border: none; background-color: #f8f9fa;")
    
    def load_categories(self):
        self.ui.comboBox_category.clear()
        self.ui.comboBox_category.addItem("Любая категория", None)
        
        categories = self.db_connection.execute_select("SELECT * FROM categories")
        for cat in categories:
            self.ui.comboBox_category.addItem(cat['name'], cat['id'])
    
    def change_sort_order(self, order: str):
        self.current_sort_order = order
        self.refresh_product_list()
    
    def refresh_product_list(self):
        while self.ui.gridLayout_products.count():
            item = self.ui.gridLayout_products.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        query = """
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.id 
            WHERE p.is_active = 1
        """
        params = []
        
        search_text = self.ui.lineEdit_search.text().strip()
        if search_text:
            query += " AND (p.name LIKE %s OR p.description LIKE %s)"
            search_pattern = f"%{search_text}%"
            params.extend([search_pattern, search_pattern])
        
        category_id = self.ui.comboBox_category.currentData()
        if category_id:
            query += " AND p.category_id = %s"
            params.append(category_id)
        
        query += f" ORDER BY p.price {self.current_sort_order}"
        
        products = self.db_connection.execute_select(query, tuple(params))
        
        for index, prod in enumerate(products):
            product_data = ProductData(
                id=prod['id'],
                name=prod['name'],
                price=float(prod['price']),
                description=prod.get('description', ''),
                weight=prod.get('weight', ''),
                category_name=prod.get('category_name', '')
            )
            
            card_widget = ProductCardWidget(product_data)
            row = index // 4
            col = index % 4
            self.ui.gridLayout_products.addWidget(card_widget, row, col)
    
    def handle_goto_cart(self):
        main_window = self.window()
        if hasattr(main_window, 'switch_to_cart_page'):
            main_window.switch_to_cart_page()


class Ui_CartWidget(object):
    def setupUi(self, CartWidget):
        if not CartWidget.objectName():
            CartWidget.setObjectName("CartWidget")
        
        self.horizontalLayout_main = QHBoxLayout(CartWidget)
        self.horizontalLayout_main.setObjectName("horizontalLayout_main")
        
        self.verticalLayout_left = QVBoxLayout()
        self.verticalLayout_left.setObjectName("verticalLayout_left")
        
        self.pushButton_back = QPushButton(CartWidget)
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_back.setText("Назад")
        self.verticalLayout_left.addWidget(self.pushButton_back)
        
        self.label_cart_title = QLabel(CartWidget)
        self.label_cart_title.setObjectName("label_cart_title")
        self.label_cart_title.setText("Корзина заказа")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_cart_title.setFont(font)
        self.verticalLayout_left.addWidget(self.label_cart_title)
        
        self.tableWidget_cart = QTableWidget(CartWidget)
        self.tableWidget_cart.setObjectName("tableWidget_cart")
        self.tableWidget_cart.setColumnCount(5)
        self.tableWidget_cart.setHorizontalHeaderLabels([
            "Наименование", "Цена", "Количество", "Сумма", ""
        ])
        self.tableWidget_cart.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_cart.setColumnWidth(0, 200)
        self.tableWidget_cart.setColumnWidth(1, 80)
        self.tableWidget_cart.setColumnWidth(2, 100)
        self.tableWidget_cart.setColumnWidth(3, 100)
        self.tableWidget_cart.setColumnWidth(4, 100)
        self.verticalLayout_left.addWidget(self.tableWidget_cart)
        
        self.horizontalLayout_main.addLayout(self.verticalLayout_left, 3)
        
        self.verticalLayout_right = QVBoxLayout()
        self.verticalLayout_right.setObjectName("verticalLayout_right")
        
        self.label_order_title = QLabel(CartWidget)
        self.label_order_title.setObjectName("label_order_title")
        self.label_order_title.setText("Заказ клиента")
        font2 = QFont()
        font2.setPointSize(16)
        font2.setBold(True)
        self.label_order_title.setFont(font2)
        self.verticalLayout_right.addWidget(self.label_order_title)
        
        self.label_client = QLabel(CartWidget)
        self.label_client.setObjectName("label_client")
        self.label_client.setText("Клиент:")
        self.verticalLayout_right.addWidget(self.label_client)
        
        self.comboBox_client = QComboBox(CartWidget)
        self.comboBox_client.setObjectName("comboBox_client")
        self.verticalLayout_right.addWidget(self.comboBox_client)
        
        self.checkBox_no_client = QCheckBox(CartWidget)
        self.checkBox_no_client.setObjectName("checkBox_no_client")
        self.checkBox_no_client.setText("Без клиента")
        self.verticalLayout_right.addWidget(self.checkBox_no_client)
        
        self.label_total = QLabel(CartWidget)
        self.label_total.setObjectName("label_total")
        self.label_total.setText("Итого: 0.00 руб.")
        font3 = QFont()
        font3.setPointSize(16)
        font3.setBold(True)
        self.label_total.setFont(font3)
        self.verticalLayout_right.addWidget(self.label_total)
        
        self.label_payment = QLabel(CartWidget)
        self.label_payment.setObjectName("label_payment")
        self.label_payment.setText("Тип оплаты:")
        self.verticalLayout_right.addWidget(self.label_payment)
        
        self.comboBox_payment = QComboBox(CartWidget)
        self.comboBox_payment.setObjectName("comboBox_payment")
        self.comboBox_payment.addItems(["Наличные", "Карта", "Онлайн"])
        self.verticalLayout_right.addWidget(self.comboBox_payment)
        
        self.label_order_type = QLabel(CartWidget)
        self.label_order_type.setObjectName("label_order_type")
        self.label_order_type.setText("Тип заказа:")
        self.verticalLayout_right.addWidget(self.label_order_type)
        
        self.radioButton_in_place = QRadioButton(CartWidget)
        self.radioButton_in_place.setObjectName("radioButton_in_place")
        self.radioButton_in_place.setText("В заведении")
        self.radioButton_in_place.setChecked(True)
        self.verticalLayout_right.addWidget(self.radioButton_in_place)
        
        self.radioButton_takeaway = QRadioButton(CartWidget)
        self.radioButton_takeaway.setObjectName("radioButton_takeaway")
        self.radioButton_takeaway.setText("На вынос")
        self.verticalLayout_right.addWidget(self.radioButton_takeaway)
        
        self.radioButton_delivery = QRadioButton(CartWidget)
        self.radioButton_delivery.setObjectName("radioButton_delivery")
        self.radioButton_delivery.setText("Курьером")
        self.verticalLayout_right.addWidget(self.radioButton_delivery)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_right.addItem(spacerItem)
        
        self.pushButton_submit_order = QPushButton(CartWidget)
        self.pushButton_submit_order.setObjectName("pushButton_submit_order")
        self.pushButton_submit_order.setText("Оформить заказ")
        self.pushButton_submit_order.setMinimumSize(0, 50)
        self.verticalLayout_right.addWidget(self.pushButton_submit_order)
        
        self.horizontalLayout_main.addLayout(self.verticalLayout_right, 1)
    
    def retranslateUi(self, CartWidget):
        pass


class CartWidget(QWidget):
    def __init__(self, db_connection: DatabaseConnection, parent=None):
        super().__init__(parent)
        self.db_connection = db_connection
        self.cart_items_list: List[CartItem] = []
        self.ui = Ui_CartWidget()
        self.ui.setupUi(self)
        self.setup_connections()
        self.apply_stylesheet()
        self.load_clients_list()
    
    def setup_connections(self):
        self.ui.pushButton_back.clicked.connect(self.handle_back_to_catalog)
        self.ui.checkBox_no_client.stateChanged.connect(self.toggle_client_combo)
        self.ui.pushButton_submit_order.clicked.connect(self.handle_submit_order)
    
    def apply_stylesheet(self):
        self.ui.label_total.setStyleSheet("color: #FF5722; margin-top: 20px;")
        self.ui.label_payment.setStyleSheet("margin-top: 15px;")
        self.ui.label_order_type.setStyleSheet("margin-top: 15px;")
        self.ui.pushButton_submit_order.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
        """)
    
    def load_clients_list(self):
        self.ui.comboBox_client.clear()
        clients = self.db_connection.execute_select("SELECT * FROM clients")
        
        for client in clients:
            display_name = client.get('name') or client['phone_number']
            self.ui.comboBox_client.addItem(display_name, client['phone_number'])
    
    def toggle_client_combo(self, state):
        self.ui.comboBox_client.setEnabled(not state)
    
    def add_product_to_cart(self, product: ProductData):
        for item in self.cart_items_list:
            if item.product.id == product.id:
                item.quantity += 1
                self.update_cart_table()
                return
        
        self.cart_items_list.append(CartItem(product=product, quantity=1))
        self.update_cart_table()
    
    def update_cart_table(self):
        self.ui.tableWidget_cart.setRowCount(len(self.cart_items_list))
        total_sum = 0.0
        
        for row_index, item in enumerate(self.cart_items_list):
            item_name = QTableWidgetItem(item.product.name)
            self.ui.tableWidget_cart.setItem(row_index, 0, item_name)
            
            item_price = QTableWidgetItem(f"{item.product.price:.2f}")
            self.ui.tableWidget_cart.setItem(row_index, 1, item_price)
            
            spinbox_quantity = QSpinBox()
            spinbox_quantity.setRange(1, 99)
            spinbox_quantity.setValue(item.quantity)
            spinbox_quantity.valueChanged.connect(
                lambda val, idx=row_index: self.update_item_quantity(idx, val)
            )
            self.ui.tableWidget_cart.setCellWidget(row_index, 2, spinbox_quantity)
            
            item_total = item.product.price * item.quantity
            total_sum += item_total
            item_sum = QTableWidgetItem(f"{item_total:.2f}")
            self.ui.tableWidget_cart.setItem(row_index, 3, item_sum)
            
            button_remove = QPushButton("Удалить")
            button_remove.clicked.connect(
                lambda _, idx=row_index: self.remove_item_from_cart(idx)
            )
            self.ui.tableWidget_cart.setCellWidget(row_index, 4, button_remove)
        
        self.ui.label_total.setText(f"Итого: {total_sum:.2f} руб.")
    
    def update_item_quantity(self, row: int, value: int):
        if 0 <= row < len(self.cart_items_list):
            self.cart_items_list[row].quantity = value
            self.update_cart_table()
    
    def remove_item_from_cart(self, row: int):
        if 0 <= row < len(self.cart_items_list):
            del self.cart_items_list[row]
            self.update_cart_table()
    
    def handle_submit_order(self):
        if not self.cart_items_list:
            QMessageBox.warning(self, "Пустая корзина", "Добавьте товары в корзину")
            return
        
        reply = QMessageBox.question(
            self, "Подтверждение", "Оформить заказ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        if self.ui.radioButton_in_place.isChecked():
            order_type = 1
        elif self.ui.radioButton_takeaway.isChecked():
            order_type = 2
        else:
            order_type = 3
        
        payment_text = self.ui.comboBox_payment.currentText()
        if payment_text == "Наличные":
            payment_id = 1
        elif payment_text == "Карта":
            payment_id = 2
        else:
            payment_id = 3
        
        total = sum(item.product.price * item.quantity for item in self.cart_items_list)
        
        order_query = """
            INSERT INTO orders 
            (order_number, date_create, type_id, employer_id, total_cost, pay_id) 
            VALUES (
                (SELECT IFNULL(MAX(order_number), 0) + 1 FROM orders o2),
                NOW(), %s, 1, %s, %s
            )
        """
        
        order_id = self.db_connection.execute_insert(order_query, (order_type, total, payment_id))
        
        if order_id:
            for item in self.cart_items_list:
                item_query = """
                    INSERT INTO order_shopcase 
                    (order_id, product_id, current_count) 
                    VALUES (%s, %s, %s)
                """
                self.db_connection.execute_insert(
                    item_query,
                    (order_id, item.product.id, item.quantity)
                )
            
            QMessageBox.information(self, "Успех", f"Заказ №{order_id} оформлен")
            
            self.cart_items_list.clear()
            self.update_cart_table()
            self.handle_back_to_catalog()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать заказ")
    
    def handle_back_to_catalog(self):
        main_window = self.window()
        if hasattr(main_window, 'switch_to_catalog_page'):
            main_window.switch_to_catalog_page()


class Ui_ProductDetailsDialog(object):
    def setupUi(self, ProductDetailsDialog):
        if not ProductDetailsDialog.objectName():
            ProductDetailsDialog.setObjectName("ProductDetailsDialog")
        ProductDetailsDialog.resize(450, 400)
        
        self.verticalLayout = QVBoxLayout(ProductDetailsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.label_product_name = QLabel(ProductDetailsDialog)
        self.label_product_name.setObjectName("label_product_name")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_product_name.setFont(font)
        self.label_product_name.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_product_name)
        
        self.line = QFrame(ProductDetailsDialog)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        
        self.verticalLayout_info = QVBoxLayout()
        self.verticalLayout_info.setObjectName("verticalLayout_info")
        self.verticalLayout_info.setSpacing(10)
        
        self.label_category = QLabel(ProductDetailsDialog)
        self.label_category.setObjectName("label_category")
        self.verticalLayout_info.addWidget(self.label_category)
        
        self.label_description = QLabel(ProductDetailsDialog)
        self.label_description.setObjectName("label_description")
        self.label_description.setWordWrap(True)
        self.verticalLayout_info.addWidget(self.label_description)
        
        self.label_price = QLabel(ProductDetailsDialog)
        self.label_price.setObjectName("label_price")
        self.verticalLayout_info.addWidget(self.label_price)
        
        self.label_weight = QLabel(ProductDetailsDialog)
        self.label_weight.setObjectName("label_weight")
        self.verticalLayout_info.addWidget(self.label_weight)
        
        self.verticalLayout.addLayout(self.verticalLayout_info)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        self.pushButton_close = QPushButton(ProductDetailsDialog)
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.setText("Закрыть")
        self.verticalLayout.addWidget(self.pushButton_close)
    
    def retranslateUi(self, ProductDetailsDialog):
        ProductDetailsDialog.setWindowTitle("Информация о продукте")


class ProductDetailsDialog(QDialog):
    active_dialog_instance = None
    
    @classmethod
    def show_dialog(cls, product: ProductData, parent):
        if cls.active_dialog_instance:
            cls.active_dialog_instance.close()
        
        cls.active_dialog_instance = cls(product, parent)
        cls.active_dialog_instance.show()
    
    def __init__(self, product: ProductData, parent):
        super().__init__(parent)
        self.product = product
        self.ui = Ui_ProductDetailsDialog()
        self.ui.setupUi(self)
        self.setup_product_info()
        self.setup_connections()
    
    def setup_product_info(self):
        self.ui.label_product_name.setText(self.product.name)
        
        category_text = f"<b>Категория:</b> {self.product.category_name or 'Не указана'}"
        self.ui.label_category.setText(category_text)
        
        desc_text = f"<b>Описание:</b> {self.product.description or 'Нет описания'}"
        self.ui.label_description.setText(desc_text)
        
        price_text = f"<b>Цена:</b> <span style='color:#FF5722; font-size:16px;'>{self.product.price:.2f} руб.</span>"
        self.ui.label_price.setText(price_text)
        
        if self.product.weight:
            weight_text = f"<b>Вес/Объем:</b> {self.product.weight}"
            self.ui.label_weight.setText(weight_text)
        else:
            self.ui.label_weight.hide()
    
    def setup_connections(self):
        self.ui.pushButton_close.clicked.connect(self.close)
    
    def closeEvent(self, event):
        ProductDetailsDialog.active_dialog_instance = None
        event.accept()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 750)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Система учета кафетерия - Оператор-кассир")
    
    def retranslateUi(self, MainWindow):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_connection = DatabaseConnection()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_pages()
        self.apply_global_stylesheet()
    
    def setup_pages(self):
        self.catalog_page = CatalogWidget(self.db_connection)
        self.ui.stackedWidget.addWidget(self.catalog_page)
        
        self.cart_page = CartWidget(self.db_connection)
        self.ui.stackedWidget.addWidget(self.cart_page)
    
    def apply_global_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QWidget {
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #FF5722;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QSpinBox {
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 8px;
                border: 1px solid #E0E0E0;
                font-weight: bold;
            }
            QCheckBox, QRadioButton {
                spacing: 8px;
            }
            QScrollArea {
                background-color: #FAFAFA;
                border: none;
            }
        """)
    
    def switch_to_catalog_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.catalog_page)
    
    def switch_to_cart_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.cart_page)
    
    def add_product_to_cart(self, product: ProductData):
        self.cart_page.add_product_to_cart(product)
        QMessageBox.information(self, "Добавлено", f"Товар «{product.name}» добавлен в корзину")
    
    def show_product_details_dialog(self, product: ProductData):
        ProductDetailsDialog.show_dialog(product, self)


def main():
    app = QApplication(sys.argv)
    
    login_dialog = LoginDialog()
    
    if login_dialog.exec() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()