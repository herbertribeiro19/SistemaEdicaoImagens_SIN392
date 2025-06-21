#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aba de operações morfológicas
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QSpinBox, QGroupBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class MorphologyTab(QWidget):
    """Aba para operações morfológicas"""
    
    # Sinais
    morphology_applied = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Operações Morfológicas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Grupo de operações básicas
        self.create_basic_operations_group(layout)
        
        layout.addStretch()
        
    def create_basic_operations_group(self, parent_layout):
        """Cria o grupo de operações morfológicas básicas"""
        group = QGroupBox("Operações Básicas")
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
        
        # Controles para tamanho do kernel
        kernel_layout = QHBoxLayout()
        kernel_label = QLabel("Tamanho do Kernel:")
        kernel_label.setStyleSheet("color: #c9efb2;")
        
        self.kernel_size_spinbox = QSpinBox()
        self.kernel_size_spinbox.setRange(3, 15)
        self.kernel_size_spinbox.setValue(3)
        self.kernel_size_spinbox.setSingleStep(2)  # Apenas valores ímpares
        self.kernel_size_spinbox.setStyleSheet("""
            QSpinBox {
                background: #2c3825;
                border: 1px solid #324624;
                border-radius: 4px;
                color: #c9efb2;
                padding: 4px;
            }
        """)
        
        kernel_layout.addWidget(kernel_label)
        kernel_layout.addWidget(self.kernel_size_spinbox)
        kernel_layout.addStretch()
        
        layout.addLayout(kernel_layout)
        
        # Descrição das operações
        desc_label = QLabel("""
        <b>Erosão:</b> Reduz objetos brancos e expande objetos negros<br>
        <b>Dilatação:</b> Expande objetos brancos e reduz objetos negros
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #c9efb2; padding: 8px; background: #2c3825; border-radius: 4px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botões para operações morfológicas
        buttons_layout = QHBoxLayout()
        
        self.erosion_btn = QPushButton("Erosão")
        self.erosion_btn.clicked.connect(self.apply_erosion)
        self.erosion_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 12px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        self.dilation_btn = QPushButton("Dilatação")
        self.dilation_btn.clicked.connect(self.apply_dilation)
        self.dilation_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 12px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #4b6f32;
            }
            QPushButton:pressed {
                background: #324624;
            }
        """)
        
        buttons_layout.addWidget(self.erosion_btn)
        buttons_layout.addWidget(self.dilation_btn)
        
        layout.addLayout(buttons_layout)
        
        parent_layout.addWidget(group)
        
    def apply_erosion(self):
        """Aplica operação de erosão"""
        params = {"kernel_size": self.kernel_size_spinbox.value()}
        self.morphology_applied.emit("erosion", params)
        
    def apply_dilation(self):
        """Aplica operação de dilatação"""
        params = {"kernel_size": self.kernel_size_spinbox.value()}
        self.morphology_applied.emit("dilation", params) 