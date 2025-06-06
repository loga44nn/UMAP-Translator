# accessible for everyone #
# this is python, meaning you also need pip and biopython #
# you dont know the pain i went through trouble shooting... #

import re
import csv
from Bio import Entrez

# !!! IF YOU WANT TAX IDS YOU MUST HAVE EMAIL WITH NCBI !!! #
Entrez.email = '@gmail.com'

# Questions #
choice = input('Extract (1: names, 2: IDs, 3: both)?\n')

if choice not in {"1", "2", "3"}:
    print("Invalid input. Please enter 1, 2, or 3.")
    exit()

# UMAP String #
print("Paste the newick format string below ↓↓↓, then press enter")
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
        print(f"\n{'Scientific Name':60} | {'Tax ID'}")
        print("-" * 80)
        writer.writerow(["Scientific Name", "Tax ID"])
        for species in unique_species:
            tax_id = get_tax_id(species)
            print(f"{species:60} | {tax_id}")
            writer.writerow([species, tax_id])
    else:
        exit()
