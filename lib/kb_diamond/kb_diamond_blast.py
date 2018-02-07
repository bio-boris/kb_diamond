# -*- coding: utf-8 -*-
# BEGIN_HEADER
from collections import namedtuple
from subprocess import Popen, check_output, CalledProcessError
import os
# END_HEADER


class kb_diamond_blast:
    """
    Module Name:
    kb_diamond

    Module Description:
    A KBase module: kb_diamond
    """

    database_stats = namedtuple("database_stats", "makedb_output dbinfo_output")
    blast_output = namedtuple("blast_output", "result output_filename search_parameters")
    fasta_file = namedtuple("fasta_file", "file_path stdin")

    create_db = False
    db_stats = None

    diamond = "/kb/deployment/bin/diamond"
    if not os.path.isfile(diamond):
        diamond = "diamond"

    # config contains contents of config file in a hash or None if it couldn"t
    # be found
    def __init__(self):
        # BEGIN_CONSTRUCTOR
        # END_CONSTRUCTOR
        pass


    # TODO Support <STDIN> sequence collections
    # TODO Error Handling
    def makedbs(self, filenames):
        """
        Create database for diamond search from a list of input files
        :param filenames:
        :return:
        """
        create_db = True
        status = {}
        for filename in filenames:
            status[filename] = self.database_stats(self.makedb(filename),
                                                   self.dbinfo(filename))
        self.status = status

    # TODO Check to see if database already exists, and don"t create it again
    # TODO Place in the correct temporary location
    def makedb(self, filename):
        """
        Create a database for diamond to search against
        :param filename: the filename to
        :returns: status of command
        """
        args = [self.diamond, "makedb", "--in", filename, "--db", filename]
        return check_output(args)


    def dbinfo(self, filename):
        """
        Gather statistics for an existing diamond database file
        :param filename:
        :returns: status of command or information about the database file
        """
        filename = filename + ".dmnd"
        args = [self.diamond, "dbinfo", "--db", filename]
        return check_output(args)


    def blast(self, parameters):
        query = parameters["query_filepath"]
        databases = parameters["databases"]
        results = []
        for database_subject in databases:
            output_file = "{0}_{1}.out".format(os.path.basename(query), os.path.basename(database_subject))
            blast_type = parameters["blast_type"]
            args = [self.diamond, blast_type, "--query", query, "--db", database_subject, "--out", output_file]
            try:
                result = check_output(args)
                results.append(self.blast_output(result, output_file, parameters))
            except CalledProcessError as e:
                results.append(self.blast_output(e, output_file, parameters))

        return results

    # TODO REMOVE dmnd files
    # TODO REMOVE result files
    def cleanup(self, files):
        for filename in files:
            try:
                os.remove(filename + ".dmnd")
            except OSError:
                pass

