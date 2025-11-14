import os, re
from flask import Flask, render_template

app = Flask(__name__)

static_dir = "./static"
projects_dir = "./img/projects"
projects = []
for project in [d.name for d in os.scandir(os.path.join(static_dir, projects_dir))]:
    if not os.path.isdir(os.path.join(static_dir, projects_dir, project)):
        continue
    desc = "Project default description"
    top_image = "default.jpg"
    images = []
    for n in os.listdir(os.path.join(static_dir, projects_dir, project)):
        image_path = os.path.join(projects_dir, project, n)
        if n == "description":
            with open(os.path.join(static_dir, projects_dir, project, n), "r") as f:
                desc = f.read()
        elif n == "top.jpg":
            top_image = image_path
        else:
            images.append(image_path)
    projects.append({"name": project, "description": desc, "top_image": top_image, "images": images})
print(projects)

@app.route('/')
def index():
    return render_template('index.html', data=projects)

if __name__ == '__main__':
    app.run(debug=True)

