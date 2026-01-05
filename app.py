import os, random, yaml
from flask import Flask, render_template, request, redirect, url_for, flash


debug = True
def debug(d):
    if debug:
        print(d)


def is_image(i):
    return i.lower().endswith("jpg") or i.lower().endswith("jpeg")


app = Flask(__name__)
app.secret_key = "change_this_secret_key"

with open("config.yml", "r") as f:
    config = yaml.load(f.read(), Loader=yaml.Loader)

sections = []
for section in config["sections"]:
    tmp = []
    if not section["topics"]:
        continue
    for topic in section["topics"]:
        if not os.path.isdir(topic["path"]):
            continue
        images = []
        for fname in os.listdir(topic["path"]):
            debug(fname)
            if is_image(fname):
                image_path = os.path.join(topic["path"], fname)
                txt = image_path.split(".")[0] + ".txt"
                desc = ""
                if debug:
                    desc = fname
                if os.path.exists(txt):
                    with open(txt, "r") as f:
                        desc = f.read()
                images.append({"path": image_path, "desc": desc})
                config["gallery"]["images"].append(image_path)
        topic.setdefault("tag", topic["path"].split(os.sep)[-1])
        topic.setdefault("images", images)
        debug(topic)

for path in config["gallery"]["paths"]:
    for fname in os.listdir(path):
        debug(fname)
        if is_image(fname):
            config["gallery"]["images"].append(os.path.join(path, fname))
random.shuffle(config["gallery"]["images"])

debug(config)

@app.route("/")
def index():
    return render_template('index.html', config=config)

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")

    with open("forms", "a") as f:
        f.write(f"{name}\n{email}\n{phone}\n{message}\n----\n")

    return {"status": "success"}


if __name__ == '__main__':
    app.run(debug=True)

