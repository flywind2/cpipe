#!/usr/bin/env bash
# parameters
# 1. input
# 2. output
# 3. scripts
# 4. java 
# 5. gatk
# 6. ref

VARIANTS=`grep -c -v '^#' < $1`
echo "$VARIANTS variant(s) found in $1"
if [ $VARIANTS -eq 0 ];
then
    # nothing to put in the table
    touch $2
else
    GATK_TABLE_PARAMS=`python $3/extract_gatk_table_params.py < $1`

    $4 -Xmx3g -jar $5/GenomeAnalysisTK.jar -T VariantsToTable \
      -F CHROM -F POS -F ID -F REF -F ALT -F QUAL -F FILTER \
      $GATK_TABLE_PARAMS \
      -R $6 \
      --allowMissingData \
      --showFiltered \
      -V $1 \
      -o $2
fi
 