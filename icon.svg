import sys
import mysql.connector
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QCheckBox,
    QRadioButton,
    QScrollArea,
    QGridLayout,
    QFrame,
    QMessageBox,
    QStackedWidget,
    QDialog,
    QGroupBox,
    QButtonGroup,
)
from PySide6.QtCore import Qt, Signal

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Lbhtrnjh_4231",
    "database": "cafeteria_db",
    "port": 3305,
}

STYLE = """QMainWindow, QWidget, QDialog { background: #FFF; color: #333; }QLabel { color: #333; }QPushButton { background: #FF5722; color: white; border: none; border-radius: 5px; padding: 10px; font-weight: bold; }QPushButton:hover { background: #E64A19; }QLineEdit, QComboBox, QSpinBox { border: 1px solid #E0E0E0; border-radius: 5px; padding: 8px; background: #FFF; color: #333; }QComboBox QAbstractItemView { background: #FFF; color: #333; }QTableWidget { background: #FFF; color: #333; gridline-color: #E0E0E0; }QHeaderView::section { background: #F5F5F5; color: #333; padding: 8px; border: 1px solid #E0E0E0; }QCheckBox, QRadioButton { color: #333; }QScrollArea { background: #FAFAFA; }QGroupBox { color: #333; }
"""


class LoginDialog(QDialog):
    """Окно авторизации"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(350, 200)
        self.setStyleSheet(STYLE)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Вход в систему</h2>"))

        layout.addWidget(QLabel("Логин:"))
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        layout.addWidget(self.login_input)

        layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(self.login_btn)

        self.user = None

    def check_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        if login == "admin" and password == "123":
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")


class DB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
        except:
            self.conn = None

    def query(self, sql, params=()):
        if not self.conn:
            return []
        cur = self.conn.cursor(dictionary=True)
        cur.execute(sql, params)
        result = cur.fetchall()
        cur.close()
        return result

    def execute(self, sql, params=()):
        if not self.conn:
            return None
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        lid = cur.lastrowid
        cur.close()
        return lid


class ProductCard(QFrame):
    add_clicked = Signal(dict)
    card_clicked = Signal(dict)

    def __init__(self, product):
        super().__init__()
        self.product = product
        self.setFixedSize(250, 280)
        self.setStyleSheet(
            "QFrame { background: #FFF; border: 1px solid #E0E0E0; border-radius: 8px; }"
        )
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)

        img = QLabel("Изображение")
        img.setAlignment(Qt.AlignCenter)
        img.setFixedHeight(100)
        img.setStyleSheet("background: #F5F5F5; border: 1px dashed #CCC; color: #999;")
        layout.addWidget(img)

        layout.addWidget(QLabel(f"<b>{product['name']}</b>"))
        desc = (
            product.get("description", "")[:40] + "..."
            if len(product.get("description", "")) > 40
            else product.get("description", "")
        )
        layout.addWidget(QLabel(f"<span style='color:#777'>{desc}</span>"))
        layout.addStretch()

        bottom = QHBoxLayout()
        bottom.addWidget(
            QLabel(f"<b style='color:#FF5722'>{product['price']:.2f} руб.</b>")
        )
        bottom.addWidget(
            QLabel(f"<span style='color:#999'>{product.get('weight', '')}</span>")
        )
        bottom.addStretch()

        btn = QPushButton("Добавить")
        btn.setFixedSize(90, 30)
        btn.setStyleSheet(
            "QPushButton { background: #FF5722; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background: #E64A19; }"
        )
        btn.clicked.connect(lambda: self.add_clicked.emit(self.product))
        bottom.addWidget(btn)
        layout.addLayout(bottom)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.card_clicked.emit(self.product)


class CatalogPage(QWidget):
    product_added = Signal(dict)
    go_to_cart = Signal()
    product_clicked = Signal(dict)

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.sort_order = "ASC"

        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        header.addWidget(QLabel("<h2>Каталог продуктов</h2>"))
        header.addStretch()
        cart_btn = QPushButton("🛒 Корзина")
        cart_btn.clicked.connect(self.go_to_cart.emit)
        header.addWidget(cart_btn)
        layout.addLayout(header)

        filters = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Поиск...")
        self.search.textChanged.connect(self.load)
        filters.addWidget(self.search)

        self.category = QComboBox()
        self.category.addItem("Любая категория", None)
        for c in db.query("SELECT * FROM categories"):
            self.category.addItem(c["name"], c["id"])
        self.category.currentIndexChanged.connect(self.load)
        filters.addWidget(self.category)

        asc_btn = QPushButton("Цена ↑")
        asc_btn.clicked.connect(lambda: self.set_sort("ASC"))
        filters.addWidget(asc_btn)

        desc_btn = QPushButton("Цена ↓")
        desc_btn.clicked.connect(lambda: self.set_sort("DESC"))
        filters.addWidget(desc_btn)
        layout.addLayout(filters)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: #FAFAFA;")
        self.grid_widget = QWidget()
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        scroll.setWidget(self.grid_widget)
        layout.addWidget(scroll)

        self.load()

    def set_sort(self, order):
        self.sort_order = order
        self.load()

    def load(self):
        while self.grid.count():
            w = self.grid.takeAt(0).widget()
            if w:
                w.deleteLater()

        sql = "SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id=c.id WHERE p.is_active=1"
        params = []

        if self.search.text():
            sql += " AND (p.name LIKE %s OR p.description LIKE %s)"
            params += [f"%{self.search.text()}%"] * 2

        if self.category.currentData():
            sql += " AND p.category_id=%s"
            params.append(self.category.currentData())

        sql += f" ORDER BY p.price {self.sort_order}"

        products = self.db.query(sql, params)
        for i, p in enumerate(products):
            card = ProductCard(p)
            card.add_clicked.connect(self.product_added.emit)
            card.card_clicked.connect(self.product_clicked.emit)
            self.grid.addWidget(card, i // 4, i % 4)


class CartPage(QWidget):
    go_back = Signal()
    order_done = Signal()

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.items = []

        main = QHBoxLayout(self)

        left = QVBoxLayout()
        back = QPushButton("← Назад")
        back.clicked.connect(self.go_back.emit)
        left.addWidget(back)
        left.addWidget(QLabel("<h2>Корзина заказа</h2>"))

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Наименование", "Цена", "Кол-во", "Стоимость", ""]
        )
        left.addWidget(self.table)
        main.addLayout(left, 2)

        right = QVBoxLayout()
        right.addWidget(QLabel("<h2>Заказ клиента</h2>"))

        self.client = QComboBox()
        for c in db.query("SELECT * FROM clients"):
            self.client.addItem(c["name"] or c["phone_number"], c["phone_number"])
        right.addWidget(self.client)

        self.no_client = QCheckBox("Без клиента")
        self.no_client.stateChanged.connect(lambda s: self.client.setEnabled(not s))
        right.addWidget(self.no_client)

        self.total_lbl = QLabel("<b style='color:#FF5722'>Итого: 0.00 руб.</b>")
        right.addWidget(self.total_lbl)

        right.addWidget(QLabel("Тип оплаты:"))
        self.payment = QComboBox()
        self.payment.addItems(["Наличные", "Карта", "Онлайн"])
        right.addWidget(self.payment)

        self.r_here = QRadioButton("В заведении")
        self.r_here.setChecked(True)
        self.r_out = QRadioButton("На вынос")
        self.r_cour = QRadioButton("Курьером")
        right.addWidget(self.r_here)
        right.addWidget(self.r_out)
        right.addWidget(self.r_cour)

        right.addStretch()

        submit = QPushButton("Оформить заказ")
        submit.setMinimumHeight(50)
        submit.clicked.connect(self.submit)
        right.addWidget(submit)
        main.addLayout(right, 1)

    def add(self, product):
        for item in self.items:
            if item["product"]["id"] == product["id"]:
                item["qty"] += 1
                self.refresh()
                return
        self.items.append({"product": product, "qty": 1})
        self.refresh()

    def refresh(self):
        self.table.setRowCount(len(self.items))
        total = 0
        for i, item in enumerate(self.items):
            p, q = item["product"], item["qty"]
            price = float(p["price"])
            sub = price * q
            total += sub

            self.table.setItem(i, 0, QTableWidgetItem(p["name"]))
            self.table.setItem(i, 1, QTableWidgetItem(f"{price:.2f}"))

            spin = QSpinBox()
            spin.setRange(1, 99)
            spin.setValue(q)
            spin.valueChanged.connect(lambda v, row=i: self.set_qty(row, v))
            self.table.setCellWidget(i, 2, spin)

            self.table.setItem(i, 3, QTableWidgetItem(f"{sub:.2f}"))

            del_btn = QPushButton("Исключить")
            del_btn.clicked.connect(lambda _, row=i: self.remove(row))
            self.table.setCellWidget(i, 4, del_btn)

        self.total_lbl.setText(f"<b style='color:#FF5722'>Итого: {total:.2f} руб.</b>")

    def set_qty(self, row, val):
        if row < len(self.items):
            self.items[row]["qty"] = val
            self.refresh()

    def remove(self, row):
        if row < len(self.items):
            self.items.pop(row)
            self.refresh()

    def submit(self):
        if not self.items:
            QMessageBox.warning(self, "Ошибка", "Корзина пуста!")
            return

        if (
            QMessageBox.question(self, "Подтверждение", "Оформить заказ?")
            != QMessageBox.Yes
        ):
            return

        client_id = None if self.no_client.isChecked() else self.client.currentData()
        delivery = (
            "В заведении"
            if self.r_here.isChecked()
            else ("На вынос" if self.r_out.isChecked() else "Курьером")
        )
        total = sum(float(i["product"]["price"]) * i["qty"] for i in self.items)

        order_id = self.db.execute(
            "INSERT INTO orders (order_number, date_create, type_id, employer_id, total_cost, pay_id) VALUES ((SELECT IFNULL(MAX(order_number),0)+1 FROM orders o2), NOW(), %s, 1, %s, %s)",
            (
                1 if self.r_here.isChecked() else (2 if self.r_out.isChecked() else 3),
                total,
                (
                    1
                    if self.payment.currentText() == "Наличные"
                    else (
                        2 if self.payment.currentText() == "Перевод на карту МИР" else 3
                    )
                ),
            ),
        )

        for item in self.items:
            self.db.execute(
                "INSERT INTO order_shopcase (order_id, product_id, current_count) VALUES (%s,%s,%s)",
                (
                    order_id,
                    item["product"]["id"],
                    item["qty"],
                ),
            )

        QMessageBox.information(self, "Успех", f"Заказ #{order_id} оформлен!")
        self.items = []
        self.refresh()
        self.order_done.emit()


class ProductDialog(QDialog):
    _instance = None

    @classmethod
    def show_product(cls, product, parent):
        if cls._instance:
            cls._instance.close()
        cls._instance = cls(product, parent)
        cls._instance.show()

    def __init__(self, product, parent):
        super().__init__(parent)
        self.setWindowTitle("Информация о продукте")
        self.setFixedSize(400, 350)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<h2>{product['name']}</h2>"))
        layout.addWidget(QLabel(f"Категория: {product.get('category_name', '-')}"))
        layout.addWidget(QLabel(f"Описание: {product.get('description', '-')}"))
        layout.addWidget(
            QLabel(f"<b style='color:#FF5722'>Цена: {product['price']:.2f} руб.</b>")
        )
        layout.addWidget(QLabel(f"Вес: {product.get('weight', '-')}"))
        layout.addStretch()

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def closeEvent(self, e):
        ProductDialog._instance = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кафетерий - Оператор-кассир")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet(STYLE)

        self.db = DB()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.catalog = CatalogPage(self.db)
        self.catalog.product_added.connect(self.on_add)
        self.catalog.go_to_cart.connect(lambda: self.stack.setCurrentIndex(1))
        self.catalog.product_clicked.connect(
            lambda p: ProductDialog.show_product(p, self)
        )
        self.stack.addWidget(self.catalog)

        self.cart = CartPage(self.db)
        self.cart.go_back.connect(lambda: self.stack.setCurrentIndex(0))
        self.cart.order_done.connect(lambda: self.stack.setCurrentIndex(0))
        self.stack.addWidget(self.cart)

    def on_add(self, product):
        self.cart.add(product)
        QMessageBox.information(
            self, "Добавлено", f"«{product['product_name']}» добавлен!"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)
