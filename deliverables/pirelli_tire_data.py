import pandas as pd

data = [
    ["Australia", False, "X", "X", "X", "", "", ""],
    ["China", False, "X", "X", "X", "", "", ""],
    ["Japan", False, "X", "X", "X", "", "", ""],
    ["Bahrain", False, "X", "X", "X", "", "", ""],
    ["Saudi Arabia", True, "X", "X", "X", "", "", ""],
    ["Miami", True, "X", "X", "X", "", "", ""],
    ["Emilia-Romagna", True, "", "", "", "X", "X", "X"],
    ["Monaco", True, "", "", "", "X", "X", "X"],
    ["Spain", False, "X", "X", "X", "", "", ""],
    ["Canada", True, "", "", "", "X", "X", "X"],
    ["Austria", False, "", "", "", "X", "X", "X"],
    ["Great Britain", True, "X", "X", "X", "", "", ""],
    ["Belgium", True, "X", "", "X", "X", "", ""],
    ["Hungary", False, "", "", "", "X", "X", "X"],
    ["Netherlands", True, "X", "X", "X", "", "", ""],
    ["Italy", False, "", "", "", "X", "X", "X"],
    ["Azerbaijan", True, "", "", "", "X", "X", "X"],
    ["Singapore", False, "", "", "", "X", "X", "X"],
    ["United States", True, "X", "", "X", "X", "", ""],
    ["Mexico City", True, "X", "", "", "X", "X", ""],
    ["São Paulo", True, "X", "X", "X", "", "", ""],
    ["Las Vegas", False, "", "", "", "X", "X", "X"],
    ["Qatar", False, "X", "X", "X", "", "", ""],
    ["Abu Dhabi", False, "", "", "", "X", "X", "X"],
]

columns = ["Grand Prix", "New Course", "C1", "C2", "C3", "C4", "C5", "C6"]
df = pd.DataFrame(data, columns=columns)

print(df)
