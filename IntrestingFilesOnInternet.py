import pandas as pd
from googlesearch import search
import time

# Define the file extensions we want to search for
extensions = [
    'pdf', 'txt', 'xls', 'doc', 'xlsx', 'ppt', 'zip', 'tar', 'json', 'csv'
]

# Function to search for files with specific extensions
def find_files_with_extensions(query, extensions):
    results = []

    # Loop through each extension and search for it
    for ext in extensions:
        search_query = f"{query} filetype:{ext}"
        print(f"Searching for: {search_query}")

        # Perform the Google search using the defined extension
        try:
            for url in search(search_query):  
                results.append({"URL": url, "Extension": ext})
                time.sleep(1)  # Delay to avoid hitting Google's rate limits

        except Exception as e:
            print(f"Error during search for {search_query}: {e}")
            continue

    return results

# Save the results to an Excel file
def save_to_excel(results, filename="search_results.xlsx"):
    # Convert results to a DataFrame
    df = pd.DataFrame(results)
    
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")

# Main function to execute the search and save results
def main():
    query = input("Enter the search query (e.g., 'site:example.com') or topic (e.g., 'open file'): ").strip()

    # Find files for the specified query and extensions
    results = find_files_with_extensions(query, extensions)

    # Save results to Excel
    if results:
        save_to_excel(results)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
