import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, 
    QSlider, QLabel, QCheckBox, QPushButton, QSizePolicy,
    QScrollArea
)
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QGuiApplication

# Definição das cores solicitadas
COLORS = {
    "circle1": QColor(173, 216, 230), # Azul Claro
    "circle2": QColor(144, 238, 144), # Verde Claro
    "circle3": QColor(255, 255, 224), # Amarelo
    "cross": QColor(255, 102, 102)    # Vermelho Claro
}

class DrawingArea(QWidget):
    """
    Widget transparente onde os círculos e a cruz são desenhados.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Configurações padrão
        self.cross_visible = True
        
        self.circles = {
            'c1': {'visible': True, 'radius': 50, 'thickness': 2, 'color': COLORS["circle1"]},
            'c2': {'visible': True, 'radius': 100, 'thickness': 2, 'color': COLORS["circle2"]},
            'c3': {'visible': True, 'radius': 150, 'thickness': 2, 'color': COLORS["circle3"]},
        }

    def paintEvent(self, event):
        """
        Método chamado automaticamente para desenhar/redesenhar o widget.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # Para círculos suaves

        # O fundo é transparente por padrão
        
        # Obtém o centro da área de desenho
        center = self.rect().center()

        # Desenha os círculos
        for circle in self.circles.values():
            if circle['visible']:
                pen = QPen(circle['color'])
                pen.setWidth(circle['thickness'])
                painter.setPen(pen)
                painter.drawEllipse(center, circle['radius'], circle['radius'])

        # Desenha a cruz
        if self.cross_visible:
            pen = QPen(COLORS["cross"])
            pen.setWidth(2) # Espessura fixa para a cruz
            painter.setPen(pen)
            
            # Linha vertical
            painter.drawLine(center.x(), 0, center.x(), self.height())
            # Linha horizontal
            painter.drawLine(0, center.y(), self.width(), center.y())

    # Slots públicos para atualizar as propriedades via sidebar
    def set_circle_visible(self, circle_id, visible):
        if circle_id in self.circles:
            self.circles[circle_id]['visible'] = visible
            self.update() # Força o redesenho

    def set_circle_radius(self, circle_id, radius):
        if circle_id in self.circles:
            self.circles[circle_id]['radius'] = radius
            self.update()

    def set_circle_thickness(self, circle_id, thickness):
        if circle_id in self.circles:
            self.circles[circle_id]['thickness'] = thickness
            self.update()

    def set_cross_visible(self, visible):
        self.cross_visible = visible
        self.update()


class Sidebar(QWidget):
    """
    O painel de controle (sidebar) com todos os botões e sliders.
    """
    def __init__(self, drawing_area, parent=None):
        super().__init__(parent)
        self.drawing_area = drawing_area
        
        # Define uma largura fixa e um estilo semi-transparente
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 220);
                color: white;
                font-family: Arial;
            }
            QLabel {
                font-size: 13px;
                margin-top: 5px;
            }
            QCheckBox {
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton {
                background-color: #555;
                border: 1px solid #777;
                padding: 5px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #777;
            }
            QPushButton:pressed {
                background-color: #333;
            }
            QSlider::handle:horizontal {
                background: #BBB;
                width: 15px;
            }
        """)

        # Layout principal do sidebar
        self.main_layout = QVBoxLayout()

        # --- Área de Rolagem para Responsividade ---
        # Isso garante que se a tela for muito baixa, os controles não sumam
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Widget de contêiner para todos os controles
        scroll_content = QWidget()
        controls_layout = QVBoxLayout(scroll_content)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        controls_layout.setSpacing(5)

        # --- Controles ---
        
        # Círculo 1 (Azul)
        self.add_circle_controls(controls_layout, 'c1', 'Círculo 1 (Azul Claro)')
        # Círculo 2 (Verde)
        self.add_circle_controls(controls_layout, 'c2', 'Círculo 2 (Verde Claro)')
        # Círculo 3 (Amarelo)
        self.add_circle_controls(controls_layout, 'c3', 'Círculo 3 (Amarelo)')

        # Separador visual
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #555; margin-top: 10px;")
        controls_layout.addWidget(sep)

        # Cruz (Vermelha)
        cb_cross = QCheckBox("Cruz (Vermelho Claro)")
        cb_cross.setChecked(True)
        cb_cross.toggled.connect(self.drawing_area.set_cross_visible)
        controls_layout.addWidget(cb_cross)
        
        # Adiciona um "espaçador" para empurrar os controles para cima
        controls_layout.addStretch()
        
        # --- Botão Sair ---
        btn_quit = QPushButton("Sair do Colimador")
        btn_quit.clicked.connect(QApplication.instance().quit)
        
        # Montagem final do layout
        scroll_area.setWidget(scroll_content)
        self.main_layout.addWidget(scroll_area) # Área de rolagem ocupa a maior parte
        self.main_layout.addWidget(btn_quit)    # Botão Sair fica fixo embaixo
        self.setLayout(self.main_layout)

    def add_circle_controls(self, layout, circle_id, title):
        """Helper para adicionar o conjunto de controles de um círculo."""
        
        # Título / Checkbox
        cb = QCheckBox(title)
        cb.setChecked(True)
        # Conecta o sinal 'toggled' ao slot 'set_circle_visible', passando o ID e o estado
        cb.toggled.connect(lambda state: self.drawing_area.set_circle_visible(circle_id, state))
        layout.addWidget(cb)

        # Slider Raio
        layout.addWidget(QLabel("Raio:"))
        slider_radius = QSlider(Qt.Horizontal)
        # Tenta pegar o tamanho da tela para um range máximo razoável
        try:
            max_radius = QGuiApplication.primaryScreen().geometry().height() // 2
        except:
            max_radius = 1000 # Fallback
        slider_radius.setRange(0, max_radius)
        slider_radius.setValue(self.drawing_area.circles[circle_id]['radius'])
        slider_radius.valueChanged.connect(lambda value: self.drawing_area.set_circle_radius(circle_id, value))
        layout.addWidget(slider_radius)

        # Slider Espessura
        layout.addWidget(QLabel("Espessura:"))
        slider_thickness = QSlider(Qt.Horizontal)
        slider_thickness.setRange(1, 30) # De 1px a 30px
        slider_thickness.setValue(self.drawing_area.circles[circle_id]['thickness'])
        slider_thickness.valueChanged.connect(lambda value: self.drawing_area.set_circle_thickness(circle_id, value))
        layout.addWidget(slider_thickness)


class CollimatorApp(QWidget):
    """
    Janela principal da aplicação.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCAL Collimator")
        
        # --- Configuração da Janela Transparente ---
        # 1. Sem moldura (sem barra de título, botões de fechar, etc.)
        # 2. Sempre no topo (para ficar sobre o software da câmera)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # 3. Habilita o fundo translúcido (essencial!)
        # Isso faz o fundo da *janela* ser transparente.
        # Widgets dentro dela (como o sidebar) podem definir sua própria cor.
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout horizontal principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0) # Sem margens
        main_layout.setSpacing(0)                  # Sem espaçamento

        # Instancia as duas partes da UI
        self.drawing_area = DrawingArea()
        self.sidebar = Sidebar(self.drawing_area) # Passa a referência da área de desenho

        # Adiciona os widgets ao layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.drawing_area, 1) # '1' faz a área de desenho esticar
        
        self.setLayout(main_layout)

        # Variável para permitir mover a janela (já que não tem barra de título)
        self.drag_pos = None

    def mousePressEvent(self, event):
        """
        Captura o clique do mouse para iniciar o movimento da janela.
        """
        # Só permite arrastar se clicar no sidebar
        if self.sidebar.geometry().contains(event.pos()):
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        Move a janela se o mouse estiver pressionado.
        """
        if self.drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        Para o movimento da janela.
        """
        self.drag_pos = None
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = CollimatorApp()
    
    # Inicia a janela maximizada para cobrir a tela (como um overlay)
    window.showMaximized()
    
    sys.exit(app.exec())