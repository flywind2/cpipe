////////////////////////////////////////////////////////////////////////
//
// This is the main configuration file for Cpipe.
//
// In here are configured the locations for all the tools that the
// pipeline uses. This should be automatically copied to config.groovy
// by running `doit install` in the root directory
//
// NOTE: please use C-style single line comments (//), and not BASH 
// style comments in this file (#)
//
////////////////////////////////////////////////////////////////////////

/////////////////////////// BASIC PARAMETERS ///////////////////////////
//
// The base of everything - set this to the absolute path of the
// root of the pipeline distribution (most likely, parent folder of
// the folder this file is in)
BASE="/home/michael/Programming/cpipe_installer/cpipe"

DATA="$BASE/data"

// Set a good location for storing large temp files here (probably not /tmp)
TMPDIR="$BASE/tmpdata"

// Enter email here to get notified by email about failures
EMAILS=""

//////////////////// REFERENCE FILES ////////////////////////////////////

// Set location of your reference files here (see hg19/README for what is required)
REFBASE="$BASE/data"

// Set to the reference FASTA file, which must be indexed with bwa, and samtools faidx
// To download this file, and the files below, visit the GATK resource bundle
// at ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/2.8/hg19
REF="$REFBASE/ucsc/ucsc.hg19.fasta"

// Set to a VCF file containing DBSNP entries (or leave it if you are downloading the default)
DBSNP="$REFBASE/dbsnp/dbsnp_138.hg19.vcf"

// Set to a VCF file containing known indels here
GOLD_STANDARD_INDELS="$REFBASE/mills_and_1000g/Mills_and_1000G_gold_standard.indels.hg19.sites.vcf"

// For self tests and other default features to work, you should
// set a "default" exome target here. Note that you can specify a different
// exome capture region for any individual analysis
EXOME_TARGET=""

//////////////////// OPTIONAL PARAMTERS ////////////////////////////////
//
// You probably do NOT need to set anything under here! 
// 
// However you may wish to customise the locations of some tools such
// as java, python and perl installations.
// 
///////////////////////////////////////////////////////////////////////

// The variant database requires every sample id to map to a different
// individual. If multiple sample ids can map to the same individual
// (for example, you repeat sequencing on a sample, etc.), then
// you can mask out the part of the sample id that is not unique
// with a regular expression here. For example, Melbourne Genomics
// uses a 9 digit sample (study) id, but only the first 7 digits are
// unique for an individual. We can use a mask of ".{7}" to indicate
// that only the first 8 digits of the study id should be used in
// the variant database.
SAMPLE_ID_MASK=".*"

// Filter out variants observed more than 10 times (ie: 11 times or more)
// in samples from a different cohort / disease target
OUT_OF_COHORT_VARIANT_COUNT_FILTER=10

// This is only used for setting read group information in the
// BAM files
PLATFORM="illumina"

// The coverage level below which a sample should be failed
MEDIAN_COVERAGE_THRESHOLD=0

// Base location of all the tools that we use
TOOLS="$BASE/tools"

// Various support scripts that the pipeline uses
SCRIPTS="$BASE/pipeline/scripts"

// Location of Picard tools here
PICARD_HOME="$BASE/tools/picard"

HTSLIB="$BASE/tools/htslib"

// Due to GATK license restrictions, you must download
// GATK yourself and place it in this location
// (or point this to your installation)
// GATK="$TOOLS/gatk/2.3.9"
GATK="$TOOLS/gatk"

// gatk < 2.8
GATK_LEGACY=false

// do not do genotyping, directly call the variants
// gatk < 3.5
GATK_VARIANT_ONLY=false

// Utilities for making Excel files 
EXCEL="$TOOLS/excel"

// Location of Bedtools distribution
BEDTOOLS="$TOOLS/bedtools"

// Location of Samtools
BCFTOOLS="$TOOLS/bcftools"
SAMTOOLS="$TOOLS/samtools"

// FastQC tool
FASTQC="$TOOLS/fastqc"

// Utilties for processing NGS data in Java/Groovy
GROOVY_NGS="$TOOLS/java_libs"

// Set location of Variant Effect Predictor here
// and store it in the local directory called 'vep_cache'
// (you can create a symlink to an existing directory with 
// that name if desired).
// See tools/vep/README for more information
VEP_VERSION="83"
VEP="$TOOLS/vep"

VEP_CACHE="$DATA/vep_cache"

IGVTOOLS="$TOOLS/IGVTools"

// IGV location
IGV="$TOOLS/tools/igv"

// Location and version of BWA
BWA="$TOOLS/bwa/bwa"
BWA_THREADS="5"

CONDEL="$TOOLS/vep_plugins/config/Condel"
DBNSFP="$REFBASE/dbnsfp"

// Database of unique variants, updated for each sample
VARIANT_DB="$BASE/variants.db"
ID_FILE="$BASE/pipeline_id"

// set this to be a central db of all analyses
SAMPLE_DB="$BASE/samples.db"

// By default variant counts are annotated from the same database as the
// one that they were added to in the first place
// However you can modify them to be separate if you wish
UPDATE_VARIANT_DB=VARIANT_DB
ANNOTATION_VARIANT_DB=VARIANT_DB

// Location of groovy installation
GROOVY_HOME="$TOOLS/groovy"
GROOVY_VERSION="2.4.7"
// GROOVY binary
GROOVY="$TOOLS/groovy/bin/groovy"

// Whether to fail analysis if FASTQC produces warnings
CHECK_FASTQC_FAILURES=false

// If adapter sequence for exome capture is known, put here
ADAPTERS_FASTA=false

// By default synonymous variants are excluded from all outputs
// Set to true to include them
EXCLUDE_VARIANT_TYPES="synonymous SNV"

// Use default Java installed in PATH
JAVA="java"

// SNPEFF location
// Note: snpeff is not needed by default pipeline
SNPEFF="$TOOLS/snpeff"

// Genome needed for expanded splice regions
HG19_CHROM_INFO="$BASE/data/chromosomes/hg19.genome"

// Trimmomatic location
TRIMMOMATIC="$TOOLS/trimmomatic"

// Bamsurgeon location
BAMSURGEON="$TOOLS/bamsurgeon"


PYTHON="python"

splice_region_window=2

/////////////////////////////////////////////
// analysis options.
/////////////////////////////////////////////

// custom annotation for variants in specified bed file
ANNOTATE_CUSTOM_REGIONS=""

// interval padding to pass to the variant caller
INTERVAL_PADDING_CALL=25

// interval padding for SNVs in filter_variants
INTERVAL_PADDING_SNV=10

// interval padding for indels in filter_variants
INTERVAL_PADDING_INDEL=25

// do not filter synonymous with this range
ALLOW_SYNONYMOUS_INTRON=0
ALLOW_SYNONYMOUS_EXON=0

// mark batch directory read only after an analysis completes
POST_ANALYSIS_READ_ONLY=false

// move batch directory after an analysis completes
POST_ANALYSIS_MOVE=false

// space separated list of additional beds to search when generating gap report
GAP_ANNOTATOR_CUSTOM_BEDS=""

/////////////////////////////////////////////
// filtering options. 
// if any of these criteria are not met, the variant will be filtered
// if the variant includes multiple samples (i.e. trio), the average value must meet this criteria
/////////////////////////////////////////////
// minimum allele depth
HARD_FILTER_AD=2

// minimum allele frequency
HARD_FILTER_AF=0.15

// minimum depth
HARD_FILTER_DP=5

// minimum quality
HARD_FILTER_QUAL=5

////////////////////////////////////////////
// trio related resources
////////////////////////////////////////////
// note: only needed for trio pathway
TRIO_REFINEMENT_SUPPORTING="$REFBASE/1000G_phase3/1000G_phase3_v4_20130502.sites.hg19.vcf.gz"

////////////////////////////////////////////
// check related resources
////////////////////////////////////////////
READ_PERCENTAGE_THRESHOLD=50

////////////////////////////////////////////
// output options
////////////////////////////////////////////

// generate a filtered bam file. options are exons, design, or skip
FILTERED_ON_EXONS="skip"

////////////////////////////////////////////
// qc options
////////////////////////////////////////////
// what depth is required to contribute to satisfactory coverage
QC_THRESHOLD=20
// what percentage of QC_THRESHOLD must be achieved across the gene to get a good rating
QC_GOOD=95
// what percentage of QC_THRESHOLD must be achieved across the gene to get a pass rating
QC_PASS=80
// what percentage of QC_THRESHOLD must be achieved across the gene to get a fail rating
QC_FAIL=0
