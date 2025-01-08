import subprocess
import pandas as pd
import json

# Function to run DNSTwist and capture its output
def run_dnstwist(domain):
    try:
        # Run DNSTwist using subprocess to generate similar domain names in JSON format
        result = subprocess.run(
            ["dnstwist", "--format", "json", domain],  # '--format json' flag for JSON output
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.stderr:
            print(f"Error running DNSTwist: {result.stderr}")
            return None
        
        # Parse the JSON output
        output = json.loads(result.stdout)
        return output
    
    except Exception as e:
        print(f"Error executing DNSTwist: {e}")
        return None

# Function to save the DNSTwist output to Excel
def save_to_excel(output, filename="similar_domains.xlsx"):
    if output:
        # Convert the JSON output into a pandas DataFrame
        df = pd.DataFrame(output)
        
        # Save the DataFrame to an Excel file
        df.to_excel(filename, index=False)
        print(f"Results saved to {filename}")
    else:
        print("No data to save.")

# Main function to fetch similar domains and save the result to Excel
def main():
    domain = input("Enter a domain name (e.g., example.com): ").strip()
    
    # Run DNSTwist to fetch similar domain names
    print(f"Generating similar domains for {domain}...")
    similar_domains_output = run_dnstwist(domain)
    
    # Save the output to an Excel file
    save_to_excel(similar_domains_output)

if __name__ == "__main__":
    main()
