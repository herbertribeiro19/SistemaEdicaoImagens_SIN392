#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget para exibição do histograma da imagem
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import cv2

class HistogramWidget(QWidget):
    """Widget para exibição do histograma da imagem"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Histograma da Imagem")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Frame para o histograma
        self.histogram_frame = QFrame()
        self.histogram_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.histogram_frame.setStyleSheet("""
            QFrame {
                background: #242921;
                border: 1px solid #324624;
                border-radius: 4px;
            }
        """)
        
        # Criar figura do matplotlib
        self.figure = Figure(figsize=(6, 4), facecolor='#242921')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: #242921; border: none;")
        
        # Configurar subplot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#242921')
        self.ax.tick_params(colors='#c9efb2')
        self.ax.spines['bottom'].set_color('#c9efb2')
        self.ax.spines['top'].set_color('#c9efb2')
        self.ax.spines['left'].set_color('#c9efb2')
        self.ax.spines['right'].set_color('#c9efb2')
        self.ax.xaxis.label.set_color('#c9efb2')
        self.ax.yaxis.label.set_color('#c9efb2')
        
        # Layout para o canvas
        canvas_layout = QVBoxLayout(self.histogram_frame)
        canvas_layout.addWidget(self.canvas)
        
        layout.addWidget(self.histogram_frame)
        
        # Informações estatísticas
        self.stats_label = QLabel("Carregue uma imagem para ver o histograma")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setWordWrap(True)
        self.stats_label.setStyleSheet("""
            QLabel {
                color: #c9efb2;
                background: #2c3825;
                border: 1px solid #324624;
                border-radius: 4px;
                padding: 8px;
                margin: 4px;
            }
        """)
        layout.addWidget(self.stats_label)
        
    def update_histogram(self, image):
        """Atualiza o histograma com a imagem fornecida"""
        if image is None:
            self.ax.clear()
            self.ax.text(0.5, 0.5, 'Nenhuma imagem carregada', 
                        ha='center', va='center', transform=self.ax.transAxes,
                        color='#c9efb2', fontsize=12)
            self.canvas.draw()
            return
            
        # Calcular histograma
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        
        # Limpar gráfico anterior
        self.ax.clear()
        
        # Configurar cores do gráfico
        self.ax.set_facecolor('#242921')
        self.ax.tick_params(colors='#c9efb2')
        self.ax.spines['bottom'].set_color('#c9efb2')
        self.ax.spines['top'].set_color('#c9efb2')
        self.ax.spines['left'].set_color('#c9efb2')
        self.ax.spines['right'].set_color('#c9efb2')
        self.ax.xaxis.label.set_color('#c9efb2')
        self.ax.yaxis.label.set_color('#c9efb2')
        
        # Plotar histograma
        self.ax.plot(hist, color='#77bb41', linewidth=1.5)
        self.ax.fill_between(range(256), hist.flatten(), alpha=0.3, color='#42602e')
        
        # Configurar labels
        self.ax.set_xlabel('Níveis de Cinza', color='#c9efb2')
        self.ax.set_ylabel('Frequência', color='#c9efb2')
        self.ax.set_title('Histograma da Imagem', color='#c9efb2', fontsize=12)
        
        # Configurar limites
        self.ax.set_xlim(0, 255)
        self.ax.set_ylim(0, hist.max() * 1.1)
        
        # Adicionar grade
        self.ax.grid(True, alpha=0.2, color='#324624')
        
        # Atualizar canvas
        self.canvas.draw()
        
        # Atualizar estatísticas
        self.update_statistics(image)
        
    def update_statistics(self, image):
        """Atualiza as informações estatísticas"""
        if image is None:
            self.stats_label.setText("Carregue uma imagem para ver as estatísticas")
            return
            
        # Calcular estatísticas
        mean_val = np.mean(image)
        std_val = np.std(image)
        min_val = np.min(image)
        max_val = np.max(image)
        median_val = np.median(image)
        
        # Calcular percentis
        p25 = np.percentile(image, 25)
        p75 = np.percentile(image, 75)
        
        # Formatar texto das estatísticas
        stats_text = f"""
        <b>Estatísticas da Imagem:</b><br>
        • Média: {mean_val:.2f}<br>
        • Mediana: {median_val:.2f}<br>
        • Desvio Padrão: {std_val:.2f}<br>
        • Mínimo: {min_val:.0f}<br>
        • Máximo: {max_val:.0f}<br>
        • Percentil 25%: {p25:.2f}<br>
        • Percentil 75%: {p75:.2f}<br>
        • Contraste: {max_val - min_val:.0f}
        """
        
        self.stats_label.setText(stats_text) 