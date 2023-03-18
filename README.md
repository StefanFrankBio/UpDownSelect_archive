# UpDownSelect
## ToDo's
- ~~Replace gene_presence_absence_filtered.tsv with clustered_proteins~~
- ~~Shift to codon-aware multiple sequence alignment~~
- ~~Update report_table.py to allow for flexible output directory~~
- ~~Add 'presence_percentage' column to report_table.tsv~~
- Add 'source' column to report_table.tsv (Chromosome, Plasmid)
- Add 'dNdS' column to report_table.tsv
 
## Issues
- gene_presence_absence.temp is appended to, might cause problems over multiple runs
- sequences containing internal stop codons cause errors in meme, fel and slac -> check for internal stop codons
- Trees can have branch lengths of -0, if there are only indels but no substitution, causing errors during SLAC analysis
- How to distinguish between significant positive and negativ selection in MEME, FEL and SLAC report
- RNA Sequences are excluded from roarys pa-matrix
