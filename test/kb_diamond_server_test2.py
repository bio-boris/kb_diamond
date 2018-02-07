# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

# Do the import
from kb_diamondImpl import kb_diamond




class kb_diamondTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config_file = '/Users/celsloaner/modules/kb_diamond/deploy.cfg'
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_diamond'):
            cls.cfg[nameval[0]] = nameval[1]


        cls.serviceImpl = kb_diamond(cls.cfg)
        cls.scratch = cls.cfg['scratch']


    @classmethod
    def tearDownClass(cls):
        pass

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_blastp(self):
        parameters = { 'workspace_name': 'None',
                       'input_one_sequence': "ATGCATGC",
                       'blast_type': "blastp",
                       'e_value': ".001",
                       'bitscore': "50",
                       'ident_thresh': "40",
                       'overlap_fraction': "50",
                       'maxaccepts': "1000",
                       'output_extra_format': "none" }

        file = "/kb/data/Athaliana_167_TAIR10.protein.fa"
        if not os.path.isfile(file):
            file = "/Users/celsloaner/modules/kb_diamond/data/Athaliana_167_TAIR10.protein.fa"


        query_filepath = "/kb/data/query.fa"
        if not os.path.isfile(query_filepath):
            query_filepath = "/Users/celsloaner/modules/kb_diamond/data/query.fa"

        parameters['databases'] = [file]
        parameters['query_filepath'] = query_filepath

        output = self.getImpl().Diamond_Blastp_Search(None, parameters)[0]
        blast_output_filename = output['blast_outputs'][0].output_filename

        with open(blast_output_filename) as f:
            output_file_contents = f.readlines()

        expected = ['ATCG00500.1\tATCG00500.1\t100.0\t489\t0\t0\t1\t489\t1\t489\t2.5e-270\t928.3\n']

        self.assertEqual(expected,output_file_contents)
        pass

    def test_blastx(self):
        parameters = {'workspace_name': 'None',
                      'input_one_sequence': "ATGCATGC",
                      'blast_type': "blastx",
                      'e_value': ".001",
                      'bitscore': "50",
                      'ident_thresh': "40",
                      'overlap_fraction': "50",
                      'maxaccepts': "1000",
                      'output_extra_format': "none"}

        file = "/kb/data/Athaliana_167_TAIR10.protein.fa"
        if not os.path.isfile(file):
            file = "/Users/celsloaner/modules/kb_diamond/data/Athaliana_167_TAIR10.protein.fa"

        query_filepath = "/kb/data/query.fa"
        if not os.path.isfile(query_filepath):
            query_filepath = "/Users/celsloaner/modules/kb_diamond/data/query.fa"

        parameters['databases'] = [file]
        parameters['query_filepath'] = query_filepath

        output = self.getImpl().Diamond_Blastp_Search(None, parameters)[0]
        blast_output_filename = output['blast_outputs'][0].output_filename

        with open(blast_output_filename) as f:
            output_file_contents = f.readlines()

        expected = ['ATCG00500.1\tATCG00500.1\t100.0\t489\t0\t0\t1\t489\t1\t489\t2.5e-270\t928.3\n']

        self.assertEqual(expected, output_file_contents)
