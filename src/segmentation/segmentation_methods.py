#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Métodos de segmentação de imagens
"""

import cv2
import numpy as np

class SegmentationMethods:
    """Classe para métodos de segmentação"""
    
    def __init__(self):
        pass
        
    def otsu_thresholding(self, image):
        """
        Aplica limiarização de Otsu
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem segmentada (binária)
        """
        # Aplicar limiarização de Otsu
        _, result = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return result 