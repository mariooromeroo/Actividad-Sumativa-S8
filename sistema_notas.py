import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QMessageBox, QComboBox)

class SistemaCalificaciones(QWidget):
    def __init__(self):
        super().__init__()
        self.estudiantes = []
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Sistema de Calificaciones')
        self.setGeometry(300, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        # Titulo
        titulo = QLabel('Sistema de Calificaciones Estudiantiles')
        layout.addWidget(titulo)
        
        # Campos de entrada
        layout.addWidget(QLabel('Nombre del estudiante:'))
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_input)
        
        layout.addWidget(QLabel('Materia:'))
        self.materia_combo = QComboBox()
        self.materia_combo.addItems(['Matemáticas', 'Lenguajes', 'Sociales', 'Ciencia'])
        layout.addWidget(self.materia_combo)
        
        layout.addWidget(QLabel('Calificación (0-100):'))
        self.calificacion_input = QLineEdit()
        layout.addWidget(self.calificacion_input)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        self.agregar_btn = QPushButton('Agregar')
        self.agregar_btn.clicked.connect(self.agregar_estudiante)
        botones_layout.addWidget(self.agregar_btn)
        
        self.promedio_btn = QPushButton('Calcular Promedio')
        self.promedio_btn.clicked.connect(self.calcular_promedio)
        botones_layout.addWidget(self.promedio_btn)
        
        self.limpiar_lista_btn = QPushButton('Limpiar Lista')
        self.limpiar_lista_btn.clicked.connect(self.limpiar_lista)
        botones_layout.addWidget(self.limpiar_lista_btn)
        
        layout.addLayout(botones_layout)
        
        # Area de resultados
        layout.addWidget(QLabel('Lista de estudiantes:'))
        self.resultados_text = QTextEdit()
        self.resultados_text.setReadOnly(True)
        layout.addWidget(self.resultados_text)
        
        # Estadisticas
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(QLabel('Promedio general:'))
        self.promedio_label = QLabel('0.00')
        stats_layout.addWidget(self.promedio_label)
        
        stats_layout.addWidget(QLabel('Total estudiantes:'))
        self.total_label = QLabel('0')
        stats_layout.addWidget(self.total_label)
        
        layout.addLayout(stats_layout)
        
        self.setLayout(layout)
    
    def agregar_estudiante(self):
        # Obtener datos
        nombre = self.nombre_input.text().strip()
        materia = self.materia_combo.currentText()
        cal_str = self.calificacion_input.text().strip()
        
        # Validar
        if not nombre or not cal_str:
            QMessageBox.warning(self, 'Error', 'Faltan datos')
            return
        
        try:
            calificacion = float(cal_str)
            if calificacion < 0 or calificacion > 100:
                QMessageBox.warning(self, 'Error', 'Calificación debe ser 0-100')
                return
        except:
            QMessageBox.warning(self, 'Error', 'Calificación debe ser número')
            return
        
        # Agregar estudiante
        estado = 'Aprobado' if calificacion >= 60 else 'Reprobado'
        estudiante = {
            'nombre': nombre,
            'materia': materia,
            'calificacion': calificacion,
            'estado': estado
        }
        
        self.estudiantes.append(estudiante)
        self.actualizar_lista()
        QMessageBox.information(self, 'Listo', 'Estudiante agregado')
    
    def calcular_promedio(self):
        if not self.estudiantes:
            QMessageBox.information(self, 'Info', 'No hay estudiantes registrados')
            return
        
        total = sum(est['calificacion'] for est in self.estudiantes)
        promedio = total / len(self.estudiantes)
        
        self.promedio_label.setText(f'{promedio:.2f}')
        self.total_label.setText(str(len(self.estudiantes)))
        
        QMessageBox.information(self, 'Promedio', f'Promedio general: {promedio:.2f}')
    
    def actualizar_lista(self):
        if not self.estudiantes:
            self.resultados_text.setText('No hay estudiantes registrados')
            return
        
        texto = ''
        for est in self.estudiantes:
            texto += f"{est['nombre']} - {est['materia']}: {est['calificacion']} [{est['estado']}]\n"
        
        self.resultados_text.setText(texto)
    
    def limpiar_lista(self):
        # Limpiar lista de estudiantes y resultados
        self.estudiantes = []
        self.resultados_text.clear()
        self.promedio_label.setText('0.00')
        self.total_label.setText('0')
        
        QMessageBox.information(self, 'Limpiar', 'Lista de estudiantes borrada')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = SistemaCalificaciones()
    ventana.show()
    sys.exit(app.exec_())