# accessible for everyone #
# you dont know the pain i went through trouble shooting... #

import re
import csv
from Bio import Entrez

# !!! MUST HAVE EMAIL WITH NCBI !!! #
Entrez.email = 'youremail@gmail.com'

# Questions #
print("What do you want to extract?")
print("1 = Scientific names only")
print("2 = Tax IDs only")
print("3 = Both scientific names and Tax IDs")
print("Enter 1, 2, or 3 below ↓↓↓")
choice = input().strip()

# UMAP String #
print("Please paste the string below ↓↓↓; then press enter")
tree_str = input()

# If it works it works, somehow. ↓↓↓ #
pattern = re.compile(r'\b([A-Z][a-z]+(?: [a-z]+)+)\b')
matches = pattern.findall(tree_str)
unique_species = sorted(set(matches))

def get_tax_id(scientific_name):
    try:
        handle = Entrez.esearch(db="taxonomy", term=scientific_name)
        record = Entrez.read(handle)
        handle.close()
        return record['IdList'][0] if record['IdList'] else "Not found"
    except Exception as e:
        return f"Error"

output_file = "species_tax_ids.csv"

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    if choice == "1":
        print(f"\n{'Scientific Names':40}")
        print("-" * 40)
        writer.writerow(["Scientific Name"])
        for species in unique_species:
            print(species)
            writer.writerow([species])

    elif choice == "2":
        print(f"\n{'Tax ID':10}")
        print("-" * 10)
        writer.writerow(["Tax ID"])
        for species in unique_species:
            tax_id = get_tax_id(species)
            print(tax_id)
            writer.writerow([tax_id])

    elif choice == "3":
        print(f"\n{'Scientific Name':40} | {'Tax ID'}")
        print("-" * 60)
        writer.writerow(["Scientific Name", "Tax ID"])
        for species in unique_species:
            tax_id = get_tax_id(species)
            print(f"{species:40} | {tax_id}")
            writer.writerow([species, tax_id])
    else:
        print("Invalid input. Please enter 1, 2, or 3.")
