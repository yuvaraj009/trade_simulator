from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QComboBox, QLineEdit, QPushButton, QDoubleSpinBox, 
                            QFormLayout, QGroupBox)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer

class TradeSimulatorUI(QMainWindow):
    def __init__(self, simulator_core):
        super().__init__()
        self.simulator = simulator_core
        self.setup_style()
        self.init_ui()
        
    def setup_style(self):
        # Dark theme palette setup
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)
        
        self.setFont(QFont("Segoe UI", 10))
        
    def init_ui(self):
        self.setWindowTitle('Cryptocurrency Trade Simulator')
        self.setGeometry(100, 100, 1200, 700)
        
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left panel - Inputs
        input_group = QGroupBox("TRADE PARAMETERS")
        input_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        input_layout = QFormLayout()
        input_layout.setVerticalSpacing(15)
        input_layout.setHorizontalSpacing(20)
        
        self.exchange_combo = self.create_styled_combo(["OKX"])
        self.symbol_combo = self.create_styled_combo(["BTC-USDT-SWAP", "ETH-USDT-SWAP", "SOL-USDT-SWAP"])
        self.order_type_combo = self.create_styled_combo(["market"])
        
        # Notice the black text color here for inputs:
        self.quantity_input = self.create_styled_spinbox(0.01, 10000, 100, " USD", input_text_color="black")
        self.volatility_input = self.create_styled_spinbox(0.1, 200, 50, "%", input_text_color="black")
        self.fee_tier_input = self.create_styled_spinbox(0.01, 1, 0.05, "%", input_text_color="black")
        
        self.start_button = QPushButton("START SIMULATION")
        self.start_button.setStyleSheet(self.get_button_style())
        self.start_button.setFixedHeight(40)
        self.start_button.clicked.connect(self.start_simulation)
        
        input_layout.addRow(self.create_styled_label("Exchange:"), self.exchange_combo)
        input_layout.addRow(self.create_styled_label("Spot Asset:"), self.symbol_combo)
        input_layout.addRow(self.create_styled_label("Order Type:"), self.order_type_combo)
        input_layout.addRow(self.create_styled_label("Quantity:"), self.quantity_input)
        input_layout.addRow(self.create_styled_label("Volatility:"), self.volatility_input)
        input_layout.addRow(self.create_styled_label("Fee Tier:"), self.fee_tier_input)
        input_layout.addRow(self.start_button)
        
        input_group.setLayout(input_layout)
        
        # Right panel - Outputs
        output_group = QGroupBox("SIMULATION RESULTS")
        output_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        output_layout = QFormLayout()
        output_layout.setVerticalSpacing(15)
        output_layout.setHorizontalSpacing(20)
        
        self.slippage_label = self.create_output_label("0.00%")
        self.fees_label = self.create_output_label("0.00 USD")
        self.impact_label = self.create_output_label("0.00%")
        self.net_cost_label = self.create_output_label("0.00 USD")
        self.maker_taker_label = self.create_output_label("50% / 50%")
        self.latency_label = self.create_output_label("0.00 ms")
        self.order_book_depth_label = self.create_output_label("0 levels")
        
        output_layout.addRow(self.create_styled_label("Expected Slippage:"), self.slippage_label)
        output_layout.addRow(self.create_styled_label("Expected Fees:"), self.fees_label)
        output_layout.addRow(self.create_styled_label("Market Impact:"), self.impact_label)
        output_layout.addRow(self.create_styled_label("Net Cost:"), self.net_cost_label)
        output_layout.addRow(self.create_styled_label("Maker/Taker:"), self.maker_taker_label)
        output_layout.addRow(self.create_styled_label("Internal Latency:"), self.latency_label)
        output_layout.addRow(self.create_styled_label("Order Book Depth:"), self.order_book_depth_label)
        
        output_group.setLayout(output_layout)
        
        main_layout.addWidget(input_group, 1)
        main_layout.addWidget(output_group, 1)
        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_results)
        self.update_timer.start(100)
        
    def create_styled_combo(self, items):
        combo = QComboBox()
        combo.addItems(items)
        combo.setStyleSheet("""
            QComboBox {
                background-color: #353535;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: #353535;
                color: white;
                selection-background-color: #8e2dc5;
            }
        """)
        combo.setFixedHeight(30)
        return combo
        
    def create_styled_spinbox(self, min_val, max_val, default_val, suffix="", input_text_color="white"):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        if suffix:
            spinbox.setSuffix(suffix)
        # Here's where the input text color is applied:
        spinbox.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: #353535;
                color: {input_text_color};
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
            }}
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
                width: 15px;
                border: none;
            }}
        """)
        spinbox.setFixedHeight(30)
        return spinbox
        
    def create_styled_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("color: #bbb;")
        return label
        
    def create_output_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                color: #8e2dc5;
                font-weight: bold;
                font-size: 12px;
                background-color: rgba(142, 45, 197, 0.1);
                border-radius: 4px;
                padding: 5px 10px;
            }
        """)
        return label
        
    def get_button_style(self):
        return """
            QPushButton {
                background-color: #8e2dc5;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #9d3dd4;
            }
            QPushButton:pressed {
                background-color: #7e1db6;
            }
        """
        
    def start_simulation(self):
        symbol = self.symbol_combo.currentText()
        quantity = self.quantity_input.value()
        volatility = self.volatility_input.value() / 100
        fee_tier = self.fee_tier_input.value() / 100
        
        self.simulator.start(symbol, quantity, volatility, fee_tier)
        
    def update_results(self):
        if not self.simulator.running:
            return
            
        results = self.simulator.get_results()
        
        self.slippage_label.setText(f"{results['slippage']:.4f}%")
        self.fees_label.setText(f"{results['fees']:.4f} USD")
        self.impact_label.setText(f"{results['market_impact']:.4f}%")
        self.net_cost_label.setText(f"{results['net_cost']:.4f} USD")
        self.maker_taker_label.setText(f"{results['maker_prob']*100:.1f}% / {(1-results['maker_prob'])*100:.1f}%")
        self.latency_label.setText(f"{results['latency']*1000:.2f} ms")
        self.order_book_depth_label.setText(f"{results['book_depth']} levels")
    