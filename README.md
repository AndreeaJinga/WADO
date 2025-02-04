# WADO

# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project-and-technologies)
- [Getting Started](#getting-started)
  - [Installation](#Installation)
  - [Set Frontend](#3-set-frontend)
  - [Clone the Repository](#1-clone-the-repository)
  - [Set Backend](#2-set-backend)
  - [Set Frontend](#3-set-frontend)
- [Run Locally](#Run-Locally)
- [License](#warning-license)
- [Contact](#handshake-contact)
- [Acknowledgements](#gem-resources)


<!-- About the Project -->
## :star2: About the Project and Technologies
This project is a Flask + Angular web application that enables users to explore an ontology related to programming concepts, frameworks, and languages. It provides a RESTful API for querying RDF data stored into Ontology, integrating SPARQL queries to retrieve ontology instances and relationships dynamically.

The Angular frontend allows users to:

✅ Search for frameworks based on a programming language.

✅ Explore instances of ontology classes dynamically.

✅ View detailed information about concepts with linked semantic properties.

✅ Use RDFa + Schema.org to enhance structured data for SEO and linked data integration.

The backend uses Flask, rdflib, and JWT authentication, ensuring secure access to ontology data. The frontend is fully responsive and deployed on Heroku, supporting semantic web technologies to create a knowledge-driven user experience. 🚀

<!-- Screenshots -->
### :camera: Videos
<iframe width="560" height="315" src="https://youtu.be/eWXzYP9_s4Q" 
        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
</iframe>
<iframe width="560" height="315" src="[https://youtu.be/eWXzYP9_s4Q](https://youtu.be/Y4TuQuMhg74)" 
        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
</iframe>

<div align="center"> 
  <!-- <img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" /> -->
</div>


## :partying_face:Getting Started

### Installation

Follow these steps to set up the **backend (Flask)** and **frontend (Angular)**.

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-repo.git
cd your-repo
```
### 2️⃣ **Set Backend**

```bash
cd backend
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
pip install -r requirements.txt  # Install dependencies

# Set environment variables
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
BASE_URL=http://example.org/
```

### 3️⃣ **Set Frontend**

```bash
npm install -g @angular/cli
cd frontend
npm install  # Installs all packages from package.json
```

## :runner:**Run Locally**

```bash
# Start backend
cd backend
source venv/bin/activate  # Activate virtual environment (Windows: venv\Scripts\activate)
python app.py  # Start the Flask server
# Start frontend
cd frontend
ng serve
```

## :warning: License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- Contact -->
## :handshake: Contact

Andreea Jinga - andreea.jinga@yahoo.com

Mihai-Alexandru Tomescu - tomihai15@yahoo.com

Project Link: [https://github.com/AndreeaJinga/WADO.git](https://github.com/AndreeaJinga/WADO.git)


## :gem: Resources

Useful resources and libraries:

 - [Shields.io](https://shields.io/)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md#travel--places)
 - [Readme Template](https://github.com/othneildrew/Best-README-Template)











