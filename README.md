# YAML driven portfolio using python flask and bootstrap

This project supports creating a web based portfolio by simply updating a yaml file.

Below is a sample yaml.

```yaml
home: # Home section with background images.
  text: <h1 class="display-1 fw-bold">HIKE. BIKE. RIDE.</h1>
        <h2 class="display-5 fw-bold">On your land.</h2>
  image: static/img/home.jpg
  image_mobile: static/img/home.jpg
# Gallery section, app.py will append all images found in the paths list in addition
# to all images from sections below. Note that gallery images do not have captions.
gallery:
  justify_topics: center
  image: static/img/gallery.jpg
  image_mobile: static/img/gallery.jpg
  paths: [static/img/gallery,]
  images: []
contact: # Contact section, may require updating index.html and app.py for your application.
  justify_topics: end
  image: static/img/contact.jpg
  image_mobile: static/img/contact.jpg
sections: # List of sections along with background images.
- name: Services # Name of section displayed in a list box that scrolls over bg image.
  justify_topics: start # Position of list box.
  image: static/img/services.jpg # Background images.
  image_mobile: static/img/services.jpg
  tag: services # Used within index.html, must not contain spaces.
  # Each section has a list of topics with associated directories.
  # Within each directory can be multiple images and associated captions.
  # e.g., image1.jpg and image1.txt, alpha-numeric ordered.
  topics:
  - name: Trail Construction
    path: static/img/services/construction
  - name: Trail Consulting
    path: static/img/services/consulting
  - name: Trail Repairs
    path: static/img/services/repairs
  - name: Small Projects
    path: static/img/services/projects
- name: About Me
  justify_topics: end
  image: static/img/abouts.jpg
  image_mobile: static/img/abouts.jpg
  tag: abouts
  topics:
  - name: Background
    path: static/img/abouts/background
  - name: Experience
    path: static/img/abouts/experience
  - name: Tools
    path: static/img/abouts/tools
```
