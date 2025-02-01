import tkinter as tk
from tkinter import messagebox, scrolledtext
from Determinant import *
from InverseMatrix import *


# 🧠 가우스 소거법 단계별 출력 함수
def gaussian_elimination(matrix, process_output):
    maat = get_rows(get_columns(matrix))
    process = GetGaussianEliminationProcess(matrix)
    for num in range(len(process)) :
        pro = process[num]
        pro = pro.split(',')
        if pro[0] == "A" :
            process_output.insert(tk.END, "{0}행과 {1}행을 바꿉니다.\n\n".format(pro[1], pro[2]))
            maat = Operation1(maat, int(pro[1])-1, int(pro[2])-1)
            maat = CleanMatrix(maat, 2)
            pro_text = "\n".join(" ".join(map(lambda x: f"{x:.2f}", row)) for row in maat)
            process_output.insert(tk.END, pro_text)
            process_output.update_idletasks()
        elif pro[0] == "B" :
            process_output.insert(tk.END, "{0}행에 {1:.2f}배를 곱합니다.\n\n".format(pro[1], float(pro[2])))
            maat = Operation2(maat, int(pro[1])-1, float(pro[2]))
            maat = CleanMatrix(maat, 2)
            pro_text = "\n".join(" ".join(map(lambda x: f"{x:.2f}", row)) for row in maat)
            process_output.insert(tk.END, pro_text)
            process_output.update_idletasks()
        elif pro[0] == "C" :
            process_output.insert(tk.END, "{0}행에 {1}행의 {2:.2f}배를 더합니다.\n\n".format(pro[1], pro[2], float(pro[3])))
            maat = Operation3(maat, int(pro[1])-1, int(pro[2])-1, float(pro[3]))
            maat = CleanMatrix(maat, 2)
            pro_text = "\n".join(" ".join(map(lambda x: f"{x:.2f}", row)) for row in maat)
            process_output.insert(tk.END, pro_text)
            process_output.update_idletasks()
        process_output.insert(tk.END, '\n\n')
        process_output.update_idletasks()
    return GetGaussianEliminationResult(matrix)

# 🛠️ 선형 독립성 검사 버튼 함수
def check_linear_independence():
    input_text = input_field.get("1.0", tk.END).strip()
    result_label.config(text="")  # 이전 결과 초기화
    
    try:
        matrix = [list(map(float, row.split())) for row in input_text.splitlines()]
        is_independent = isLinearlyIndependent(matrix)
        result_text = "선형 독립입니다!" if is_independent else "선형 종속입니다!"
        result_label.config(text=result_text, fg="green" if is_independent else "red")
    except Exception as e:
        messagebox.showerror("오류", str(e))

# 🛠️ 가우스 소거법 실행 버튼 함수
def calculate():
    input_text = input_field.get("1.0", tk.END).strip()
    process_output.delete("1.0", tk.END)
    result_output.delete("1.0", tk.END)
    
    try:
        matrix = [list(map(float, row.split())) for row in input_text.splitlines()]
        result = gaussian_elimination(matrix, process_output)
        result_text = "\n".join(" ".join(map(lambda x: f"{x:.2f}", row)) for row in result)
        result_output.insert(tk.END, result_text)
    except Exception as e:
        messagebox.showerror("오류", str(e))

def format_solution(result_columned):
    """
    result_columned를 특수해 + 일반해 형태로 변환합니다.
    """
    try:
        if not result_columned or not result_columned[0]:
            raise ValueError("빈 결과 행렬입니다.")
        
        rows = len(result_columned)
        cols = len(result_columned[0])
        # 특수해 (첫 번째 열)
        particular_solution = [result_columned[i][0] for i in range(rows)]
        
        # 일반해 (나머지 열들)
        general_solution = [[result_columned[row][col] for col in range(1, cols)] for row in range(rows)]
        result_lines = []
        for i in range(rows):
            line = f"{particular_solution[i]:>6.2f}"  # 첫 번째 열 (특수해)
            for j in range(len(general_solution[i])):
                if i == rows // 2 and j == 0:
                    line += " + span ("
                else : 
                    if j == 0 :
                        line += "               "
                line += f"{general_solution[i][j]:>8.2f}"
            if i == rows // 2 and len(general_solution[i]) > 0:
                line += "   )"
            result_lines.append(line)
        
        return "\n".join(result_lines)
    
    except Exception as e:
        return f"오류: {str(e)}"
    
# 선형 시스템 풀이 함수
def solve() :
    input_text = input_field.get("1.0", tk.END).strip()
    solve_output.delete("1.0", tk.END)
    
    try:
        matrix = [list(map(float, row.split())) for row in input_text.splitlines()]
        A = get_rows(get_columns(matrix)[:len(get_columns(matrix))-1])
        b = get_columns(matrix)[-1]
        result = solve_linear_system(A,b)
        if result == [] :
            solve_output.insert(tk.END, "해가 없습니다.")
        else :
            result_columned = get_columns(result)
            if len(result_columned) ==1 :
                solved = "\n".join(" ".join(map(lambda x: f"{x:.2f}", row)) for row in result)
            else :
                solved = format_solution(result_columned)
            solve_output.insert(tk.END, solved)
    except Exception as e:
        messagebox.showerror("오류", str(e))

def det_calculate() :
        input_text = input_field.get("1.0", tk.END).strip()
        det_output.delete("1.0", tk.END)
        
        try:
            matrix = [list(map(float, row.split())) for row in input_text.splitlines()]
            det_output.insert(tk.END, det(matrix))
        except Exception as e:
            messagebox.showerror("오류", str(e))

def inverse_calculate() :
        input_text = input_field.get("1.0", tk.END).strip()
        inverse_output.delete("1.0", tk.END)
        
        try:
            matrix = [list(map(float, row.split())) for row in input_text.splitlines()]
            inverse = getInverse(matrix)
            inverse_text = "\n".join(" ".join(map(lambda x: f"{x:.2f}", row)) for row in inverse)
            inverse_output.insert(tk.END, inverse_text)
        except Exception as e:
            messagebox.showerror("오류", str(e))


# 🖥️ GUI 생성
root = tk.Tk()
root.title("스크롤 가능한 GUI - 가운데 정렬")
root.geometry("400x400")

# 📜 메인 프레임
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# 📝 Canvas 생성
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 🛠️ Scrollbar 추가
scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 📋 Canvas와 Scrollbar 연결
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))

# 🖼️ 스크롤 가능한 Frame 생성
scrollable_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

# 🛠️ 스크롤 영역 업데이트
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)

# ✅ 가운데 정렬을 위한 Frame 생성
inner_frame = tk.Frame(scrollable_frame)
inner_frame.pack(pady=10, anchor="center")

# 🖱️ 마우스 휠 스크롤 이벤트 처리
def on_mousewheel(event):
    if root.tk.call("tk", "windowingsystem") == "aqua":  # macOS
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
    else:  # Windows, Linux
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

# 🖱️ 마우스 휠 이벤트 바인딩
canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows, Linux
canvas.bind_all("<Button-4>", on_mousewheel)    # macOS (휠 위)
canvas.bind_all("<Button-5>", on_mousewheel)    # macOS (휠 아래)


# 📝 입력 필드
tk.Label(scrollable_frame, text="행렬 입력 (줄 단위로 입력):", font=("Arial", 14)).pack(pady=5)
input_field = scrolledtext.ScrolledText(scrollable_frame, height=5, width=80, font=("Arial", 12))
input_field.pack(pady = 5)

# 🟢 선형 독립성 검사 버튼
linear_independence_button = tk.Button(
    scrollable_frame, text="선형 독립성 검사", command=check_linear_independence, font=("Arial", 14), bg="#2196F3", fg="white"
)
linear_independence_button.pack(pady = 5)

# 행렬식 풀이 버튼
determinant_button = tk.Button(
    scrollable_frame, text="행렬식 계산", command=det_calculate, font=("Arial", 14), bg="#4CAF50", fg="white"
)
determinant_button.pack(pady=5)

# 🔄 방정식
solve_button = tk.Button(
    scrollable_frame, text="선형 방정식 풀이", command=solve, font=("Arial", 14), bg="#4CAF50", fg="white"
)
solve_button.pack(pady=5)

# 🔄 가우스 소거법 실행 버튼
calculate_button = tk.Button(
    scrollable_frame, text="가우스 소거법 실행", command=calculate, font=("Arial", 14), bg="#4CAF50", fg="white"
)
calculate_button.pack(pady=5)

# 역행렬 계산 버튼
solve_button = tk.Button(
    scrollable_frame, text="역행렬 계산", command=inverse_calculate, font=("Arial", 14), bg="#4CAF50", fg="white"
)
solve_button.pack(pady=5)

# 📊 선형 독립성 검사 결과 출력
result_label = tk.Label(scrollable_frame, text="", font=("Arial", 14))
result_label.pack(pady=5)

# 📋 가우스 소거법 과정 출력
tk.Label(scrollable_frame, text="가우스 소거법 과정:", font=("Arial", 14)).pack(pady=5)
process_output = scrolledtext.ScrolledText(scrollable_frame, height=10, width=80, font=("Arial", 12), bg="#f9f9f9")
process_output.pack(pady=5)

# ✅ 최종 결과 출력
tk.Label(scrollable_frame, text="최종 결과:", font=("Arial", 14)).pack(pady=5)
result_output = scrolledtext.ScrolledText(scrollable_frame, height=5, width=80, font=("Arial", 12), bg="#e8f5e9")
result_output.pack(pady=5)

# 방정식 풀이 출력 창
tk.Label(scrollable_frame, text="일반해:", font=("Arial", 14)).pack(pady=5)
solve_output = scrolledtext.ScrolledText(scrollable_frame, height=10, width=60, font=("Arial", 12), bg="#e8f5e9")
solve_output.pack(pady=5)

# 행렬식 출력
tk.Label(scrollable_frame, text="행렬식의 값:", font=("Arial", 14)).pack(pady=5)
det_output= scrolledtext.ScrolledText(scrollable_frame, height=5, width=60, font=("Arial", 12), bg="#e8f5e9")
det_output.pack(pady=5)

# 역행렬 출력
tk.Label(scrollable_frame, text="역행렬:", font=("Arial", 14)).pack(pady=5)
inverse_output= scrolledtext.ScrolledText(scrollable_frame, height=5, width=60, font=("Arial", 12), bg="#e8f5e9")
inverse_output.pack(pady=5)

# 🖥️ GUI 실행
root.mainloop() 