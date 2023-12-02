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

    # Minicursos com inscrições em comum não podem ser ofertados no mesmo slot.
    no_common_registrations = [Not(And(courses[(x - 1) * m + i], courses[(y - 1) * m + i]))
                               for (x, y) in pairs for i in range(m)]

    # Solucionador do Z3
    solver = Solver()

    # Adicionando as restrições ao solucionador
    solver.add(at_least_one_slot + at_most_one_slot + no_common_registrations)

    # Verificando a satisfabilidade do algoritmo
    if solver.check() == sat:
        model = solver.model()

        # Extraindo a valoração do cronograma
        schedule = {courses[i * m + j]: (i + 1, slots[j]) for i in range(k) for j in range(m) if is_true(model.evaluate(courses[i * m + j], model_completion=True))}

        # Print cronograma
        for course in sorted(schedule, key=lambda x: int(re.search(r'\d+', str(x)).group())):
            course_id, time_slot = schedule[course]
            print(f"{course_id} {time_slot}")
    else:
        print("Not possible to schedule the courses with the given constraints.")

# Examples:
k = 4
m = 3
pairs = [(1, 2), (2, 3), (2, 4), (3, 4)]

schedule_courses(k, m, pairs)
