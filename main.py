
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from data.VehiculoPlusLocation import VehiculoPlusLocation
import matplotlib.pyplot as plt
import pickle

# Load environment variables
load_dotenv()

UTC = ZoneInfo("UTC")  # Define UTC timezone

# Use a valid IANA timezone name for UTC-5
LOCAL_TIMEZONE = ZoneInfo("America/Bogota")

# Access variables from .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")
encoded_password = quote_plus(db_password)

uri = f"mongodb+srv://{db_user}:{encoded_password}@{db_server}/{db_name}?retryWrites=true&w=majority&appName=Cluster0"

def create_export_filename(start_date: datetime, end_date: datetime) -> str:
    #Generate a filename based on the selected date range
    formatted_start = start_date.strftime("%Y-%m-%d_%H-%M-%S")
    formatted_end = end_date.strftime("%Y-%m-%d_%H-%M-%S")
    return f"local_exports/location_data_{formatted_start}_to_{formatted_end}.pkl"

def save_to_pickle(location_data_list: list[VehiculoPlusLocation], file_path: str):
    #save to a pickle file
    os.makedirs(os.path.dirname(file_path), exist_ok=True) #Ensure the directory exists
    with open(file_path, 'wb') as f:
        pickle.dump(location_data_list, f)

def load_from_pickle(file_path: str) -> list[VehiculoPlusLocation]:
    #load from a pickle file
    with open(file_path, 'rb') as f:
        return pickle.load(f) 


def double_newline():
    print("\n\t********************************************************")
    print("\n")

def ping_database(client: MongoClient)-> bool:
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        double_newline()
        return True
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        print(e)
        return False

def create_date_range_query(start_date: datetime, end_date: datetime)-> dict:
    # Create a query to find documents between the start and end dates
    query = {"timeStamp": {"$gte": start_date, "$lte": end_date}}
    return query

def print_results(location_data_list: list[VehiculoPlusLocation]):
    # Print the results
    for location_data in location_data_list:
        print(location_data)

# Display available placas with an integer identifier
def display_placas(placas: list[str]):
    print("Choose a vehicle to analyze:")
    for index, placa in enumerate(placas, 1):
        print(f"{index}. {placa}")

# Safely get user input for vehicle selection
def get_user_selection(placas: list[str]) -> str:
    print("")
    while True:
        try:
            choice = int(input("Enter the number corresponding to the vehicle: "))
            if 1 <= choice <= len(placas):
                return placas[choice - 1]
            else:
                print("Invalid number. Please choose a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Show the menu with analysis options
def show_menu():
    print("\nSelect an option:")
    print("1. Graph time vs batteryPercentage")
    print("2. Graph time vs speed")
    print("3. Graph time vs locationAccuracy")
    print("4. Graph time vs speed and batteryPercentage")
    print("5. Graph time vs speed and locationAccuracy")
    print("6. Graph time vs batteryPercentage and locationAccuracy")
    print("7. Graph time vs speed, batteryPercentage, and locationAccuracy")
    print("9. Find the oldest and newest location reports")
    print("99. Go back to vehicle selection menu")

    double_newline()
    # Add more options as needed

    # Graph time vs batteryPercentage for a selected vehicle
def graph_time_vs_battery(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    filtered_data.sort(key=lambda x: x.timeStamp)
    times = [entry.timeStamp for entry in filtered_data]
    battery_percentages = [entry.batteryPercentage for entry in filtered_data]

    # Convert timeStamp to datetime for plotting if needed
    # (You can use datetime parsing if your time format is a string)

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")

    plt.figure(figsize=(10, 6))
    plt.plot(times, battery_percentages, marker='o', color='b', label='Battery %')
    plt.title(f'Time vs Battery Percentage for {placa}\n  from {formatted_start} to {formatted_end}' )
    plt.xlabel('Time')
    plt.ylabel('Battery Percentage')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Graph time vs speed for a selected vehicle
def graph_time_vs_speed(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    filtered_data.sort(key=lambda x: x.timeStamp)
    times = [entry.timeStamp for entry in filtered_data]
    speeds_mps = [entry.speed for entry in filtered_data]

     # Convert speeds from m/s to km/h
    speeds_kmph = [speed * 3.6 for speed in speeds_mps]  # Conversion factor 3.6

    # Convert timeStamp to datetime for plotting if needed
    # (You can use datetime parsing if your time format is a string)

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")

    plt.figure(figsize=(10, 6))
    plt.plot(times, speeds_kmph, marker='o', color='b', label='Speed (km/h)')
    plt.title(f'Time vs Speed for {placa}\n  from {formatted_start} to {formatted_end}' )
    plt.xlabel('Time')
    plt.ylabel('Speed (km/h)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

#graph time vs locationAccuracy for a selected vehicle
def graph_time_vs_locationAccuracy(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    filtered_data.sort(key=lambda x: x.timeStamp)
    times = [entry.timeStamp for entry in filtered_data]
    location_accuracies = [entry.locationAccuracy for entry in filtered_data]

    # Convert timeStamp to datetime for plotting if needed
    # (You can use datetime parsing if your time format is a string)

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")

    plt.figure(figsize=(10, 6))
    plt.plot(times, location_accuracies, marker='o', color='b', label='Location Accuracy')
    plt.title(f'Time vs Location Accuracy for {placa}\n  from {formatted_start} to {formatted_end}' )
    plt.xlabel('Time')
    plt.ylabel('Location Accuracy')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()



def get_oldest_and_newest_reports(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    filtered_data.sort(key=lambda x: x.timeStamp)
    oldest_report = filtered_data[0].timeStamp
    newest_report = filtered_data[-1].timeStamp

    # Convert timeStamp to datetime for display if needed
    # (You can use datetime parsing if your time format is a string)

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_oldest = oldest_report.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_newest = newest_report.strftime("%A, %b %d, %Y, %I:%M %p")

    print(f"Oldest report for {placa} from {formatted_start} to {formatted_end}:")
    print(formatted_oldest)

    print(f"Newest report for {placa} from {formatted_start} to {formatted_end}:")
    print(formatted_newest)

    # Add more analysis functions as needed

# graph time vs speed and batteryPercentage for a selected vehicle
def graph_time_vs_speed_and_batteryPercentage(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    filtered_data.sort(key=lambda x: x.timeStamp)
    times = [entry.timeStamp for entry in filtered_data]
    speeds_mps = [entry.speed for entry in filtered_data]
    battery_percentages = [entry.batteryPercentage for entry in filtered_data]

    # Convert speeds from m/s to km/h
    speeds_kmph = [speed * 3.6 for speed in speeds_mps]  # Conversion factor 3.6

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Speed (km/h)', color=color)
    ax1.plot(times, speeds_kmph, marker='o', color=color, label='Speed (km/h)')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Battery Percentage', color=color)
    ax2.plot(times, battery_percentages, marker='o', color=color, label='Battery %')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Time vs Speed and Battery Percentage for {placa}\n  from {formatted_start} to {formatted_end}' )
    fig.tight_layout()
    plt.grid(True)
    plt.show()

def graph_time_vs_speed_and_locationAccuracy(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    filtered_data.sort(key=lambda x: x.timeStamp)
    times = [entry.timeStamp for entry in filtered_data]
    speeds_mps = [entry.speed for entry in filtered_data]
    location_accuracies = [entry.locationAccuracy for entry in filtered_data]

    # Convert speeds from m/s to km/h
    speeds_kmph = [speed * 3.6 for speed in speeds_mps]  # Conversion factor 3.6

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Speed (km/h)', color=color)
    ax1.plot(times, speeds_kmph, marker='o', color=color, label='Speed (km/h)')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Location Accuracy', color=color)
    ax2.plot(times, location_accuracies, marker='o', color=color, label='Location Accuracy')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Time vs Speed and Location Accuracy for {placa}\n  from {formatted_start} to {formatted_end}' )
    fig.tight_layout()
    plt.grid(True)
    plt.show()

# Graph time vs batteryPercentage and locationAccuracy
def graph_time_vs_batteryPercentage_and_locationAccuracy(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    filtered_data.sort(key=lambda x: x.timeStamp)
    times = [entry.timeStamp for entry in filtered_data]
    battery_percentages = [entry.batteryPercentage for entry in filtered_data]
    location_accuracies = [entry.locationAccuracy for entry in filtered_data]

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Battery Percentage', color=color)
    ax1.plot(times, battery_percentages, marker='o', color=color, label='Battery %')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Location Accuracy', color=color)
    ax2.plot(times, location_accuracies, marker='o', color=color, label='Location Accuracy')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Time vs Battery Percentage and Location Accuracy for {placa}\n  from {formatted_start} to {formatted_end}' )
    fig.tight_layout()
    plt.grid(True)
    plt.show()

# Graph time vs speed, batteryPercentage, and locationAccuracy
def graph_time_vs_speed_batteryPercentage_and_locationAccuracy(placa: str, data: list[dict], start_date: datetime, end_date: datetime):
    filtered_data = [entry for entry in data if entry.vehiculo.placa == placa]
    filtered_data.sort(key=lambda x: x.timeStamp)
    times = [entry.timeStamp for entry in filtered_data]
    speeds_mps = [entry.speed for entry in filtered_data]
    battery_percentages = [entry.batteryPercentage for entry in filtered_data]
    location_accuracies = [entry.locationAccuracy for entry in filtered_data]

    # Convert speeds from m/s to km/h
    speeds_kmph = [speed * 3.6 for speed in speeds_mps]  # Conversion factor 3.6

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Speed (km/h)', color=color)
    ax1.plot(times, speeds_kmph, marker='o', color=color, label='Speed (km/h)')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Battery Percentage', color=color)
    ax2.plot(times, battery_percentages, marker='o', color=color, label='Battery %')
    ax2.tick_params(axis='y', labelcolor=color)

    ax3 = ax1.twinx()
    color = 'tab:green'
    ax3.spines['right'].set_position(('outward', 60))
    ax3.set_ylabel('Location Accuracy', color=color)
    ax3.plot(times, location_accuracies, marker='o', color=color, label='Location Accuracy')
    ax3.tick_params(axis='y', labelcolor=color)

    plt.title(f'Time vs Speed, Battery Percentage, and Location Accuracy for {placa}\n  from {formatted_start} to {formatted_end}' )
    fig.tight_layout()
    plt.grid(True)
    plt.show()


def main():
    double_newline()
    print("\t\t WELCOME TO VEHICULO PLUS LOCATION DATA ANALYSIS \n")

    # List to hold the LocationData objects
    location_data_list : list[VehiculoPlusLocation] = []

    ####################THE ONLY VARIABLE YOU HAVE TO INPUT IS THE START AND END DATE####################
    #
    #
    #
    start_date = datetime(2024, 11, 29, 1, 0, 0, tzinfo=LOCAL_TIMEZONE) # 2024-11-22 5:0:0 pm
    end_date = datetime(2024, 11, 29, 16, 0, 0, tzinfo=LOCAL_TIMEZONE)
    #
    #
    #
    ####################THE ONLY VARIABLE YOU HAVE TO INPUT IS THE START AND END DATE####################

    # Define a format for display (e.g., "Nov 25, 2024, 3:30 PM")
    formatted_start = start_date.strftime("%A, %b %d, %Y, %I:%M %p")
    formatted_end = end_date.strftime("%A, %b %d, %Y, %I:%M %p")

    print("The selected date range is: \n")

    # Print the formatted dates
    print(f"Start Date: {formatted_start}")
    print(f"End Date: {formatted_end}")
    print("")

    print("\t\t Checking if a local export exists for the selected date range ... \n")
    export_file = create_export_filename(start_date, end_date)

    # Check if a local export exists inside the folder local_exports
    if os.path.exists(export_file):
        print(f"Local export found: {export_file}")
        # print the size
        print("Size of the file: ", os.path.getsize(export_file), "bytes")
        print("Loading data from the local export ... \n")
        location_data_list = load_from_pickle(export_file)

        print("\nThe system will find all the vehicles that were active during this time period.")
        double_newline()

        print("\t\t Computing results, please wait ... \n\n")
    else:
        print("Local export not found. Retrieving data from the database ... \n")
        print("\t\t Connecting to the database, please wait ... \n")

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Ping the database
        if not ping_database(client):
            return  # Exit if the database cannot be reached

        # Access the database (already specified in the connection URI)
        db = client[db_name]

        # Access the collection
        collection = db['locations']

        print("\nThe system will find all the vehicles that were active during this time period.")
        double_newline()

        print("\t\t Computing results, please wait ... \n\n")

        # Create the query
        query = create_date_range_query(start_date, end_date)

        results = collection.find(query)

        # Convert each MongoDB document into a VehiculoPlusLocation object and append to the list
        for document in results:
            # Convert MongoDB document to VehiculoPlusLocation object
            location_data = VehiculoPlusLocation(**document)
            location_data.timeStamp = location_data.timeStamp.replace(tzinfo=UTC)
            location_data.timeStamp = location_data.timeStamp.astimezone(LOCAL_TIMEZONE)
            location_data.timeStampServer = location_data.timeStampServer.replace(tzinfo=UTC)
            location_data.timeStampServer = location_data.timeStampServer.astimezone(LOCAL_TIMEZONE)
            location_data_list.append(location_data)
        save_to_pickle(location_data_list, export_file)

            # Close the connection
        print("Closing the connection to the database ...")
        client.close() #idk what is this

        # Print the results
        #print_results(location_data_list)

    print("The size of the list is: ", len(location_data_list))

    double_newline()
    print("Counting the number of times each vehicle appears in the data ... \n")

    # Sort location data by vehiculo.placa
    placa_counts  = Counter([location_data.vehiculo.placa for location_data in location_data_list])

    # Display results
    for placa, count in placa_counts.most_common():
        print(f"Placa: {placa}, Count: {count}")

    placa_list = list(placa_counts.keys())

    ###########################################################################################
    # Main interactive loop
    while True:
        double_newline()
        print("Vehicle Selection Menu")
        display_placas(placa_list)
        double_newline()

        # Get the user's selection
        selected_placa = get_user_selection(placa_list)

        # Options menu loop
        while True:
            show_menu()
            try:
                option = int(input("Enter option number: "))
                if option == 1:
                    graph_time_vs_battery(selected_placa, location_data_list, start_date, end_date)
                elif option == 2:
                    graph_time_vs_speed(selected_placa, location_data_list, start_date, end_date)
                elif option == 3:
                    graph_time_vs_locationAccuracy(selected_placa, location_data_list, start_date, end_date)
                elif option == 4:
                    graph_time_vs_speed_and_batteryPercentage(selected_placa, location_data_list, start_date, end_date)
                elif option == 5:
                    graph_time_vs_speed_and_locationAccuracy(selected_placa, location_data_list, start_date, end_date)
                elif option == 6:
                    graph_time_vs_batteryPercentage_and_locationAccuracy(selected_placa, location_data_list, start_date, end_date)
                elif option == 7:
                    graph_time_vs_speed_batteryPercentage_and_locationAccuracy(selected_placa, location_data_list, start_date, end_date)
                elif option == 9:
                    get_oldest_and_newest_reports(selected_placa, location_data_list, start_date, end_date)
                elif option == 99:
                    print("Returning to vehicle selection menu ...")
                    break  # Break the options menu loop
                else:
                    print("Option not implemented yet.")
            except ValueError:
                print("Invalid input. Please enter a valid option number.")
        
        # Check if the user wants to exit the program
        exit_choice = input("Do you want to exit the program? (yes/no): ").strip().lower()
        if exit_choice in {"yes", "y", "YES", "Y"}:
            print("Exiting the program ...")
            break  # Exit the main loop
        double_newline()

    #######################################################################################
    double_newline()
    print("END OF LINE")


if __name__ == "__main__":
    main()