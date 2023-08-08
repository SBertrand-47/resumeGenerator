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
    print(request.form)
    # Get the list of education periods
    education_periods = [
        f"{start} - {end}"
        for start, end in zip(request.form.getlist('start_date'), request.form.getlist('end_date'))
    ]

    # Get the list of GPAs
    gpas = request.form.getlist('gpa')

    # Get the list of relevant courses
    courses = request.form.getlist('courses')

    # Get the list of experience periods
    experience_periods = [
        f"{start} - {end}"
        for start, end in zip(request.form.getlist('job_start_date'), request.form.getlist('job_end_date'))
    ]

    data = {
        'name': request.form.get('name', 'default'),
        'location': request.form.get('location', 'default'),
        'email': request.form.get('email', 'default'),
        'phone': request.form.get('phone', 'default'),
        'github': request.form.get('github', None),
        'portfolio': request.form.get('portfolio', None),
        'majors': request.form.getlist('major'),
        'universities': request.form.getlist('university'),
        'education_periods': education_periods,
        'gpas': gpas, # Added GPAs
        'courses': courses, # Added relevant courses
        'skills': request.form.get('skills', 'default'),
        'roles': request.form.getlist('role'),
        'companies': request.form.getlist('company'),
        'experience_periods': experience_periods,
        'job_descriptions': request.form.getlist('job-description'),
        'project_names': request.form.getlist('project_names[]'),
        'project_urls': request.form.getlist('project_urls[]'),
        'project_descriptions': request.form.getlist('project_descriptions[]'),
        'award_titles': request.form.getlist('award_title[]'),
        'award_descriptions': request.form.getlist('award_description[]'),
    }

    print(data)
    print(request.form.getlist('start_date'))
    print(request.form.getlist('end_date'))

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
