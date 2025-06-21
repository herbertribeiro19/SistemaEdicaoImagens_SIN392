#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aba de filtros no domínio da frequência
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QGroupBox, QDialog,
                             QVBoxLayout as QVBoxLayoutDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import cv2

class FrequencyTab(QWidget):
    """Aba para filtros no domínio da frequência"""
    
    # Sinais
    frequency_applied = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Filtros no Domínio da Frequência")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Grupo de filtros de frequência
        self.create_frequency_filters_group(layout)
        
        # Grupo de espectro de Fourier
        self.create_fourier_spectrum_group(layout)
        
        layout.addStretch()
        
    def create_frequency_filters_group(self, parent_layout):
        """Cria o grupo de filtros de frequência"""
        group = QGroupBox("Filtros de Frequência")
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
        <b>Filtros de Frequência:</b> Operam no domínio da frequência usando a transformada de Fourier.<br>
        • <b>Passa-Baixa:</b> Remove altas frequências (suaviza a imagem)<br>
        • <b>Passa-Alta:</b> Remove baixas frequências (destaca bordas)<br>
        • <b>Frequência de Corte:</b> 30 pixels
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #c9efb2; padding: 8px; background: #2c3825; border-radius: 4px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botões para filtros de frequência
        buttons_layout = QHBoxLayout()
        
        self.low_pass_btn = QPushButton("Filtro Passa-Baixa")
        self.low_pass_btn.clicked.connect(self.apply_low_pass_filter)
        self.low_pass_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 12px 16px;
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
        
        self.high_pass_btn = QPushButton("Filtro Passa-Alta")
        self.high_pass_btn.clicked.connect(self.apply_high_pass_filter)
        self.high_pass_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 12px 16px;
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
        
        buttons_layout.addWidget(self.low_pass_btn)
        buttons_layout.addWidget(self.high_pass_btn)
        
        layout.addLayout(buttons_layout)
        
        parent_layout.addWidget(group)
        
    def create_fourier_spectrum_group(self, parent_layout):
        """Cria o grupo de espectro de Fourier"""
        group = QGroupBox("Espectro de Fourier")
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
        desc_label = QLabel("Visualize o espectro de Fourier da imagem para analisar suas componentes de frequência.")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #c9efb2; padding: 8px;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botão para mostrar espectro
        self.spectrum_btn = QPushButton("Mostrar Espectro de Fourier")
        self.spectrum_btn.clicked.connect(self.show_fourier_spectrum)
        self.spectrum_btn.setStyleSheet("""
            QPushButton {
                background: #42602e;
                color: #fff;
                border: none;
                padding: 12px 16px;
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
        layout.addWidget(self.spectrum_btn)
        
        parent_layout.addWidget(group)
        
    def apply_low_pass_filter(self):
        """Aplica filtro passa-baixa"""
        params = {"cutoff": 30}
        self.frequency_applied.emit("low_pass", params)
        
    def apply_high_pass_filter(self):
        """Aplica filtro passa-alta"""
        params = {"cutoff": 30}
        self.frequency_applied.emit("high_pass", params)
        
    def show_fourier_spectrum(self):
        """Mostra o espectro de Fourier da imagem atual"""
        self.frequency_applied.emit("fourier_spectrum", {})
        
    def show_fourier_spectrum_dialog(self, image):
        """Mostra o espectro de Fourier em uma janela separada"""
        dialog = FourierSpectrumDialog(image, self)
        dialog.exec()

class FourierSpectrumDialog(QDialog):
    """Dialog para exibir o espectro de Fourier"""
    
    def __init__(self, image, parent=None):
        super().__init__(parent)
        self.image = image
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do dialog"""
        self.setWindowTitle("Espectro de Fourier")
        self.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayoutDialog(self)
        
        # Criar figura do matplotlib
        self.figure = Figure(figsize=(10, 8), facecolor='#242921')
        self.canvas = FigureCanvas(self.figure)
        
        # Calcular e exibir espectro de Fourier
        self.plot_fourier_spectrum()
        
        layout.addWidget(self.canvas)
        
    def plot_fourier_spectrum(self):
        """Plota o espectro de Fourier da imagem"""
        if self.image is None:
            return
            
        # Calcular transformada de Fourier
        f_transform = np.fft.fft2(self.image)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.log(np.abs(f_shift) + 1)
        
        # Criar subplots
        self.figure.clear()
        
        # Subplot 1: Imagem original
        ax1 = self.figure.add_subplot(221)
        ax1.imshow(self.image, cmap='gray')
        ax1.set_title('Imagem Original', color='#c9efb2')
        ax1.axis('off')
        
        # Subplot 2: Espectro de magnitude
        ax2 = self.figure.add_subplot(222)
        im2 = ax2.imshow(magnitude_spectrum, cmap='viridis')
        ax2.set_title('Espectro de Magnitude', color='#c9efb2')
        ax2.axis('off')
        self.figure.colorbar(im2, ax=ax2)
        
        # Subplot 3: Perfil horizontal do centro
        ax3 = self.figure.add_subplot(223)
        center_row = magnitude_spectrum[magnitude_spectrum.shape[0]//2, :]
        ax3.plot(center_row, color='#77bb41')
        ax3.set_title('Perfil Horizontal (Centro)', color='#c9efb2')
        ax3.set_xlabel('Frequência', color='#c9efb2')
        ax3.set_ylabel('Magnitude (log)', color='#c9efb2')
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(colors='#c9efb2')
        
        # Subplot 4: Perfil vertical do centro
        ax4 = self.figure.add_subplot(224)
        center_col = magnitude_spectrum[:, magnitude_spectrum.shape[1]//2]
        ax4.plot(center_col, color='#77bb41')
        ax4.set_title('Perfil Vertical (Centro)', color='#c9efb2')
        ax4.set_xlabel('Frequência', color='#c9efb2')
        ax4.set_ylabel('Magnitude (log)', color='#c9efb2')
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(colors='#c9efb2')
        
        # Configurar cores do gráfico
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_facecolor('#242921')
            for spine in ax.spines.values():
                spine.set_color('#c9efb2')
        
        self.figure.tight_layout()
        self.canvas.draw() 