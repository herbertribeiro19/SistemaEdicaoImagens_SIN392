#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transformações de intensidade para imagens
"""

import cv2
import numpy as np
from skimage import exposure

class IntensityTransforms:
    """Classe para transformações de intensidade de imagens"""
    
    def __init__(self):
        pass
        
    def contrast_stretch(self, image, params):
        """
        Aplica alargamento de contraste à imagem
        
        Args:
            image: Imagem de entrada (numpy array)
            params: Dicionário com parâmetros
                - min_val: Valor mínimo para o alargamento
                - max_val: Valor máximo para o alargamento
                
        Returns:
            Imagem com contraste alargado
        """
        min_val = params.get("min_val", 0)
        max_val = params.get("max_val", 255)
        
        # Normalizar a imagem para o intervalo [0, 1]
        image_norm = image.astype(np.float32) / 255.0
        
        # Aplicar alargamento de contraste
        stretched = exposure.rescale_intensity(image_norm, 
                                             in_range=(min_val/255.0, max_val/255.0),
                                             out_range=(0, 1))
        
        # Converter de volta para uint8
        result = (stretched * 255).astype(np.uint8)
        
        return result
        
    def histogram_equalization(self, image):
        """
        Aplica equalização de histograma à imagem
        
        Args:
            image: Imagem de entrada (numpy array)
            
        Returns:
            Imagem com histograma equalizado
        """
        # Aplicar equalização de histograma
        equalized = cv2.equalizeHist(image)
        
        return equalized 