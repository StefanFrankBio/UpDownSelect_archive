params.taxon = 'staphylococcus aureus'
params.output = 'ncbi_dataset.zip'
taxon_ch = Channel.from(params.taxon)
output_ch = Channel.from(params.output)

process downloadGenomes {

    input:
    val x from taxon_ch
    val y from output_ch

    output:
    file "$y" into zip_ch

    """
    datasets download genome taxon "$x" \
    --assembly-level complete \
    --exclude-atypical \
    --released-after 12/01/2022 \
    --filename "$y"
    """
}
