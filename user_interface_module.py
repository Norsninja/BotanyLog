import argparse
from datetime import datetime
from database_manager import DatabaseManager
from models_module import Plant, Measurement, NutrientType, Nutrient, Comment
from data_visualization import visualization_menu
from utility_module import (
    convert_date_string,
    validate_height,
    validate_leaf_count,
    validate_stem_diameter,
    format_float,
    format_integer,
    format_date,
    validate_nutrient_amount,
)

def get_plant_details():
    name = input("Enter plant name: ")
    strain = input("Enter plant strain: ")
    return name, strain

def get_nutrient_type_details():
    name = input("Enter nutrient type name: ")
    description = input("Enter nutrient type description (optional): ")
    return name, description

def get_measurement_details(plant):
    while True:
        date_str = input(f"Enter measurement date for {plant.name} (YYYY-MM-DD) or press Enter for the current date: ")
        if date_str == "":
            date = datetime.now().date()
            print(f"Using current date: {date}")
            break
        else:
            try:
                date = convert_date_string(date_str)
                break
            except ValueError as e:
                print(str(e))

    height_str = input("Enter plant height (cm): ")
    height = validate_height(height_str)
    leaf_count_str = input("Enter leaf count: ")
    leaf_count = validate_leaf_count(leaf_count_str)
    stem_diameter_str = input("Enter stem diameter (mm): ")
    stem_diameter = validate_stem_diameter(stem_diameter_str)
    return date, height, leaf_count, stem_diameter

def get_nutrient_details(nutrient_types):
    print("Available nutrient types:")
    for i, nutrient_type in enumerate(nutrient_types, start=1):
        print(f"{i}. {nutrient_type.name}")

    choice = int(input("Select a nutrient type: "))
    nutrient_type = nutrient_types[choice - 1]
    amount_str = input(f"Enter amount for {nutrient_type.name} (in ml): ")
    amount = validate_nutrient_amount(amount_str)  # Use the new validation function
    return nutrient_type, amount

def get_comment(plant):
    content = input(f"Enter a comment for {plant.name} (optional): ")
    return content

def add_plant(session, db_manager):
    name, strain = get_plant_details()
    plant = db_manager.add_plant(session, name, strain)
    print(f"Plant '{plant.name}' added successfully.")

def add_nutrient_type(session, db_manager):
    name, description = get_nutrient_type_details()
    nutrient_type = db_manager.add_nutrient_type(session, name, description)
    print(f"Nutrient type '{nutrient_type.name}' added successfully.")

def record_measurements_and_nutrients(session, db_manager):
    plants = db_manager.get_all_plants(session)
    if not plants:
        print("No plants available. Add a plant first.")
        return

    for i, plant in enumerate(plants, start=1):
        print(f"{i}. {plant.name} ({plant.strain})")

    plant_choice = int(input("Enter the number of the plant: "))
    plant = plants[plant_choice - 1]

    date, height, leaf_count, stem_diameter = get_measurement_details(plant)
    measurement = db_manager.add_measurement(session, plant, date, height, leaf_count, stem_diameter)
    print(f"Measurement added for {plant.name} on {format_date(date)}.")

    nutrient_types = db_manager.get_all_nutrient_types(session)
    if not nutrient_types:
        print("No nutrient types available. Add a nutrient type first.")
    else:
        while True:
            nutrient_type, amount = get_nutrient_details(nutrient_types)
            nutrient = db_manager.add_nutrient(session, plant, nutrient_type, date, amount)
            print(f"Nutrient '{nutrient_type.name}' added for {plant.name} on {format_date(date)}.")

            choice = input("Add another nutrient? (y/n): ")
            if choice.lower() != 'y':
                break

    comment = get_comment(plant)
    if comment:
        db_manager.add_comment(session, plant, date, comment)
        print(f"Comment added for {plant.name} on {format_date(date)}.")

def view_plants(session, db_manager):
    plants = db_manager.get_all_plants(session)
    if not plants:
        print("No plants available.")
        return

    for plant in plants:
        print(f"\nPlant: {plant.name} ({plant.strain})")
        print("Measurements:")
        measurements = db_manager.get_measurements(session, plant)
        for measurement in measurements:
            print(
                f"  {format_date(measurement.date)}: Height={format_float(measurement.height)} cm, "
                f"Leaf Count={format_integer(measurement.leaf_count)}, "
                f"Stem Diameter={format_float(measurement.stem_diameter)} mm"
            )

        print("Nutrients:")
        nutrients = db_manager.get_nutrients(session, plant)
        for nutrient in nutrients:
            print(
                f"  {format_date(nutrient.date)}: {nutrient.nutrient_type.name} - {format_float(nutrient.amount)} ml"
            )

        print("Comments:")
        comments = db_manager.get_comments(session, plant)
        for comment in comments:
            print(f"  {format_date(comment.date)}: {comment.content}")

def view_nutrient_types(session, db_manager):
    nutrient_types = db_manager.get_all_nutrient_types(session)
    if not nutrient_types:
        print("No nutrient types available.")
        return

    for nutrient_type in nutrient_types:
        print(f"{nutrient_type.name}: {nutrient_type.description}")

def menu_loop():
    parser = argparse.ArgumentParser(description="Plant Tracking Application")
    parser.add_argument("-d", "--database", help="Path to the database file")
    args = parser.parse_args()

    database_uri = args.database if args.database else "sqlite:///plant_tracker.db"
    db_manager = DatabaseManager(database_uri)

    while True:
        print("\nPlant Tracking Menu")
        print("1. Add a new plant")
        print("2. Add a nutrient type")
        print("3. Record measurements and nutrients")
        print("4. View plants")
        print("5. View nutrient types")
        print("6. Data visualization")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        with db_manager.create_session() as session:
            if choice == "1":
                add_plant(session, db_manager)
            elif choice == "2":
                add_nutrient_type(session, db_manager)
            elif choice == "3":
                record_measurements_and_nutrients(session, db_manager)
            elif choice == "4":
                view_plants(session, db_manager)
            elif choice == "5":
                view_nutrient_types(session, db_manager)
            elif choice == "6":
                plants = db_manager.get_all_plants(session)
                visualization_menu(plants)
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu_loop()