#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aba de segmentação de imagens
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class SegmentationTab(QWidget):
    """Aba para segmentação de imagens"""
    
    # Sinais
    segmentation_applied = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Segmentação de Imagens")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Grupo de limiarização
        self.create_thresholding_group(layout)
        
        layout.addStretch()
        
    def create_thresholding_group(self, parent_layout):
        """Cria o grupo de limiarização"""
        group = QGroupBox("Limiarização")
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
        
        # Descrição do método de Otsu
        desc_label = QLabel("""
        <b>Método de Otsu:</b> Determina automaticamente o melhor limiar para 
        separar o objeto do fundo, maximizando a variância entre as classes.
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #c9efb2; padding: 8px; background: #2c3825; border-radius: 4px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botão para aplicar limiarização de Otsu
        self.otsu_btn = QPushButton("Aplicar Limiarização de Otsu")
        self.otsu_btn.clicked.connect(self.apply_otsu_thresholding)
        self.otsu_btn.setStyleSheet("""
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
        layout.addWidget(self.otsu_btn)
        
        parent_layout.addWidget(group)
        
    def apply_otsu_thresholding(self):
        """Aplica limiarização de Otsu"""
        params = {}
        self.segmentation_applied.emit("otsu", params) 