# UpDownSelect
## Issues
- use truncate after the per_gene step to remove stop codons earlier and remove current stopless approach
- specify output directory instead of just writing to 'data'
- gene_presence_ansence.temp is appended to, might cause problems over multiple runs
- RMDUP might lead to multifasta containing only a single sequence -> if-statement in meme, fel and slac
- sequences containing internal stop codons cause errors in meme, fel and slac -> check for internal stop codons
- FEL, SLAC Analyses need at least 3 sequences in msa
- Trees can have branch lengths of -0, if there are only indels but no substitution, causing errors during SLAC analysis