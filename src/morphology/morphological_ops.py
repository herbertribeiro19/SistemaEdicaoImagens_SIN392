#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Operações morfológicas para processamento de imagens
"""

import cv2
import numpy as np

class MorphologicalOps:
    """Classe para operações morfológicas"""
    
    def __init__(self):
        pass
        
    def erosion(self, image, kernel_size=3):
        """
        Aplica operação de erosão
        
        Args:
            image: Imagem de entrada
            kernel_size: Tamanho do kernel (deve ser ímpar)
            
        Returns:
            Imagem erodida
        """
        # Garantir que o kernel seja ímpar
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        # Criar kernel estruturante
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        
        # Aplicar erosão
        result = cv2.erode(image, kernel, iterations=1)
        
        return result
        
    def dilation(self, image, kernel_size=3):
        """
        Aplica operação de dilatação
        
        Args:
            image: Imagem de entrada
            kernel_size: Tamanho do kernel (deve ser ímpar)
            
        Returns:
            Imagem dilatada
        """
        # Garantir que o kernel seja ímpar
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        # Criar kernel estruturante
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        
        # Aplicar dilatação
        result = cv2.dilate(image, kernel, iterations=1)
        
        return result 