from flask import Flask, render_template, jsonify

app = Flask(__name__)
JOBS = [{
    'id': 1,
    'title': 'Financial Analyst',
    'location': 'Nairobi, Kenya',
    'salary': 'KES. 9000,000'
}, {
    'id': 2,
    'title': 'Data Scientist',
    'location': 'Cairo, Egypt',
    'salary': 'USD. 10,000'
}, {
    'id': 3,
    'title': 'Commercial Analyst',
    'location': 'New York, USA',
    'salary': 'USD. 100,000'
}, {
    'id': 4,
    'title': 'Backend Engineer',
    'location': 'Cape Town, South Africa',
    'salary': 'Rand. 1,000,000'
}]


@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS, company_name='Kratos')


@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
