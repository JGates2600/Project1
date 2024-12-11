import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton,
                   QLabel, QTableWidget, QTableWidgetItem, QWidget, QMessageBox)

from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from collections import Counter

from PyQt6.QtWidgets import QMessageBox


# this function assigns grade based on score and best score - same logic as LAB02
def assign_grade(score, best):
    if score >= best - 10:
        return 'A'
    elif score >= best - 20:
        return 'B'
    elif score >= best - 30:
        return 'C'
    elif score >= best - 40:
        return 'D'
    else:
        return 'F'

#Main Gui
class GradeCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Calculator")
        self.setGeometry(300, 300, 600, 600)

        #main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        #input fields
        self.student_count_label = QLabel("Student Count")
        self.layout.addWidget(self.student_count_label)

        self.student_count_input = QLineEdit()
        self.layout.addWidget(self.student_count_input)

        self.scores_label = QLabel("Scores")
        self.layout.addWidget(self.scores_label)

        self.scores_input = QLineEdit()
        self.layout.addWidget(self.scores_input)

        #buttons
        self.submit_button = QPushButton("Calculate Grades")
        self.submit_button.clicked.connect(self.calculate_grades)
        self.layout.addWidget(self.submit_button)

        self.chart_button = QPushButton("Show Grade Distribution")
        self.chart_button.clicked.connect(self.show_grade_distribution)
        self.layout.addWidget(self.chart_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_inputs)
        self.layout.addWidget(self.clear_button)

        #table for results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Score", "Grade"])
        self.layout.addWidget(self.results_table)

        #strorage to csv
        self.scores = []
        self.grades = []


    # Calculation of Grades Logic - Formerly Main
    def calculate_grades(self):
        try:
            # gets the number of students
            num_students = int(self.student_count_input.text())
            if num_students <= 0:
                raise ValueError("Number of students must be a positive integer")

            # Get the scores; Handle commas and spaces
            score_input = self.scores_input.text().strip().replace(',', ' ').split()
            self.scores = [int(score) for score in score_input]

            if len(self.scores) != num_students:
                raise ValueError("Number of students does not match number of students")

            #Calculation of grades
            best_score=max(self.scores)
            self.grades = [assign_grade(score, best_score) for score in self.scores]

            #Display Results
            self.results_table.setRowCount(len(self.grades))
            for i, (score, grade) in enumerate(zip(self.scores, self.grades)):
                self.results_table.setItem(i, 0, QTableWidgetItem(str(score)))
                self.results_table.setItem(i, 1, QTableWidgetItem(str(grade)))

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    #show grade distibution
    def show_grade_distribution(self):
        if not self.grades:
            QMessageBox.warning(self, "Error", "No grades entered")
            return
        #Count grades
        grade_counts = Counter(self.grades)
        grades, counts = zip(*grade_counts.items())

        #plot distribution
        plt.bar(grades, counts)
        plt.xlabel('Grades')
        plt.ylabel('Number of students')
        plt.title('Grades Distribution')
        plt.show()

    def clear_inputs(self):
            self.student_count_input.clear()
            self.scores_input.clear()
            self.results_table.setRowCount(0)
            self.scores = []
            self.grades = []



# runs the main program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradeCalculatorApp()
    window.show()
    sys.exit(app.exec())

