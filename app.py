from flask import Flask, render_template, request, jsonify
import sympy as sp
import os
import uuid
import sympy as sp
import ast 
import subprocess
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
        # Convert the matrix to a SymPy matrix (though we store strings, SymPy can handle symbolic matrices)
        latexmatrix = sp.latex(matrix)
        
        transposed_matrix =sp.latex(matrix.T)
        

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
        output_list = ast.literal_eval(output)
        m=sp.Matrix(output_list)
        output_latex=sp.latex(m)
        error = result.stderr
    except Exception as e:
        output = ""
        error = str(e)
    finally:
        # 执行完毕后删除临时文件
        if os.path.exists(filename):
            os.remove(filename)
    
    # 返回执行结果给前端
    return jsonify({"output": output_latex, "error": error})
if __name__ == '__main__':
    app.run(debug=True)