import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QFrame, QStyle,
    QDialog, QStyleFactory
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from qt_material import apply_stylesheet, list_themes
from config_manager import ConfigManager
from repo_manager import RepoManager

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('About GitHub Repository Pruner')
        self.setFixedSize(500, 300)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel('GitHub Repository Pruner')
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel(
            'A simple utility to help you manage and clean up your local GitHub repositories.'
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        version = QLabel('Version 1.0.0')
        version.setFont(QFont('Arial', 12))
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        devs_frame = QFrame()
        devs_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        devs_layout = QVBoxLayout(devs_frame)
        
        devs_title = QLabel('Developers')
        devs_title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        devs_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        devs_layout.addWidget(devs_title)
        
        daniel = QLabel('Daniel Rosehill')
        daniel.setFont(QFont('Arial', 12))
        daniel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        devs_layout.addWidget(daniel)
        
        website = QLabel('<a href="https://danielrosehill.com">danielrosehill.com</a>')
        website.setOpenExternalLinks(True)
        website.setFont(QFont('Arial', 12))
        website.setAlignment(Qt.AlignmentFlag.AlignCenter)
        devs_layout.addWidget(website)
        
        roo = QLabel('Roo')
        roo.setFont(QFont('Arial', 12))
        roo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        devs_layout.addWidget(roo)
        
        layout.addWidget(devs_frame)
        
        repo = QLabel('<a href="https://github.com/danielrosehill/Github-Repo-Pruner">View on GitHub</a>')
        repo.setOpenExternalLinks(True)
        repo.setFont(QFont('Arial', 12))
        repo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(repo)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.repo_manager = RepoManager()
        self.current_theme = 'light_blue'
        
        base_path = self.config_manager.get_base_path()
        print(f"Loaded base path from config: {base_path}")  # Debug print
        if base_path:
            self.repo_manager.set_base_path(base_path)
            print(f"Total repositories found: {self.repo_manager.get_total_count()}")  # Debug print
        
        self.init_ui()
        
        # Update UI with the loaded path
        if base_path:
            self.update_path_label()
            self.update_repo_count()
        
    def init_ui(self):
        self.setWindowTitle('GitHub Repository Pruner')
        self.setMinimumSize(800, 600)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with title, theme toggle, and about button
        header_layout = QHBoxLayout()
        
        title_label = QLabel('GitHub Repository Pruner')
        title_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        
        self.theme_btn = QPushButton()
        self.theme_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarShadeButton))  # Sun icon
        self.theme_btn.setFixedWidth(40)
        self.theme_btn.setToolTip('Toggle Light/Dark Theme')
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        about_btn = QPushButton()
        about_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton))
        about_btn.setFixedWidth(40)
        about_btn.setToolTip('About')
        about_btn.clicked.connect(self.show_about)
        header_layout.addWidget(about_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(header_layout)
        
        # Mode selection
        mode_frame = QFrame()
        mode_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        mode_frame.setStyleSheet("""
            QFrame {
                border-radius: 10px;
                box-shadow: 2px 2px 5px #888888;
            }
        """)
        mode_layout = QHBoxLayout(mode_frame)
        mode_layout.setSpacing(15)
        
        self.alpha_btn = QPushButton('Alphabetical Mode')
        self.alpha_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        self.alpha_btn.setMinimumHeight(40)
        self.alpha_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.random_btn = QPushButton('Random Mode')
        self.random_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.random_btn.setMinimumHeight(40)
        self.random_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
        self.alpha_btn.clicked.connect(lambda: self.set_mode(False))
        self.random_btn.clicked.connect(lambda: self.set_mode(True))
        mode_layout.addWidget(self.alpha_btn)
        mode_layout.addWidget(self.random_btn)
        layout.addWidget(mode_frame)
        
        # Settings section
        settings_frame = QFrame()
        settings_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        settings_frame.setStyleSheet("""
            QFrame {
                border-radius: 10px;
                box-shadow: 2px 2px 5px #888888;
            }
        """)
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setSpacing(10)
        
        path_header = QLabel('Repository Base Path')
        path_header.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        settings_layout.addWidget(path_header)
        
        self.path_label = QLabel('Not Set')
        self.path_label.setWordWrap(True)
        self.path_label.setFont(QFont('Arial', 12))
        self.path_label.setStyleSheet("""
            QLabel {
                color: #000000;
                background-color: #ffffff;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #cccccc;
            }
        """)
        settings_layout.addWidget(self.path_label)
        
        set_path_btn = QPushButton('Set Base Path')
        set_path_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))
        set_path_btn.setMinimumHeight(40)
        set_path_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        set_path_btn.clicked.connect(self.set_base_path)
        settings_layout.addWidget(set_path_btn)
        
        layout.addWidget(settings_frame)
        
        # Repository display
        self.repo_frame = QFrame()
        self.repo_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.repo_frame.setStyleSheet("""
            QFrame {
                border-radius: 10px;
                box-shadow: 2px 2px 5px #888888;
            }
        """)
        repo_layout = QVBoxLayout(self.repo_frame)
        repo_layout.setSpacing(10)
        
        self.repo_name_label = QLabel('Select a mode to start')
        self.repo_name_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        self.repo_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.repo_name_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                margin: 10px;
            }
        """)
        
        self.repo_path_label = QLabel('')
        self.repo_path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.repo_path_label.setFont(QFont('Arial', 12))
        self.repo_path_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                margin: 5px;
            }
        """)
        
        repo_layout.addWidget(self.repo_name_label)
        repo_layout.addWidget(self.repo_path_label)
        layout.addWidget(self.repo_frame)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        self.delete_btn = QPushButton('Delete')
        self.delete_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        self.delete_btn.setMinimumHeight(40)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #922b21;
            }
        """)
        
        self.keep_btn = QPushButton('Keep')
        self.keep_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        self.keep_btn.setMinimumHeight(40)
        self.keep_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        
        self.delete_btn.clicked.connect(self.delete_current_repo)
        self.keep_btn.clicked.connect(self.keep_current_repo)
        action_layout.addWidget(self.delete_btn)
        action_layout.addWidget(self.keep_btn)
        layout.addLayout(action_layout)
        
        # Status message
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Repository count
        self.count_label = QLabel('Total Repositories: 0')
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label.setFont(QFont('Arial', 12))
        layout.addWidget(self.count_label)
        
        # Set up status message timer
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.clear_status)
        
        # Update UI state
        self.set_actions_enabled(False)
    
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()
    
    def set_mode(self, random_mode):
        if not self.repo_manager.base_path:
            QMessageBox.warning(self, 'Warning', 'Please set base path first')
            return
            
        self.repo_manager.set_random_mode(random_mode)
        self.alpha_btn.setEnabled(not random_mode)
        self.random_btn.setEnabled(random_mode)
        self.load_current_repo()
        self.set_actions_enabled(True)
    
    def set_base_path(self):
        dialog = QFileDialog()
        path = dialog.getExistingDirectory(
            self,
            'Select Base Repository Directory',
            str(Path.home())
        )
        
        if path:
            try:
                self.config_manager.set_base_path(path)
                self.repo_manager.set_base_path(path)
                self.update_path_label()
                self.update_repo_count()
                self.show_status('Base path updated successfully')
            except ValueError as e:
                QMessageBox.warning(self, 'Error', str(e))
    
    def update_path_label(self):
        base_path = self.repo_manager.base_path
        path_text = str(base_path or "Not Set")
        print(f"Updating path label to: {path_text}")  # Debug print
        self.path_label.setText(path_text)
    
    def load_current_repo(self):
        repo = self.repo_manager.get_current_repo()
        if repo:
            self.repo_name_label.setText(repo['name'])
            self.repo_path_label.setText(repo['path'])
            self.animate_repo_frame()
        else:
            if not self.repo_manager._random_mode:
                self.show_status('End of repositories reached')
                self.set_actions_enabled(False)
            self.repo_name_label.setText('No repositories available')
            self.repo_path_label.setText('')
    
    def delete_current_repo(self):
        if self.repo_manager.delete_current_repo():
            self.show_status('Repository deleted')
            self.update_repo_count()
            self.load_current_repo()
    
    def keep_current_repo(self):
        self.repo_manager.next_repo()
        self.load_current_repo()
    
    def update_repo_count(self):
        count = self.repo_manager.get_total_count()
        self.count_label.setText(f'Total Repositories: {count}')
    
    def show_status(self, message, duration=1000):
        self.status_label.setText(message)
        self.status_timer.start(duration)
    
    def clear_status(self):
        self.status_label.setText('')
        self.status_timer.stop()
    
    def set_actions_enabled(self, enabled):
        self.delete_btn.setEnabled(enabled)
        self.keep_btn.setEnabled(enabled)

    def toggle_theme(self):
        themes = ['light_blue', 'dark_blue']
        current_index = themes.index(self.current_theme)
        self.current_theme = themes[(current_index + 1) % len(themes)]
        apply_stylesheet(QApplication.instance(), theme=f'{self.current_theme}.xml')
        
        # Additional stylesheet for better text contrast and consistent styling
        if self.current_theme.startswith('light'):
            QApplication.instance().setStyleSheet("""
                QLabel { color: #000000; }
                QPushButton { 
                    color: #000000;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 0.1);
                }
                QMainWindow { background-color: #ffffff; }
                QFrame {
                    border-radius: 8px;
                    background-color: rgba(255, 255, 255, 0.8);
                    border: 1px solid #dddddd;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
            """)
            self.theme_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarShadeButton))  # Sun icon
        else:
            QApplication.instance().setStyleSheet("""
                QLabel { color: #ffffff; }
                QPushButton { 
                    color: #ffffff;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
                QMainWindow { background-color: #2d2d2d; }
                QFrame {
                    border-radius: 8px;
                    background-color: rgba(45, 45, 45, 0.8);
                    border: 1px solid #444444;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                }
            """)
            self.theme_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarUnshadeButton))  # Moon icon

    def animate_repo_frame(self):
        animation = QPropertyAnimation(self.repo_frame, b"geometry")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        current_geometry = self.repo_frame.geometry()
        start_geometry = QRect(current_geometry.x() + 50, current_geometry.y(),
                             current_geometry.width(), current_geometry.height())
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(current_geometry)
        animation.start()

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    # Additional stylesheet for better text contrast and consistent styling
    app.setStyleSheet("""
        QLabel { color: #000000; }
        QPushButton { 
            color: #000000;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: rgba(0, 0, 0, 0.1);
        }
        QMainWindow { background-color: #ffffff; }
        QFrame {
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.8);
            border: 1px solid #dddddd;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

import shutil
import os

def build_program():
    build_dir = '/home/daniel/Development/Build/compiled/repopruner'
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    # Copy main.py, config_manager.py, repo_manager.py, and requirements.txt
    shutil.copy('main.py', build_dir)
    shutil.copy('config_manager.py', build_dir)
    shutil.copy('repo_manager.py', build_dir)
    shutil.copy('requirements.txt', build_dir)
    
    print(f"Program built to {build_dir}")

if __name__ == '__main__':
    main()
