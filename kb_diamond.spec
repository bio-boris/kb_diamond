/*
A KBase module: kb_diamond
*/

module kb_diamond {
    /*
    ** The workspace object refs are of form:
    **
    **    objects = ws.get_objects([{'ref': params['workspace_id']+'/'+params['obj_name']}])
    **
    ** "ref" means the entire name combining the workspace id and the object name
    ** "id" is a numerical identifier of the workspace or object, and should just be used for workspace
    ** "name" is a string identifier of a workspace or object.  This is received from Narrative.
    */
    typedef string workspace_name;
    typedef string sequence;
    typedef string data_obj_name;
    typedef string data_obj_ref;


    /* Diamond Input Params
    */
    typedef structure {
        workspace_name workspace_name;
        string         input_query_string;
        data_obj_ref   input_object_ref;
        data_obj_ref   target_object_ref;
        data_obj_name  output_sequence_set_name;

        float  id;
        float  evalue;
        int    min-score;

    } Diamond_Params;

    /* Diamond Output
    */
    typedef structure {
	    string report_name;
        string report_ref;
    } Diamond_Output;

    /*  Methods for BLAST of various flavors of one or more sequences against many sequences
    */
    funcdef Diamond_Blast_Search (Diamond_Params params)  returns (Diamond_Output output) authentication required;


};
