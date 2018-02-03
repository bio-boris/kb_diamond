# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_diamond.kb_diamondImpl import kb_diamond
from kb_diamond.kb_diamondServer import MethodContext
from kb_diamond.authclient import KBaseAuth as _KBaseAuth


class kb_diamondTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_diamond'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_diamond',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_diamond(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_diamond_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        obj_basename = 'tBLASTn'
        obj_out_name = obj_basename + '.' + "test_output.FS"
        obj_out_type = "KBaseCollections.FeatureSet"

        reference_prok_genomes_WS = 'ReferenceDataManager'  # PROD and CI
        genome_ref_1 = 'ReferenceDataManager/GCF_001566335.1/1'  # E. coli K-12 MG1655

        parameters = { 'workspace_name': self.getWsName(),
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


        ret = self.getImpl().tBLASTn_Search(self.getContext(), parameters)[0]
        

        pass


