import phonenumbers
from phonenumbers import geocoder, carrier, PhoneNumberType, PhoneNumberFormat
import datetime
import tkinter as tk
import webbrowser
import mysql.connector 
from opencage.geocoder import OpenCageGeocode
import folium

map_path = None

connection = mysql.connector.connect(host = "localhost", user = "root", password = "cfdgh234")
cursor = connection.cursor()

def x_map(location):

    if not location:
        return "No map generated due to missing location data."
    
    try:
        key = "1cbd7bf4acfa4ca7a120d66771afa238"
        geocoder = OpenCageGeocode(key)
        results = geocoder.geocode(location)

        if not results:
            print("DEBUG: Geocoder returned no results for", location)
            return False
        
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']

        my_map = folium.Map(location = [lat,lng], zoom_start = 9)
        folium.Marker([lat,lng], popup = location).add_to(my_map)

        global map_path
        map_path = rf"C:\Users\Shivanshi\Desktop\phone-number-analyzer\maps\location_map.html"
        my_map.save(map_path)

        return "Map generated.\n(Exact location on map may not be accurate.)"
    
    except Exception as e:
        print(f"Map generation error: {str(e)}")
        return False
    
def get_phone_type(parsed_number):

    if phonenumbers.number_type(parsed_number) == PhoneNumberType.MOBILE: 
        return "Mobile"
    elif phonenumbers.number_type(parsed_number) == PhoneNumberType.FIXED_LINE:
        return "Landline"
    else:
        return "Other"
    
def get_info():
    number = phone_number_entry.get().strip()

    if not number:
        result_label.config(text="Error: Please enter a phone number.", fg = "red")
        return
    
    if not number.startswith("+"):
        result_label.config(text = "Error: Please include the country code (e.g., +91 for India).", fg = 'red')
        return
    
    try:
        parsed_number = phonenumbers.parse(number)
        if not phonenumbers.is_valid_number(parsed_number):
            result_label.config(text = "Error: Invalid phone number.", fg = "red")
            return
        
        formatted_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
        location = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en") 
        phone_type = get_phone_type(parsed_number)
        current_time = datetime.datetime.now()

        success = x_map(location)
        if success:
            show_map_button.config(state='normal')
        else:
            result_label.config(text="Map could not be generated.", fg="red")

        insert_data(formatted_number, location, service_provider, phone_type, current_time)
        
        result_label.config(text=(f"Phone Number: {formatted_number}\n\n"
                                  f"Location: {location}\n\n"
                                  f"Service Provider: {service_provider}\n\n"
                                  f"Phone Type: {phone_type}\n\n"), fg = "black")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg="red")
        
def show_map():
    try:
        if map_path:
            webbrowser.open_new_tab("file:///" + map_path.replace("\\", "/"))
        else:
            result_label.config(text="No map available to display.", fg="red")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg="red")

def insert_data(Phone_Number, Location, Service_Provider, Phone_Type, Added_At):
    try:
        query = "insert into details (Phone_Number, Location, Service_Provider, Phone_Type, Added_At) values (%s, %s, %s, %s, %s)"
        values = (Phone_Number, Location, Service_Provider, Phone_Type, Added_At)
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        print(f"Error: {str(e)}")

def initialize_database():
    try:
        cursor.execute("create database if not exists p_no")
        cursor.execute("use p_no")
        cursor.execute("create table if not exists details (Phone_Number varchar(20),Location varchar(50),Service_Provider varchar(50),Phone_Type varchar(20),Added_At datetime)")
        connection.commit()
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        
initialize_database()

def show_database():
    try:
        cursor.execute("select * from details")
        rows = cursor.fetchall()
        database_text.delete(1.0, tk.END)
        if rows:
            database_text.insert(tk.END, "Database Records:\n\n")
            for row in rows:
                database_text.insert(tk.END, (f"Phone Number: {row[0]}\n"
                                              f"Location: {row[1]}\n"
                                              f"Service Provider: {row[2]}\n"
                                              f"Phone Type: {row[3]}\n"
                                              f"Added at: {row[4]}\n\n"))
        else:
            database_text.insert(tk.END, "No records found in the database.")
    except Exception as e:
        database_text.insert(tk.END, f"Error fetching data: {str(e)}")

root = tk.Tk()
root.title("Phone Number Information") 

phone_number_label = tk.Label(root, text = "Enter Phone Number:")
phone_number_entry = tk.Entry(root)
get_info_button = tk.Button(root, text = "Get Information", command = get_info) 
result_label = tk.Label(root, text = "")
show_map_button = tk.Button(root, text = "Show Map", command = show_map, state = "disabled")
show_db_button = tk.Button(root, text = "Show Database", command = show_database)
database_text = tk.Text(root, height = 15, width = 60)

phone_number_label.grid(row = 0, column = 0, padx = 10, pady = 10)  
phone_number_entry.grid(row = 0, column = 1, padx = 10, pady = 10)
get_info_button.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady=10)
result_label.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10) 
show_db_button.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10)
show_map_button.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 10)
database_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

print("Code Running...")
root.mainloop()
connection.close()
