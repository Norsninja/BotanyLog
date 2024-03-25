import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from models_module import Plant, Measurement, Nutrient
from datetime import datetime

def plot_plant_heights(plants):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title("Plant Heights Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Height (cm)")

    for plant in plants:
        measurements = plant.measurements
        dates = [measurement.date for measurement in measurements]
        heights = [measurement.height for measurement in measurements]
        ax.plot(dates, heights, label=plant.name, marker='o')

    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.show()

def plot_growth_rates_all_plants(plants):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title("Growth Rates for All Plants")
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth Rate (cm/day)")

    for plant in plants:
        measurements = plant.measurements
        dates = [measurement.date for measurement in measurements]
        growth_rates = calculate_growth_rates(measurements, 'height')
        ax.plot(dates[1:], growth_rates, label=plant.name, marker='o')

    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.show()

def plot_growth_rates_individual_plant(plant):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title(f"Growth Rates for {plant.name}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth Rate")

    measurements = plant.measurements
    dates = [measurement.date for measurement in measurements]
    height_growth_rates = calculate_growth_rates(measurements, 'height')
    leaf_count_growth_rates = calculate_growth_rates(measurements, 'leaf_count')
    stem_diameter_growth_rates = calculate_growth_rates(measurements, 'stem_diameter')

    ax.plot(dates[1:], height_growth_rates, label="Height Growth Rate", marker='o')
    ax.plot(dates[1:], leaf_count_growth_rates, label="Leaf Count Growth Rate", marker='o')
    ax.plot(dates[1:], stem_diameter_growth_rates, label="Stem Diameter Growth Rate", marker='o')

    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.show()

def plot_nutrient_schedule_all_plants(plants):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title("Nutrient Schedule for All Plants")
    ax.set_xlabel("Date")
    ax.set_ylabel("Nutrient Amount (ml)")

    nutrient_types = set()
    for plant in plants:
        for nutrient in plant.nutrients:
            nutrient_types.add(nutrient.nutrient_type.name)

    nutrient_types = list(nutrient_types)
    num_nutrient_types = len(nutrient_types)

    for plant in plants:
        nutrient_dates = set()
        for nutrient in plant.nutrients:
            nutrient_dates.add(nutrient.date)

        nutrient_dates = sorted(list(nutrient_dates))

        for nutrient_type in nutrient_types:
            nutrient_amounts = []
            for date in nutrient_dates:
                nutrient = next((n for n in plant.nutrients if n.nutrient_type.name == nutrient_type and n.date == date), None)
                nutrient_amounts.append(nutrient.amount if nutrient else 0)

            ax.plot(nutrient_dates, nutrient_amounts, label=f"{plant.name} - {nutrient_type}", marker='o')

    ax.legend(ncol=num_nutrient_types)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.show()

def plot_nutrient_schedule_individual_plant(plant):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title(f"Nutrient Schedule for {plant.name}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Nutrient Amount (ml)")

    nutrient_types = set(nutrient.nutrient_type.name for nutrient in plant.nutrients)
    nutrient_types = list(nutrient_types)
    num_nutrient_types = len(nutrient_types)

    measurements = plant.measurements
    dates = [measurement.date for measurement in measurements]

    for i, nutrient_type in enumerate(nutrient_types):
        nutrient_amounts = [nutrient.amount for nutrient in plant.nutrients if nutrient.nutrient_type.name == nutrient_type]
        ax.plot(dates, nutrient_amounts, label=nutrient_type, marker='o')

    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.show()

def calculate_growth_rates(measurements, measurement_type):
    growth_rates = []
    for i in range(1, len(measurements)):
        current_measurement = measurements[i]
        previous_measurement = measurements[i - 1]

        time_diff = (current_measurement.date - previous_measurement.date).days
        if time_diff == 0:
            continue

        if measurement_type == 'height':
            growth = current_measurement.height - previous_measurement.height
        elif measurement_type == 'leaf_count':
            growth = current_measurement.leaf_count - previous_measurement.leaf_count
        elif measurement_type == 'stem_diameter':
            growth = current_measurement.stem_diameter - previous_measurement.stem_diameter
        else:
            raise ValueError("Invalid measurement type.")

        growth_rate = growth / time_diff
        growth_rates.append(growth_rate)

    return growth_rates

def visualization_menu(plants):
    while True:
        print("\nData Visualization Menu")
        print("1. Plant Heights Over Time")
        print("2. Growth Rates for All Plants")
        print("3. Individual Plant Growth Rates")
        print("4. Nutrient Schedule for All Plants")
        print("5. Individual Plant Nutrient Schedule")
        print("6. Back to Main Menu")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            plot_plant_heights(plants)
        elif choice == "2":
            plot_growth_rates_all_plants(plants)
        elif choice == "3":
            if plants:
                print("Select a plant:")
                for i, plant in enumerate(plants, start=1):
                    print(f"{i}. {plant.name}")

                while True:
                    try:
                        plant_choice = int(input("Enter the number of the plant: "))
                        if 1 <= plant_choice <= len(plants):
                            selected_plant = plants[plant_choice - 1]
                            break
                        else:
                            print("Invalid plant choice. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                plot_growth_rates_individual_plant(selected_plant)
            else:
                print("No plant data available.")
        elif choice == "4":
            plot_nutrient_schedule_all_plants(plants)
        elif choice == "5":
            if plants:
                print("Select a plant:")
                for i, plant in enumerate(plants, start=1):
                    print(f"{i}. {plant.name}")

                while True:
                    try:
                        plant_choice = int(input("Enter the number of the plant: "))
                        if 1 <= plant_choice <= len(plants):
                            selected_plant = plants[plant_choice - 1]
                            break
                        else:
                            print("Invalid plant choice. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                plot_nutrient_schedule_individual_plant(selected_plant)
            else:
                print("No plant data available.")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")