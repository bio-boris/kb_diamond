# -*- coding: utf-8 -*-
#BEGIN_HEADER
from collections import namedtuple,defaultdict
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
from Bio import SeqIO
from KBaseDataObjectToFileUtils.KBaseDataObjectToFileUtilsClient import KBaseDataObjectToFileUtils


class FastaException(Exception):
    pass


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


    def genome_cds_to_fasta(self, object_ref):
        GenomeToFASTA_params = {
            'genome_ref': object_ref,
            'file': str(uuid.uuid4()) + ".fasta",
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
        #print("About to write fasta")
        DOTFU = KBaseDataObjectToFileUtils(url=self.callback_url, token=self.token)
        output = DOTFU.GenomeToFASTA(GenomeToFASTA_params)

        if len(output['feature_ids']) > 0:
            return output['fasta_file_path']

        raise FastaException('No features found in genome')





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
        elif input_type in ['GenomeSet', 'FeatureSet', 'ContigSet', 'Assembly']:
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
        elif 'target_object_ref' in params:
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


    def create_sequence_set(self, **sequence_set_parameters):
        fasta_filepath = sequence_set_parameters['fasta_filepath']
        output_filename = sequence_set_parameters['output_filename']
        sequence_set_id = sequence_set_parameters['sequence_set_id']
        sequence_set_description = sequence_set_parameters['sequence_set_description']

        sequences = list()
        for record in SeqIO.parse(fasta_filepath, "fasta"):
            sequences.append
            {'sequence_id': record.id, 'description': '', 'sequence': str(record.seq)}

        new_obj_info=self.ws.save_objects({
            'workspace': self.workspace_name,
            'objects': [{
                'type': 'KBaseSequences.SequenceSet',
                'data': {'sequence_set_id': sequence_set_id, 'description': sequence_set_description,
                         'sequences': sequences},
                'name': 'seqset_'+str(uuid.uuid4())
            }]
        })[0]
        return {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]),
                'description' : 'Sequence Set for ' + output_filename}


    def fasta_to_dict(self,filename):
        print("Saving fasta" + filename)
        records = {}
        for record in SeqIO.parse(filename, "fasta"):
            if record.id in records:
                print("Error, key already exists")  # Log or do something here
            records[record.id] = str(record.seq)
        return records

    def fasta_to_dict_alternative(self,filename):
        print("Saving fasta" + filename)
        records = {}
        for record in SeqIO.parse(filename, "fasta"):
            id = record.id.split(" ")[0]
            if id in records:
                print("Error, key already exists")  # Log or do something here
            records[id] = str(record.seq)
        return records


    def generate_blast_results_set(self,output_parameters):
        blast_file = output_parameters['blast_file']
        query_fasta_file = output_parameters['query_fasta_file']
        subject_fasta_file = output_parameters['subject_fasta_file']

        queries = self.fasta_to_dict(query_fasta_file)
        #queries_alternative = self.fasta_to_dict_alternative(query_fasta_file)

        subjects = self.fasta_to_dict(subject_fasta_file)
        #subjects_alternative = self.fasta_to_dict_alternative(subject_fasta_file)

        keys = ['qseqid','sseqid','pident','length','mismatch',
                'gapopen','qstart','qend','sstart','send','evalue','bitscore']

        blast_results = list()

        with open(blast_file) as bf:
            for line in bf:
                values = line.split("\t")
                blast_result_line = dict(zip(keys, values))
                qseqid = blast_result_line['qseqid']
                sseqid = blast_result_line['sseqid']

                if qseqid in queries:
                    query_seq = queries[qseqid]
                else:
                    query_seq = 'Not Found'

                if sseqid in subjects:
                    target_seq = subjects[sseqid]
                else:
                    target_seq = 'Not Found'

                blast_results.append(
                    {'description': '',
                     'sequence_id': qseqid,
                     'sequence': query_seq,
                     'target_sequence_id': sseqid,
                     'target_sequence': target_seq,
                     'blast_output': blast_result_line})


        #pprint(blast_results)

        new_obj_info =  self.ws.save_objects({
            'workspace': self.workspace_name,
            'objects': [{
                'type': 'KBaseSequences.SequenceSet',
                'data': {'sequence_set_id': 'sequence_set_id', 'description': 'sequence_set_description',
                         'sequences': blast_results},
                'name': "blast_"+str(uuid.uuid4()),
            }]
        })[0]
        return {'ref':str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]),
                'description' : 'output_blast' }


    def generate_sequence_set(self, **output_parameters):
        blast_file = output_parameters['blast_file']
        query_fasta_file = output_parameters['query_fasta_file']
        subject_fasta_file = output_parameters['subject_fasta_file']
        output_sequence_set_name = output_parameters['output_sequence_set_name']

        created_objects = list()
        if output_sequence_set_name is not None:
            created_objects.append(self.create_sequence_set(fasta_filepath=query_fasta_file,
                                     output_filename=output_sequence_set_name,
                                     sequence_set_id=output_sequence_set_name,
                                     sequence_set_description='INPUT QUERY FASTA'))

        created_objects.append(self.create_sequence_set(fasta_filepath=subject_fasta_file,
                                output_filename=os.path.basename(subject_fasta_file),
                                sequence_set_id=os.path.basename(subject_fasta_file),
                                sequence_set_description='TARGET FASTA'))

        created_objects.append(self.generate_blast_results_set(output_parameters))

        return created_objects

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

        self.ws = Workspace(self.workspaceURL, token=ctx['token'])
        self.workspace_name = params['workspace_name']
        self.token = ctx['token']




        if 'input_query_string' in params:
            query_fasta_filepath = os.path.join(self.shared_folder, 'STDIN.fasta')
            with open(query_fasta_filepath, "w") as a:
                a.write(params['input_query_string'])
                a.close()
            return query_fasta_filepath
            del params['input_object_ref']
        elif 'input_object_ref' in params:
            query_fasta_filepath = self.get_fasta_from_query_object(params['input_object_ref'])

        #subject_fasta_filepath = self.get_fasta_from_query_object(params['target_object_ref'])
        subject_fasta_filepath = query_fasta_filepath


        blast_parameters = {'query_fasta_filepath': query_fasta_filepath,
                              "subject_fasta_filepath": subject_fasta_filepath,
                              "blast_type": 'blastp'}

        blast_result = kb_diamond_blast.blast(blast_parameters).output_filename



        # HTML File
        html_file = os.path.join(self.shared_folder, 'output.html')
        with open(html_file, 'w') as f:
            contents = "<html><body>Hello</body></html>"
            f.write(contents)

        output_sequence_set = params['output_sequence_set_name'] if 'output_sequence_set_name' in params else None

        objects_created = self.generate_sequence_set(blast_file=blast_result, query_fasta_file=query_fasta_filepath,
                                   subject_fasta_file=subject_fasta_filepath,
                                   output_sequence_set_name=output_sequence_set)

        # Upload Blast File
        output_results = list()

        output_file_shock_id = self.dfu.file_to_shock({'file_path': blast_result})['shock_id']
        output_results.append({'shock_id': output_file_shock_id,
                               'name': os.path.basename(blast),
                               'label': os.path.basename(blast),
                               'description': 'Shock Uploaded Blast'})

        # HTML Files for Report
        report_shock_id = self.dfu.file_to_shock({'file_path': html_file, 'pack': 'zip'})['shock_id']
        html_report = [{'shock_id': report_shock_id,
                        'name': os.path.basename(html_file),
                        'label': os.path.basename(html_file),
                        'description': 'HTML Version of Blast Results '}]

        report_params = {'message': 'This is a report',
                         'workspace_name': params.get('workspace_name'),
                         'objects_created': objects_created,
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
