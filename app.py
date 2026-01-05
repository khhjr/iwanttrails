import os, yaml
from flask import Flask, render_template, request, redirect, url_for, flash

debug = True

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
            if debug:
                print(fname)
            if fname.lower().endswith("jpg") or fname.lower().endswith("jpeg"):
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
        if debug:
            print(topic)
if debug:
    print(config)

@app.route("/")
def index():
    return render_template('index.html', config=config)

def is_valid_email(email):
    return "@" in parseaddr(email)[1]

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")

    # Example: print or save data
    with open("forms", "a") as f:
        f.write(f"{name}\n{email}\n{phone}\n{message}\n----\n")

    return {"status": "success"}



if __name__ == '__main__':
    app.run(debug=True)

