'''
TargetScan target list processor

What this script does:
1. Finds every Excel file (.xlsx) downloaded from TargetScan in the current folder (one file per miRNA).
2. Extracts the "Target gene" column from each file.
3. Removes duplicates and saves the gene list as a .txt file (one gene per line), ready to upload to the Venn diagram tool.
4. Prints how many unique targets each miRNA has.
5. Prints the genes shared by ALL miRNAs (the centre of the Venn diagram).

Before running:
- Install the libraries once: pip install pandas openpyxl
- Put this script in the SAME folder as the TargetScan Excel files.
- Rename each Excel with the miRNA name, e.g. "miR-33a-5p.xlsx", because the script uses the file name as the miRNA name.
'''

import glob          # lets us search for files matching a pattern (e.g. *.xlsx)
import pandas as pd  # library for reading and handling tables (Excel, CSV...)

# Dictionary to store the results.
# Key   = miRNA name (taken from the file name)
# Value = set of target genes for that miRNA
target_lists = {}

# glob.glob("*.xlsx") returns a list with every .xlsx file in this folder
# sorted() puts them in alphabetical order so the output is tidy
for excel_file in sorted(glob.glob("*.xlsx")):

    # Read the Excel file into a table (called a "DataFrame" in pandas)
    table = pd.read_excel(excel_file)

    # Find the column whose name contains "target gene"
    # We search instead of typing the exact name, in case TargetScan adds extra spaces or changes capitalisation
    gene_column = [col for col in table.columns
                   if "target gene" in str(col).lower()][0]

    '''
    Take that column and clean it:
    .dropna()          -> remove empty cells
    .astype(str)       -> make sure every value is text
    .str.strip()       -> remove spaces before/after each gene name
    set(...)           -> keep only unique genes (removes duplicates)
    sorted(...)        -> sort genes alphabetically
    '''
    genes = sorted(set(table[gene_column].dropna().astype(str).str.strip()))

    # Use the file name without ".xlsx" as the miRNA name
    # ie. "miR-33a-5p.xlsx" --> "miR-33a-5p"
    mirna_name = excel_file.replace(".xlsx", "")

    # Store this miRNA's genes in the dictionary (as a set, for the intersection we calculate later)
    target_lists[mirna_name] = set(genes)

    # Write the gene list to a .txt file, one gene per line.
    # "\n".join(genes) joins all genes with a line break between them.
    with open(mirna_name + ".txt", "w") as output_file:
        output_file.write("\n".join(genes))

    # Report how many unique targets this miRNA has.
    print(f"{mirna_name}: {len(genes)} unique targets  -> saved {mirna_name}.txt")

'''
Most and fewest targets
max()/min() with key=... compare miRNAs by the size of their gene set.
'''
most = max(target_lists, key=lambda m: len(target_lists[m]))
fewest = min(target_lists, key=lambda m: len(target_lists[m]))
print(f"\nMost targets:   {most} ({len(target_lists[most])})")
print(f"Fewest targets: {fewest} ({len(target_lists[fewest])})")

'''
Common targets (genes present in ALL lists)
set.intersection(*...) keeps only the genes that appear in every set
The * "unpacks" the dictionary values so each set is passed separately
'''
common_targets = set.intersection(*target_lists.values())

print(f"\nTargets shared by all {len(target_lists)} miRNAs "
      f"({len(common_targets)} genes):")
for gene in sorted(common_targets):
    print("  " + gene)

# Also save the common genes to a file, ready to paste into GeneCodis.
with open("common_targets.txt", "w") as output_file:
    output_file.write("\n".join(sorted(common_targets)))
print("\nSaved common_targets.txt")
