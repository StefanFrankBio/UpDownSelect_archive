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

mkdir data/prokka/
SAMPLE=$(find "data/genomes" -name "*.fna")
parallel -j 1 prokka --cpus 0 --prefix {/.} --locustag {/.} --outdir data/prokka/{/.} {} ::: "${SAMPLE[@]}"

fi

GFF_SAMPLE=$(find "data/prokka" -name "*.gff")
# GFF_SAMPLE=$(find "data/prokka" -name "*.gff" | shuf -n 12)
roary -f data/roary/ -e --mafft -p 12 -v $GFF_SAMPLE

# Get relevant column from roary presence absence matrix
# Some values in the column "Annotation" might contain ","
# Reversing the table to circumvent this problem
input_file="data/roary/gene_presence_absence.csv"
dos2unix $input_file
cut -d "," -f1 "$input_file" > genes.txt
sed -i 's/[\t/ ]/_/g' genes.txt

output_file="data/roary/shortened_gene_presence_absence.csv"

while read -r line; do
  rev_line=$(echo "$line" | rev | cut -d "," -f-2245 | rev)
  echo "$rev_line" >> "$output_file.tmp"
done < "$input_file"

paste -d "," genes.txt "$output_file.tmp" > "$output_file"
sed -i '1d' "$output_file"
sed -i 's/,/\t/g' "$output_file"
sed -i 's/"//g' "$output_file"
rm "$output_file.tmp"
rm genes.txt

# CDS=$(find "data/prokka/" -name "*.ffn")
# parallel -j 12 "seqkit split -i --by-id-prefix '' --out-dir data/seqkit/{/.} {}" ::: "${CDS[@]}"

# # Set the input file
# input_file="data/roary/shortened_gene_presence_absence.csv"

# # Read the input file line by line
# while IFS= read -r line; do
# # Extract the directory name (first column) and the file names (second to last columns)
# directory=$(awk '{print $1}' <<< "$line")
# files=$(awk '{$1=""; print $0}' <<< "$line")
# mkdir -p data/per_gene/"$directory"
# for file in $files; do
# modified_file=$(sed 's/\([^_]*_[^_]*\)_.*/\1\/'"$file"'/' <<< "$file")
# # Copy the files to the directory
# cp data/seqkit/"$modified_file".ffn data/per_gene/"$directory"/
# done
# done < "$input_file"

mkdir data/msa
# GENES=$(find data/per_gene/* -type d)
find data/per_gene/* -type d > test.genes
# parallel -j 12 "cat {}/*.ffn > data/msa/{/.}.fasta" ::: "${GENES[@]}"
parallel -j 12 "cat {}/*.ffn > data/msa/{/.}.fasta" :::: test.genes