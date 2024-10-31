import os
import json
import urllib.request
import socket

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to get local IP information from ip-api
def get_local_ip_info():
    url = "http://ip-api.com/json/"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return json.loads(data)
    except Exception as e:
        print("Error retrieving your IP information:", e)
        return {}

# Function to get target IP information from ipstack
def get_ip_info(ip):
    ipstack_access_key = "cd83b55266d8aecb47fa1b1e6f5f625f"
    ipstack_api_url = f"http://api.ipstack.com/{ip}?access_key={ipstack_access_key}"
    ip_api_url = f"http://ip-api.com/json/{ip}"

    ipstack_result = {}
    ip_api_result = {}

    try:
        with urllib.request.urlopen(ipstack_api_url) as response:
            data = response.read()
            ipstack_result = json.loads(data)
    except Exception as e:
        print("Error accessing ipstack API:", e)

    try:
        with urllib.request.urlopen(ip_api_url) as response:
            data = response.read()
            ip_api_result = json.loads(data)
    except Exception as e:
        print("Error accessing ip-api API:", e)

    return ipstack_result, ip_api_result

# Function to save data to a JSON file
def save_to_json(data, filename="ip_info.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data has been saved to {filename}.")

# Function to get IP from domain
def get_ip_from_domain(domain):
    try:
        if domain.startswith('http://'):
            domain = domain[7:]
        elif domain.startswith('https://'):
            domain = domain[8:]
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.error as e:
        print("Error getting IP address from domain:", e)
        return None

# Clear the screen and display the banner
clear_screen()
print('''\033[1;37m
        ██████╗ ███████╗       ███████╗██████╗  ██████╗  ██████╗ ██╗   ██╗███████╗██████╗  
        ██╔══██╗██╔════╝       ██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██║   ██║██╔════╝██╔══██╗ 
        ██║  ██║█████╗         █████╗  ██████╔╝██║   ██║██║   ██║██║   ██║█████╗  ██████╔╝ 
        ██║  ██║██╔══╝         ██╔══╝  ██╔══██╗██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗ 
        ██████╔╝███████╗       ██║     ██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║ 
        ╚═════╝ ╚══════╝       ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
\033[1;37m
''')

# Display details section with improved formatting
print("\033[1;32m==========================================\033[1;32m")
print("╭─────────────[ Details ]─────────────────────────╮")
print("│  ✦ Author      : Elc                           │")
print("│  ✦ Discord     : https://discord.gg/bEEFxSYxM2 │")
print("╰─────────────────────────────────────────────────╯")
print("==========================================\n")

# Display help menu
def display_help():
    print("\n\033[1;32m[HELP MENU]\033[1;32m")
    print("1. Enter an IP address or domain name to retrieve information.")
    print("2. To track your local IP, simply press 'Enter' without input.")
    print("3. Type 'exit' to quit the program.")
    print("4. Type 'save' after retrieving results to save information to a JSON file.")
    print("5. Type 'clear' to clear the screen.\n")

# Display local IP information
print("\033[1;32mYour Local IP Information:\033[1;32m\n")

local_ip_info = get_local_ip_info()
print("\033[1;37mYour IP: \033[1;37m" + local_ip_info.get('query', 'N/A'))
print("\033[1;34mUse 'help' for guidance or 'exit' to quit.\033[1;34m\n")

# Run the IP tracking tool with additional commands
ip_history = []

while True:
    ip = input("\033[1;36mEnter IP or Domain (without http/https): \033[1;36m")

    if ip.lower() == 'exit':
        break
    elif ip.lower() == 'help':
        display_help()
        continue
    elif ip.lower() == 'clear':
        clear_screen()
        continue
    
    # Check if input is a domain and convert to IP
    if not ip.replace('.', '').isdigit():
        ip = get_ip_from_domain(ip)
        if not ip:
            print("\033[1;31mInvalid domain name or unable to resolve IP.\033[1;31m")
            continue

    ipstack_data, ip_api_data = get_ip_info(ip)

    if ip_api_data.get('status') == 'success':
        lati = ipstack_data.get('latitude', 'N/A')
        lon = ipstack_data.get('longitude', 'N/A')
        lat = "{:.4f}".format(lati) if lati != 'N/A' else lati
        long = "{:.4f}".format(lon) if lon != 'N/A' else lon

        more_info = ipstack_data.get('location', 'N/A')

        print("\n\033[1;32m[INFO IP]\033[1;32m [" + ip + "] :\n")
        print("\033[1;37mIP: \033[1;37m" + ipstack_data.get('ip', 'N/A'))
        print("\033[1;36mIP Type: \033[1;36m" + ipstack_data.get('type', 'N/A'))
        print("\033[1;34mContinent: \033[1;34m" + ipstack_data.get('continent_name', 'N/A'))
        print("\033[1;34mContinent Code: \033[1;34m" + ipstack_data.get('continent_code', 'N/A'))
        print("\033[1;37mCountry: \033[1;37m" + ipstack_data.get('country_name', 'N/A'))
        print("\033[1;37mCountry Code: \033[1;37m" + ip_api_data.get('countryCode', 'N/A'))
        print("\033[1;36mRegion: \033[1;36m" + ipstack_data.get('region_name', 'N/A'))
        print("\033[1;36mRegion Code: \033[1;36m" + ipstack_data.get('region_code', 'N/A'))
        print("\033[1;32mCity: \033[1;32m" + ipstack_data.get('city', 'N/A'))
        print("\033[1;32mZip: \033[1;32m" + ipstack_data.get('zip', 'N/A'))
        print("\033[1;37mTime Zone: \033[1;37m" + ip_api_data.get('timezone', 'N/A'))
        print("\033[1;37mISP: \033[1;37m" + ip_api_data.get('isp', 'N/A'))
        print("\033[1;34mGoogle Maps Link: \033[1;34m" + f"https://www.google.com/maps?q={lat},{long}")
        print("\033[1;37mLatitude: \033[1;37m" + lat)
        print("\033[1;37mLongitude: \033[1;37m" + long)
        print("\033[1;36mAdditional Information: \033[1;36m" + json.dumps(more_info, indent=2))

        ip_history.append({"IP": ip, "Details": ipstack_data})

    else:
        print("\n\033[1;31mSorry, information for IP [" + ip + "] is not available.\033[1;31m\n")

    save_option = input("\033[1;32mWould you like to save the results to a JSON file? (yes/no): \033[1;32m")
    if save_option.lower() == 'yes':
        save_to_json(ip_history)
