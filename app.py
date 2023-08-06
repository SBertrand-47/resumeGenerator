from flask import Flask, render_template, request, make_response
from flask_weasyprint import HTML, render_pdf

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    # Get form data
    data = {
        'name': request.form.get('name'),
        'location': request.form.get('location'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'linkedin': request.form.get('linkedin'),
        'portfolio': request.form.get('portfolio'),
        'education': request.form.get('education'),
        'skills': request.form.get('skills'),
        'experience': request.form.get('experience'),
        'projects': request.form.get('projects'),
        'awards': request.form.get('awards')
    }

    # Render the resume.html template with the form data
    html = render_template('resume.html', **data)

    # Convert the HTML to a PDF
    pdf = HTML(string=html).write_pdf()

    # Create a response with the PDF data
    response = make_response(pdf)
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='resume.pdf')

    return response

if __name__ == "__main__":
    app.run(debug=True)
