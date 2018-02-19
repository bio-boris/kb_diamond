import cerberus
import pprint


class ValidationException(Exception):
    pass


class DiamondValidator(object):
    """
    Validate parameters for diamondValidator
    """

    def __init__(self):
        self.v = cerberus.Validator(self._build_schema())


    def _build_schema(self):
        """

        :return:
        """
        schema = {}

        integer_parameters = ["freq-sd", "band", "block-size", "max-hsps", "min-score", "top", "min-orf",
                              "subject-cover", "query-cover", "max-target-seqs", "frameshift", "gapopen", "gapextend", ]
        for int_param in integer_parameters:
            schema[int_param] = {'type': 'integer'}

        binary_parameters = ["algo", "comp-based-stats"]
        for binary_param in binary_parameters:
            schema[binary_param] = {'type': 'binary', 'min': 0, 'max': 1}

        switches = ["sensitive", "more-sensitive"]
        for boolean_parameter in switches:
            schema[boolean_parameter] = {'type': 'boolean', 'required': False}

        float_parameters_0_100 = ["range-cover", "id"]
        for int_param in float_parameters_0_100:
            schema[int_param] = {'type': 'number', 'min': 0, 'max': 100}

        float_parameters_0_1 = ["evalue"]
        for int_param in float_parameters_0_1:
            schema[int_param] = {'type': 'float', 'min': 0, 'max': 1}

        scoring_matrices = ["BLOSUM45", "BLOSUM50", "BLOSUM62", "BLOSUM80", "BLOSUM90", "PAM250", "PAM70", "PAM30"]
        performance_parameters_int = ["index-chunks"]

        narrative_parameters_string = ['workspace_name','scratch','target_object_ref','input_object_ref','input_query_string']
        for narrative_param in narrative_parameters_string:
            schema[narrative_param] = {'type': 'string'}

        schema['context'] = {'type': 'dict'}


        return schema

    def validate_input(self, params):
        """

        :param params:
        :return:
        """

        print params['context']
        validation_result = self.v.validate(params)

        if validation_result:
            return True
        else:
            raise ValidationException(self.v.errors)

