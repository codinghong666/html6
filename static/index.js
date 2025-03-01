// Generate the matrix input fields dynamically based on the row and column input
function generateMatrix() {
    const rows = document.getElementById("rows").value;
    const cols = document.getElementById("cols").value;

    // Set hidden fields for the POST request
    document.getElementById("hidden-rows").value = rows;
    document.getElementById("hidden-cols").value = cols;

    // Clear previous matrix inputs
    const matrixInputs = document.getElementById("matrix-inputs");
    matrixInputs.innerHTML = '';

    // Generate the input fields for the matrix
    for (let i = 0; i < rows; i++) {
        let rowDiv = document.createElement('div');
        rowDiv.classList.add('row');
        for (let j = 0; j < cols; j++) {
            let input = document.createElement('input');
            input.type = 'text';  // Allow text input (letters, symbols, etc.)
            input.name = `matrix_${i}_${j}`;
            input.classList.add('matrix-input');
            input.placeholder = `元素 (${i+1},${j+1})`;
            rowDiv.appendChild(input);
        }
        matrixInputs.appendChild(rowDiv);
    }

    // Show the matrix input section
    document.getElementById("matrix-container").style.display = 'block';
}

// Submit the matrix and display results (LaTeX matrix and transposed matrix)
function submitMatrix() {
    const matrixForm = document.getElementById("matrix-form");
    const formData = new FormData(matrixForm);

    fetch(window.location.href, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display result: Transposed Matrix and LaTeX representation
        let resultDiv = document.getElementById("result");

        if (data.result) {
            resultDiv.innerHTML = `<h3>转置矩阵:</h3><pre>${data.result}</pre>`;
        }

        if (data.latexmatrix) {
            resultDiv.innerHTML += `<h3>矩阵 (LaTeX):</h3><p>$$ ${data.latexmatrix} $$</p>`;
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);  // Re-render the LaTeX
        }
    })
    .catch(error => console.error("Error:", error));
}
