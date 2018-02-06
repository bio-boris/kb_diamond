# -*- coding: utf-8 -*-
import unittest
from os import environ  # noqa: F401
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
    def test_your_method(self):
        obj_basename = 'tBLASTn'
        obj_out_name = obj_basename + '.' + "test_output.FS"
        obj_out_type = "KBaseCollections.FeatureSet"

        reference_prok_genomes_WS = 'ReferenceDataManager'  # PROD and CI
        genome_ref_1 = 'ReferenceDataManager/GCF_001566335.1/1'  # E. coli K-12 MG1655

        parameters = { 'workspace_name': 'None',
                       'input_one_sequence': "ATGCATGC",
                       #'input_one_ref': "",
                       'output_one_name': obj_basename+'.'+"test_query.SS",
                       'input_many_ref': genome_ref_1,
                       'output_filtered_name': obj_out_name,
                       'e_value': ".001",
                       'bitscore': "50",
                       'ident_thresh': "40",
                       'overlap_fraction': "50",
                       'maxaccepts': "1000",
                       'output_extra_format': "none" }


        ret = self.getImpl().Diamond_Blastp_Search(None, parameters)[0]


        pass


