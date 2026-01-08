import os, random, yaml
from datetime import datetime, timezone
from flask import Flask, render_template, request


debug = os.getenv("WEB_DEBUG")
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
messages_password = os.getenv("MESSAGES_PASSWORD", "")


app = Flask(__name__)
app.secret_key = flask_key

sections = []
gallery_images = []
for section in config["sections"]:
    if section["name"] == "Gallery":
        gallery = section
        continue
    if section["name"] == "Videos":
        videos = section
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

with open(videos["path"], "r") as f:
    videos_config = yaml.load(f.read(), Loader=yaml.Loader)
log(videos_config)
videos.setdefault("topics", [{"name": "Videos", "tag": "videos", "videos": videos_config}])

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
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    write_forms(f"\nmessage\n{ts}\n{name}\n{email}\n{phone}\n{message}\n----\n")
    return {"status": "success"}

@app.route("/get_messages")
def get_messages():
    password = request.args.get("password")
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    write_forms(f"\nget_message\n{ts}\n{password}\n++++\n")
    if messages_password and (password == messages_password):
        forms = os.path.join(home, "forms")
        with open(forms, "r") as f:
            data = f.read().splitlines()
        return render_template("get_messages.html", data=data)
    else:
        return "Access denied", 403

if __name__ == '__main__':
    app.run(debug=True)

