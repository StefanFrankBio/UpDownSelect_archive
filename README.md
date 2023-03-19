# UpDownSelect
## ToDo's
- ~~Replace gene_presence_absence_filtered.tsv with clustered_proteins~~
- ~~Shift to codon-aware multiple sequence alignment~~
- ~~Update report_table.py to allow for flexible output directory~~
- ~~Add 'presence_percentage' column to report_table.tsv~~
- ~~Add 'source' column to report_table.tsv (Chromosome, Plasmid)~~
- Add 'dNdS' column to report_table.tsv
- Fix report_table.tsv header, they contain filepaths
- Prokka and abriTAMR gene symbols are not always the same, ex.: ermC' (Prokka) and erm(C) abriTAMR
 
## Issues
- Trees can have branch lengths of -0, if there are only indels but no substitution, causing errors during SLAC analysis
- How to distinguish between significant positive and negativ selection in MEME, FEL and SLAC report
- RNA Sequences are excluded from roarys pa-matrix
