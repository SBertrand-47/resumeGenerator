from flask import Flask, render_template, request, send_file
import pdfcrowd
import tempfile
import csv

app = Flask(__name__)

app.jinja_env.globals.update(zip=zip)

@app.route('/')
def home():
    return render_template('home.html')


def save_to_csv(data):
    # Define CSV file name
    csv_file = "users_data.csv"

    # Check if the file already exists to determine if we need to write headers
    file_exists = False
    try:
        with open(csv_file, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    # Open the CSV file in append mode and write data
    with open(csv_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "university", "email"])

        if not file_exists:
            writer.writeheader()

        # Extract data from the input data
        for major, university in zip(data["majors"], data["universities"]):
            writer.writerow({
                "name": data["name"],
                "university": university,
                "email": data["email"]
            })


@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    no_experience = request.form.get('noExperience') == 'on'

    if no_experience:
        # Set default or empty values for experience-related fields
        roles = []
        companies = []
        experience_periods = []
        job_descriptions = []
    else:
        roles = request.form.getlist('role')
        companies = request.form.getlist('company')
        job_start_dates = request.form.getlist('job_start_date')
        job_end_dates_hidden = request.form.getlist('job_end_date_hidden')
        job_end_dates_visible = request.form.getlist('job_end_date_visible')

        experience_periods = []
        for i, (start, end_hidden) in enumerate(zip(job_start_dates, job_end_dates_hidden)):
            # Check if both start and end_hidden have valid values
            if start.strip() and (end_hidden.strip() and end_hidden != "-"):
                if end_hidden == "Present":
                    experience_periods.append(f"{start} - Present")
                else:
                    end_visible = job_end_dates_visible[i] if i < len(job_end_dates_visible) else end_hidden
                    if end_visible.strip() and end_visible != "-":  # Also ensure end_visible has a valid value
                        experience_periods.append(f"{start} - {end_visible}")

        job_descriptions = request.form.getlist('job-description')

    # Get the list of education periods
    education_periods = [
        f"{start} - {end}"
        for start, end in zip(request.form.getlist('start_date'), request.form.getlist('end_date'))
    ]

    # Handling the exclusion of GPAs
    education_ids = request.form.getlist('education_ids[]')
    gpas = []
    for edu_id in education_ids:
        gpa = request.form.get(f'gpa_{edu_id}')
        exclude_gpa = request.form.get(f'exclude_gpa_{edu_id}')

        if not gpa or exclude_gpa == 'on':
            gpas.append(None)
        else:
            gpas.append(gpa)

    while len(gpas) < len(request.form.getlist('major')):
        gpas.append(None)

    courses = request.form.getlist('courses')

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
        'gpas': gpas,
        'courses': courses,
        'skills': request.form.get('skills', 'default'),
        'roles': roles,
        'companies': companies,
        'experience_periods': experience_periods,
        'job_descriptions': job_descriptions,
        'project_names': request.form.getlist('project_names[]'),
        'project_urls': request.form.getlist('project_urls[]'),
        'project_descriptions': request.form.getlist('project_descriptions[]'),
        'award_titles': request.form.getlist('award_title[]'),
        'award_descriptions': request.form.getlist('award_description[]'),
    }

    save_to_csv(data)



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
