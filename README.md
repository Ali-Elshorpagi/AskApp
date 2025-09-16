# Ask App

A sophisticated Q&A platform built with Django using the MVT (Model-View-Template) architecture. This application enables users to post questions and automatically categorizes them using machine learning, making content discovery intuitive and efficient.

## Table of Contents

- [Overview](#overview)
- [Contributors](#contributors)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Machine Learning Integration](#machine-learning-integration)
- [Contributing](#contributing)

## Overview

Ask App is a Django-based web application that follows the Model-View-Template (MVT) architecture pattern. The application addresses the common challenge of organizing questions and answers in online communities by implementing an intelligent categorization system powered by Naïve Bayes classification.

This project demonstrates the integration of machine learning with web development, showcasing how traditional web frameworks can be enhanced with AI capabilities to improve user experience and content organization.

## Contributors

This project was collaboratively developed by a dedicated team of developers.<br> 
The initial development took place in a private repository before being made publicly available.

**Development Team:**
- [Mohamed Said](https://github.com/mohamed-said03)
- [Amr Albaz](https://github.com/AmrAlbaz34)
- [Ammar Gamal](https://github.com/ammar-gamal)
- [Ali Elshorpagi](https://github.com/Ali-Elshorpagi)


## Features

### Core Functionality
- **Question Posting**: Users can submit questions with detailed descriptions
- **Answer System**: Community-driven answers with support for multiple responses per question
- **Intelligent Categorization**: Automatic classification of questions using Naïve Bayes algorithm
- **Category Browsing**: Organized navigation through questions by automatically assigned categories
- **Search Functionality**: Find questions and answers efficiently across the platform, also using categories


## Technology Stack

### Backend
- **Python 3.x**: Core programming language
- **Django**: Web framework implementing MVT architecture
- **SQLite/PostgreSQL**: Database management (configurable)
- **Scikit-learn**: Machine learning library for Naïve Bayes implementation

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Styling and responsive design
- **JavaScript**: Interactive functionality
- **Django Templates**: Server-side rendering

### Machine Learning
- **Naïve Bayes Classifier**: Text classification for automatic question categorization
- **Natural Language Processing**: Text preprocessing and feature extraction

## Installation

Follow these step-by-step instructions to set up the Ask App on your local development environment.

### Prerequisites

Before beginning the installation, ensure you have the following installed on your system:
- Python 3.8 or higher
- Git version control system
- A text editor or IDE (recommended: VS Code)

### Step 1: Clone the Repository

```bash
git clone https://github.com/mohamed-said03/AskApp.git
cd AskApp
```

### Step 2: Create a Virtual Environment

Creating a virtual environment isolates your project dependencies from other Python projects on your system:

```bash
# Create virtual environment
python -m venv askapp_env

# Activate virtual environment
# On Windows:
askapp_env\Scripts\activate
# On macOS/Linux:
source askapp_env/bin/activate
```

### Step 3: Install Dependencies

The requirements.txt file doesn't exist, install the core dependencies:

```bash
pip install django scikit-learn pandas numpy
```

### Step 4: Database Setup

Configure the database by running Django migrations:

```bash
# Create initial migration files, if "migrations" folder doesn't exist
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
```

### Step 6: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```
## Machine Learning Integration

The Ask App incorporates machine learning to automatically categorize questions, which enhances user experience by organizing content intelligently.

### How It Works

The Naïve Bayes classifier processes incoming questions through several stages:

1. **Text Preprocessing**: Questions undergo cleaning, tokenization, and feature extraction
2. **Classification**: The trained model predicts the most appropriate category based on question content
3. **Category Assignment**: Questions are automatically tagged with predicted categories
   
## Contributing

We welcome contributions from the developer community. Here's how you can contribute to the Ask App project:

### Development Guidelines

1. **Fork the Repository**: Create your own copy of the project
2. **Create Feature Branches**: Use descriptive branch names for new features
3. **Follow Code Standards**: Maintain consistent coding style and documentation
4. **Write Tests**: Include unit tests for new functionality
5. **Submit Pull Requests**: Provide clear descriptions of your changes

### Areas for Contribution

- User interface improvements and responsive design enhancements
- Additional machine learning models for better categorization accuracy
- Performance optimizations for database queries and page loading
- New features such as user voting, question scoring, or advanced search
- Documentation improvements and code examples

---
For questions, bug reports, or feature requests, please open an issue on the GitHub repository or contact the development team directly.
