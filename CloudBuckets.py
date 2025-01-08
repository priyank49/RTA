import requests
import pandas as pd

# List of known cloud storage bucket providers and their patterns
cloud_providers = {
    "s3": "s3.amazonaws.com",  # Amazon S3
    "gcs": "storage.googleapis.com",  # Google Cloud Storage
    "azure": "blob.core.windows.net",  # Azure Blob Storage
}

# List of common bucket names to test
common_bucket_names = [
    "static", "files", "backup", "public", "assets", "media", "storage", "content"
]

# Function to check if a bucket is publicly accessible on Amazon S3
def check_s3_bucket(bucket_name):
    url = f"http://{bucket_name}.s3.amazonaws.com"
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return url, "Accessible"
        else:
            return url, "Inaccessible"
    except requests.RequestException as e:
        return url, "Inaccessible"

# Function to check if a bucket is publicly accessible on Google Cloud Storage
def check_gcs_bucket(bucket_name):
    url = f"https://storage.googleapis.com/{bucket_name}"
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return url, "Accessible"
        else:
            return url, "Inaccessible"
    except requests.RequestException as e:
        return url, "Inaccessible"

# Function to check if a bucket is publicly accessible on Azure Blob Storage
def check_azure_blob(bucket_name, domain):
    url = f"https://{bucket_name}.{domain}"
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return url, "Accessible"
        else:
            return url, "Inaccessible"
    except requests.RequestException as e:
        return url, "Inaccessible"

# Function to generate potential bucket URLs for a domain
def generate_bucket_urls(domain):
    subdomains = []
    for bucket_name in common_bucket_names:
        # Generate possible bucket names for each cloud provider
        subdomains.append(f"{bucket_name}.s3.amazonaws.com")  # For AWS S3
        subdomains.append(f"{bucket_name}.storage.googleapis.com")  # For Google Cloud Storage
        subdomains.append(f"{bucket_name}.blob.core.windows.net")  # For Azure Blob Storage
    return subdomains

# Function to identify cloud buckets and check their access, then save to Excel
def identify_and_check_buckets(domain):
    results = []  # List to store bucket URLs and their access status
    
    print(f"Checking for publicly accessible cloud storage buckets for domain: {domain}")
    
    # Generate possible bucket names and URLs
    bucket_urls = generate_bucket_urls(domain)
    
    # Check if the buckets are publicly accessible
    for bucket_url in bucket_urls:
        bucket_name = bucket_url.split(".")[0]  # Extract bucket name from URL
        
        if "s3.amazonaws.com" in bucket_url:
            url, status = check_s3_bucket(bucket_name)
        elif "storage.googleapis.com" in bucket_url:
            url, status = check_gcs_bucket(bucket_name)
        elif "blob.core.windows.net" in bucket_url:
            url, status = check_azure_blob(bucket_name, "blob.core.windows.net")
        
        # Append the result to the list with full URL and status
        results.append({"Full URL": url, "Status": status})
    
    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(results)
    
    # Save the DataFrame to an Excel file
    excel_filename = f"cloud_buckets_{domain}.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Results saved to {excel_filename}")

# Main function to prompt user and run the script
def main():
    domain = input("Enter a domain name to search for public cloud buckets (e.g., example.com): ").strip()
    identify_and_check_buckets(domain)

if __name__ == "__main__":
    main()
