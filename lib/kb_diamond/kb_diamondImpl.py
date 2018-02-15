# -*- coding: utf-8 -*-
#BEGIN_HEADER
from collections import namedtuple
from subprocess import Popen, check_output, CalledProcessError
import os
import uuid
from pprint import pprint, pformat

try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

# SDK Utils
import kb_diamond_blast
from KBaseReport.KBaseReportClient import KBaseReport
from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as Workspace

from KBaseDataObjectToFileUtils.KBaseDataObjectToFileUtilsClient import KBaseDataObjectToFileUtils


#END_HEADER


class kb_diamond:
    '''
    Module Name:
    kb_diamond

    Module Description:
    A KBase module: kb_diamond
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.3"
    GIT_URL = "https://github.com/bio-boris/kb_diamond.git"
    GIT_COMMIT_HASH = "1ee8ca211b9798ea9b8436e7c2c50e30e7c7458e"

    #BEGIN_CLASS_HEADER
    fasta_file = namedtuple("fasta_file", "file_path stdin")
    diamond = "/kb/deployment/bin/diamond"
    if not os.path.isfile(diamond):
        diamond = "diamond"

    database_stats = namedtuple("database_stats", "makedb_output dbinfo_output")
    blast_output = namedtuple("blast_output", "result output_filename search_parameters")

    @staticmethod
    def get_object_type(ws_object_info):
        return ws_object_info[2].split('.')[1].split('-')[0]

    # @staticmethod
    # def genomeSetToFasta(object_ref):
    #     GenomeSetToFASTA_params = {
    #         'genomeSet_ref': input_many_ref,
    #         'file': many_forward_reads_file,
    #         'dir': many_forward_reads_file_dir,
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

    def genome_cds_to_fasta(self, object_ref):
        GenomeToFASTA_params = {
            'genome_ref': object_ref,
            'file': 'output.fasta',
            'dir': self.shared_folder,
            'console': [],
            'invalid_msgs': [],
            'residue_type': 'protein',
            'feature_type': 'CDS',
            'record_id_pattern': '%%feature_id%%',
            'record_desc_pattern': '[%%genome_id%%]',
            'case': 'upper',
            'linewrap': 50
        }

        DOTFU = KBaseDataObjectToFileUtils(url=self.callback_url, token=self.token)
        output = DOTFU.GenomeToFASTA(GenomeToFASTA_params)
        feature_ids_count = len(output['feature_ids'])
        if feature_ids_count > 0:
            return output['fasta_file_path']
        raise ValueError('No features found in genome')

    def get_fasta_from_query_object(self, query_object_ref):
        """

        :param query_object_ref:
        :return:
        """
        query_object = self.ws.get_objects2({'objects': [{'ref': query_object_ref}]})['data'][0]
        input_type = self.get_object_type(query_object['info'])

        # SequenceSet, SingleEndLibrary, FeatureSet, Genome, or GenomeSet
        if input_type == 'Genome':
            return self.genome_cds_to_fasta(query_object_ref)
        elif input_type == 'SequenceSet':
            raise ValueError('input_type not yet supported:' + input_type)
        elif input_type in ['GenomeSet', 'FeatureSet']:
            raise ValueError('input_type not yet supported:' + input_type)
        elif input_type in ['ContigSet', 'Assembly']:
            # return AssemblyUtil.assembly_as_fasta(self.ctx, {'ref': query_object_ref})['path']
            raise ValueError('input_type not yet supported:' + input_type)
        else:
            raise ValueError('Invalid object reference was provided' + query_object_ref + input_type)

    def get_query_fasta_filepath(self, params):
        """
        Get file path from input string or object reference
        :param params:
        :return:
        """
        if 'input_query_string' in params:
            filename = os.path.join(self.shared_folder, 'STDIN.fasta')
            with open(filename, "w") as a:
                a.write(params['input_query_string'])
                a.close()
            return filename
        elif 'input_object_ref' in params:
            return self.get_fasta_from_query_object(params['input_object_ref'])

        raise ValueError('No genetic sequence string or reference file object was provided')

    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def upload_to_shock(self, **upload_arguments):
        file_path = upload_arguments['file_path']
        dfu_arguments = {'file_path': file_path}
        if ('zipped' in upload_arguments and 'zipped' == True):
            dfu_arguments['pack'] = 'zip'
        return self.dfu.file_to_shock(dfu_arguments)['shock_id']

    def upload_html_report_to_shock(self, filepath):
        return self.upload_to_shock(file_path=filepath, zipped=True)

    def generate_sequence_set(self, **output_parameters):
        blast_file = output_parameters['blast_file']
        query_fasta_file = output_parameters['query_fasta_file']
        output_name = "OUTPUTNAMEGOESHERE"

        sequenceSet = {'sequence_set_id': 'SequenceSetIDGoesHere',
                       'description': 'SequenceSetDescriptionGoesHere',
                       'sequences': [{'sequence_id': ">Boris1",
                                      'description': "Boris blast out 1",
                                      'sequence': "ATGCCCCC",
                                      'extra': 'extra_goes_Here'
                                      },
                                     {'sequence_id': ">Boris2",
                                      'description': "Boris blast out 2",
                                      'sequence': "ATGGGGGG",
                                      'extra_field': 'extra_field_goes_here'
                                      }
                                     ]
                       }

        new_obj_info = self.ws.save_objects({
            'workspace': self.workspace_name,
            'objects': [{
                'type': 'KBaseSequences.SequenceSet',
                'data': sequenceSet,
                'name': output_name,
            }]
        })
        pprint(new_obj_info)
        return True

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.workspaceURL = config['workspace-url']
        self.dfu = DataFileUtil(self.callback_url)
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)
        self.scratch = config['scratch']
        self.ws = None
        self.workspace_name = None
        self.token = None
        #END_CONSTRUCTOR
        pass

    def Diamond_Blastp_Search(self, ctx, params):
        """
        Methods for BLAST of various flavors of one or more sequences against many sequences
        :param params: instance of type "Diamond_Params" (Diamond Input
           Params) -> structure: parameter "workspace_name" of type
           "workspace_name" (** The workspace object refs are of form: ** ** 
           objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_query_string" of String, parameter
           "input_object_ref" of type "data_obj_ref", parameter
           "target_object_ref" of type "data_obj_ref", parameter
           "output_sequence_set_name" of type "data_obj_name", parameter
           "output_feature_set_name" of type "data_obj_name", parameter
           "ident_thresh" of Double, parameter "e_value" of Double, parameter
           "bitscore" of Double, parameter "overlap_fraction" of Double,
           parameter "maxaccepts" of Double, parameter "output_extra_format"
           of String
        :returns: instance of type "Diamond_Output" (Diamond Output) ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN Diamond_Blastp_Search
        # workspace_name = params['workspace_name']
        #
        #
        #
        # subject_fasta_filepath = self.get_fasta_filepath(params)
        #
        # blast_parameters = {'query_fasta_filepath': query_fasta_filepath,
        #                     "subject_fasta_filepath": subject_fasta_filepath,
        #                     "blast_type": 'blastp'}
        #
        # print("About to blast")
        #
        # #blast_result = kb_diamond_blast.blast(blast_parameters)
        # #output_filepath = blast_result.output_filename
        #
        # Blast File

        self.ws = Workspace(self.workspaceURL, token=ctx['token'])
        self.workspace_name = params['workspace_name']
        self.token = ctx['token']

        query_fasta_filepath = self.get_query_fasta_filepath(params)
        # subject_fasta_filepath = self.get_query_fasta_filepath(params)

        blast = os.path.join(self.shared_folder, 'output.blast')
        with open(blast, 'w') as f:
            contents = "I am a blast"
            f.write(contents)
        # HTML File
        html_file = os.path.join(self.shared_folder, 'output.html')
        with open(html_file, 'w') as f:
            contents = "<html><body>Hello</body></html>"
            f.write(contents)

        ref = self.generate_sequence_set(blast_file=blast, query_fasta_file=query_fasta_filepath)

        # Output Files for Report
        output_file_shock_id = self.dfu.file_to_shock({'file_path': blast})['shock_id']

        output_results = list()
        output_results.append({'path': blast,
                               'name': os.path.basename(blast),
                               'label': os.path.basename(blast),
                               'description': 'Raw Blast Output File That is Not Uploaded'})

        output_results.append({'shock_id': output_file_shock_id,
                               'name': os.path.basename(blast),
                               'label': os.path.basename(blast),
                               'description': 'Shock Uploaded Blast'})

        output_results.append({'path': query_fasta_filepath,
                               'name': os.path.basename(query_fasta_filepath),
                               'label': os.path.basename(query_fasta_filepath),
                               'description': 'Query Fasta Filepath'})

        # HTML Files for Report
        report_shock_id = self.dfu.file_to_shock({'file_path': blast, 'pack': 'zip'})['shock_id']
        html_report = [{'shock_id': report_shock_id,
                        'name': os.path.basename(html_file),
                        'label': os.path.basename(html_file),
                        'description': 'HTML Version of Blast Results '}]

        report_params = {'message': 'This is a report',
                         'workspace_name': params.get('workspace_name'),
                         'objects_create': [ref],
                         'file_links': output_results,
                         'html_links': html_report,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                         'report_object_name': 'kb_diamond_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return [report_output]

        # blast_output = namedtuple("blast_output", "result output_filename search_parameters")
        # return self.generate_report(blast_result.output_filename, workspace_name)

        # blast_output = namedtuple("blast_output", "result output_filename search_parameters")
        report = []
        # for result in blast_results:
        #     stdout = result.result
        #     blast_output_file = result.output_filename
        #     search_params = result.search_parameters
        #     self.generate_report(result)

        # # Step 4 - Save the new Assembly back to the system
        # print('Uploading filtered Assembly data.')
        # new_assembly = assemblyUtil.save_assembly_from_fasta({'file': {'path': filtered_fasta_file},
        #                                                       'workspace_name': workspace_name,
        #                                                       'assembly_name': fasta_file['assembly_name']
        #                                                       })

        # results = blast_results[0]
        # report_objects = []
        # for result in blast_results:
        #     number_of_hits = self.file_len(result.output_filename)
        #     report_objects.append({
        #         'objects_created': [{'ref': result.output_filename, 'description': 'Blast Result'}],
        #         'text_message': 'Number of hits = ' + str(number_of_hits)
        #     })

        # # At some point might do deeper type checking...
        # if not isinstance(output, dict):
        #     raise ValueError("Method Diamond_Blastp_Search return value " +
        #                      "output is not type dict as required.")
        # # return the results
        # return [output]

        #END Diamond_Blastp_Search

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method Diamond_Blastp_Search return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def Diamond_Blastx_Search(self, ctx, params):
        """
        :param params: instance of type "Diamond_Params" (Diamond Input
           Params) -> structure: parameter "workspace_name" of type
           "workspace_name" (** The workspace object refs are of form: ** ** 
           objects = ws.get_objects([{'ref':
           params['workspace_id']+'/'+params['obj_name']}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_query_string" of String, parameter
           "input_object_ref" of type "data_obj_ref", parameter
           "target_object_ref" of type "data_obj_ref", parameter
           "output_sequence_set_name" of type "data_obj_name", parameter
           "output_feature_set_name" of type "data_obj_name", parameter
           "ident_thresh" of Double, parameter "e_value" of Double, parameter
           "bitscore" of Double, parameter "overlap_fraction" of Double,
           parameter "maxaccepts" of Double, parameter "output_extra_format"
           of String
        :returns: instance of type "Diamond_Output" (Diamond Output) ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN Diamond_Blastx_Search
        makedbs_output = self.makedbs(params["databases"])
        blastx_output = self.blast(params)
        output = {"success": True,
                  "makedb": makedbs_output,
                  "blast_outputs": blastx_output}
        #END Diamond_Blastx_Search

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method Diamond_Blastx_Search return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {"state": "OK",
                     "message": "",
                     "version": self.VERSION,
                     "git_url": self.GIT_URL,
                     "git_commit_hash": self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
