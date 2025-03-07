# from flask import Flask, render_template, request, jsonify
# import sympy as sp
# import os
# import uuid
# import sympy as sp
# import ast 
# import subprocess
# import base64
# import shutil
# from sympy.parsing.latex import parse_latex
# import time


# class timer:
#     def __init__(self):
#         self.start = time.time()

#     def end(self):
#         print("%.2f" % (time.time() - self.start), end="s\n")
# app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template('index.html')
# @app.route('/handinput', methods=['GET', 'POST'])
# def handinput():
#     if request.method == 'POST':
#         rows = int(request.form.get('rows'))
#         cols = int(request.form.get('cols'))
        
#         matrix = []
#         for i in range(rows):
#             row = []
#             for j in range(cols):
#                 value = request.form.get(f'matrix_{i}_{j}')
#                 if value:
#                     row.append(value)  # Store as string for alphabetic characters
#                 else:
#                     return jsonify({'error': f'矩阵元素 ({i},{j}) 缺失'}), 400
#             matrix.append(row)
#         matrix=sp.Matrix(matrix)
#         # Convert the matrix to a SymPy matrix (though we store strings, SymPy can handle symbolic matrices)
#         latexmatrix = sp.latex(matrix)
        
#         transposed_matrix =sp.latex(matrix.T)
        

#         return render_template('handinput.html', result=transposed_matrix, latexmatrix=latexmatrix)

#     return render_template('handinput.html')
# @app.route('/codeinput')
# def codeinput():
#     return render_template('codeinput.html')

# @app.route('/run', methods=['POST'])
# def run_code():
#     data = request.get_json()
#     code = data.get("code", "")
    
#     # 生成唯一的文件名，避免冲突
#     filename = f'temp_{uuid.uuid4().hex}.py'
    
#     # 将用户输入的代码保存到文件中
#     with open(filename, 'w', encoding='utf-8') as f:
#         f.write(code)
    
#     try:
#         # 使用 subprocess 运行刚保存的 Python 文件
#         result = subprocess.run(
#             ['python3', filename],
#             capture_output=True,
#             text=True,
#             timeout=10  # 限制运行时间，防止长时间运行
#         )
#         output = result.stdout.strip()
#         output_list = ast.literal_eval(output)
#         m=sp.Matrix(output_list)
#         output_latex=sp.latex(m)
#         error = result.stderr
#     except Exception as e:
#         output = ""
#         error = str(e)
#     finally:
#         # 执行完毕后删除临时文件
#         if os.path.exists(filename):
#             os.remove(filename)

    
#     # 返回执行结果给前端
#     return jsonify({"output": output_latex, "error": error})

# @app.route('/integrate', methods=['GET', 'POST'])
# def integrate():
#     if request.method == 'POST':
#         data = request.get_json()
#         expression = data.get("expression")
#         variable = data.get("variable")
#         try:
#             # 使用 Sympy 解析 LaTeX 表达式
#             parsed_expr = parse_latex(expression)
#             # 检查变量字符串是否包含积分上下界（例如 "x 0 1"）
#             bk = variable.split(" ")
#             if len(bk) == 3:
#                 # 第一个部分作为变量
#                 var = sp.symbols(bk[0])
#                 # 将下界和上界转化为数字或符号表达式
#                 lower = sp.sympify(bk[1])
#                 upper = sp.sympify(bk[2])
#                 # 计算定积分
#                 integral = sp.integrate(parsed_expr, (var, lower, upper))
#                 # 格式化积分区间的 LaTeX 表示（例如 _{0}^{1} ）
#                 rg = '_{' + sp.latex(lower) + '}^{' + sp.latex(upper) + '}'
#             else:
#                 # 只有变量，没有积分上下界，计算不定积分
#                 var = sp.symbols(variable)
#                 integral = sp.integrate(parsed_expr, var)
#                 rg = ''
#             # 对结果进行化简和约分
#             integral = sp.simplify(integral)
#             integral = sp.cancel(integral)
#             # 生成 LaTeX 格式的积分结果
#             result = r'\int' + rg + expression + '=' + sp.latex(integral)
#             return jsonify({"result": result})
#         except Exception as e:
#             return jsonify({"error": str(e)})
#     return render_template('integrate.html')
# @app.route('/handwritten', methods=['GET', 'POST'])
# def handwritten():
#     if request.method == 'GET':
#         # 返回包含手写输入画布的 HTML 页面
#         return render_template('handwritten.html')
#     if request.method == 'POST':
#         # 以下为 POST 请求，处理图像数据
#         data = request.get_json()
#         image_data = data.get("image")

#         if not image_data:
#             return jsonify({"error": "No image data received"}), 400

#         # 解析 base64 数据并转换为图片
#         image_data = image_data.split(",")[1]  # 移除 'data:image/png;base64,' 前缀
#         image_bytes = base64.b64decode(image_data)
        
#         folder_path = '/Users/coding_hong/Documents/code/html/html6/texteller/TexTeller/src'
#         image_filename = f"handwritten_math.png"
#         image_path = os.path.join(folder_path, image_filename)
        
#         # 将图片写入指定文件夹
#         try:
#             with open(image_path, "wb") as img_file:
#                 img_file.write(image_bytes)
#             print("图片已保存到：", image_path)
#         except Exception as e:
#             return jsonify({"error": f"保存图片出错: {str(e)}"}), 500
#         print(image_path)
#         folder_path = '/Users/coding_hong/Documents/code/html/html6/texteller/TexTeller/src'  # 请替换为你的目标文件夹路径
        
#         # target_path = os.path.join(folder_path, os.path.basename(image_path))
#         # shutil.copy(image_path, target_path)

#         command = 'python inference.py -img '+'"'+image_filename+'" --inference-mode mps'
#         print(command)
#         try:
#             T=timer()
#             print("in")
#             result = subprocess.run(command, shell=True, cwd=folder_path, capture_output=True, text=True)
#             print("Command output:")
#             print(result.stdout)  # 打印命令的标准输出
#             if result.stderr:
#                 print("Command error:")
#                 print(result.stderr)  # 打印命令的标准错误
#         except Exception as e:
#             print(f"Error occurred: {e}")
#         latex_content = ""
#         output_file = os.path.join(folder_path, "output.txt")
#         if os.path.exists(output_file):
#             with open(output_file, "r", encoding="utf-8") as f:
#                 latex_content = f.read().strip()
#         T.end()
#         return jsonify({"latex": latex_content})

    
# if __name__ == '__main__':
#     app.run(debug=True,port=8080)




from flask import Flask, render_template, request, jsonify
import sympy as sp
import os
import uuid
import sympy as sp
import ast 
import subprocess
import base64
import shutil
import subprocess
import webbrowser
import threading
from sympy.parsing.latex import parse_latex
import time


class timer:
    def __init__(self):
        self.start = time.time()

    def end(self):
        print("%.2f" % (time.time() - self.start), end="s\n")
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/handinput', methods=['GET', 'POST'])
def handinput():
    if request.method == 'POST':
        rows = int(request.form.get('rows'))
        cols = int(request.form.get('cols'))
        
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                value = request.form.get(f'matrix_{i}_{j}')
                if value:
                    row.append(value)  # Store as string for alphabetic characters
                else:
                    return jsonify({'error': f'矩阵元素 ({i},{j}) 缺失'}), 400
            matrix.append(row)
        matrix=sp.Matrix(matrix)
        latexmatrix = sp.latex(matrix)
        transposed_matrix =sp.latex(matrix.T)
        if matrix.shape[0] == matrix.shape[1]:
            determinant = sp.latex(matrix.det())
            if matrix.det()!=0:
                inverse = sp.latex(matrix.inv())
                return render_template('handinput.html', result=transposed_matrix, latexmatrix=latexmatrix,determinant=determinant,inverse=inverse)
        else:
            return render_template('handinput.html', result=transposed_matrix, latexmatrix=latexmatrix)
    return render_template('handinput.html')


@app.route('/codeinput')
def codeinput():
    return render_template('codeinput.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    
    # 生成唯一的文件名，避免冲突
    filename = f'temp_{uuid.uuid4().hex}.py'
    
    # 将用户输入的代码保存到文件中
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)
    
    try:
        # 使用 subprocess 运行刚保存的 Python 文件
        result = subprocess.run(
            ['python3', filename],
            capture_output=True,
            text=True,
            timeout=10  # 限制运行时间，防止长时间运行
        )
        output = result.stdout.strip()
        # print(output)
        output_list = ast.literal_eval(output)
        m=sp.Matrix(output_list)
        output_latex=sp.latex(m)
        transposed_matrix =sp.latex(m.T)
        error = result.stderr
    except Exception as e:
        output = ""
        error = str(e)
    # finally:
    #     # 执行完毕后删除临时文件
    #     if os.path.exists(filename):
    #         os.remove(filename)

    
    # 返回执行结果给前端
    if m.shape[0] == m.shape[1]:
        determinant = sp.latex(m.det())
        if m.det()!=0:
            inverse = sp.latex(m.inv())
            return jsonify({"output": output_latex, "error": error,"transposed":transposed_matrix,"determinant":determinant,"inverse":inverse})
        else:
            return jsonify({"output": output_latex, "error": error,"transposed":transposed_matrix,"determinant":determinant})
    else:
        return jsonify({"output": output_latex, "error": error,"transposed":transposed_matrix})

@app.route('/integrate', methods=['GET', 'POST'])
def integrate():
    if request.method == 'POST':
        data = request.get_json()
        expression = data.get("expression")
        variable = data.get("variable")
        try:
            # 使用 Sympy 解析 LaTeX 表达式
            parsed_expr = parse_latex(expression)
            # 检查变量字符串是否包含积分上下界（例如 "x 0 1"）
            bk = variable.split(" ")
            if len(bk) == 3:
                # 第一个部分作为变量
                var = sp.symbols(bk[0])
                # 将下界和上界转化为数字或符号表达式
                lower = sp.sympify(bk[1])
                upper = sp.sympify(bk[2])
                # 计算定积分
                integral = sp.integrate(parsed_expr, (var, lower, upper))
                # 格式化积分区间的 LaTeX 表示（例如 _{0}^{1} ）
                rg = '_{' + sp.latex(lower) + '}^{' + sp.latex(upper) + '}'
            else:
                # 只有变量，没有积分上下界，计算不定积分
                var = sp.symbols(variable)
                integral = sp.integrate(parsed_expr, var)
                rg = ''
            # 对结果进行化简和约分
            integral = sp.simplify(integral)
            integral = sp.cancel(integral)
            # 生成 LaTeX 格式的积分结果
            result = r'\int' + rg + expression + '=' + sp.latex(integral)
            return jsonify({"result": result})
        except Exception as e:
            return jsonify({"error": str(e)})
    return render_template('integrate.html')

def run_streamlit():
    """ 启动 Streamlit 应用 """
    subprocess.run(["streamlit", "run", "texteller/TexTeller/src/web.py"], check=True)

@app.route('/handwritten', methods=['GET'])
def handwritten():
    # 运行 Streamlit
    # threading.Thread(target=run_streamlit, daemon=True).start()
    
    # # 等待 Streamlit 启动
    # time.sleep(3)
    
    # # 打开 Streamlit 网页
    # webbrowser.open("http://localhost:8501")

    # return "Streamlit handwriting recognition page is opening..."


    #         folder_path = '/Users/coding_hong/Documents/code/html/html6/texteller/TexTeller/src'  # 请替换为你的目标文件夹路径
        
        # target_path = os.path.join(folder_path, os.path.basename(image_path))
        # shutil.copy(image_path, target_path)
    folder_path = '/Users/coding_hong/Documents/code/html/html6/texteller/TexTeller/src'
    command = './start_web.sh'
    print(command)
    # try:
    # T=timer()
    print("in")
    result = subprocess.run(command, shell=True, cwd=folder_path, capture_output=True, text=True)
    # except:


    
if __name__ == '__main__':
    app.run(debug=True,port=8080)