from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('Developer Portfolio')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'Project {self.id}: {self.title}'

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/add', methods=['POST'])
def add_project():
    title = request.form['title']
    link = request.form['link']
    new_project = Project(title=title, link=link)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear_projects():
    try:
        Project.query.delete()
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return str(e), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)