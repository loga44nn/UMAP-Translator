# accessible for everyone #
# this is python, meaning you also need pip and biopython #
# you dont know the pain i went through trouble shooting... #

# !!! UPDATED WITH DISTANCES !!! #

# oml i spent like 15 hours trying to figure out ete3/4 even pandas ... #
# nothing worked so i added onto this #
# i hate python #

import re
import csv
from io import StringIO
from Bio import Entrez, Phylo
from Bio.File import as_handle

# !!! YOU MUST PROVIDE A VALID EMAIL FOR NCBI !!! #
Entrez.email = 'youremail@gmail.com'  

# questions #
choice = input('Extract (1: names, 2: IDs, 3: both, 4:both & distances)?\n')
if choice not in {"1", "2", "3", "4"}:
    print("Invalid input. Please enter 1, 2, or 3.")
    exit()


# UMAP string #
print("Paste the newick format string below ↓↓↓, then press enter")
tree_str = input()

# Parse tree safely using as_handle
handle = StringIO(tree_str)
with as_handle(handle, mode='r') as h:
    try:
        tree = Phylo.read(h, "newick")
    except Exception as e:
        print(f"Error parsing Newick tree: {e}")
        exit()

# Optional: draw tree (ASCII)
# Phylo.draw_ascii(tree)

# If it works it works, somehow. ↓↓↓ #

pattern = re.compile(r'\b([A-Z][a-z]+(?: [a-z]+)+)\b')
matches = pattern.findall(tree_str)
unique_species = sorted(set(matches))

# tax ids babyyyy #
def get_tax_id(scientific_name):
    try:
        handle = Entrez.esearch(db="taxonomy", term=scientific_name)
        record = Entrez.read(handle)
        handle.close()
        return record['IdList'][0] if record['IdList'] else "Not found"
    except Exception as e:
        return f"Error"

#yayyyy the code works#
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
    
    elif choice == "4":
        print(f"\n{'Scientific Name':60} | {'Tax ID'}")
        print("-" * 80)
        writer.writerow(["Scientific Name", "Tax ID"])
        for species in unique_species:
            tax_id = get_tax_id(species)
            print(f"{species:60} | {tax_id}")
            writer.writerow([species, tax_id])

        dist_choice = input("\nPrint the distances from tips now? (1: yes, 2: no)\n")
        if dist_choice == '1':
            print("\nPairwise distances between species:")
            terminals = tree.get_terminals()
            for i in range(len(terminals)):
                for j in range(i + 1, len(terminals)):
                    d = tree.distance(terminals[i], terminals[j])
                    print(f"{terminals[i].name} ↔ {terminals[j].name}: {d:.5f}")
        elif dist_choice == '2':
            exit()
        else:
            print("Invalid input. Exiting.")
            exit()
