if false; then

# Download 2245 staphylococcus aureus genomes
datasets download genome taxon "staphylococcus aureus" \
--assembly-level complete \
--released-before 12/25/2022 \
--exclude-atypical

unzip ncbi_dataset.zip

mkdir -p data/genomes/
GENOMES=$(find "ncbi_dataset/data/" -name "*.fna")
for file in $GENOMES
do
base=$(basename $file | cut -d "_" -f -2)
cp $file "data/genomes/$base.fna"
done

# Replace fasta headers with accession
# Add incrementing header ('_n') suffix for fastas containing plasmid sequences in addition to genomic dna
GENOMES=$(find "data/genomes/" -name "*.fna")
for file in $GENOMES
do
base=$(basename $file)
header=${base%.*}
sed -i "s/^>.*$/>$header/" $file
awk -i inplace '{print $0 (/^>/ ? "_" (++c) : "")}' $file
done

fi

mkdir data/prokka/
#SAMPLE=$(find "data/genomes" -name "*.fna" | shuf -n 12)
SAMPLE=$(find "data/genomes" -name "*.fna")
parallel -j 12 prokka --prefix {/.} --outdir data/prokka/{/.} {} ::: "${SAMPLE[@]}"

GFF=$(find "data/prokka/" -name "*.gff")
roary -f data/roary/ -e --mafft -p 12 -v $GFF
