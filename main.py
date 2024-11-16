class Assignment:
    def __init__(self, name, assignment_type, score, weight):
        self.name = name
        self.assignment_type = assignment_type  # 'Formative' or 'Summative'
        self.score = score  # Score in percentage (0-100)
        self.weight = weight  # Weight in percentage (0-100)

    def weighted_score(self):
        return self.score * (self.weight / 100)


class Student:
    def __init__(self):
        self.assignments = []

    def add_assignment(self, name, assignment_type, score, weight):
        assignment = Assignment(name, assignment_type, score, weight)
        self.assignments.append(assignment)

    def calculate_totals(self):
        formative_total, summative_total = 0, 0
        formative_weight, summative_weight = 0, 0

        for assignment in self.assignments:
            if assignment.assignment_type == 'Formative':
                formative_total += assignment.weighted_score()
                formative_weight += assignment.weight
            elif assignment.assignment_type == 'Summative':
                summative_total += assignment.weighted_score()
                summative_weight += assignment.weight

        if formative_weight > 60:
            raise ValueError("Total formative weights exceed 60%!")
        if summative_weight > 40:
            raise ValueError("Total summative weights exceed 40%!")

        return formative_total, summative_total

    def check_progression(self, formative_total, summative_total):
        if formative_total >= 30 and summative_total >= 20:
            return "Pass: You have progressed to the next stage."
        elif formative_total < 30 and summative_total < 20:
            return "Fail: You did not meet the requirements for both Formative and Summative assessments."
        elif formative_total < 30:
            return "Fail: Formative score below the required 30%."
        else:
            return "Fail: Summative score below the required 20%."

    def check_resubmission(self):
        resubmissions = [
            assignment.name for assignment in self.assignments
            if assignment.assignment_type == 'Formative' and assignment.score < 50
        ]
        return resubmissions

    def generate_transcript(self, order="ascending"):
        sorted_assignments = sorted(
            self.assignments,
            key=lambda x: x.score,
            reverse=(order == "descending")
        )
        transcript = "Transcript Breakdown ({} Order):\n".format(order.capitalize())
        transcript += "Assignment          Type            Score(%)    Weight (%)\n"
        transcript += "-" * 55 + "\n"
        for assignment in sorted_assignments:
            transcript += f"{assignment.name:18} {assignment.assignment_type:14} {assignment.score:8} {assignment.weight:12}\n"
        return transcript


# Main Program
def main():
    student = Student()
    print("Welcome to the Course Progress Tracker Application!")

    while True:
        name = input("Enter assignment name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        assignment_type = input("Enter assignment type ('Formative' or 'Summative'): ").capitalize()
        score = float(input("Enter assignment score (0-100): "))
        weight = float(input("Enter assignment weight (in %): "))
        student.add_assignment(name, assignment_type, score, weight)

    try:
        formative_total, summative_total = student.calculate_totals()
        print("\nProgress Report:")
        print(student.check_progression(formative_total, summative_total))
    except ValueError as e:
        print(f"Error: {e}")
        return

    resubmissions = student.check_resubmission()
    if resubmissions:
        print("\nResubmission Eligible Assignments:")
        print(", ".join(resubmissions))
    else:
        print("\nNo resubmissions needed.")

    order = input("\nDo you want the transcript in ascending or descending order? ").lower()
    print("\n" + student.generate_transcript(order))


if __name__ == "__main__":
    main()
