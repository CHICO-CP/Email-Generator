import requests
import json
import random
import string
import time
import os
from colorama import init, Fore, Style
import pyfiglet

S = '=' * 70

init()

BASE_URL = "https://api.mail.tm"

IDIOMAS = {
    "es": {
        "welcome": "Bienvenido al Generador de Correos Temporales",
        "features": "🚀 Características:",
        "feature1": "1. Genera correos electrónicos temporales de forma rápida y segura.",
        "feature2": "2. Utiliza contraseñas aleatorias o personalizadas.",
        "feature3": "3. Guarda todos los correos en un archivo JSON para un fácil acceso.",
        "user_options": "🔍 Opciones de Usuario:",
        "developer": "💼 Desarrollador: @Gh0stDeveloper",
        "menu_option_1": "1. Crear cuenta de correo",
        "menu_option_2": "2. Analizar archivo JSON",
        "menu_option_3": "3. Unirse al canal de Telegram",
        "menu_option_4": "4. Salir del programa",
        "create_emails": "¿Cuántos correos deseas crear?",
        "password_prompt": "Introduce la contraseña para todos los correos (o presiona Enter para generar una aleatoria para cada correo): ",
        "email_created": "Correo creado",
        "error_domain": "Error: No se pudo obtener un dominio válido.",
        "save_success": "Todos los correos han sido guardados en 'emails.json'.",
        "rights": "© Todos los derechos reservados 2024 @Gh0stDeveloper",
        "enter_valid_number": "Error: Por favor, ingrese un número válido para la cantidad de correos.",
        "JSON_analysis": "Analizando archivo JSON...",
        "expired_emails": "Revisando correos expirados en el archivo JSON...",
        "no_expired_emails": "No se encontraron correos expirados.",
        "join_channel": "Redirigiendo al canal de Telegram...",
        "exit_program": "Saliendo del programa... Gracias por usar el Generador de Correos Temporales."
    },
    "en": {
        "welcome": "Welcome to the Temporary Email Generator",
        "features": "🚀 Features:",
        "feature1": "1. Quickly and securely generates temporary email addresses.",
        "feature2": "2. Use random or personalized passwords.",
        "feature3": "3. Saves all emails in a JSON file for easy access.",
        "user_options": "🔍 User Options:",
        "developer": "💼 Developer: @Gh0stDeveloper",
        "menu_option_1": "1. Create email account",
        "menu_option_2": "2. Analyze JSON file",
        "menu_option_3": "3. Join Telegram channel",
        "menu_option_4": "4. Exit the program",
        "create_emails": "How many emails do you want to create?",
        "password_prompt": "Enter a password for all emails (or press Enter to generate a random one for each email): ",
        "email_created": "Email created",
        "error_domain": "Error: Could not obtain a valid domain.",
        "save_success": "All emails have been saved to 'emails.json'.",
        "rights": "© All rights reserved 2024 @Gh0stDeveloper",
        "enter_valid_number": "Error: Please enter a valid number for the number of emails.",
        "JSON_analysis": "Analyzing JSON file...",
        "expired_emails": "Checking for expired emails in the JSON file...",
        "no_expired_emails": "No expired emails found.",
        "join_channel": "Redirecting to the Telegram channel...",
        "exit_program": "Exiting the program... Thank you for using the Temporary Email Generator."
    }
}

def typing_effect(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def seleccionar_idioma():
    typing_effect("Seleccione el idioma / Choose the language:")
    typing_effect("1. Español")
    typing_effect("2. English")
    opcion = input("Opción / Option: ")
    return "es" if opcion == "1" else "en"

idioma = seleccionar_idioma()
msg = IDIOMAS[idioma]  
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def typing_effect(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_ascii_title(text):
    ascii_art = pyfiglet.figlet_format(text)
    typing_effect(Fore.CYAN + Style.BRIGHT + ascii_art + Style.RESET_ALL, delay=0.02)

def print_menu():
    limpiar_pantalla()
    print_ascii_title("Generador de Correos" if idioma == "es" else "Email Generator")
    typing_effect(Fore.MAGENTA + msg["welcome"], delay=0.04)
    typing_effect(Fore.CYAN + Style.BRIGHT + S + Style.RESET_ALL)
    
    typing_effect(Fore.YELLOW + msg["features"], delay=0.03)
    typing_effect(Fore.GREEN + msg["feature1"], delay=0.03)
    typing_effect(Fore.GREEN + msg["feature2"], delay=0.03)
    typing_effect(Fore.GREEN + msg["feature3"], delay=0.03)

    typing_effect(Fore.YELLOW + "\n" + msg["user_options"], delay=0.03)
    typing_effect(Fore.MAGENTA + msg["developer"] + Style.RESET_ALL, delay=0.03)
    typing_effect(Fore.CYAN + S + Style.RESET_ALL)
    
    typing_effect(Fore.CYAN + f"\n{msg['menu_option_1']}", delay=0.03)
    typing_effect(Fore.CYAN + f"{msg['menu_option_2']}", delay=0.03)
    typing_effect(Fore.CYAN + f"{msg['menu_option_3']}", delay=0.03)
    typing_effect(Fore.CYAN + f"{msg['menu_option_4']}", delay=0.03)

def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def get_valid_domain():
    try:
        response = requests.get(f"{BASE_URL}/domains")
        if response.status_code == 200:
            domains = response.json()["hydra:member"]
            if domains:
                return domains[0]["domain"]
    except Exception as e:
        print(Fore.RED + f"Error al obtener dominio: {e}" + Style.RESET_ALL)
    return None

def create_temp_email(domain, password):
    email = f"{''.join(random.choice(string.ascii_lowercase) for _ in range(10))}@{domain}"
    data = {
        "address": email,
        "password": password
    }
    try:
        response = requests.post(f"{BASE_URL}/accounts", json=data)
        if response.status_code == 201:
            session = requests.Session()
            session.auth = (email, password)
            return email, password, session
    except Exception as e:
        print(Fore.RED + f"Error al crear correo: {e}" + Style.RESET_ALL)
    return None, None, None

def save_emails_to_json(emails_data):
    with open('emails.json', 'w') as f:
        json.dump(emails_data, f, indent=4)

def ejecutar_opcion(opcion):
    if opcion == "1":
        typing_effect(Fore.GREEN + msg["create_emails"], delay=0.04)
        main()  
    elif opcion == "2":
        typing_effect(Fore.GREEN + msg["johnson_analysis"], delay=0.04)
        analizar_archivo_johnson()
    elif opcion == "3":
        typing_effect(Fore.GREEN + msg["join_channel"], delay=0.04)
        time.sleep(2)
        os.system("termux-open-url 'https://t.me/+KQkliYhDy_U1N2Ex'")  
    elif opcion == "4":
        typing_effect(Fore.RED + msg["exit_program"], delay=0.04)
        exit()

def analizar_archivo_johnson():
    typing_effect(Fore.YELLOW + msg["expired_emails"], delay=0.03)
    try:
        with open('emails.json', 'r') as f:
            emails_data = json.load(f)

        expired_emails = [email['email'] for email in emails_data if email_expired(email['email'])]
        if expired_emails:
            typing_effect(Fore.RED + "\n".join(expired_emails), delay=0.03)
        else:
            typing_effect(Fore.GREEN + msg["no_expired_emails"], delay=0.03)
    except FileNotFoundError:
        typing_effect(Fore.RED + "Error: No se encontró el archivo emails.json" + Style.RESET_ALL)
    except Exception as e:
        typing_effect(Fore.RED + f"Error al analizar archivo: {e}" + Style.RESET_ALL)

def email_expired(email):
    try:
        response = requests.get(f"{BASE_URL}/accounts/{email}")
        return response.status_code == 404  
    except:
        return False

def main():
    print_menu()
    
    domain = get_valid_domain()
    if not domain:
        typing_effect(Fore.RED + msg["error_domain"] + Style.RESET_ALL)
        return

    try:
        num_emails = int(input(msg["create_emails"] + " "))
        password = input(msg["password_prompt"] + " ")

        emails_data = []

        for i in range(num_emails):
            email_password = password if password else generate_password()
            email, email_password, session = create_temp_email(domain, email_password)

            if email:
                emails_data.append({"email": email, "password": email_password})
                typing_effect(Fore.GREEN + f"{msg['email_created']} {i + 1}: {email} / Contraseña: {email_password}" + Style.RESET_ALL)
            else:
                typing_effect(Fore.YELLOW + f"No se pudo crear el correo {i + 1}." + Style.RESET_ALL)

            time.sleep(3)
        save_emails_to_json(emails_data)
        typing_effect(Fore.BLUE + msg["save_success"] + "\n" + Style.RESET_ALL)
        typing_effect(Fore.RED + msg["rights"] + Style.RESET_ALL)
    except ValueError:
        typing_effect(Fore.RED + msg["enter_valid_number"] + Style.RESET_ALL)

if __name__ == "__main__":
    while True:
        print_menu()
        opcion = input("\nSeleccione una opción/Choose an option: ")
        ejecutar_opcion(opcion)
