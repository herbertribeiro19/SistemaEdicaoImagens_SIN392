#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget para visualização de imagens
"""

from PyQt6.QtWidgets import QLabel, QScrollArea, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor
import cv2
import numpy as np

class ImageViewer(QScrollArea):
    """Widget para visualização de imagens com zoom e scroll"""
    
    def __init__(self):
        super().__init__()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("""
            QLabel {
                background: #242921;
                border: 2px solid #324624;
                border-radius: 8px;
                color: #c9efb2;
            }
        """)
        
        self.setWidget(self.image_label)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Configurar estilo do scroll area
        self.setStyleSheet("""
            QScrollArea {
                background: #242921;
                border: none;
            }
            QScrollBar:vertical {
                background: #2c3825;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #42602e;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4b6f32;
            }
            QScrollBar:horizontal {
                background: #2c3825;
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #42602e;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #4b6f32;
            }
        """)
        
    def set_image(self, image):
        """Define a imagem a ser exibida"""
        if image is None:
            self.image_label.setText("Nenhuma imagem carregada")
            return
            
        # Converter numpy array para QImage
        if len(image.shape) == 2:  # Imagem em escala de cinza
            height, width = image.shape
            bytes_per_line = width
            # Converter para bytes
            image_bytes = image.tobytes()
            q_image = QImage(image_bytes, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        else:  # Imagem colorida
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            # Converter para bytes
            image_bytes = image.tobytes()
            q_image = QImage(image_bytes, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            
        # Criar pixmap e redimensionar se necessário
        pixmap = QPixmap.fromImage(q_image)
        
        # Redimensionar para caber na área de visualização
        scaled_pixmap = self.scale_pixmap(pixmap)
        
        self.image_label.setPixmap(scaled_pixmap)
        
    def scale_pixmap(self, pixmap):
        """Redimensiona o pixmap para caber na área de visualização"""
        label_size = self.image_label.size()
        pixmap_size = pixmap.size()
        
        # Calcular escala para caber na área
        scale_x = label_size.width() / pixmap_size.width()
        scale_y = label_size.height() / pixmap_size.height()
        scale = min(scale_x, scale_y, 1.0)  # Não aumentar além do tamanho original
        
        if scale < 1.0:
            new_width = int(pixmap_size.width() * scale)
            new_height = int(pixmap_size.height() * scale)
            return pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        return pixmap 