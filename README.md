# INNTENSITY - Techno Event Website

A modern, responsive website for a techno music festival, built with Django and modern frontend tools.

## Features

- Responsive design
- Modern UI with orange accent color
- Custom font (Alte Haas Grotesk)
- Smooth animations and transitions
- Mobile-friendly navigation
- SCSS styling with variables and mixins

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (for frontend dependencies)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd inntensity
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
npm install
```

5. Set up the database:
```bash
python manage.py migrate
```

## Running the Development Server

1. Start the Django development server:
```bash
python manage.py runserver
```

2. Visit http://127.0.0.1:8000/ in your web browser

## Project Structure

```
inntensity/
├── core/                   # Main application
│   ├── static/            # Static files
│   │   ├── scss/         # SCSS files
│   │   ├── js/           # JavaScript files
│   │   └── images/       # Image assets
│   ├── templates/         # HTML templates
│   └── views.py          # View functions
├── inntensity/            # Project settings
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 