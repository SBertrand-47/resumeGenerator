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

    # Handling the exclusion of GPAs
    education_ids = request.form.getlist('education_ids[]')  # Fetch the education IDs

    gpas = []
    for edu_id in education_ids:
        # Fetch the GPA and its exclusion flag using the education ID
        gpa = request.form.get(f'gpa_{edu_id}')
        exclude_gpa = request.form.get(f'exclude_gpa_{edu_id}')  # This will return 'on' if checked, and None otherwise

        if not gpa:  # Check for empty GPA fields
            gpas.append(None)
        elif exclude_gpa == 'on':
            gpas.append(None)
        else:
            gpas.append(gpa)

    print("Processed GPAs:", gpas)

    # Ensure the `gpas` list has the same length as other lists, like 'majors'
    while len(gpas) < len(request.form.getlist('major')):
        gpas.append(None)  # This appends None for any additional majors without GPA data.

    print("Final GPAs:", gpas)

    # ... rest of the code


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
        'gpas': gpas,  # Updated GPAs with potential exclusions
        'courses': courses,
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
    client = pdfcrowd.HtmlToPdfClient('eduard25', '8dd4fd2eb74244424a3e598b70fca921')

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
