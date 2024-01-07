class TeacherPortal:
    def __init__(self):
        self.students = {}

    def add_student(self, student_name):
        self.students[student_name] = {'marks': None, 'assignments': []}

    def give_marks(self, student_name, marks):
        if student_name in self.students:
            self.students[student_name]['marks'] = marks
            print(f"Marks ({marks}) assigned to {student_name}.")
        else:
            print(f"Error: {student_name} not found.")

    def add_assignment(self, student_name, assignment):
        if student_name in self.students:
            self.students[student_name]['assignments'].append(assignment)
            print(f"Assignment added for {student_name}: {assignment}.")
        else:
            print(f"Error: {student_name} not found.")
            
    def view_student_info(self, student_name):
        if student_name in self.students:
            student_info = self.students[student_name]
            print(f"\nStudent Information for {student_name}:")
            print(f"Marks: {student_info['marks']}")
            print("Assignments:", ", ".join(student_info['assignments']))
        else:
            print(f"Error: {student_name} not found.")
            
    def view_all_students(self):
       print("\nAll Students Information:")
       for student_name, student_info in self.students.items():
           print(f"\nStudent Name: {student_name}")
           print(f"Marks: {student_info['marks']}")
           print("Assignments:", ", ".join(student_info['assignments']))

    def display_menu(self):
        print("\nTeacher Portal Menu:")
        print("1. Add Student")
        print("2. Give Marks")
        print("3. Add Assignment")
        print("4. View Student Info")
        print("5. View All Students")
        print("6. Exit")
        
    def run_portal(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                student_name = input("Enter student name: ")
                self.add_student(student_name)
            elif choice == '2':
                student_name = input("Enter student name: ")
                marks = input("Enter marks: ")
                self.give_marks(student_name, marks)
            elif choice == '3':
                student_name = input("Enter student name: ")
                assignment = input("Enter assignment: ")
                self.add_assignment(student_name, assignment)
            elif choice == '4':
                student_name = input("Enter student name: ")
                self.view_student_info(student_name)
            elif choice == '5':
                self.view_all_students()
            elif choice == '6':
                print("Exiting Teacher Portal.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":

    teacher_portal = TeacherPortal()

teacher_portal.run_portal()
