

import sys
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QListWidget, QFrame,
                             QComboBox, QToolTip, QStackedWidget, QLineEdit, QTextEdit)
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QColor, QPainter, QFont, QPalette, QPen

class BlockButton(QPushButton):
    def __init__(self, name, desc, ex, color):
        super().__init__(name)
        self.setToolTip(f"<b>Aide :</b> {desc}<br><i>Ex: {ex}</i>")
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #222;
            }}
            QPushButton:hover {{
                background-color: white;
                color: {color};
                border: 2px solid {color};
            }}
        """)

class Scene(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #ffffff; border: 4px solid #4C97FF; border-radius: 15px;")
        self.win_animation = False
        self.reset_positions()

    def reset_positions(self):
        self.cube_pos = QPoint(20, 20)
        self.win_animation = False
        rx = random.randint(2, 18) * 20
        ry = random.randint(2, 18) * 20
        self.target_pos = QPoint(rx, ry)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor("#f0f0f0"))
        painter.setPen(pen)
        for i in range(0, 401, 20):
            painter.drawLine(i, 0, i, 400)
            painter.drawLine(0, i, 400, i)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#FF4B4B"))
        painter.drawRect(self.target_pos.x(), self.target_pos.y(), 20, 20)
        color = QColor("#FFD700") if self.win_animation else QColor("#4C97FF")
        painter.setBrush(color)
        size = 26 if self.win_animation else 20
        offset = (size - 20) // 2
        painter.drawRect(self.cube_pos.x() - offset, self.cube_pos.y() - offset, size, size)

class ScratchGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projet Rhétos - Programmation Visuelle")
        self.resize(1400, 700)
        self.essais = 3 
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)
        self.scene = Scene()

        # --- BLOCS ---
        col1 = QVBoxLayout()
        self.cat_selector = QComboBox()
        self.cat_selector.addItems(["🏃 Mouvement", "⚙️ Logique"])
        self.cat_selector.setStyleSheet("padding: 5px; background: #333; color: white;")
        self.cat_selector.currentIndexChanged.connect(lambda i: self.stack.setCurrentIndex(i))
        col1.addWidget(QLabel("<b>🧩 1. CHOISIR</b>"))
        col1.addWidget(self.cat_selector)

        self.stack = QStackedWidget()
        p1 = QWidget(); l1 = QVBoxLayout(p1)
        for n in ["Avancer", "Reculer", "Monter", "Descendre"]:
            btn = BlockButton(n, f"Déplace vers {n}", n, "#4C97FF")
            btn.clicked.connect(lambda ch, name=n: self.add_to_script(name))
            l1.addWidget(btn)
        l1.addStretch(); self.stack.addWidget(p1)

        p2 = QWidget(); l2 = QVBoxLayout(p2)
        l2.addWidget(QLabel("Répétitions :"))
        self.loop_input = QLineEdit("5")
        self.loop_input.setStyleSheet("background: #1a1a1a; color: #FFAB19; border: 1px solid #FFAB19; padding: 8px;")
        l2.addWidget(self.loop_input)
        btn_w = BlockButton("Boucle (While)", "Répète le code", "while true (n)", "#FFAB19")
        btn_w.clicked.connect(self.add_loop_block)
        l2.addWidget(btn_w)
        l2.addStretch(); self.stack.addWidget(p2)
        col1.addWidget(self.stack)
        main_layout.addLayout(col1, 1)

        # --- SCRIPT visu---
        col2 = QVBoxLayout()
        col2.addWidget(QLabel("<b>📝 2. TON SCRIPT</b>"))
        self.script_view = QListWidget()
        self.script_view.itemClicked.connect(self.remove_item)
        self.script_view.setStyleSheet("background-color: #1a1a1a; color: white; border: 2px solid #333; border-radius: 10px;")
        col2.addWidget(self.script_view)

        self.btn_run = QPushButton("▶️ LANCER")
        self.btn_run.setStyleSheet("background: #4CAF50; color: white; font-weight: bold; height: 50px; border-radius: 10px;")
        self.btn_run.clicked.connect(self.run_logic)
        col2.addWidget(self.btn_run)
        main_layout.addLayout(col2, 1)

        # --- JEU ---
        col3 = QVBoxLayout()
        # Affichage des chances
        self.chances_label = QLabel(f"❤️ Chances restantes : {self.essais}")
        self.chances_label.setStyleSheet("font-size: 18px; color: #FF4B4B; font-weight: bold;")
        col3.addWidget(self.chances_label)

        self.var_label = QLabel("Cases restantes : --")
        self.var_label.setStyleSheet("font-size: 18px; color: #FFAB19; font-weight: bold; background: #222; padding: 10px; border-radius: 10px;")
        col3.addWidget(QLabel("<b>🎮 3. SIMULATION</b>"))
        col3.addWidget(self.scene)
        col3.addWidget(self.var_label)
        main_layout.addLayout(col3, 1)

        # --- CODE visu ---
        col4 = QVBoxLayout()
        col4.addWidget(QLabel("<b>💻 4. CODE</b>"))
        self.code_preview = QTextEdit()
        self.code_preview.setReadOnly(True)
        self.code_preview.setStyleSheet("background-color: #282c34; color: #98c379; font-family: 'Consolas'; font-size: 14px; border-radius: 10px;")
        col4.addWidget(self.code_preview)
        main_layout.addLayout(col4, 1)
        self.update_python_preview()

    def add_to_script(self, name):
        self.script_view.addItem(name)
        self.update_python_preview()

    def remove_item(self, item):
        self.script_view.takeItem(self.script_view.row(item))
        self.update_python_preview()

    def add_loop_block(self):
        nb = self.loop_input.text() if self.loop_input.text().isdigit() else "1"
        self.script_view.addItem(f"--- BOUCLE ({nb} fois) ---")
        self.update_python_preview()

    def update_python_preview(self):
        text = "# --- INITIALISATION ---\ncube = carré-bleu\n\n# --- PROGRAMME ---\n"
        items = [self.script_view.item(i).text() for i in range(self.script_view.count())]
        indent = ""
        for item in items:
            if "BOUCLE" in item:
                nb = item.split('(')[1].split(' ')[0]
                text += f"while true ({nb}) :\n"; indent = "    "
            else:
                cmd = item.lower()
                if cmd == "avancer": action = "cube.x = +1"
                elif cmd == "reculer": action = "cube.x = -1"
                elif cmd == "monter": action = "cube.y = +1"
                elif cmd == "descendre": action = "cube.y = -1"
                else: action = "action_inconnue()"
                text += f"{indent}{action}\n"
        self.code_preview.setText(text)

    def run_logic(self):
        if self.essais <= 0: return 
        raw_cmds = [self.script_view.item(i).text() for i in range(self.script_view.count())]
        self.final_queue = []
        i = 0
        while i < len(raw_cmds):
            if "BOUCLE" in raw_cmds[i]:
                try: count = int(raw_cmds[i].split('(')[1].split(' ')[0])
                except: count = 1
                sub_cmds = raw_cmds[i+1:]
                for _ in range(count): self.final_queue.extend(sub_cmds)
                break
            else: self.final_queue.append(raw_cmds[i])
            i += 1
        self.current_step = 0
        self.timer = QTimer(); self.timer.timeout.connect(self.execute_step); self.timer.start(150)

    def execute_step(self):
        if self.current_step < len(self.final_queue):
            cmd = self.final_queue[self.current_step]
            nx, ny = self.scene.cube_pos.x(), self.scene.cube_pos.y()
            if cmd == "Avancer": nx += 20
            elif cmd == "Reculer": nx -= 20
            elif cmd == "Monter": ny -= 20
            elif cmd == "Descendre": ny += 20
            if 0 <= nx <= 380 and 0 <= ny <= 380:
                self.scene.cube_pos.setX(nx); self.scene.cube_pos.setY(ny)
            self.scene.update()
            self.current_step += 1
        else:
            self.timer.stop()
            dist = abs(self.scene.cube_pos.x() - self.scene.target_pos.x()) + abs(self.scene.cube_pos.y() - self.scene.target_pos.y())

            if dist == 0:
                self.scene.win_animation = True; self.scene.update()
                self.var_label.setText("🏆 VICTOIRE !"); self.essais = 3
                QTimer.singleShot(2000, self.auto_reset)
            else:
                self.essais -= 1
                if self.essais > 0:
                    self.var_label.setText(f"❌ Raté ! Il reste {self.essais} essais.")
                    #c ble dép
                    self.scene.cube_pos = QPoint(20, 20); self.scene.update()
                else:
                    self.var_label.setText("💀 Perdu ! La cible change !")
                    QTimer.singleShot(2000, self.auto_reset) # Change de place

            self.chances_label.setText(f"❤️ Chances restantes : {self.essais}")

    def auto_reset(self):
        self.essais = 3
        self.chances_label.setText(f"❤️ Chances restantes : {self.essais}")
        self.script_view.clear(); self.scene.reset_positions(); self.update_python_preview()
        self.var_label.setText("Cible déplacée !")
def execute_step(self):
        # 1. cmd a
        if self.current_step < len(self.final_queue):
            cmd = self.final_queue[self.current_step]
            nx, ny = self.scene.cube_pos.x(), self.scene.cube_pos.y()

            # 2. cal mvt
            if cmd == "Avancer": nx += 20
            elif cmd == "Reculer": nx -= 20
            elif cmd == "Monter": ny -= 20
            elif cmd == "Descendre": ny += 20

            # 3. lim terr
            if 0 <= nx <= 380 and 0 <= ny <= 380:
                self.scene.cube_pos.setX(nx)
                self.scene.cube_pos.setY(ny)

            self.scene.update()

            # 4. Cal dist aff
            dist = abs(self.scene.cube_pos.x() - self.scene.target_pos.x()) + \
                   abs(self.scene.cube_pos.y() - self.scene.target_pos.y())
            self.var_label.setText(f"Cases restantes : {dist//20}")


            self.current_step += 1

        else:
            #fin
            self.timer.stop()

            # Ble sur Rgr
            final_dist = abs(self.scene.cube_pos.x() - self.scene.target_pos.x()) + \
                         abs(self.scene.cube_pos.y() - self.scene.target_pos.y())

            if final_dist == 0:
                self.scene.win_animation = True
                self.scene.update()
                self.var_label.setText("🏆 PILE DESSUS ! VICTOIRE !")
                QTimer.singleShot(2000, self.auto_reset)
            else:
                self.var_label.setText("❌ Raté ! Tu ne t'es pas arrêté dessus.")

def auto_reset(self):
        self.script_view.clear(); self.scene.reset_positions(); self.update_python_preview()
        self.var_label.setText("Nouveau challenge !")

if __name__ == "__main__":
    app = QApplication(sys.argv); app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    app.setPalette(palette)
    win = ScratchGame(); win.show(); sys.exit(app.exec())
