# -*- coding: utf-8 -*-
#BEGIN_HEADER
from collections import namedtuple
from subprocess import Popen, check_output, CalledProcessError
import os
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
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/bio-boris/kb_diamond.git"
    GIT_COMMIT_HASH = "79aa414d15225c84a7a34b5b468bac7faa0c94c1"

    #BEGIN_CLASS_HEADER
    fasta_file = namedtuple("fasta_file", "file_path stdin")
    diamond = "/kb/deployment/bin/diamond"
    if not os.path.isfile(diamond):
        diamond = "diamond"

    database_stats = namedtuple("database_stats", "makedb_output dbinfo_output")
    blast_output = namedtuple("blast_output", "result output_filename search_parameters")
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
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
        makedbs_output = self.makedbs(params["databases"])
        blastp_output = self.blast(params)
        output = {"success": True ,
                  "makedb" : makedbs_output,
                  "blast_outputs" : blastp_output}
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
