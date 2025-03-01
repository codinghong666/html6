from flask import Flask, render_template, request, jsonify
import sympy as sp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
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
        

        return render_template('index.html', result=transposed_matrix, latexmatrix=latexmatrix)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
print(11111)