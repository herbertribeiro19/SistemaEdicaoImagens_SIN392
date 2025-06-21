#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Edição e Análise de Imagens - SIN392
Autor: Sistema Interativo de Processamento Digital de Imagens
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    """Função principal que inicializa o sistema"""
    app = QApplication(sys.argv)
    
    # Configurar estilo da aplicação
    app.setStyle('Fusion')
    
    # Criar e exibir janela principal
    window = MainWindow()
    window.show()
    
    # Executar loop principal da aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 