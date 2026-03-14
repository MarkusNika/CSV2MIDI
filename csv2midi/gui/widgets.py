"""
Custom Widgets
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class DropZoneWidget(QWidget):
    """Drag & Drop Zone für CSV-Dateien (Future Feature)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        label = QLabel("Ziehe CSV-Dateien hierher\n(Coming Soon)")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                padding: 40px;
                background-color: #f9f9f9;
                color: #666;
                font-size: 14pt;
            }
        """)
        
        layout.addWidget(label)
        
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        # TODO: Handle dropped files
        print(f"Dropped files: {files}")