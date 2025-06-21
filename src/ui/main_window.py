#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Janela principal do sistema de edição de imagens
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QPushButton, QLabel, QFileDialog, 
                             QMessageBox, QSplitter, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QPalette, QColor, QFont, QIcon
import cv2
import numpy as np

from .image_viewer import ImageViewer
from .histogram_widget import HistogramWidget
from .filters_tab import FiltersTab
from .transforms_tab import TransformsTab
from .morphology_tab import MorphologyTab
from .frequency_tab import FrequencyTab
from .segmentation_tab import SegmentationTab
from .stats_widget import StatsWidget

class MainWindow(QMainWindow):
    """Janela principal do sistema de edição de imagens"""
    
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.current_image = None
        self.image_history = []
        self.history_index = -1
        
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("Sistema de Edição e Análise de Imagens - SIN392")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Painel esquerdo - Visualização da imagem
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Painel direito - Controles
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Configurar proporções do splitter
        main_splitter.setSizes([800, 600])
        
        # Barra de status
        self.statusBar().showMessage("Pronto para carregar uma imagem")
        
    def create_left_panel(self):
        """Cria o painel esquerdo com visualização da imagem"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        
        # Barra de ferramentas superior
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # Área de visualização da imagem
        self.image_viewer = ImageViewer()
        layout.addWidget(self.image_viewer)
        
        # Widget de estatísticas
        self.stats_widget = StatsWidget()
        layout.addWidget(self.stats_widget)
        
        return left_widget
        
    def create_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = QFrame()
        toolbar.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(toolbar)
        
        # Botão carregar imagem
        self.load_btn = QPushButton("📁 Carregar Imagem")
        self.load_btn.clicked.connect(self.load_image)
        layout.addWidget(self.load_btn)
        
        # Botão salvar imagem
        self.save_btn = QPushButton("💾 Salvar Imagem")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)
        
        # Botão desfazer
        self.undo_btn = QPushButton("↶ Desfazer")
        self.undo_btn.clicked.connect(self.undo)
        self.undo_btn.setEnabled(False)
        layout.addWidget(self.undo_btn)
        
        # Botão refazer
        self.redo_btn = QPushButton("↷ Refazer")
        self.redo_btn.clicked.connect(self.redo)
        self.redo_btn.setEnabled(False)
        layout.addWidget(self.redo_btn)
        
        # Botão reset
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self.reset_image)
        self.reset_btn.setEnabled(False)
        layout.addWidget(self.reset_btn)
        
        layout.addStretch()
        return toolbar
        
    def create_right_panel(self):
        """Cria o painel direito com abas de controle"""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # Título
        title = QLabel("Ferramentas de Edição")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Abas de controle
        self.tab_widget = QTabWidget()
        
        # Aba de histograma
        self.histogram_widget = HistogramWidget()
        self.tab_widget.addTab(self.histogram_widget, "Histograma")
        
        # Aba de transformações
        self.transforms_tab = TransformsTab()
        self.transforms_tab.transform_applied.connect(self.apply_transform)
        self.tab_widget.addTab(self.transforms_tab, "Transformações")
        
        # Aba de filtros
        self.filters_tab = FiltersTab()
        self.filters_tab.filter_applied.connect(self.apply_filter)
        self.tab_widget.addTab(self.filters_tab, "Filtros")
        
        # Aba de morfologia
        self.morphology_tab = MorphologyTab()
        self.morphology_tab.morphology_applied.connect(self.apply_morphology)
        self.tab_widget.addTab(self.morphology_tab, "Morfologia")
        
        # Aba de frequência
        self.frequency_tab = FrequencyTab()
        self.frequency_tab.frequency_applied.connect(self.apply_frequency)
        self.tab_widget.addTab(self.frequency_tab, "Frequência")
        
        # Aba de segmentação
        self.segmentation_tab = SegmentationTab()
        self.segmentation_tab.segmentation_applied.connect(self.apply_segmentation)
        self.tab_widget.addTab(self.segmentation_tab, "Segmentação")
        
        layout.addWidget(self.tab_widget)
        
        return right_widget
        
    def apply_dark_theme(self):
        """Aplica o tema escuro personalizado"""
        palette = QPalette()
        
        # Cores do tema lime dark
        lime_1 = QColor("#20251d")
        lime_2 = QColor("#242921")
        lime_3 = QColor("#2c3825")
        lime_4 = QColor("#324624")
        lime_5 = QColor("#3a5329")
        lime_6 = QColor("#42602e")
        lime_7 = QColor("#4b6f32")
        lime_8 = QColor("#557f36")
        lime_9 = QColor("#77bb41")
        lime_10 = QColor("#6caf34")
        lime_11 = QColor("#8cd05a")
        lime_12 = QColor("#c9efb2")
        lime_contrast = QColor("#fff")
        
        # Configurar paleta
        palette.setColor(QPalette.ColorRole.Window, lime_1)
        palette.setColor(QPalette.ColorRole.WindowText, lime_contrast)
        palette.setColor(QPalette.ColorRole.Base, lime_2)
        palette.setColor(QPalette.ColorRole.AlternateBase, lime_3)
        palette.setColor(QPalette.ColorRole.ToolTipBase, lime_contrast)
        palette.setColor(QPalette.ColorRole.ToolTipText, lime_1)
        palette.setColor(QPalette.ColorRole.Text, lime_contrast)
        palette.setColor(QPalette.ColorRole.Button, lime_4)
        palette.setColor(QPalette.ColorRole.ButtonText, lime_contrast)
        palette.setColor(QPalette.ColorRole.BrightText, lime_12)
        palette.setColor(QPalette.ColorRole.Link, lime_9)
        palette.setColor(QPalette.ColorRole.Highlight, lime_9)
        palette.setColor(QPalette.ColorRole.HighlightedText, lime_contrast)
        
        self.setPalette(palette)
        
        # Estilo CSS adicional
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #324624;
                background: #242921;
            }
            QTabBar::tab {
                background: #2c3825;
                color: #c9efb2;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #42602e;
                color: #fff;
            }
            QTabBar::tab:hover {
                background: #3a5329;
            }
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
            QPushButton:disabled {
                background: #2c3825;
                color: #6c6c6c;
            }
            QFrame {
                background: #242921;
                border: 1px solid #324624;
                border-radius: 4px;
            }
        """)
        
    def load_image(self):
        """Carrega uma imagem do sistema de arquivos"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        
        if file_path:
            try:
                # Carregar imagem
                image = cv2.imread(file_path)
                if image is None:
                    raise ValueError("Não foi possível carregar a imagem")
                
                # Converter BGR para RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Converter para escala de cinza se necessário
                if len(image.shape) == 3:
                    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                else:
                    gray_image = image.copy()
                
                # Armazenar imagens
                self.original_image = gray_image.copy()
                self.current_image = gray_image.copy()
                
                # Limpar histórico
                self.image_history = [self.original_image.copy()]
                self.history_index = 0
                
                # Atualizar interface
                self.update_image_display()
                self.update_controls()
                
                self.statusBar().showMessage(f"Imagem carregada: {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao carregar imagem: {str(e)}")
                
    def save_image(self):
        """Salva a imagem atual"""
        if self.current_image is None:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Imagem",
            "",
            "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp);;TIFF (*.tiff)"
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.current_image)
                self.statusBar().showMessage(f"Imagem salva: {os.path.basename(file_path)}")
                QMessageBox.information(self, "Sucesso", "Imagem salva com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar imagem: {str(e)}")
                
    def update_image_display(self):
        """Atualiza a exibição da imagem"""
        if self.current_image is not None:
            self.image_viewer.set_image(self.current_image)
            self.histogram_widget.update_histogram(self.current_image)
            self.stats_widget.update_stats(self.current_image)
            
    def update_controls(self):
        """Atualiza o estado dos controles"""
        has_image = self.current_image is not None
        self.save_btn.setEnabled(has_image)
        self.reset_btn.setEnabled(has_image)
        self.undo_btn.setEnabled(self.history_index > 0)
        self.redo_btn.setEnabled(self.history_index < len(self.image_history) - 1)
        
    def add_to_history(self, image):
        """Adiciona uma imagem ao histórico"""
        # Remover imagens após o índice atual
        self.image_history = self.image_history[:self.history_index + 1]
        
        # Adicionar nova imagem
        self.image_history.append(image.copy())
        self.history_index += 1
        
        # Limitar histórico a 20 imagens
        if len(self.image_history) > 20:
            self.image_history.pop(0)
            self.history_index -= 1
            
        self.update_controls()
        
    def undo(self):
        """Desfaz a última operação"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.image_history[self.history_index].copy()
            self.update_image_display()
            self.update_controls()
            self.statusBar().showMessage("Operação desfeita")
            
    def redo(self):
        """Refaz a última operação desfeita"""
        if self.history_index < len(self.image_history) - 1:
            self.history_index += 1
            self.current_image = self.image_history[self.history_index].copy()
            self.update_image_display()
            self.update_controls()
            self.statusBar().showMessage("Operação refeita")
            
    def reset_image(self):
        """Retorna à imagem original"""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.image_history = [self.original_image.copy()]
            self.history_index = 0
            self.update_image_display()
            self.update_controls()
            self.statusBar().showMessage("Imagem resetada para original")
            
    def apply_transform(self, transform_type, params):
        """Aplica uma transformação à imagem"""
        if self.current_image is None:
            return
            
        try:
            from src.transforms.intensity_transforms import IntensityTransforms
            transforms = IntensityTransforms()
            
            if transform_type == "contrast_stretch":
                result = transforms.contrast_stretch(self.current_image, params)
                message = "Alargamento de contraste aplicado"
            elif transform_type == "histogram_equalization":
                result = transforms.histogram_equalization(self.current_image)
                message = "Equalização de histograma aplicada"
            else:
                return
                
            self.current_image = result
            self.add_to_history(self.current_image)
            self.update_image_display()
            self.statusBar().showMessage(message)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao aplicar transformação: {str(e)}")
            
    def apply_filter(self, filter_type, params):
        """Aplica um filtro à imagem"""
        if self.current_image is None:
            return
            
        try:
            from src.filters.spatial_filters import SpatialFilters
            filters = SpatialFilters()
            
            if filter_type == "mean":
                result = filters.mean_filter(self.current_image, params.get("kernel_size", 3))
                message = "Filtro da média aplicado"
            elif filter_type == "median":
                result = filters.median_filter(self.current_image, params.get("kernel_size", 3))
                message = "Filtro da mediana aplicado"
            elif filter_type == "gaussian":
                result = filters.gaussian_filter(self.current_image, params.get("sigma", 1.0))
                message = "Filtro gaussiano aplicado"
            elif filter_type == "max":
                result = filters.max_filter(self.current_image, params.get("kernel_size", 3))
                message = "Filtro máximo aplicado"
            elif filter_type == "min":
                result = filters.min_filter(self.current_image, params.get("kernel_size", 3))
                message = "Filtro mínimo aplicado"
            elif filter_type == "laplacian":
                result = filters.laplacian_filter(self.current_image)
                message = "Filtro laplaciano aplicado"
            elif filter_type == "roberts":
                result = filters.roberts_filter(self.current_image)
                message = "Filtro de Roberts aplicado"
            elif filter_type == "prewitt":
                result = filters.prewitt_filter(self.current_image)
                message = "Filtro de Prewitt aplicado"
            elif filter_type == "sobel":
                result = filters.sobel_filter(self.current_image)
                message = "Filtro de Sobel aplicado"
            else:
                return
                
            self.current_image = result
            self.add_to_history(self.current_image)
            self.update_image_display()
            self.statusBar().showMessage(message)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao aplicar filtro: {str(e)}")
            
    def apply_morphology(self, morph_type, params):
        """Aplica operação morfológica à imagem"""
        if self.current_image is None:
            return
            
        try:
            from src.morphology.morphological_ops import MorphologicalOps
            morph = MorphologicalOps()
            
            if morph_type == "erosion":
                result = morph.erosion(self.current_image, params.get("kernel_size", 3))
                message = "Erosão aplicada"
            elif morph_type == "dilation":
                result = morph.dilation(self.current_image, params.get("kernel_size", 3))
                message = "Dilatação aplicada"
            else:
                return
                
            self.current_image = result
            self.add_to_history(self.current_image)
            self.update_image_display()
            self.statusBar().showMessage(message)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao aplicar operação morfológica: {str(e)}")
            
    def apply_frequency(self, freq_type, params):
        """Aplica filtro no domínio da frequência"""
        if self.current_image is None:
            return
            
        try:
            from src.frequency.frequency_filters import FrequencyFilters
            filters = FrequencyFilters()
            
            if freq_type == "low_pass":
                result = filters.low_pass_filter(self.current_image, params.get("cutoff", 30))
                message = "Filtro passa-baixa aplicado"
            elif freq_type == "high_pass":
                result = filters.high_pass_filter(self.current_image, params.get("cutoff", 30))
                message = "Filtro passa-alta aplicado"
            elif freq_type == "fourier_spectrum":
                self.frequency_tab.show_fourier_spectrum_dialog(self.current_image)
                return
            else:
                return
                
            self.current_image = result
            self.add_to_history(self.current_image)
            self.update_image_display()
            self.statusBar().showMessage(message)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao aplicar filtro de frequência: {str(e)}")
            
    def apply_segmentation(self, seg_type, params):
        """Aplica segmentação à imagem"""
        if self.current_image is None:
            return
            
        try:
            from src.segmentation.segmentation_methods import SegmentationMethods
            seg = SegmentationMethods()
            
            if seg_type == "otsu":
                result = seg.otsu_thresholding(self.current_image)
                message = "Limiarização de Otsu aplicada"
            else:
                return
                
            self.current_image = result
            self.add_to_history(self.current_image)
            self.update_image_display()
            self.statusBar().showMessage(message)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao aplicar segmentação: {str(e)}") 