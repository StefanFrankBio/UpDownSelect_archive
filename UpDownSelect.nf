params.taxon = 'staphylococcus aureus'
params.output = 'ncbi_dataset.zip'
taxon_ch = Channel.from(params.taxon)
outfile_ch = Channel.from(params.output)

process downloadGenomes {

    input:
    val taxon from taxon_ch
    val outfile from outfile_ch

    output:
    file "$outfile" into zip_dataset_ch

    """
    datasets download genome taxon "$taxon" \
    --assembly-level complete \
    --exclude-atypical \
    --released-after 12/01/2022 \
    --filename "$outfile"
    """
}

process unzipDataset {
    
    input:
    file zip_dataset from zip_dataset_ch

    output:
    file 'ncbi_dataset/data/**.fna' into dataset_ch

    """
    unzip $zip_dataset
    """
}

process annotateProkka {

    input:
    file data from dataset_ch.flatten()

    output:
    file '**.gff'

    """
    prokka $data
    """
}

result.view()