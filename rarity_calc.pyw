import sys
import pathlib
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QComboBox, QPushButton, QWidget

def read_scores_from_file(file_path):
    scores = {}
    with open(file_path, "r") as file:
        exec(file.read(), scores)
    return scores

def read_items_from_file(file_path):
    items = {}
    with open(file_path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:
                if ":" not in line:
                    print(f"Irregularity found in items.txt on line {line_number}: Missing colon (':'). Skipping line.")
                    continue

                item, rarity = line.split(":", 1)
                item = item.strip()
                rarity = rarity.strip()

                if not item:
                    print(f"Irregularity found in items.txt on line {line_number}: Missing item name. Skipping line.")
                    continue

                if not rarity:
                    print(f"Irregularity found in items.txt on line {line_number}: Missing rarity. Skipping line.")
                    continue

                items[item] = rarity

    return items

def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = pathlib.Path(sys._MEIPASS)
    else:
        base_path = pathlib.Path(__file__).resolve().parent
    return str(base_path / relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Item Score Calculator")
        self.setWindowIcon(QIcon(get_resource_path("icon.ico")))
        self.setFixedWidth(281)
        
        scores = read_scores_from_file(get_resource_path("scores.txt"))
        rarities = scores.get("rarities", {})
        
        items = read_items_from_file(get_resource_path("items.txt"))
        
        self.item_label = QLabel("Item:")
        self.item_combo = QComboBox()
        self.item_combo.addItems(items.keys())
        
        self.color_label = QLabel("Color:")
        self.color_combo = QComboBox()
        self.color_combo.addItems(scores.get("colors", {}).keys())
        
        self.shiny_label = QLabel("Shiny Value:")
        self.shiny_combo = QComboBox()
        self.shiny_combo.addItems(scores.get("shiny_values", {}).keys())
        
        self.particle_label = QLabel("Particle:")
        self.particle_combo = QComboBox()
        self.particle_combo.addItems(scores.get("particles", {}).keys())
        
        self.calculate_button = QPushButton("Calculate Score")
        self.calculate_button.clicked.connect(self.calculate_score)
        
        self.score_label = QLabel()
        
        layout = QVBoxLayout()
        layout.addWidget(self.item_label)
        layout.addWidget(self.item_combo)
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_combo)
        layout.addWidget(self.shiny_label)
        layout.addWidget(self.shiny_combo)
        layout.addWidget(self.particle_label)
        layout.addWidget(self.particle_combo)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.score_label)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.rarities = rarities
        self.items = items
        
    def calculate_score(self):
        selected_item = self.item_combo.currentText()
        selected_color = self.color_combo.currentText()
        selected_shiny = self.shiny_combo.currentText()
        selected_particle = self.particle_combo.currentText()
        
        item_rarity = self.items.get(selected_item, "")
        item_score = self.rarities.get(item_rarity, 0)
        color_score = read_scores_from_file(get_resource_path("scores.txt")).get("colors", {}).get(selected_color, 0)
        shiny_score = read_scores_from_file(get_resource_path("scores.txt")).get("shiny_values", {}).get(selected_shiny, 0)
        particle_score = read_scores_from_file(get_resource_path("scores.txt")).get("particles", {}).get(selected_particle, 0)
        
        overall_score = item_score + color_score + shiny_score + particle_score
        
        self.score_label.setText("Overall Score: " + str(overall_score))
        
    def save_score(self, score):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
