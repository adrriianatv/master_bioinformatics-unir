## Activity 1 — miRNA target prediction and shared targets

### Context
Hypothetical experiment: human macrophages loaded with acetylated LDL (a model of
foam-cell formation in atherosclerosis) **down-regulate** five miRNAs:

`hsa-miR-33a-5p`, `hsa-miR-33b-5p`, `hsa-miR-144-3p`, `hsa-miR-758-3p`, `hsa-miR-106b-5p`

The goal is to predict their targets, find the genes shared by all of them and
explore the pathways those genes are involved in.

### What the script does
`procesar_targetscan.py` takes the predicted-target tables downloaded from
TargetScan and:

1. Reads every `.xlsx` file in the working folder (one per miRNA).
2. Extracts the **Target gene** column and removes duplicates.
3. Saves one gene list per miRNA as `<miRNA>.txt` (one gene per line), ready
   for Venn diagram tools.
4. Reports the number of unique targets per miRNA and which miRNA has the most
   and the fewest.
5. Computes the targets shared by **all** miRNAs and saves them to
   `common_targets.txt`, ready for functional enrichment (e.g. GeneCodis).

### Requirements
- Python ≥ 3.9
- `pandas`
- `openpyxl`

With conda / miniforge:
```bash
conda create -n geneact1 python=3.12 pandas openpyxl -y
conda activate geneact1
```

### Usage
1. Go to [TargetScanHuman 8.0](https://www.targetscan.org/vert_80/), search each
   miRNA (species: *Human*) and click **Download table**.
2. Rename each Excel file with the miRNA name, e.g. `miR-144-3p.xlsx`.
   The file name is used as the miRNA label in the output.
3. Place the script in the same folder as the Excel files and run:
   ```bash
   python procesar_targetscan.py
   ```

### Example output
```
miR-106b-5p: 1385 unique targets  -> saved miR-106b-5p.txt
miR-144-3p: 1048 unique targets  -> saved miR-144-3p.txt
miR-33-5p: 545 unique targets  -> saved miR-33-5p.txt
miR-758-3p: 271 unique targets  -> saved miR-758-3p.txt

Most targets:   miR-106b-5p (1385)
Fewest targets: miR-758-3p (271)

Targets shared by all 4 miRNAs (5 genes):
  ABCA1
  KPNA3
  SCN1A
  SNTB2
  TSC22D2
```

### Notes
- **miR-33a-5p and miR-33b-5p share the same seed sequence**,
