# Phone Number Analysis and Geographic Visualization Tool
## Overview
This project is a Python-based application that analyzes international phone numbers to extract metadata such as country/location, service provider and phone number type. The processed data is stored in a MySQL database and visualized geographically using an interactive world map generated through geocoding and mapping APIs. A Tkinter-based GUI allows users to interact with the application easily. 

## Features
- Validates international phone numbers with country codes
- Identifies:
  - Country/region associated with the phone number
  - Service provider (carrier)
  - Phone number type (mobile, landline, etc.)
- Formats phone numbers using the E.164 standard
- Stores analyzed data in a structured MySQL database
- Generates an interactive world map
- Opens the generated map in a web browser
- Allows users to view stored database records via the GUI

## Tech Stack
- **Language:** Python
- **GUI:** Tkinter
- **Phone Number Processing:** phonenumbers Library
- **Geocoding:** OpenCage Geocode API
- **Mapping:** Folium
- **Database:** MySQL
- **Browser Integration:** webbrowser Module

## How It Works 
1. The user enters a phone number along with its country code (e.g., `+91`).
2. The application validates and parses the number using the `phonenumbers` library.
3. Location, carrier and phone number type information are extracted.
4. The location name is sent to the OpenCage Geocoding API to obtain latitude and longitude.
5. An interactive map is generated using Folium and saved as an HTML file.
6. All relevant details are stored in a MySQL database with a timestamp.
7. The user can view the generated map and inspect stored records through the GUI.

## Database Schema

**Database:** `p_no`  
**Table:** `details`

| Column Name       | Data Type   |
|------------------|-------------|
| Phone_Number     | VARCHAR(20) |
| Location         | VARCHAR(50) |
| Service_Provider | VARCHAR(50) |
| Phone_Type       | VARCHAR(20) |
| Added_At         | DATETIME    |
