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
from biokbase.workspace.client import Workspace as workspaceService
# from KBaseDataObjectToFileUtils.KBaseDataObjectToFileUtilsClient import KBaseDataObjectToFileUtils
# from DataFileUtil.DataFileUtilClient import DataFileUtil as DFUClient
# from KBaseReport.KBaseReportClient import KBaseReport
# from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
# from kb_diamond.kb_diamondServer import MethodContext
# from kb_diamond.kb_diamondImpl import kb_diamond
# from kb_diamond.authclient import KBaseAuth as _KBaseAuth
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
import kb_diamond_blast
from KBaseReport.KBaseReportClient import KBaseReport


#END_HEADER

class kb_diamond:
    """
    Module Name:
    kb_diamond

    Module Description:
    A KBase module: kb_diamond
    """

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/bio-boris/kb_diamond.git"
    GIT_COMMIT_HASH = "a914f9a9d486ed6c2e0739580e27b386b0d1faad"

    #BEGIN_CLASS_HEADER
    fasta_file = namedtuple("fasta_file", "file_path stdin")
    diamond = "/kb/deployment/bin/diamond"
    if not os.path.isfile(diamond):
        diamond = "diamond"

    database_stats = namedtuple("database_stats", "makedb_output dbinfo_output")
    blast_output = namedtuple("blast_output", "result output_filename search_parameters")


    def get_fasta_filepath(self,params):
        if 'input_one_sequence' in params:
            sequence = params['input_one_sequence']
            filename = os.path.join(self.shared_folder, 'STDIN.fasta')
            with open(filename, "w") as a:
                a.write(sequence)
                a.close()
            return filename

        if 'assembly_input_ref' in params:
            assembly_input_ref = params['assembly_input_ref']
            pass

        raise ValueError('No genetic sequence string or reference file was provided')



        #Object Input

    def saveFileToScratch(self,file_path):
        output_path = os.path.join(self.shared_folder, file_path)
        print("Saving to " + output_path)
        os.rename(file_path, output_path)
        return output_path


    def file_len(self,fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def generate_report(self, output_file, workspace_name):
        """
        
        :param output_file: 
        :param workspace_name: 
        :return: 
        """
        output_files = []

        output_files.append({'path': output_file,
                             'name': os.path.basename(output_file),
                             'label': os.path.basename(output_file),
                             'description': 'Blast Output'})

        output_html_files = []


        objects_created = []


        report_params = {'message': '',
                         'workspace_name': workspace_name,
                         'objects_created': objects_created,
                         'file_links': output_files,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                         'report_object_name': 'kb_deseq2_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output


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


    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn"t
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR




    def Diamond_Blastp_Search(self, ctx, params):
        """
        Methods for BLAST of various flavors of one or more sequences against many sequences
        :param params: instance of type "Diamond_Params" (Diamond Input
           Params) -> structure: parameter "workspace_name" of type
           "workspace_name" (** The workspace object refs are of form: ** **
           objects = ws.get_objects([{"ref":
           params["workspace_id"]+"/"+params["obj_name"]}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_one_sequence" of type "sequence", parameter
           "input_one_ref" of type "data_obj_ref", parameter "input_many_ref"
           of type "data_obj_ref", parameter "output_one_name" of type
           "data_obj_name", parameter "output_filtered_name" of type
           "data_obj_name", parameter "ident_thresh" of Double, parameter
           "e_value" of Double, parameter "bitscore" of Double, parameter
           "overlap_fraction" of Double, parameter "maxaccepts" of Double,
           parameter "output_extra_format" of String
        :returns: instance of type "Diamond_Output" (Diamond Output) ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output

        #BEGIN Diamond_Blastp_Search
        workspace_name = params['workspace_name']

        query_fasta_filepath = self.get_fasta_filepath(params)
        subject_fasta_filepath = self.get_fasta_filepath(params)

        blast_parameters = {'query_fasta_filepath': query_fasta_filepath,
                            "subject_fasta_filepath": subject_fasta_filepath,
                            "blast_type": 'blastp'}

        print("About to blast")

        blast_result = kb_diamond_blast.blast(blast_parameters)

        #blast_output = namedtuple("blast_output", "result output_filename search_parameters")
        return self.generate_report(blast_result.output_filename, workspace_name)

        
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

        report_output = self.generate_report(blast_results[0].output_filename,workspace_name)



        # STEP 6: contruct the output to send back
        output = {'report_name': report_output['report_name'],
                  'report_ref': report_output['report_ref'],
                  'inputs': [query_fasta_filepath, subject_database_filepath],
                  'blast_results': blast_results
                  }
        print('returning:' + pformat(output))





        # k = kb_diamond_blast()
        #
        # file_utils = KBaseDataObjectToFileUtils(url=params['callback_url'], token=ctx['token'])
        # workspace_service = workspaceService(self.workspaceURL, token=ctx['token'])
        # makedbs_output = k.make_db_from_object_ref(params,file_utils,workspace_service)

        #
        # return makedbs_output
        # blastp_output = k.blast(params,file_utils)
        # output = {"success": True ,
        #           "makedb" : makedbs_output,
        #           "blast_outputs" : blastp_output}

        #
        # # At some point might do deeper type checking...
        # if not isinstance(output, dict):
        #     raise ValueError("Method Diamond_Blastp_Search return value " +
        #                      "output is not type dict as required.")
        # # return the results
        # return [output]

        #END Diamond_Blastp_Search

    def check_output(self,blast):
        return blast


    def Diamond_Blastx_Search(self, ctx, params):
        """
        :param params: instance of type "Diamond_Params" (Diamond Input
           Params) -> structure: parameter "workspace_name" of type
           "workspace_name" (** The workspace object refs are of form: ** **
           objects = ws.get_objects([{"ref":
           params["workspace_id"]+"/"+params["obj_name"]}]) ** ** "ref" means
           the entire name combining the workspace id and the object name **
           "id" is a numerical identifier of the workspace or object, and
           should just be used for workspace ** "name" is a string identifier
           of a workspace or object.  This is received from Narrative.),
           parameter "input_one_sequence" of type "sequence", parameter
           "input_one_ref" of type "data_obj_ref", parameter "input_many_ref"
           of type "data_obj_ref", parameter "output_one_name" of type
           "data_obj_name", parameter "output_filtered_name" of type
           "data_obj_name", parameter "ident_thresh" of Double, parameter
           "e_value" of Double, parameter "bitscore" of Double, parameter
           "overlap_fraction" of Double, parameter "maxaccepts" of Double,
           parameter "output_extra_format" of String
        :returns: instance of type "Diamond_Output" (Diamond Output) ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN Diamond_Blastx_Search
        makedbs_output = self.makedbs(params["databases"])
        blastx_output = self.blast(params)
        output = {"success": True ,
                  "makedb" : makedbs_output,
                  "blast_outputs" : blastx_output}
        #END Diamond_Blastx_Search

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError("Method Diamond_Blastx_Search return value " +
                             "output is not type dict as required.")
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

    def process_params(self, params):
        valid_commands = ["makedb", "blastp", "blastx", "view", "version", "dbinfo", "help"]
        makedb_options = ["in", "db"]
        general_options = ["threads"]
        output_options = ["out"]
        return True

    # TODO Support <STDIN> sequence collections
    # TODO Error Handling
    def makedbs(self, filenames):
        """
        Create database for diamond search from a list of input files
        :param filenames:
        :return:
        """
        status = {}
        for filename in filenames:
            status[filename] = self.database_stats(self.makedb(filename),
                                                   self.dbinfo(filename))
        return status

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
            except CalledProcessError as e :
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
            os.remove()

