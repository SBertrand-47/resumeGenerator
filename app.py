from flask import Flask, render_template, request, send_file
import pdfcrowd
import tempfile

app = Flask(__name__)

app.jinja_env.globals.update(zip=zip)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = {
        'name': request.form.get('name', 'default'),
        'location': request.form.get('location', 'default'),
        'email': request.form.get('email', 'default'),
        'phone': request.form.get('phone', 'default'),
        'github': request.form.get('github', 'default'),
        'major': request.form.get('major', 'default'),
        'university': request.form.get('university', 'default'),
        'period': request.form.get('period', 'default'),
        'skills': request.form.get('skills', 'default'),
        'roles': request.form.get('role', 'default'),
        'companies': request.form.get('company', 'default'),
        'experience_periods': request.form.get('experience_period', 'default'),
        'descriptions': request.form.get('description', 'default'),
        'project_names': request.form.get('project_name', 'default'),
        'project_descriptions': request.form.get('project_description', 'default'),
        'awards': request.form.get('awards', 'default'),
    }

    # Render the HTML as usual but as a string
    rendered = render_template('resume.html', **data)

    # Create a Pdfcrowd API client instance
    client = pdfcrowd.HtmlToPdfClient('mr47', '23f23109334517f141f7494c8132ecc0')

    # Set the page margins (top, right, bottom, left) in points
    client.setPageMargins("2pt", "2pt", "2pt", "2pt")

    # Use HTTP instead of HTTPS
    client.setUseHttp(True)

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
