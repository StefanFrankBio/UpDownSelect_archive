# UpDownSelect
## Issues
- gene_presence_absence.temp is appended to, might cause problems over multiple runs
- sequences containing internal stop codons cause errors in meme, fel and slac -> check for internal stop codons
- FEL, SLAC Analyses need at least 3 sequences in msa
- Trees can have branch lengths of -0, if there are only indels but no substitution, causing errors during SLAC analysis
- How to distinguish between significant positive and negativ selection in MEME, FEL and SLAC report
- Column in Report that shows sample percentage
- Column in report that shows gene source (chromosome or plasmid)
- RNA Sequences are excluded from roarys pa-matrix
- use prokka output to check for sequence length != multiple of 3
