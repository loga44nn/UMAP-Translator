# accessible for everyone #
# this is python, meaning you also need pip and biopython #
# you dont know the pain i went through trouble shooting... #

# !!! UPDATED WITH DISTANCES !!! #

# oml i spent like 15 hours trying to figure out ete3/4 even pandas ... #
# nothing worked so i added onto this #
# i hate python #

# for rf/normalized distances, enter the first tree, then it will ask you for the second #
# easiest way to keep original structure #
# yayyyyyy #

import re
import csv
from io import StringIO
from Bio import Entrez, Phylo
from Bio.File import as_handle

# !!! YOU MUST PROVIDE A VALID EMAIL FOR NCBI !!! #
Entrez.email = 'youremail@gmail.com'

# questions #
choice = input('Extract (1: names, 2: IDs, 3: both, 4:both & distances)?\n')
if choice not in {"1", "2", "3"}:
    print("Invalid input. Please enter 1, 2, 3")
    exit()

# UMAP string #
print("Paste the Newick format string below ↓↓↓, then press enter")
tree_str = input()

# Parse tree safely using as_handle
handle = StringIO(tree_str)
with as_handle(handle, mode='r') as h:
    try:
        tree = Phylo.read(h, "newick")
    except Exception as e:
        print(f"Error parsing Newick tree: {e}")
        exit()

# organizing species #
pattern = re.compile(r'\b([A-Z][a-z]+(?: [a-z]+)+)\b')
matches = pattern.findall(tree_str)
unique_species = sorted(set(matches))

# tax ids using NCBI #
def get_tax_id(scientific_name):
    try:
        handle = Entrez.esearch(db="taxonomy", term=scientific_name)
        record = Entrez.read(handle)
        handle.close()
        return record['IdList'][0] if record['IdList'] else "Not found"
    except Exception:
        return "Error"

# Output file
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


# rf distance #
rf_choice = input("\nDo you want to compare two trees using RF distance? (1: yes, 2: no)\n")
if rf_choice == '1':
    print("Paste the second Newick tree string to compare:")
    second_tree_str = input()

    # parsing both trees #
    try:
        t1 = Phylo.read(StringIO(tree_str), "newick")
        t2 = Phylo.read(StringIO(second_tree_str), "newick")
    except Exception as e:
        print(f"Error parsing one of the trees: {e}")
        exit()

    # Get clade sets (internal clades only)
    def get_clade_set(tree):
        return set(
            frozenset(leaf.name for leaf in clade.get_terminals())
            for clade in tree.find_clades(order='level')
            if not clade.is_terminal() and clade.get_terminals()
        )

    clades1 = get_clade_set(t1)
    clades2 = get_clade_set(t2)

    symmetric_diff = clades1.symmetric_difference(clades2)
    total_clades = len(clades1.union(clades2))
    rf_distance = len(symmetric_diff)
    normalized_rf = rf_distance / total_clades if total_clades else 0.0

    print(f"\nRobinson-Foulds (RF) distance: {rf_distance}")
    print(f"Normalized RF distance: {normalized_rf:.4f}")

elif rf_choice == '2':
    exit()
else:
    print("Invalid input. Exiting.")
    exit()
