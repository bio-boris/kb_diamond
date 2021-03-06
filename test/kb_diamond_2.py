# # -*- coding: utf-8 -*-
# import unittest
# import sys
# import os  # noqa: F401
# import json  # noqa: F401
# import time
# import requests
#
#
#
# try:
#     from kb_diamondImpl import kb_diamond
# except:
#     from biokbase.workspace.client import Workspace as workspaceService
#     from kb_diamond.kb_diamondImpl import kb_diamond
#     from kb_diamond.kb_diamondServer import MethodContext
#     from kb_diamond.authclient import KBaseAuth as _KBaseAuth
#
# try:
#     from ConfigParser import ConfigParser  # py2
# except:
#     from configparser import ConfigParser  # py3
#
#
# class kb_diamondTest(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
#         cls.cfg = {}
#         config = ConfigParser()
#         config.read(config_file)
#         for nameval in config.items('kb_diamond'):
#             cls.cfg[nameval[0]] = nameval[1]
#
#
#         cls.serviceImpl = kb_diamond(cls.cfg)
#         cls.scratch = cls.cfg['scratch']
#
#
#     @classmethod
#     def tearDownClass(cls):
#         pass
#
#     def getImpl(self):
#         return self.__class__.serviceImpl
#
#     def getContext(self):
#         return self.__class__.ctx
#
#     # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
#     def test_blastp(self):
#         parameters = { 'workspace_name': 'None',
#                        'input_one_sequence': "ATGCATGC",
#                        'blast_type': "blastp",
#                        'e_value': ".001",
#                        'bitscore': "50",
#                        'ident_thresh': "40",
#                        'overlap_fraction': "50",
#                        'maxaccepts': "1000",
#                        'output_extra_format': "none" }
#
#         file = "/kb/module/data/Athaliana_167_TAIR10.protein.fa"
#         if not os.path.isfile(file):
#             file = "/Users/celsloaner/modules/kb_diamond/data/Athaliana_167_TAIR10.protein.fa"
#
#
#         query_filepath = "/kb/module/data/query.fa"
#         if not os.path.isfile(query_filepath):
#             query_filepath = "/Users/celsloaner/modules/kb_diamond/data/query.fa"
#
#         parameters['databases'] = [file]
#         parameters['query_filepath'] = query_filepath
#
#         output = self.getImpl().Diamond_Blastp_Search(None, parameters)[0]
#         blast_output_filename = output['blast_outputs'][0].output_filename
#
#         with open(blast_output_filename) as f:
#             output_file_contents = f.readlines()
#
#         expected = ['ATCG00500.1\tATCG00500.1\t100.0\t489\t0\t0\t1\t489\t1\t489\t2.5e-270\t928.3\n']
#
#         self.assertEqual(expected,output_file_contents)
#         pass
#
#     def test_blastx(self):
#         parameters = {'workspace_name': 'None',
#                       'input_one_sequence': "ATGCATGC",
#                       'blast_type': "blastx",
#                       'e_value': ".001",
#                       'bitscore': "50",
#                       'ident_thresh': "40",
#                       'overlap_fraction': "50",
#                       'maxaccepts': "1000",
#                       'output_extra_format': "none"}
#
#         file = "/kb/module/data/Athaliana_167_TAIR10.protein.fa"
#         if not os.path.isfile(file):
#             file = "/Users/celsloaner/modules/kb_diamond/data/Athaliana_167_TAIR10.protein.fa"
#
#         query_filepath = "/kb/module/data/query_nt.fa"
#         if not os.path.isfile(query_filepath):
#             query_filepath = "/Users/celsloaner/modules/kb_diamond/data/query_nt.fa"
#
#         parameters['databases'] = [file]
#         parameters['query_filepath'] = query_filepath
#
#         output = self.getImpl().Diamond_Blastp_Search(None, parameters)[0]
#         blast_output_filename = output['blast_outputs'][0].output_filename
#
#         with open(blast_output_filename) as f:
#             output_file_contents = f.readlines()
#
#         expected = ['TRANSLATED\tATCG00500.1\t100.0\t489\t0\t0\t1\t1467\t1\t489\t2.5e-270\t928.3\n']
#
#         self.assertEqual(expected, output_file_contents)
#
#     def test_blastx_catch_error(self):
#         parameters = {'workspace_name': 'None',
#                       'input_one_sequence': "ATGCATGC",
#                       'blast_type': "blastx",
#                       'e_value': ".001",
#                       'bitscore': "50",
#                       'ident_thresh': "40",
#                       'overlap_fraction': "50",
#                       'maxaccepts': "1000",
#                       'output_extra_format': "none"}
#
#         file = "/kb/module/data/Athaliana_167_TAIR10.protein.fa"
#         if not os.path.isfile(file):
#             file = "/Users/celsloaner/modules/kb_diamond/data/Athaliana_167_TAIR10.protein.fa"
#
#         query_filepath = "/kb/module/data/query_nt_broken.fa"
#         if not os.path.isfile(query_filepath):
#             query_filepath = "/Users/celsloaner/modules/kb_diamond/data/query_nt_broken.fa"
#
#         parameters['databases'] = [file]
#         parameters['query_filepath'] = query_filepath
#
#         output = self.getImpl().Diamond_Blastp_Search(None, parameters)[0]
#         returncode = (output['blast_outputs'][0].result.returncode)
#
#
#         self.assertEqual(1, returncode)
#
