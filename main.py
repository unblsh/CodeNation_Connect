import os
import csv
from collections import defaultdict
from abc import ABC, abstractmethod


class Subject:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks


class Student:
    def __init__(self, student_id, name, class_name):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.subjects = []

    def add_subject(self, subject):
        self.subjects.append(subject)


class MarksSystemBase(ABC):
    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def handle_missing_files(self):
        pass

    @abstractmethod
    def validate_user_input(self, prompt, validator):
        pass

    @abstractmethod
    def validate_subject_choice(self, user_input):
        pass

    @abstractmethod
    def validate_assignment_number(self, user_input):
        pass

    @abstractmethod
    def calculate_average(self, student_id):
        pass

    @abstractmethod
    def generate_report(self):
        pass

    @abstractmethod
    def display_all_students(self):
        pass

    @abstractmethod
    def export_students_to_csv(self, filename):
        pass

    @abstractmethod
    def track_progress_over_time(self):
        pass

    @abstractmethod
    def save_data(self):
        pass


class StudentMarksSystem(MarksSystemBase):
    def __init__(self):
        super().__init__()
        self.students = defaultdict(dict)
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
                self.students[student_id]['Name'] = row['Name']
                self.students[student_id]['Class'] = row['Class']

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
                    self.students[student_id]['Math'] = [int(mark) for mark in row['Math'].split(',')]
                    self.students[student_id]['Science'] = [int(mark) for mark in row['Science'].split(',')]
                    self.students[student_id]['English'] = [int(mark) for mark in row['English'].split(',')]
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

    def calculate_average(self, student_id):
        # Calculate the average marks of a student
        if student_id in self.students:
            marks = [value for subject_marks in self.students[student_id].values() for value in subject_marks if isinstance(value, int)]
            if marks:
                return sum(marks) / len(marks)
        return None

    def generate_report(self):
        # Generate a report based on processed data
        for student_id, data in self.students.items():
            average = self.calculate_average(student_id)
            if average is not None:
                print(f"Student ID: {student_id}")
                print(f"Name: {data['Name']}")
                print(f"Class: {data['Class']}")
                for subject, marks in data.items():
                    if subject not in ['Name', 'Class']:
                        print(f"{subject}: {', '.join(map(str, marks))}")
                print(f"Average: {average:.2f}\n")
            else:
                print(f"Student ID {student_id} not found or has invalid data.\n")

    def display_all_students(self):
        # Display all students along with their IDs, names, and classes
        for student_id, data in self.students.items():
            print(f"Student ID: {student_id}")
            print(f"Name: {data['Name']}")
            print(f"Class: {data['Class']}\n")

    def export_students_to_csv(self, filename='all_students.csv'):
        # Export all students' data to a CSV file
        with open(filename, 'w', newline='') as file:
            fieldnames = ['StudentID', 'Name', 'Class', 'Math', 'Science', 'English']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for student_id, data in self.students.items():
                row = {'StudentID': student_id, 'Name': data['Name'], 'Class': data['Class'],
                       'Math': ','.join(map(str, data['Math'])),
                       'Science': ','.join(map(str, data['Science'])),
                       'English': ','.join(map(str, data['English']))}
                writer.writerow(row)
        print(f"All students' data exported to {filename}.\n")

    def track_progress_over_time(self):
        # Implement progress tracking over time
        for student_id, data in self.students.items():
            total_marks = sum(sum(subject_marks) for subject_marks in data.values() if isinstance(subject_marks, list))
            if total_marks > 0:
                progress = (total_marks / (100 * len(data))) * 100
                print(f"Student ID: {student_id}")
                print(f"Name: {data['Name']}")
                print(f"Total Marks: {total_marks}")
                print(f"Progress: {progress:.2f}%")

                # Nested Loop for tracking progress over time for each subject
                for subject, marks in data.items():
                    if subject not in ['Name', 'Class']:
                        print(f"Subject: {subject}")
                        previous_mark = None
                        for assignment_number, assignment_mark in enumerate(marks, start=1):
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
