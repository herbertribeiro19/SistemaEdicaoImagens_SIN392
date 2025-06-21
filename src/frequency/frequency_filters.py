#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filtros no domínio da frequência
"""

import numpy as np
import cv2

class FrequencyFilters:
    """Classe para filtros no domínio da frequência"""
    
    def __init__(self):
        pass
        
    def low_pass_filter(self, image, cutoff=30):
        """
        Aplica filtro passa-baixa no domínio da frequência
        
        Args:
            image: Imagem de entrada
            cutoff: Frequência de corte
            
        Returns:
            Imagem filtrada
        """
        # Calcular transformada de Fourier
        f_transform = np.fft.fft2(image)
        f_shift = np.fft.fftshift(f_transform)
        
        # Criar máscara passa-baixa
        rows, cols = image.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.zeros((rows, cols), np.uint8)
        cv2.circle(mask, (ccol, crow), cutoff, 1, -1)
        
        # Aplicar máscara
        f_shift_filtered = f_shift * mask
        
        # Transformada inversa
        f_ishift = np.fft.ifftshift(f_shift_filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        
        # Normalizar para [0, 255]
        result = np.uint8(img_back)
        
        return result
        
    def high_pass_filter(self, image, cutoff=30):
        """
        Aplica filtro passa-alta no domínio da frequência
        
        Args:
            image: Imagem de entrada
            cutoff: Frequência de corte
            
        Returns:
            Imagem filtrada
        """
        # Calcular transformada de Fourier
        f_transform = np.fft.fft2(image)
        f_shift = np.fft.fftshift(f_transform)
        
        # Criar máscara passa-alta
        rows, cols = image.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.ones((rows, cols), np.uint8)
        cv2.circle(mask, (ccol, crow), cutoff, 0, -1)
        
        # Aplicar máscara
        f_shift_filtered = f_shift * mask
        
        # Transformada inversa
        f_ishift = np.fft.ifftshift(f_shift_filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        
        # Normalizar para [0, 255]
        result = np.uint8(img_back)
        
        return result 