#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aba de filtros espaciais
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QGroupBox, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class FiltersTab(QWidget):
    """Aba para filtros espaciais"""
    
    # Sinais
    filter_applied = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do widget"""
        # Scroll area para acomodar todos os controles
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        # Widget principal
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        # Título
        title = QLabel("Filtros Espaciais")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Grupo de filtros passa-baixa
        self.create_low_pass_group(layout)
        
        # Grupo de filtros passa-alta
        self.create_high_pass_group(layout)
        
        layout.addStretch()
        
        scroll.setWidget(main_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        
    def create_low_pass_group(self, parent_layout):
        """Cria o grupo de filtros passa-baixa"""
        group = QGroupBox("Filtros Passa-Baixa (Suavização)")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #8cd05a;
                border: 2px solid #324624;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # Descrição dos filtros
        desc_label = QLabel("""
        <b>Filtros Passa-Baixa:</b> Suavizam a imagem removendo ruído e detalhes finos.<br>
        • <b>Média:</b> Kernel 3x3<br>
        • <b>Mediana:</b> Kernel 3x3<br>
        • <b>Gaussiano:</b> Sigma = 1.0<br>
        • <b>Máximo/Mínimo:</b> Kernel 3x3
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #c9efb2; padding: 8px; background: #2c3825; border-radius: 4px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botões para filtros passa-baixa
        buttons_layout = QHBoxLayout()
        
        self.mean_btn = QPushButton("Filtro da Média")
        self.mean_btn.clicked.connect(self.apply_mean_filter)
        self.mean_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        self.median_btn = QPushButton("Filtro da Mediana")
        self.median_btn.clicked.connect(self.apply_median_filter)
        self.median_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        self.gaussian_btn = QPushButton("Filtro Gaussiano")
        self.gaussian_btn.clicked.connect(self.apply_gaussian_filter)
        self.gaussian_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        buttons_layout.addWidget(self.mean_btn)
        buttons_layout.addWidget(self.median_btn)
        buttons_layout.addWidget(self.gaussian_btn)
        
        layout.addLayout(buttons_layout)
        
        # Botões para filtros de ordem
        order_buttons_layout = QHBoxLayout()
        
        self.max_btn = QPushButton("Filtro Máximo")
        self.max_btn.clicked.connect(self.apply_max_filter)
        self.max_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        self.min_btn = QPushButton("Filtro Mínimo")
        self.min_btn.clicked.connect(self.apply_min_filter)
        self.min_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        order_buttons_layout.addWidget(self.max_btn)
        order_buttons_layout.addWidget(self.min_btn)
        
        layout.addLayout(order_buttons_layout)
        
        parent_layout.addWidget(group)
        
    def create_high_pass_group(self, parent_layout):
        """Cria o grupo de filtros passa-alta"""
        group = QGroupBox("Filtros Passa-Alta (Detecção de Bordas)")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #8cd05a;
                border: 2px solid #324624;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # Descrição dos filtros
        desc_label = QLabel("""
        <b>Filtros Passa-Alta:</b> Destacam bordas e detalhes finos da imagem.<br>
        • <b>Laplaciano:</b> Detecção de bordas<br>
        • <b>Roberts:</b> Detecção de bordas diagonais<br>
        • <b>Prewitt:</b> Detecção de bordas horizontais e verticais<br>
        • <b>Sobel:</b> Detecção de bordas com suavização
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #c9efb2; padding: 8px; background: #2c3825; border-radius: 4px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botões para filtros passa-alta
        buttons_layout = QHBoxLayout()
        
        self.laplacian_btn = QPushButton("Laplaciano")
        self.laplacian_btn.clicked.connect(self.apply_laplacian_filter)
        self.laplacian_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        self.roberts_btn = QPushButton("Roberts")
        self.roberts_btn.clicked.connect(self.apply_roberts_filter)
        self.roberts_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        self.prewitt_btn = QPushButton("Prewitt")
        self.prewitt_btn.clicked.connect(self.apply_prewitt_filter)
        self.prewitt_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        self.sobel_btn = QPushButton("Sobel")
        self.sobel_btn.clicked.connect(self.apply_sobel_filter)
        self.sobel_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        buttons_layout.addWidget(self.laplacian_btn)
        buttons_layout.addWidget(self.roberts_btn)
        buttons_layout.addWidget(self.prewitt_btn)
        buttons_layout.addWidget(self.sobel_btn)
        
        layout.addLayout(buttons_layout)
        
        parent_layout.addWidget(group)
        
    def apply_mean_filter(self):
        """Aplica filtro da média"""
        params = {"kernel_size": 3}
        self.filter_applied.emit("mean", params)
        
    def apply_median_filter(self):
        """Aplica filtro da mediana"""
        params = {"kernel_size": 3}
        self.filter_applied.emit("median", params)
        
    def apply_gaussian_filter(self):
        """Aplica filtro gaussiano"""
        params = {"sigma": 1.0}
        self.filter_applied.emit("gaussian", params)
        
    def apply_max_filter(self):
        """Aplica filtro máximo"""
        params = {"kernel_size": 3}
        self.filter_applied.emit("max", params)
        
    def apply_min_filter(self):
        """Aplica filtro mínimo"""
        params = {"kernel_size": 3}
        self.filter_applied.emit("min", params)
        
    def apply_laplacian_filter(self):
        """Aplica filtro laplaciano"""
        params = {}
        self.filter_applied.emit("laplacian", params)
        
    def apply_roberts_filter(self):
        """Aplica filtro de Roberts"""
        params = {}
        self.filter_applied.emit("roberts", params)
        
    def apply_prewitt_filter(self):
        """Aplica filtro de Prewitt"""
        params = {}
        self.filter_applied.emit("prewitt", params)
        
    def apply_sobel_filter(self):
        """Aplica filtro de Sobel"""
        params = {}
        self.filter_applied.emit("sobel", params) 