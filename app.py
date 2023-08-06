from flask import Flask, render_template, request, send_file
import tempfile
import pdfcrowd

app = Flask(__name__)

app.jinja_env.globals.update(zip=zip)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = {
        'name': request.form.get('name'),
        'location': request.form.get('location'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'github': request.form.get('github'),
        'major': request.form.get('major'),
        'university': request.form.get('university'),
        'period': request.form.get('period'),
        'skills': request.form.get('skills'),
        'roles': request.form.get('role'),
        'companies': request.form.get('company'),
        'experience_periods': request.form.get('experience_period'),
        'descriptions': request.form.get('description'),
        'project_names': request.form.get('project_name'),
        'project_descriptions': request.form.get('project_description'),
        'awards': request.form.get('awards'),
    }

    # Render the HTML as usual but as a string
    rendered = render_template('resume.html', **data)

    # Create a Pdfcrowd API client instance
    client = pdfcrowd.HtmlToPdfClient('mr47', '23f23109334517f141f7494c8132ecc0')

    # Set the page margins (top, right, bottom, left) in points
    client.setPageMargins("2pt", "2pt", "2pt", "2pt")


    # Convert HTML string to a PDF
    pdf = client.convertString(rendered)

    # Create a temporary file to save the PDF
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_file.write(pdf)
    pdf_file.close()

    # Send the PDF file as a response
    return send_file(pdf_file.name, mimetype='application/pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
