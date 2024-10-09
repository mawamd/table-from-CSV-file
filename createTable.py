import streamlit as st
import pandas as pd
import random
import io
import streamlit.components.v1 as components  # Correct import for components

# Function to create the scrambled drag-and-drop table
def create_scrambled_drag_and_drop_html(csv_data):
    data = pd.read_csv(io.StringIO(csv_data), header=None)
    data = data.fillna('')  # Fill NaN values with empty string
    data = data.loc[:, (data != '').any(axis=1)]  # Remove empty columns
    rows, cols = data.shape
    
    # Extract and scramble cell values
    all_values = data.values.flatten().tolist()
    random.shuffle(all_values)
    
    # Generate HTML with updated styles for drag-and-drop functionality
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scrambled Drag and Drop Table</title>
        <style>
            body {
                background-color: #FFFFFF;
                color: black;
                font-family: Arial, sans-serif;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            td {
                border: 1px solid black;
                padding: 10px;
                text-align: center;
                width: 25%;
                vertical-align: top;
                background-color: #F0F2F6;  /* Secondary background color for table cells */
            }
            .draggable {
                cursor: move;
                padding: 5px;
                border: 1px solid #000;
                background-color: #F0F2F6;  /* Secondary background color for draggable items */
                display: inline-block;
                margin-bottom: 5px;
            }
        </style>
    </head>
    <body>
        <h2>Scrambled Drag and Drop Table</h2>
        <table>
    '''
    
    # Create table rows and columns dynamically based on CSV data
    for i in range(rows):
        html_content += "<tr>"
        for j in range(cols):
            cell_id = f"r{i}_c{j}"
            correct_value = data.iloc[i, j]
            # Add correct value as a data attribute and leave the cell empty for drag-and-drop
            html_content += f'<td id="{cell_id}" data-correct="{correct_value}" ondrop="drop(event)" ondragover="allowDrop(event)"></td>'
        html_content += "</tr>"
    
    html_content += '''
        </table>
        <br>
        <div id="data">
    '''
    
    # Generate draggable items based on the scrambled content
    for idx, cell_value in enumerate(all_values):
        draggable_id = f"item_{idx}"
        html_content += f'<div id="{draggable_id}" class="draggable" draggable="true" ondragstart="drag(event)">{cell_value}</div>\n'

    # End of HTML content with JavaScript for drag-and-drop
    html_content += '''
        </div>
        <script>
            function allowDrop(ev) {
                ev.preventDefault();
            }

            function drag(ev) {
                ev.dataTransfer.setData("text", ev.target.id);
            }

            function drop(ev) {
                ev.preventDefault();
                var data = ev.dataTransfer.getData("text");
                var draggedElement = document.getElementById(data);
                var droppedCell = ev.target;

                // Get the correct value from the cell's data attribute
                var correctValue = droppedCell.getAttribute("data-correct");

                // Check if the dropped value matches the correct value
                if (draggedElement.innerText === correctValue) {
                    // Correct match: append to the cell
                    droppedCell.innerText = draggedElement.innerText;
                    draggedElement.style.display = 'none';  // Hide the dragged element
                } else {
                    // Incorrect match: alert the user and do nothing
                    alert("Incorrect! Try again.");
                }
            }
        </script>
    </body>
    </html>
    '''
    
    return html_content

# Streamlit interface
st.title("Upload CSV to Generate Blank Table")
st.markdown("#### Created by Michael Wassef")

# Add blank space
st.write("")
st.write("")

# Upload CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read uploaded CSV file into memory
    csv_data = uploaded_file.getvalue().decode("utf-8")
    
    # Display the uploaded CSV for preview
    st.write("Uploaded CSV:")
    df = pd.read_csv(io.StringIO(csv_data))
    st.dataframe(df)
    
    # When the user clicks the button, generate scrambled HTML table
    if st.button("Scramble and Generate Table"):
        scrambled_html = create_scrambled_drag_and_drop_html(csv_data)
        
        # Render the generated HTML in Streamlit
        components.html(scrambled_html, height=800, scrolling=True)
