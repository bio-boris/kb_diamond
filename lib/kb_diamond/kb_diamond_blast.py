# -*- coding: utf-8 -*-
# BEGIN_HEADER
from collections import namedtuple
from subprocess import Popen, check_output, CalledProcessError
import os

# SDK Utils
from KBaseDataObjectToFileUtils.KBaseDataObjectToFileUtilsClient import KBaseDataObjectToFileUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil as DFUClient
from KBaseReport.KBaseReportClient import KBaseReport

from Bio import SeqIO

# END_HEADER

database_stats = namedtuple("database_stats", "makedb_output dbinfo_output")
blast_output = namedtuple("blast_output", "result output_filename search_parameters")
fasta_file = namedtuple("fasta_file", "file_path stdin")

create_db = False
db_stats = None

diamond = "/kb/deployment/bin/diamond"
if not os.path.isfile(diamond):
    diamond = "diamond"


class FastaException(Exception):
    pass


#
# ws = workspaceService(self.workspaceURL, token=ctx['token'])
# # objects = ws.get_objects([{'ref': input_many_ref}])
# objects = ws.get_objects2({'objects': [{'ref': input_many_ref}]})['data']
# input_many_data = objects[0]['data']
# info = objects[0]['info']
# input_many_name = str(info[1])
# many_type_name = info[2].split('.')[1].split('-')[0]


# TODO Support <STDIN> sequence collections
# TODO Error Handling
def makedbs(filenames):
    """
    Create database for diamond search from a list of input files
    :param filenames:
    :return:
    """
    create_db = True
    status = {}
    for filename in filenames:
        status[filename] = database_stats(makedb(filename),
                                          dbinfo(filename))


# TODO Check to see if database already exists, and don"t create it again
# TODO Place in the correct temporary location

def makedb(filename):
    """
    Create a database for diamond to search against
    :param filename: the filename to
    :returns: status of command
    """
    return True
    args = [diamond, "makedb", "--in", filename, "--db", filename]
    return check_output(args)


def dbinfo(filename):
    """
    Gather statistics for an existing diamond database file
    :param filename:
    :returns: status of command or information about the database file
    """
    return True
    filename = filename + ".dmnd"
    args = [diamond, "dbinfo", "--db", filename]
    return check_output(args)


def blast(parameters):
    """
    Build a database and blast against it
    :param parameters: 
    :return: 
    """
    query_fasta_filepath = parameters["query_fasta_filepath"]
    subject_fasta_filepath = parameters["subject_fasta_filepath"]

    for filepath in [query_fasta_filepath, subject_fasta_filepath]:
        if not any(SeqIO.parse(filepath, "fasta")):
            raise FastaException('Not a valid FASTA file')

    db = subject_fasta_filepath + ".dmnd"
    blast_type = parameters["blast_type"]

    makedb(subject_fasta_filepath)

    output_file = "{0}/{1}_{2}.out".format(
        os.path.dirname(query_fasta_filepath),
        os.path.basename(query_fasta_filepath),
        os.path.basename(subject_fasta_filepath)
    )
    # args = [diamond, blast_type, "--query", query_fasta_filepath, "--db", db, "--out", output_file]
    try:
        # result = check_output(args)
        # return blast_output(result, output_file, parameters)
        return blast_output("SUCCESS BLAST", query_fasta_filepath, parameters)
    except CalledProcessError as e:
        return blast_output(e, output_file, parameters)


# TODO REMOVE dmnd files
# TODO REMOVE result files

def cleanup(files):
    for filename in files:
        try:
            os.remove(filename + ".dmnd")
        except OSError:
            pass

# @staticmethod
# def process_params(parameters):
#     source = parameters['source']
#     if source == 'command-line':
#         parameters['query_file'] = parameters['query']
#         parameters['database'] = parameters['database']
#     elif source == 'ui':
#         sequence = write_sequence_to_file(parameters)
#         location = write_sequence_to_file(sequence)
#     elif source == 'sequenceSet':
#         location = parameters['query']
#         database = parameters['database']
#         extracted_location = 'extracted_location'
#         extracted_database = 'extracted_database'
#         parameters['query_file'] = extracted_location
#         parameters['database'] = extracted_database
#
#
# def write_sequence_to_file(self, params):
#     DOTFU = KBaseDataObjectToFileUtils(url=params.callbackURL, token=ctx['token'])
#     ParseFastaStr_retVal = DOTFU.ParseFastaStr({
#         'fasta_str': params['input_one_sequence'],
#         'residue_type': 'NUC',
#         'case': 'UPPER',
#         'console': console,
#         'invalid_msgs': invalid_msgs
#     })
#     header_id = ParseFastaStr_retVal['id']
#     header_desc = ParseFastaStr_retVal['desc']
#     sequence_str_buf = ParseFastaStr_retVal['seq']
