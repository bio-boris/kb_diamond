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
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from kb_diamond.util.diamond import FastaException


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
        wsName = "test_example1_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def load_fasta_file(self, filename, obj_name, contents):
        f = open(filename, 'w')
        f.write(contents)
        f.close()
        assemblyUtil = AssemblyUtil(self.callback_url)
        assembly_ref = assemblyUtil.save_assembly_from_fasta({'file': {'path': filename},
                                                              'workspace_name': self.getWsName(),
                                                              'assembly_name': obj_name
                                                              })
        return assembly_ref

    def Xtest_input_sequence(self):
        # First load a test FASTA file as an KBase Assembly
        fasta_content = '>seq1 something soemthing asdf\n' \
                        'agcttttcat\n' \
                        '>seq2\n' \
                        'agctt\n' \
                        '>seq3\n' \
                        'agcttttcatgg'

        params = {'workspace_name': self.getWsName(),
                  'input_one_sequence': fasta_content,
                  'scratch': self.scratch,
                  'context': self.ctx
                  }
        # Second, call your implementation
        output = self.getImpl().Diamond_Blastp_Search(self.ctx, params)
        pprint(output)

        self.assertEquals(1, 1)

    def test_input_ref(self):

        query_seq = ">ATCG00500.1 pacid=19637947 transcript=ATCG00500.1 locus=ATCG00500 ID=ATCG00500.1.TAIR10 annot-version=TAIR10\n\
MEKSWFNFMFSKGELEYRGELSKAMDSFAPGEKTTISQDRFIYDMDKNFYGWDERSSYSSSYSNNVDLLVSSKDIRNFIS\
DDTFFVRDSNKNSYSIFFDKKKKIFEIDNDFSDLEKFFYSYCSSSYLNNRSKGDNDLHYDPYIKDTKYNCTNHINSCIDS\
YFRSYICIDNNFLIDSNNFNESYIYNFICSESGKIRESKNYKIRTNRNRSNLISSKDFDITQNYNQLWIQCDNCYGLMYK\
KVKMNVCEQCGHYLKMSSSERIELSIDPGTWNPMDEDMVSADPIKFHSKEEPYKNRIDSAQKTTGLTDAVQTGTGQLNGI\
PVALGVMDFRFMGGSMGSVVGEKITRLIEYATNQCLPLILVCSSGGARMQEGSLSLMQMAKISSVLCDYQSSKKLFYISI\
LTSPTTGGVTASFGMLGDIIIAEPYAYIAFAGKRVIEQTLKKAVPEGSQAAESLLRKGLLDAIVPRNLLKGVLSELFQLH\
AFFPLNTN*" + "\n" + \
">ATCG00510.1 pacid=19637948 transcript=ATCG00510.1 locus=ATCG00510 ID=ATCG00510.1.TAIR10 annot-version=TAIR10 \
MTTFNNLPSIFVPLVGLVFPAIAMASLFLHIQKNKIF*" + "\n"

        params = {'workspace_name': self.getWsName(),
                  'evalue' : 0.1,
                  'input_query_string': query_seq,
                  'target_object_ref': '12588/9/1',
                  'scratch': self.scratch,
                  'context': self.ctx
                  }
        # Second, call your implementation
        output = self.getImpl().Diamond_Blast_Search(self.ctx, params)
        pprint(output)

        self.assertEquals(1, 1)


    def test_input_sequence_with_repeating_ids(self):
        pass

    # # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # def XtestX_filter_contigs_ok(self):
    #
    #     # First load a test FASTA file as an KBase Assembly
    #     fasta_content = '>seq1 something soemthing asdf\n' \
    #                     'agcttttcat\n' \
    #                     '>seq2\n' \
    #                     'agctt\n' \
    #                     '>seq3\n' \
    #                     'agcttttcatgg'
    #
    #     assembly_ref = self.load_fasta_file(os.path.join(self.scratch, 'test1.fasta'),
    #                                         'TestAssembly',
    #                                         fasta_content)
    #     params = {'workspace_name': self.getWsName(),
    #                                          'assembly_input_ref': assembly_ref,
    #                                          'min_length': 10
    #                                          }
    #     # Second, call your implementation
    #     output = self.getImpl().Diamond_Blastp_Search(self.ctx, params)
    #     pprint(output)
    #
    #     self.assertEquals(1,1)
    # # Validate the returned data
    # self.assertEqual(ret[0]['n_initial_contigs'], 3)
    # self.assertEqual(ret[0]['n_contigs_removed'], 1)
    # self.assertEqual(ret[0]['n_contigs_remaining'], 2)

    # def test_filter_contigs_err1(self):
    #     with self.assertRaises(ValueError) as errorContext:
    #         self.getImpl().filter_contigs(self.getContext(),
    #                                       {'workspace_name': self.getWsName(),
    #                                        'assembly_input_ref': '1/fake/3',
    #                                        'min_length': '-10'})
    #     self.assertIn('min_length parameter cannot be negative', str(errorContext.exception))
    #
    # def test_filter_contigs_err2(self):
    #     with self.assertRaises(ValueError) as errorContext:
    #         self.getImpl().filter_contigs(self.getContext(),
    #                                       {'workspace_name': self.getWsName(),
    #                                        'assembly_input_ref': '1/fake/3',
    #                                        'min_length': 'ten'})
    #     self.assertIn('Cannot parse integer from min_length parameter', str(errorContext.exception))
