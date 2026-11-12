import pandas as pd

marks = pd.Series([80, 70, 55, 35, 25])
print(marks)

courses = pd.Series(["PYTHON", "JAVA", "AWS"])
print(courses)
print(courses[0])

courses = pd.Series(
            ["PYTHON", "JAVA", "AWS"],
            index = ["C1", "C2", "C3"]
            )

print(courses)
print(courses["C2"])