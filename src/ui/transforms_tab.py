#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aba de transformações de intensidade
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QGroupBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class TransformsTab(QWidget):
    """Aba para transformações de intensidade"""
    
    # Sinais
    transform_applied = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Transformações de Intensidade")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Grupo de alargamento de contraste
        self.create_contrast_stretch_group(layout)
        
        # Grupo de equalização de histograma
        self.create_histogram_equalization_group(layout)
        
        layout.addStretch()
        
    def create_contrast_stretch_group(self, parent_layout):
        """Cria o grupo de alargamento de contraste"""
        group = QGroupBox("Alargamento de Contraste")
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
        
        # Descrição
        desc_label = QLabel("""
        <b>Alargamento de Contraste:</b> Expande o intervalo de níveis de cinza para melhorar o contraste.<br>
        • <b>Valor Mínimo:</b> 0<br>
        • <b>Valor Máximo:</b> 255
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #c9efb2; padding: 8px; background: #2c3825; border-radius: 4px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botão para aplicar alargamento de contraste
        self.contrast_btn = QPushButton("Aplicar Alargamento de Contraste")
        self.contrast_btn.clicked.connect(self.apply_contrast_stretch)
        self.contrast_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 16px;
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
        layout.addWidget(self.contrast_btn)
        
        parent_layout.addWidget(group)
        
    def create_histogram_equalization_group(self, parent_layout):
        """Cria o grupo de equalização de histograma"""
        group = QGroupBox("Equalização de Histograma")
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
        
        # Descrição
        desc_label = QLabel("""
        <b>Equalização de Histograma:</b> Redistribui automaticamente os níveis de cinza para maximizar o contraste.
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #c9efb2; padding: 8px; background: #2c3825; border-radius: 4px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botão para aplicar equalização
        self.equalize_btn = QPushButton("Aplicar Equalização de Histograma")
        self.equalize_btn.clicked.connect(self.apply_histogram_equalization)
        self.equalize_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 8px 16px;
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
        layout.addWidget(self.equalize_btn)
        
        parent_layout.addWidget(group)
        
    def apply_contrast_stretch(self):
        """Aplica alargamento de contraste"""
        params = {
            "min_val": 0,
            "max_val": 255
        }
        self.transform_applied.emit("contrast_stretch", params)
        
    def apply_histogram_equalization(self):
        """Aplica equalização de histograma"""
        params = {}
        self.transform_applied.emit("histogram_equalization", params) 