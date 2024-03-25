# Plant Tracking Application
The Plant Tracking Application is a Python-based tool that allows users to record, monitor, and visualize the growth and nutrient data of their plants. It provides a simple and intuitive command-line interface for managing plant information, measurements, nutrients, and comments.

## Features
Record and track plant measurements (height, leaf count, stem diameter)
Record and track nutrient application for each plant
Add comments and observations for each plant
Visualize plant growth and nutrient schedules using interactive plots
Store and manage plant data in a SQLite database

Requirements:
Python 3.x
SQLAlchemy
Matplotlib

## Installation

Clone the repository:

git clone https://github.com/your-username/plant-tracking-app.git

Install the required dependencies:
matplotlib
SQLAlchemy

## Run the application:

python user_interface_module.py
Use the command-line interface to navigate through the application:
Add new plants, nutrient types, measurements, nutrients, and comments
View plant data, including measurements, nutrients, and comments
Access the data visualization menu to generate plots for plant growth and nutrient schedules
Scripts
data_visualization.py: Contains functions for visualizing plant data, including plant heights over time, growth rates, and nutrient schedules.
database_manager.py: Manages the interaction with the SQLite database, providing methods for adding and retrieving plant data.
models_module.py: Defines the data models for plants, measurements, nutrients, and comments using SQLAlchemy.
user_interface_module.py: Implements the command-line user interface for interacting with the application, handling user inputs, and calling the appropriate functions from other modules.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgements
SQLAlchemy - SQL toolkit and Object-Relational Mapping (ORM) library for Python.
Matplotlib - Plotting library for Python.
Claude - Anthropic
