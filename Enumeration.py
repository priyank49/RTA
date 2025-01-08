import subprocess
import socket
import dns.resolver
import requests
import pandas as pd
from requests.exceptions import RequestException

# Function to get subdomains using Subfinder via subprocess
def get_subdomains(domain):
    try:
        # Run subfinder command to find subdomains of the given domain
        print(f"Running subfinder for {domain}...")
        result = subprocess.run(
            ["subfinder", "-d", domain, "-silent"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Check for errors in subfinder execution
        if result.stderr:
            print(f"Error with Subfinder: {result.stderr}")
            return None
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Error running Subfinder: {e}")
        return None

# DNS query functions
def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None

def get_cname(domain):
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        return str(answers[0].target)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return None

# Function to check if a domain is live (HTTP request to check if domain responds)
def check_live(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        return True if response.status_code == 200 else False
    except (RequestException, socket.error):
        return False

# Function to get the server banner from HTTP headers
def get_server_banner(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        server_banner = response.headers.get("Server", "Unknown")
        return server_banner
    except RequestException:
        return "Error"

# Function to save subdomains data to an Excel file
def save_subdomains_to_excel(data, filename="subdomains_output.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")

# Main function to orchestrate the subdomain discovery and analysis
def main(domain):
    # Step 1: Get subdomains using Subfinder
    subdomains = get_subdomains(domain)
    
    if not subdomains:
        print("Failed to fetch subdomains. Exiting.")
        return
    
    # Step 2: Gather information for each subdomain
    subdomain_data = []
    print(f"Processing subdomains for {domain}...")
    for subdomain in subdomains:
        # Get IP address, CNAME, live status, and server banner
        ip = get_ip(subdomain)
        cname = get_cname(subdomain)
        is_live = check_live(subdomain)
        server_banner = get_server_banner(subdomain)
        
        subdomain_data.append({
            "Subdomain": subdomain,
            "IP": ip,
            "CNAME": cname,
            "Live": "Yes" if is_live else "No",
            "Server Banner": server_banner
        })
    
    # Step 3: Save the results to Excel
    save_subdomains_to_excel(subdomain_data)

if __name__ == "__main__":
    domain = input("Enter the domain name (e.g., example.com): ").strip()
    main(domain)
