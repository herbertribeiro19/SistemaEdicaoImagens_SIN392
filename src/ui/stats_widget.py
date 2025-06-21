#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget para exibição de estatísticas detalhadas da imagem
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import numpy as np

class StatsWidget(QWidget):
    """Widget para exibição de estatísticas detalhadas da imagem"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Estatísticas Detalhadas")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Frame para estatísticas
        self.stats_frame = QFrame()
        self.stats_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.stats_frame.setStyleSheet("""
            QFrame {
                background: #2c3825;
                border: 1px solid #324624;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        
        # Grid layout para estatísticas
        self.stats_layout = QGridLayout(self.stats_frame)
        
        # Labels para estatísticas
        self.create_stat_labels()
        
        layout.addWidget(self.stats_frame)
        
    def create_stat_labels(self):
        """Cria os labels para as estatísticas"""
        self.stat_labels = {}
        
        stats = [
            ("Dimensões", "dims"),
            ("Tamanho Total", "size"),
            ("Média", "mean"),
            ("Mediana", "median"),
            ("Desvio Padrão", "std"),
            ("Variância", "variance"),
            ("Mínimo", "min"),
            ("Máximo", "max"),
            ("Amplitude", "range"),
            ("Assimetria", "skewness"),
            ("Curtose", "kurtosis"),
            ("Entropia", "entropy")
        ]
        
        for i, (label, key) in enumerate(stats):
            # Label do nome da estatística
            name_label = QLabel(f"{label}:")
            name_label.setStyleSheet("""
                QLabel {
                    color: #8cd05a;
                    font-weight: bold;
                    padding: 2px;
                }
            """)
            
            # Label do valor da estatística
            value_label = QLabel("N/A")
            value_label.setStyleSheet("""
                QLabel {
                    color: #c9efb2;
                    padding: 2px;
                }
            """)
            
            self.stats_layout.addWidget(name_label, i // 2, (i % 2) * 2)
            self.stats_layout.addWidget(value_label, i // 2, (i % 2) * 2 + 1)
            
            self.stat_labels[key] = value_label
            
    def update_stats(self, image):
        """Atualiza as estatísticas com a imagem fornecida"""
        if image is None:
            for label in self.stat_labels.values():
                label.setText("N/A")
            return
            
        # Calcular estatísticas básicas
        mean_val = np.mean(image)
        median_val = np.median(image)
        std_val = np.std(image)
        variance_val = np.var(image)
        min_val = np.min(image)
        max_val = np.max(image)
        range_val = max_val - min_val
        
        # Calcular assimetria
        skewness_val = self.calculate_skewness(image)
        
        # Calcular curtose
        kurtosis_val = self.calculate_kurtosis(image)
        
        # Calcular entropia
        entropy_val = self.calculate_entropy(image)
        
        # Atualizar labels
        self.stat_labels["dims"].setText(f"{image.shape[1]} × {image.shape[0]}")
        self.stat_labels["size"].setText(f"{image.size:,} pixels")
        self.stat_labels["mean"].setText(f"{mean_val:.2f}")
        self.stat_labels["median"].setText(f"{median_val:.2f}")
        self.stat_labels["std"].setText(f"{std_val:.2f}")
        self.stat_labels["variance"].setText(f"{variance_val:.2f}")
        self.stat_labels["min"].setText(f"{min_val:.0f}")
        self.stat_labels["max"].setText(f"{max_val:.0f}")
        self.stat_labels["range"].setText(f"{range_val:.0f}")
        self.stat_labels["skewness"].setText(f"{skewness_val:.3f}")
        self.stat_labels["kurtosis"].setText(f"{kurtosis_val:.3f}")
        self.stat_labels["entropy"].setText(f"{entropy_val:.3f}")
        
    def calculate_skewness(self, image):
        """Calcula a assimetria da imagem"""
        mean = np.mean(image)
        std = np.std(image)
        if std == 0:
            return 0
        return np.mean(((image - mean) / std) ** 3)
        
    def calculate_kurtosis(self, image):
        """Calcula a curtose da imagem"""
        mean = np.mean(image)
        std = np.std(image)
        if std == 0:
            return 0
        return np.mean(((image - mean) / std) ** 4) - 3
        
    def calculate_entropy(self, image):
        """Calcula a entropia da imagem"""
        # Calcular histograma
        hist, _ = np.histogram(image, bins=256, range=(0, 256))
        hist = hist[hist > 0]  # Remover bins vazios
        prob = hist / hist.sum()
        
        # Calcular entropia
        entropy = -np.sum(prob * np.log2(prob))
        return entropy 