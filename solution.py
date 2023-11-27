import re
from z3 import *

def schedule_courses(k, m, pairs):
    # Criando as varáveis lógicas
    slots = [Int(f"s{i}") for i in range(1, m + 1)]
    courses = [Bool(f"x{i},{j}") for i in range(1, k + 1) for j in range(1, m + 1)]

    # Cada minicurso deve ser ofertado em pelo menos um slot.
    at_least_one_slot = [Or([courses[i * m + j] for j in range(m)]) for i in range(k)]

    # Cada minicurso deve ser ofertado em no m ́aximo um slot.
    at_most_one_slot = [Sum([If(courses[i * m + j], 1, 0) for j in range(m)]) <= 1 for i in range(k)]
