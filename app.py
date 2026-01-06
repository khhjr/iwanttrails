import os, random, yaml, datetime
from flask import Flask, render_template, request, redirect, url_for, flash


debug = True
def log(d):
    if debug:
        print(d)


def is_image(i):
    return i.lower().endswith("jpg") or i.lower().endswith("jpeg")


def write_forms(d):
    forms = os.path.join(home, "forms")
    with open(forms, "a") as f:
        f.write(d)


home = os.path.dirname(__file__)
yaml_file = os.path.join(home, "config.yml")
with open(yaml_file, "r") as f:
    config = yaml.load(f.read(), Loader=yaml.Loader)
flask_key = os.getenv("FLASK_KEY", "this is the flask key")
check_password = os.getenv("CHECK_PASSWORD", "")


app = Flask(__name__)
app.secret_key = flask_key

sections = []
gallery_images = []
for section in config["sections"]:
    if section["name"] == "Gallery":
        gallery = section
        continue
    tmp = []
    if not section["topics"]:
        continue
    for topic in section["topics"]:
        if not os.path.isdir(topic["path"]):
            continue
        images = []
        for fname in os.listdir(topic["path"]):
            log(fname)
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
                ign = image_path.split(".")[0] + ".ign"
                if not os.path.exists(ign):
                    desc = ""
                    if debug:
                        desc = fname
                    gallery_images.append({"path": image_path, "desc": desc})
        topic.setdefault("tag", topic["path"].split(os.sep)[-1])
        topic.setdefault("images", images)
        log(topic)

for path in gallery["paths"]:
    for fname in os.listdir(path):
        log(fname)
        if is_image(fname):
            image_path = os.path.join(path, fname)
            desc = ""
            if debug:
                desc = fname
            gallery_images.append({"path": image_path, "desc": desc})
random.shuffle(gallery_images)
gallery.setdefault("topics", [{"name": "Gallery", "tag": "gallery", "images": gallery_images}])

log(config)

@app.route("/")
def index():
    return render_template("index.html", config=config)

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    write_forms(f"\n----\n{ts}\n{name}\n{email}\n{phone}\n{message}\n----\n")
    return {"status": "success"}

@app.route("/check_messages")
def check_messages():
    password = request.args.get("password")

    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    write_forms(f"\n++++\n{ts}\n{password}\n\+++++\n")
    if check_password and (password == check_password):
        forms = os.path.join(home, "forms")
        with open(forms, "r") as f:
            data = f.read().splitlines()
        return render_template("check_messages.html", data=data)
    else:
        return "Access denied", 403

if __name__ == '__main__':
    app.run(debug=True)

