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



# SDK Utils
from KBaseDataObjectToFileUtils.KBaseDataObjectToFileUtilsClient import KBaseDataObjectToFileUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil as DFUClient
from KBaseReport.KBaseReportClient import KBaseReport

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

    def test_blastpWithSequence(self):
        query_seq_prot = ">Boris" + "\n" + "ATGATGCATGC"
        obj_out_name = "IndividualSequence"
        obj_basename = "Boris"

        self.callbackURL = os.environ.get('SDK_CALLBACK_URL')
        if self.callbackURL == None:
            raise ValueError("SDK_CALLBACK_URL not set in environment")

        params = {'workspace_name': self.getWsName(),
                      'input_one_sequence': query_seq_prot,
                      # 'input_one_ref': "",
                      'output_one_name': obj_basename + '.' + "test_query.SS",
                      'input_many_ref': None,
                      'output_filtered_name': obj_out_name,
                      'e_value': ".001",
                      'bitscore': "50",
                      'ident_thresh': "40.0",
                      'overlap_fraction': "50.0",
                      'maxaccepts': "1000",
                      'output_extra_format': "none",
                      'blast_type': 'blastp',
                      'callback_url' :  self.callbackURL,

                      }

        output = self.getImpl().Diamond_Blastp_Search(self.ctx, params)
        database_file = output['database_output']
        sequence_set_result = output['sequence_set_result']
        self.assertEquals(1,1)



    def atest_kb_blast_BLASTp_Search_01(self):
        obj_basename = 'BLASTp'
        obj_out_name = obj_basename + ".test_output.FS"
        obj_out_type = "KBaseCollections.FeatureSet"

        reference_prok_genomes_WS = 'ReferenceDataManager'  # PROD and CI
        genome_ref_1 = 'ReferenceDataManager/GCF_001566335.1/1'  # E. coli K-12 MG1655

        # E. coli K-12 MG1655 dnaA
        query_seq_prot = 'MSLSLWQQCLARLQDELPATEFSMWIRPLQAELSDNTLALYAPNRFVLDWVRDKYLNNINGLLTSFCGADAPQLRFEVGTKPVTQTPQAAVTSNVAAPAQVAQTQPQRAAPSTRSGWDNVPAPAEPTYRSNVNVKHTFDNFVEGKSNQLARAAARQVADNPGGAYNPLFLYGGTGLGKTHLLHAVGNGIMARKPNAKVVYMHSERFVQDMVKALQNNAIEEFKRYYRSVDALLIDDIQFFANKERSQEEFFHTFNALLEGNQQIILTSDRYPKEINGVEDRLKSRFGWGLTVAIEPPELETRVAILMKKADENDIRLPGEVAFFIAKRLRSNVRELEGALNRVIANANFTGRAITIDFVREALRDLLALQEKLVTIDNIQKTVAEYYKIKVADLLSKRRSRSVARPRQMAMALAKELTNHSLPEIGDAFGGRDHTTVLHACRKIEQLREESHDIKEDFSNLIRTLSS'

        parameters = {'workspace_name': self.getWsName(),
                      'input_one_sequence': query_seq_prot,
                      # 'input_one_ref': "",
                      'output_one_name': obj_basename + '.' + "test_query.SS",
                      'input_many_ref': genome_ref_1,
                      'output_filtered_name': obj_out_name,
                      'e_value': ".001",
                      'bitscore': "50",
                      'ident_thresh': "40.0",
                      'overlap_fraction': "50.0",
                      'maxaccepts': "1000",
                      'output_extra_format': "none",
                      'blast_type' : 'blastp'
                      }

        parameters['databases'] = [file]
        console = []
        invalid_msgs = []

        self.callbackURL = os.environ.get('SDK_CALLBACK_URL')
        if self.callbackURL == None:
            raise ValueError("SDK_CALLBACK_URL not set in environment")



        DOTFU = KBaseDataObjectToFileUtils(url=self.callbackURL, token=self.ctx['token'])
        ParseFastaStr_retVal = DOTFU.ParseFastaStr({
            'fasta_str': parameters['input_one_sequence'],
            'residue_type': 'PROT',
            'case': 'UPPER',
            'console': console,
            'invalid_msgs': invalid_msgs
        })

        pprint(ParseFastaStr_retVal)




        # output = self.getImpl().Diamond_Blastp_Search(None, parameters)
        # self.assertIsNotNone(output)
        #
        # # check created obj
        # # report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})[0]['data']
        # report_obj = self.getWsClient().get_objects([{'ref': ret['report_ref']}])[0]['data']
        # self.assertIsNotNone(report_obj['objects_created'][0]['ref'])
        #
        # created_obj_0_info = \
        # self.getWsClient().get_object_info_new({'objects': [{'ref': report_obj['objects_created'][0]['ref']}]})[0]
        # [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I,
        #  META_I] = range(11)  # object_info tuple
        # self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        # self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)
        pass

        #
        # def input_one_sequence():
        #         DOTFU = KBaseDataObjectToFileUtils(url=self.callbackURL, token=ctx['token'])
        #         ParseFastaStr_retVal = DOTFU.ParseFastaStr({
        #             'fasta_str': params['input_one_sequence'],
        #             'residue_type': 'NUC',
        #             'case': 'UPPER',
        #             'console': console,
        #             'invalid_msgs': invalid_msgs
        #         })
        #         header_id = ParseFastaStr_retVal['id']
        #         header_desc = ParseFastaStr_retVal['desc']
        #         sequence_str_buf = ParseFastaStr_retVal['seq']
        #
        #         output_one_sequenceSet = {'sequence_set_id': header_id,
        #                                   'description': header_desc,
        #                                   'sequences': [{'sequence_id': header_id,
        #                                                  'description': header_desc,
        #                                                  'sequence': sequence_str_buf
        #                                                  }
        #                                                 ]
        #                                   }
        #         try:
        #             ws = workspaceService(self.workspaceURL, token=ctx['token'])
        #             new_obj_info = ws.save_objects({
        #                 'workspace': params['workspace_name'],
        #                 'objects': [{
        #                     'type': 'KBaseSequences.SequenceSet',
        #                     'data': output_one_sequenceSet,
        #                     'name': params['output_one_name'],
        #                     'meta': {},
        #                     'provenance': provenance
        #                 }]
        #             })[0]
        #             output_one_ref = str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4])
        #         except Exception as e:
        #             raise ValueError('Unable to store output_one_name SequenceSet object from workspace: ' + str(e))
        #             # to get the full stack trace: traceback.format_exc()
        #
        # def sequenceSet():
        #     if one_type_name = 'SequenceSet':
        #         try:
        #             input_one_sequenceSet = input_one_data
        #         except Exception as e:
        #             print(traceback.format_exc())
        #             raise ValueError('Unable to get sequenceSet object: ' + str(e))
        #
        #         header_id = input_one_sequenceSet['sequences'][0]['sequence_id']
        #         sequence_str = input_one_data['sequences'][0]['sequence']
        #
        #         # PROT_pattern = re.compile("^[acdefghiklmnpqrstvwyACDEFGHIKLMNPQRSTVWYxX ]+$")
        #         DNA_pattern = re.compile("^[acgtuACGTUnryNRY ]+$")
        #         if not DNA_pattern.match(sequence_str):
        #             self.log(invalid_msgs, "BAD record for sequence_id: " + header_id + "\n" + sequence_str + "\n")
        #         else:
        #             appropriate_sequence_found_in_one_input = True
        #
        #         one_forward_reads_file_path = os.path.join(self.scratch, header_id + '.fasta')
        #         one_forward_reads_file_handle = open(one_forward_reads_file_path, 'w', 0)
        #         self.log(console, 'writing reads file: ' + str(one_forward_reads_file_path))
        #         one_forward_reads_file_handle.write('>' + header_id + "\n")
        #         one_forward_reads_file_handle.write(sequence_str + "\n")
        #         one_forward_reads_file_handle.close();
        #
        # def featureSet():
        #     one_type_name = 'FeatureSet'
        #     # retrieve sequences for features
        #     # input_one_featureSet = input_one_data
        #     one_forward_reads_file_dir = self.scratch
        #     one_forward_reads_file = input_one_name + ".fasta"
        #
        #     # DEBUG
        #     # beg_time = (datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()
        #     FeatureSetToFASTA_params = {
        #         'featureSet_ref': input_one_ref,
        #         'file': one_forward_reads_file,
        #         'dir': one_forward_reads_file_dir,
        #         'console': console,
        #         'invalid_msgs': invalid_msgs,
        #         'residue_type': 'nucleotide',
        #         'feature_type': 'ALL',
        #         'record_id_pattern': '%%genome_ref%%' + genome_id_feature_id_delim + '%%feature_id%%',
        #         'record_desc_pattern': '[%%genome_ref%%]',
        #         'case': 'upper',
        #         'linewrap': 50,
        #         'merge_fasta_files': 'TRUE'
        #     }
        #
        #     # self.log(console,"callbackURL='"+self.callbackURL+"'")  # DEBUG
        #     DOTFU = KBaseDataObjectToFileUtils(url=self.callbackURL, token=ctx['token'])
        #     FeatureSetToFASTA_retVal = DOTFU.FeatureSetToFASTA(FeatureSetToFASTA_params)
        #     one_forward_reads_file_path = FeatureSetToFASTA_retVal['fasta_file_path']
        #     if len(FeatureSetToFASTA_retVal['feature_ids_by_genome_ref'].keys()) > 0:
        #         appropriate_sequence_found_in_one_input = True
        #
        # def feature():
        #     one_type_name = 'Feature'
        #     # export feature to FASTA file
        #     feature = input_one_data
        #     one_forward_reads_file_path = os.path.join(self.scratch, input_one_name + ".fasta")
        #     self.log(console, 'writing fasta file: ' + one_forward_reads_file_path)
        #     # BLASTn is nuc-nuc
        #     if feature['dna_sequence'] != None:
        #         record = SeqRecord(Seq(feature['dna_sequence']), id=feature['id'],
        #                            description='[' + feature['genome_id'] + ']' + ' ' + feature['function'])
        #         # record = SeqRecord(Seq(feature['protein_translation']), id=feature['id'], description='['+feature['genome_id']+']'+' '+feature['function'])
        #         SeqIO.write([record], one_forward_reads_file_path, "fasta")
        #         appropriate_sequence_found_in_one_input = True
        #
