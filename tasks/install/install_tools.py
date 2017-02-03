
import os
import glob
import sys
from tasks.nectar.nectar_util import *

from tasks.install.install_c_libs import *

def task_install_perl():
    return {
        'actions': [
            cmd('''
                cd %(perl_dir)s
                ./Configure -de -Dprefix={}
                make
                make install
            '''.format(INSTALL_ROOT)),
            (add_to_manifest, ['perl'])
        ],
        'setup': ['download_perl'],
        'getargs': {'perl_dir': ('download_perl', 'dir')},
        'targets': [os.path.join(INSTALL_ROOT, 'bin', 'perl')],
        'uptodate': [not nectar_asset_needs_update('perl')],
    }


def task_install_r():
    return {
        'actions': [
            cmd('''
                cd %(r_dir)s
                ./configure --prefix={0}
                make
                make prefix={0} install
            '''.format(INSTALL_ROOT)),
            (add_to_manifest, ['r'])
        ],
        'task_dep': ['install_perl', 'install_bzip2', 'install_xz', 'install_pcre', 'install_libcurl', 'install_zlib'],
        'getargs': {'r_dir': ('download_r', 'dir')},
        'setup': ['download_r'],
        'targets': [os.path.join(INSTALL_BIN, 'R')],
        'uptodate': [not nectar_asset_needs_update('r')],
    }


def task_install_bwa():
    def action(bwa_dir):
        delete_and_copy(os.path.join(bwa_dir, 'bwa'), INSTALL_BIN)

    return {
        'actions': [
            cmd('''
                cd %(bwa_dir)s
                make
            '''),
            action,
            (add_to_manifest, ['bwa'])
        ],
        'getargs': {'bwa_dir': ('download_bwa', 'dir')},
        'setup': ['download_bwa'],
        'targets': [os.path.join(INSTALL_BIN, 'bwa')],
        'uptodate': [not nectar_asset_needs_update('bwa')],
    }


def task_install_htslib():
    return {
        'task_dep': ['install_zlib'],
        'actions': [
            cmd('''
                cd %(htslib_dir)s
                ./configure --prefix={0}
                make
                make prefix={0} install
                '''.format(INSTALL_ROOT)),
            (add_to_manifest, ['htslib'])
        ],
        'getargs': {'htslib_dir': ('download_htslib', 'dir')},
        'setup': ['download_htslib'],
        'targets': [os.path.join(INSTALL_ROOT, 'bin', 'htsfile')],
        'uptodate': [not nectar_asset_needs_update('htslib')],
    }


def task_install_samtools():
    return {
        'task_dep': ['install_zlib', 'install_htslib'],
        'actions': [
            cmd('''
                cd %(samtools_dir)s
                ./configure --prefix={0} --with-htslib={1}
                make
                make prefix={0} install
            '''.format(INSTALL_ROOT, INSTALL_LIB)),
            (add_to_manifest, ['samtools'])
        ],
        'setup': ['download_samtools'],
        'getargs': {'samtools_dir': ('download_samtools', 'dir')},
        'targets': [os.path.join(INSTALL_ROOT, 'bin', 'samtools')],
        'uptodate': [not nectar_asset_needs_update('samtools')],
    }


def task_install_bcftools():
    return {
        'actions': [
            cmd('''
                cd %(bcftools_dir)s
                make
                make prefix={} install
            '''.format(INSTALL_ROOT)),
            (add_to_manifest, ['bcftools'])
        ],
        'task_dep': ['install_zlib'],
        'setup': ['download_bcftools'],
        'getargs': {'bcftools_dir': ('download_bcftools', 'dir')},
        'targets': [os.path.join(INSTALL_BIN, 'bcftools')],
        'uptodate': [not nectar_asset_needs_update('bcftools')],
    }


def task_install_bedtools():
    return {
        'actions': [
            cmd('''
                cd %(bedtools_dir)s
                make
                make prefix={} install
            '''.format(INSTALL_ROOT)),
            (add_to_manifest, ['bedtools'])
        ],
        'getargs': {'bedtools_dir': ('download_bedtools', 'dir')},
        'task_dep': ['install_zlib'],
        'setup': ['download_bedtools'],
        'targets': [os.path.join(INSTALL_BIN, 'bedtools')],
        'uptodate': [not nectar_asset_needs_update('bedtools')],
    }


def task_install_gatk():
    # If they're part of Melbourne Genomics they can use our licensed copy of GATK. Otherwise they have to install it
    # themselves
    if has_swift_auth():
        return {
            'actions': [
                cmd('''
                    cd %(gatk_dir)s
                    GATK_JAR=`readlink -f target/GenomeAnalysisTK.jar`\
                    cp GenomeAnalysisTK.jar {}
                '''.format(JAVA_LIBS_ROOT)),
                (add_to_manifest, ['gatk'])
            ],
            'getargs': {'gatk_dir': ('download_gatk', 'dir')},
            'setup': ['download_gatk'],
            'targets': [os.path.join(JAVA_LIBS_ROOT, 'GenomeAnalysisTK.jar')],
            'uptodate': [not nectar_asset_needs_update('gatk')],
        }
    else:
        def action():
            print('''
                It looks like you aren't a member of Melbourne Genomics (since you don't have a swift_credentials.sh
                file in your cpipe directory). In this case, you'll have to obtain your own copy of the
                GenomeAnalysisTK.jar and place it in cpipe/tools/java_libs. You'll be able to obtain a copy from the
                Broad website: https://software.broadinstitute.org/gatk/download/
            ''', file=sys.stderr)

        return {
            'actions': [action],
            'uptodate': [False]
        }


def task_install_perl_libs():
    """
    Installs all cpan libs from the cpan directory into the perl_lib directory
    :return:
    """
    return {
        'targets': [os.path.join(PERL_LIB_ROOT, 'bin')],
        'task_dep': ['install_perl', 'install_cpanm', 'install_htslib'],
        'actions': [
            # Use the cpan directory we made in download_perl_libs as a cpan mirror and install from there
            cmd('cpanm -l {perl_lib} --mirror file://%(cpan_mirror_dir)s --installdeps .'.format(
                perl_lib=PERL_LIB_ROOT),
                cwd=ROOT),
            (add_to_manifest, ['perl_libs'])
        ],
        'setup': ['download_perl_libs'],
        'getargs': {'cpan_mirror_dir': ('download_perl_libs', 'dir')},
        'uptodate': [not nectar_asset_needs_update('perl_libs')],
    }


def task_install_cpanm():
    target = os.path.join(INSTALL_BIN, 'cpanm')

    def action(cpanm_dir):
        delete_and_copy(os.path.join(cpanm_dir, 'cpanm'), target)
        add_to_manifest('cpanm')

    return {
        'actions': [action],
        'uptodate': [not nectar_asset_needs_update('cpanm')],
        'setup': ['download_cpanm'],
        'getargs': {'cpanm_dir': ('download_cpanm', 'dir')}
    }


def task_install_vep():
    def action(vep_dir):
        delete_and_copy(vep_dir, VEP_ROOT)
        add_to_manifest('vep')

    return {
        'actions': [action],
        'targets': [VEP_ROOT, os.path.join(VEP_ROOT, 'variant_effect_predictor.pl')],
        'uptodate': [not nectar_asset_needs_update('vep')],
        'setup': ['download_vep'],
        'getargs': {'vep_dir': ('download_vep', 'dir')},
    }


def task_install_fastqc():
    script_bin = os.path.join(INSTALL_BIN, 'fastqc')

    def action(fastqc_dir):
        delete_and_copy(fastqc_dir, FASTQC_ROOT)

        # Symlink bin/fastqc to fastqc, deleting the existing symlink if there is one
        if os.path.exists(script_bin):
            os.remove(script_bin)
        os.symlink(os.path.join(FASTQC_ROOT, 'fastqc'), script_bin)

        add_to_manifest('fastqc')

    return {
        'actions': [action],
        'targets': [script_bin, FASTQC_ROOT],
        'setup': ['download_fastqc'],
        'uptodate': [not nectar_asset_needs_update('fastqc')],
        'getargs': {'fastqc_dir': ('download_fastqc', 'dir')},
    }


def task_install_bpipe():
    def action(bpipe_dir):
        delete_and_copy(bpipe_dir, BPIPE_ROOT)
        add_to_manifest('bpipe')

    return {
        'actions': [action],
        'targets': [BPIPE_ROOT, os.path.join(BPIPE_ROOT, 'bin', 'bpipe')],
        'setup': ['download_bpipe'],
        'uptodate': [not nectar_asset_needs_update('bpipe')],
        'getargs': {'bpipe_dir': ('download_bpipe', 'dir')},
    }


def task_install_picard():
    picard_target = os.path.join(JAVA_LIBS_ROOT, 'picard.jar')

    def action(picard_dir):
        picard_jar = os.path.join(picard_dir, 'picard.jar')
        delete_and_copy(picard_jar, picard_target)
        add_to_manifest('picard')

    return {
        'actions': [action],
        'targets': [picard_target],
        'setup': ['download_picard'],
        'uptodate': [not nectar_asset_needs_update('picard')],
        'getargs': {'picard_dir': ('download_picard', 'dir')},
    }


def task_install_groovy():
    groovy_target = os.path.join(INSTALL_BIN, 'groovy')

    def action(groovy_dir):
        # Make the groovy directory
        delete_and_copy(groovy_dir, GROOVY_ROOT)

        # Symlink all binaries to this directory
        groovy_bin = os.path.join(GROOVY_ROOT, 'bin')
        for bin_file in os.listdir(groovy_bin):
            bin_target = os.path.join(groovy_bin, bin_file)
            symlink = os.path.join(INSTALL_BIN, bin_file)
            replace_symlink(bin_target, symlink)
            make_executable(bin_target)

        add_to_manifest('groovy')

    return {
        'actions': [action],
        'targets': [groovy_target, GROOVY_ROOT],
        'uptodate': [not nectar_asset_needs_update('groovy')],
        'setup': ['download_groovy'],
        'getargs': {'groovy_dir': ('download_groovy', 'dir')},
    }


def task_install_vep_libs():
    def action(vep_libs_dir):
        delete_and_copy(vep_libs_dir, VEP_LIBS_ROOT)
        add_to_manifest('vep_libs')

    return {
        'actions': [action],
        'uptodate': [not nectar_asset_needs_update('vep_libs')],
        'targets': [VEP_LIBS_ROOT, os.path.join(VEP_LIBS_ROOT, 'Bio', 'TreeIO.pm')],
        'setup': ['download_vep_libs'],
        'getargs': {'vep_libs_dir': ('download_vep_libs', 'dir')},
    }


def task_install_vep_plugins():
    def action(vep_plugins_dir):
        delete_and_copy(vep_plugins_dir, VEP_PLUGIN_ROOT)
        add_to_manifest('vep_plugins')

    return {
        'actions': [action],
        'uptodate': [not nectar_asset_needs_update('vep_plugins')],
        'setup': ['download_vep_plugins'],
        'targets': [VEP_PLUGIN_ROOT, os.path.join(VEP_PLUGIN_ROOT, 'GO.pm')],
        'getargs': {'vep_plugins_dir': ('download_vep_plugins', 'dir')},
    }


def task_install_junit_xml_formatter():
    target = os.path.join(JAVA_LIBS_ROOT, 'JUnitXmlFormatter.jar')

    def action(junit_xml_dir):
        jar = glob.glob(os.path.join(junit_xml_dir, 'JUnitXmlFormatter*'))[0]
        delete_and_copy(jar, target)
        add_to_manifest('junit_xml_formatter')

    return {
        'actions': [action],
        'targets': [target],
        'setup': ['download_junit_xml_formatter'],
        'uptodate': [not nectar_asset_needs_update('junit_xml_formatter')],
        'getargs': {'junit_xml_dir': ('download_junit_xml_formatter', 'dir')},
    }


def task_install_groovy_ngs_utils():
    target = os.path.join(JAVA_LIBS_ROOT, 'groovy-ngs-utils.jar')

    def action(groovy_ngs_dir):
        jar = os.path.join(groovy_ngs_dir, 'groovy-ngs-utils.jar')
        delete_and_copy(jar, target)
        add_to_manifest('groovy_ngs_utils')

    return {
        'actions': [action],
        'targets': [target],
        'setup': ['download_groovy_ngs_utils'],
        'uptodate': [not nectar_asset_needs_update('groovy_ngs_utils')],
        'getargs': {'groovy_ngs_dir': ('download_groovy_ngs_utils', 'dir')},
    }


def task_install_takari_cpsuite():
    target = os.path.join(JAVA_LIBS_ROOT, 'takari-cpsuite.jar')

    def action(takari_cpsuite_dir):
        jar = glob.glob(os.path.join(takari_cpsuite_dir, 'takari-cpsuite*.jar'))[0]
        delete_and_copy(jar, target)
        add_to_manifest('takari_cpsuite')

    return {
        'actions': [action],
        'targets': [target],
        'setup': ['download_takari_cpsuite'],
        'uptodate': [not nectar_asset_needs_update('takari_cpsuite')],
        'getargs': {'takari_cpsuite_dir': ('download_takari_cpsuite', 'dir')},
    }


def task_install_maven():
    target = os.path.join(MAVEN_ROOT, 'bin', 'mvn')

    def action(maven_dir):
        delete_and_copy(maven_dir, MAVEN_ROOT)
        add_to_manifest('maven')

    return {
        'actions': [action],
        'targets': [target],
        'setup': ['download_maven'],
        'uptodate': [True],
        'getargs': {'maven_dir': ('download_maven', 'dir')},
    }