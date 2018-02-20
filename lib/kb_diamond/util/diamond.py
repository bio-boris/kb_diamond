# -*- coding: utf-8 -*-
from collections import namedtuple
from subprocess import check_output, CalledProcessError
import os
from Bio import SeqIO


class FastaException(Exception):
    pass


database_stats = namedtuple("database_stats", "makedb_output dbinfo_output")
blast_output = namedtuple("blast_output", "result output_filename search_parameters")
fasta_file = namedtuple("fasta_file", "file_path stdin")

diamond = "/kb/deployment/bin/diamond"
if not os.path.isfile(diamond):
    diamond = "diamond"


def fasta_to_dict(filename):
    print("Saving fasta" + filename)
    records = {}
    for record in SeqIO.parse(filename, "fasta"):
        if record.id in records:
            print("Error, key already exists")  # Log or do something here
        records[record.id] = str(record.seq)
    return records


def fasta_to_dict_alternative(filename):
    print("Saving fasta" + filename)
    records = {}
    for record in SeqIO.parse(filename, "fasta"):
        record_id = record.id.split(" ")[0]
        if record_id in records:
            print("Error, key already exists")  # Log or do something here
        records[record_id] = str(record.seq)
    return records


def makedb(filename):
    """
    Create a database for diamond to search against
    :param filename: the filename to
    :returns: status of command
    """
    args = [diamond, "makedb", "--in", filename, "--db", filename]
    print("Making DATABASE with" + filename + " ".join(args))
    return check_output(args)


def dbinfo(filename):
    """
    Gather statistics for an existing diamond database file
    :param filename:
    :returns: status of command or information about the database file
    """
    filename = filename + ".dmnd"
    args = [diamond, "dbinfo", "--db", filename]
    return check_output(args)


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def check_for_empty_database(output):
    """

    :return:
    """

    for line in output.split("\n"):
        if line == 'Processed 0 sequences, 0 letters.':
            raise FastaException(
                "Fasta file doesn't contain sequences. Check line endings and for an even number of lines" + output)


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

    check_for_empty_database(makedb(subject_fasta_filepath))


    output_file = "{0}/{1}_{2}.out".format(
        os.path.dirname(query_fasta_filepath),
        os.path.basename(query_fasta_filepath),
        os.path.basename(subject_fasta_filepath)
    )
    args = [diamond, blast_type, "--query", query_fasta_filepath, "--db", db, "--out", output_file]
    blast_options = parameters['blast_options']
    for key in blast_options.keys():
        args.append("--" + key)
        val = blast_options[key]
        if type(val) != bool:
            args.append(str(val))
    print "About to blast"

    print(args)
    try:
        result = check_output(args)
        return blast_output(result, output_file, parameters)
        # return blast_output("SUCCESS BLAST", query_fasta_filepath, parameters)
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
