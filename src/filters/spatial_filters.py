#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filtros espaciais para processamento de imagens
"""

import cv2
import numpy as np
from scipy import ndimage
from skimage import filters

class SpatialFilters:
    """Classe para filtros espaciais"""
    
    def __init__(self):
        pass
        
    def mean_filter(self, image, kernel_size=3):
        """
        Aplica filtro da média
        
        Args:
            image: Imagem de entrada
            kernel_size: Tamanho do kernel (deve ser ímpar)
            
        Returns:
            Imagem filtrada
        """
        # Garantir que o kernel seja ímpar
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        # Aplicar filtro da média
        result = cv2.blur(image, (kernel_size, kernel_size))
        
        return result
        
    def median_filter(self, image, kernel_size=3):
        """
        Aplica filtro da mediana
        
        Args:
            image: Imagem de entrada
            kernel_size: Tamanho do kernel (deve ser ímpar)
            
        Returns:
            Imagem filtrada
        """
        # Garantir que o kernel seja ímpar
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        # Aplicar filtro da mediana
        result = cv2.medianBlur(image, kernel_size)
        
        return result
        
    def gaussian_filter(self, image, sigma=1.0):
        """
        Aplica filtro gaussiano
        
        Args:
            image: Imagem de entrada
            sigma: Desvio padrão do filtro gaussiano
            
        Returns:
            Imagem filtrada
        """
        # Aplicar filtro gaussiano
        result = ndimage.gaussian_filter(image, sigma=sigma)
        
        return result.astype(np.uint8)
        
    def max_filter(self, image, kernel_size=3):
        """
        Aplica filtro máximo
        
        Args:
            image: Imagem de entrada
            kernel_size: Tamanho do kernel (deve ser ímpar)
            
        Returns:
            Imagem filtrada
        """
        # Garantir que o kernel seja ímpar
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        # Aplicar filtro máximo
        result = ndimage.maximum_filter(image, size=kernel_size)
        
        return result
        
    def min_filter(self, image, kernel_size=3):
        """
        Aplica filtro mínimo
        
        Args:
            image: Imagem de entrada
            kernel_size: Tamanho do kernel (deve ser ímpar)
            
        Returns:
            Imagem filtrada
        """
        # Garantir que o kernel seja ímpar
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        # Aplicar filtro mínimo
        result = ndimage.minimum_filter(image, size=kernel_size)
        
        return result
        
    def laplacian_filter(self, image):
        """
        Aplica filtro laplaciano para detecção de bordas
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem com bordas detectadas
        """
        # Aplicar filtro laplaciano
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        
        # Converter para valores absolutos
        abs_laplacian = np.absolute(laplacian)
        
        # Normalizar para [0, 255]
        result = np.uint8(abs_laplacian)
        
        return result
        
    def roberts_filter(self, image):
        """
        Aplica filtro de Roberts para detecção de bordas
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem com bordas detectadas
        """
        # Aplicar filtro de Roberts
        roberts = filters.roberts(image)
        
        # Normalizar para [0, 255]
        result = np.uint8(roberts * 255)
        
        return result
        
    def prewitt_filter(self, image):
        """
        Aplica filtro de Prewitt para detecção de bordas
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem com bordas detectadas
        """
        # Aplicar filtro de Prewitt
        prewitt = filters.prewitt(image)
        
        # Normalizar para [0, 255]
        result = np.uint8(prewitt * 255)
        
        return result
        
    def sobel_filter(self, image):
        """
        Aplica filtro de Sobel para detecção de bordas
        
        Args:
            image: Imagem de entrada
            
        Returns:
            Imagem com bordas detectadas
        """
        # Aplicar filtro de Sobel
        sobel = filters.sobel(image)
        
        # Normalizar para [0, 255]
        result = np.uint8(sobel * 255)
        
        return result 