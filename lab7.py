import tkinter as tk
from tkinter import scrolledtext
import numpy as np
import random


def generate_matrix_algorithm_with_constraint(n, submatrix_size, matrix_A, threshold_sum):
    results = []

    def replace_submatrix_with_zeros(matrix, submatrix_coords):
        for coord in submatrix_coords:
            i, j = coord
            submatrix_sum = matrix[i:i + submatrix_size, j:j + submatrix_size].sum()
            if submatrix_sum <= threshold_sum:
                matrix[i:i + submatrix_size, j:j + submatrix_size] = 0

    def generate_all_zero_combinations(matrix, block_size, r, submatrices, temp_combination, index):
        if r == 0:
            temp_matrix = matrix.copy()
            submatrix_values = [temp_matrix[i:i + block_size, j:j + block_size].sum() for i, j in temp_combination]
            if all(value <= threshold_sum for value in submatrix_values):
                replace_submatrix_with_zeros(temp_matrix, temp_combination)
                results.append(temp_matrix)
            return

        if index >= len(submatrices):
            return

        temp_combination.append(submatrices[index])
        generate_all_zero_combinations(matrix, block_size, r - 1, submatrices, temp_combination, index + 1)
        temp_combination.pop()
        generate_all_zero_combinations(matrix, block_size, r, submatrices, temp_combination, index + 1)

    submatrices = [(i, j) for i in range(0, n, submatrix_size) for j in range(0, n, submatrix_size)]

    for r in range(1, len(submatrices) + 1):
        temp_combination = []
        generate_all_zero_combinations(matrix_A, submatrix_size, r, submatrices, temp_combination, 0)

    return results


def on_generate():
    try:
        n = int(entry_matrix_size.get())
        threshold_sum = int(entry_threshold.get())
        submatrix_size = n // 2
        matrix_A = np.array([[random.randint(1, 5) for _ in range(n)] for _ in range(n)])

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "Исходная матрица:\n")
        text_output.insert(tk.END, f"{matrix_A}\n\n")

        result_matrices = generate_matrix_algorithm_with_constraint(n, submatrix_size, matrix_A, threshold_sum)

        text_output.insert(tk.END, "\nВывод результов с ограничениями:\n")
        for idx, result in enumerate(result_matrices):
            text_output.insert(tk.END, f"Результат {idx + 1}:\n{result}\n\n")
    except ValueError:
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "Пожалуйста, введите корректные значения.")


app = tk.Tk()
app.title("Matrix Generator")
app.geometry('600x600')
app.eval('tk::PlaceWindow . center')

# Ввод размера матрицы и пороговой суммы
frame_input = tk.Frame(app)
frame_input.pack(pady=10)

label_matrix_size = tk.Label(frame_input, text="Размер матрицы:")
label_matrix_size.pack(side=tk.LEFT)

entry_matrix_size = tk.Entry(frame_input)
entry_matrix_size.pack(side=tk.LEFT)

label_threshold = tk.Label(frame_input, text="Пороговая сумма:")
label_threshold.pack(side=tk.LEFT)

entry_threshold = tk.Entry(frame_input)
entry_threshold.pack(side=tk.LEFT)

# Кнопка генерации
button_generate = tk.Button(app, text="Сгенерировать", command=on_generate)
button_generate.pack(pady=10)

# Окно вывода с прокруткой
frame_output = tk.Frame(app)
frame_output.pack(pady=10, fill=tk.BOTH, expand=True)

text_output = scrolledtext.ScrolledText(frame_output, wrap=tk.WORD)
text_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

app.mainloop()