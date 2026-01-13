# YAML driven portfolio

This project supports creating a web based portfolio by simply updating a yaml file.

The basic layout is shown below. Section and topic attributes are defined within the yaml file.
Images and captions are derived from directory contents specified in the yaml. Once you have
the basic stuff working, you can simply add additional images and captions to the working
directory and restart the web server. This makes updating and maintaining the portfolio
extremely easy.

```
NAVBAR (requires updating index.html)

Home (Title) Section

# Configurable Sections (including Gallery and Videos)
  Section 1
    Topic a
       Image i with optional caption
       Image ii with optional caption
       Image iii with optional caption
       ...
    Topic b
       Image i with caption
       Image ii with caption
       Image iii with caption
       ...
    Topic c
       Image i with caption
       Image ii with caption
       Image iii with caption
       ...
  Section 2
    Topic a
       Image i with caption
       Image ii with caption
       Image iii with caption
       ...
    Topic b
       Image i with caption
       Image ii with caption
       Image iii with caption
       ...
    Topic c
       Image i with caption
       Image ii with caption
       Image iii with caption
       ...
    Section N
    Gallery Section
       N images
    Video Section
       N images

Contact Section (requires editing contact.html)
Footer (requires editing index.html)

```
Below is a sample yaml.

```
navbar:
  title: iwanttrails.com
home: # Home section with background images.
  href: home
  text: <h1 class="display-1 fw-bold">HIKE. BIKE. RIDE.</h1>
        <h2 class="display-5 fw-bold">On your land.</h2>
  image: static/img/home.jpg
  image_mobile: static/img/home.jpg
sections: # List of sections along with background images.
- name: Services # Name of section displayed in a list box that scrolls over bg image.
  href: services # Must match NAVBAR href.
  justify_topics: start # Position of list box.
  image: static/img/services.jpg # Desktop bg image.
  image_mobile: static/img/services.jpg # Mobile bg image.
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
  - name: Areas Served
    path: static/img/abouts/areas
- name: About Me
  href: abouts
  justify_topics: end
  image: static/img/abouts.jpg
  image_mobile: static/img/abouts.jpg
  topics:
  - name: Background
    path: static/img/abouts/background
  - name: Experience
    path: static/img/abouts/experience
  - name: Tools
    path: static/img/abouts/tools
- name: Gallery
  href: gallery
  justify_topics: center
  image: static/img/gallery.jpg
  image_mobile: static/img/gallery.jpg
  paths: [static/img/gallery,]
  images: [] # Will be filled by app.py.
- name: Videos
  href: videos
  justify_topics: begin
  image: static/img/videos.jpg
  image_mobile: static/img/videos.jpg
  path: static/img/videos # list of youtube links and descriptions.
  videos: [] # Will be filled by app.py.
contact: # Contact section, may require updating contact.html and app.py for your application.
  justify_topics: end
  image: static/img/contact.jpg
  image_mobile: static/img/contact.jpg
