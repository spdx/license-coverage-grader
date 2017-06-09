
class Grader:
	def __init__(self, grade, letterGrade):
        self.grade = grade
        self.letterGrade = letterGrade

    def gradesScore(self):
  
		if (grade > 90):
			letterGrade = 'A'
		elif grade > 75:
			letterGrade = 'B'
		elif grade >= 55:
			letterGrade = 'C'
		elif grade >= 30:
			letterGrade = 'D'
		else:
			letterGrade = 'F'

	return letterGrade
		


