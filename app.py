from flask import Flask, render_template

app = Flask(__name__)
JOBS = [
  {
    'id': 1,
    'title': 'Financial Analyst',
    'location': 'Nairobi, Kenya',
    'salary': 'KES. 9000,000'},
  {
    'id': 2,
    'title': 'Data Scientist',
    'location': 'Bengaluru, India',
    'salary': 'KES. 3,000,000'},
  {
    'id': 3,
    'title': 'Commercial Analyst',
    'location': 'New York, USA',
    'salary': 'USD. 100,000'},
  {
    'id': 4,
    'title': 'Backend Engineer',
    'location': 'Bengaluru, India',
    'salary': 'Rs. 1,000,000'
  }
]
@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS, company_name='Tush')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True) 