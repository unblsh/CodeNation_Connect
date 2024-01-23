import os
import csv
from collections import defaultdict

class Subject:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

class Student:
    def __init__(self, student_id, name, class_name):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.subjects = {}

    def add_subject(self, subject):
        self.subjects[subject.name] = subject

class MarksSystemBase:
    def __init__(self):
        self.students = defaultdict(Student)
        self.subject_weights = {'Math': 1, 'Science': 1, 'English': 1}
        self.load_data()

    def load_data(self):
        # Load data from files
        try:
            self.load_student_data('students.csv')
            self.load_marks_data('marks.csv')
            self.load_subject_weights('weights.csv')
        except FileNotFoundError:
            print("Error: One or both of the CSV files not found.")
            self.handle_missing_files()

    def handle_missing_files(self):
        # Additional error handling for missing files
        print("Please check if the CSV files are present in the correct path.")
        exit()

    def load_student_data(self, filename):
        # Load student data from a CSV file
        with open(filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=";")
            required_columns = ['StudentID', 'Name', 'Class']
            for column in required_columns:
                if column not in reader.fieldnames:
                    print(f"Error: {column} column is missing in {filename}.")
                    exit()

            for row in reader:
                student_id = row['StudentID']
                self.students[student_id] = Student(student_id, row['Name'], row['Class'])

    def load_marks_data(self, filename):
        # Load marks data from a CSV file
        with open(filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=";")
            required_columns = ['StudentID', 'Math', 'Science', 'English']
            for column in required_columns:
                if column not in reader.fieldnames:
                    print(f"Error: {column} column is missing in {filename}.")
                    exit()

            for row in reader:
                student_id = row['StudentID']
                try:
                    math_marks = [int(mark) for mark in row['Math'].split(',')]
                    science_marks = [int(mark) for mark in row['Science'].split(',')]
                    english_marks = [int(mark) for mark in row['English'].split(',')]
                    math_subject = Subject('Math', math_marks)
                    science_subject = Subject('Science', science_marks)
                    english_subject = Subject('English', english_marks)
                    self.students[student_id].add_subject(math_subject)
                    self.students[student_id].add_subject(science_subject)
                    self.students[student_id].add_subject(english_subject)
                except ValueError as e:
                    print(f"Error converting values for student {student_id}: {e}")
                    exit()

    def load_subject_weights(self, filename):
        # Load subject weights from a CSV file
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    subject = row['Subject']
                    weight = float(row['Weight'])
                    self.subject_weights[subject] = weight
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Using default weights for subjects.")

    def validate_user_input(self, prompt, validator):
        while True:
            user_input = input(prompt)
            try:
                user_input = validator(user_input)
                return user_input
            except ValueError as e:
                print(f"Invalid input. {e}")

    def validate_subject_choice(self, user_input):
        subject_mapping = {'1': 'Math', '2': 'Science', '3': 'English'}
        if user_input in subject_mapping:
            return subject_mapping[user_input]
        else:
            raise ValueError("Please enter a valid subject choice (1, 2, or 3).")

    def validate_assignment_number(self, user_input):
        try:
            assignment_number = int(user_input)
            if assignment_number > 0:
                return assignment_number
            else:
                raise ValueError("Assignment number must be greater than 0.")
        except ValueError:
            raise ValueError("Please enter a valid assignment number.")

class StudentMarksSystem(MarksSystemBase):
    def calculate_weighted_average(self, student_id):
        # Calculate the weighted average marks of a student
        if student_id in self.students:
            total_weighted_marks = 0
            total_weight = 0

            for subject in self.students[student_id].subjects.values():
                subject_weight = self.subject_weights.get(subject.name, 1)
                total_weighted_marks += sum(subject.marks) * subject_weight
                total_weight += len(subject.marks) * subject_weight

            if total_weight > 0:
                return total_weighted_marks / total_weight

        return None

    def generate_report(self):
        # Generate a report based on processed data, sorted by weighted average
        sorted_students = sorted(self.students.items(), key=lambda x: self.calculate_weighted_average(x[0]), reverse=True)
        for student_id, student in sorted_students:
            weighted_average = self.calculate_weighted_average(student_id)
            if weighted_average is not None:
                print(f"Student ID: {student_id}")
                print(f"Name: {student.name}")
                print(f"Class: {student.class_name}")
                for subject in student.subjects.values():
                    print(f"{subject.name}: {', '.join(map(str, subject.marks))}")
                print(f"Weighted Average: {weighted_average:.2f}\n")
            else:
                print(f"Student ID {student_id} not found or has invalid data.\n")

    def display_all_students(self):
        # Display all students sorted by name
        sorted_students = sorted(self.students.items(), key=lambda x: x[1].name)
        for student_id, student in sorted_students:
            print(f"Student ID: {student_id}")
            print(f"Name: {student.name}")
            print(f"Class: {student.class_name}\n")

    def export_students_to_csv(self, filename='all_students.csv'):
        # Export all students' data to a CSV file
        with open(filename, 'w', newline='') as file:
            fieldnames = ['StudentID', 'Name', 'Class', 'Math', 'Science', 'English']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for student_id, student in self.students.items():
                row = {'StudentID': student_id, 'Name': student.name, 'Class': student.class_name,
                       'Math': ','.join(map(str, student.subjects['Math'].marks)),
                       'Science': ','.join(map(str, student.subjects['Science'].marks)),
                       'English': ','.join(map(str, student.subjects['English'].marks))}
                writer.writerow(row)
        print(f"All students' data exported to {filename}.\n")

    def track_progress_over_time(self):
        # Implement progress tracking over time
        for student_id, student in self.students.items():
            total_marks = sum(mark for subject in student.subjects.values() for mark in subject.marks)
            if total_marks > 0:
                progress = (total_marks / (100 * len(student.subjects))) * 100
                print(f"Student ID: {student_id}")
                print(f"Name: {student.name}")
                print(f"Total Marks: {total_marks}")
                print(f"Progress: {progress:.2f}%")

                # Nested Loop for tracking progress over time for each subject
                for subject in student.subjects.values():
                    print(f"Subject: {subject.name}")
                    previous_mark = None
                    for assignment_number, assignment_mark in enumerate(subject.marks, start=1):
                        # Calculate progress based on the difference from the previous assignment's score
                        if previous_mark is not None:
                            assignment_progress = ((assignment_mark - previous_mark) / previous_mark) * 100
                            print(f"  Assignment {assignment_number}: {assignment_mark} (Progress: {assignment_progress:.2f}%)")
                        else:
                            print(f"  Assignment {assignment_number}: {assignment_mark}")
                        previous_mark = assignment_mark
                print("\n")
            else:
                print(f"Student ID {student_id} has no valid marks data.\n")

    def save_data(self):
        # Save data back to files if needed
        pass

if __name__ == "__main__":
    try:
        marks_system = StudentMarksSystem()
    except FileNotFoundError:
        print("Error: One or both of the CSV files not found.")
        exit()

    while True:
        print("1. Generate Report")
        print("2. Display All Students")
        print("3. Export All Students to CSV")
        print("4. Track Progress Over Time")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            marks_system.generate_report()
        elif choice == '2':
            marks_system.display_all_students()
        elif choice == '3':
            marks_system.export_students_to_csv()
        elif choice == '4':
            marks_system.track_progress_over_time()
        elif choice == '5':
            marks_system.save_data()
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
