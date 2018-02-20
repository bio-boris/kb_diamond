import cerberus
from pprint import pprint


class ValidationException(Exception):
    pass


class DiamondValidator(object):
    """
    Validate parameters for diamondValidator
    """

    narrative_parameters = ["scratch", "target_object_ref", "input_object_ref",
                            "input_query_string", "context", "workspace_name", 'output_feature_set_name',
                            'output_sequence_set_name']
    blast_params = {}
    narrative_params = {}
    valid = False

    def __init__(self, params):
        self.narrative_ui_schema = self._build_narrative_ui_schema()
        self.blast_schema = self._build_blast_schema()
        self.narrative_ui = cerberus.Validator(self.narrative_ui_schema)
        self.blast_validator = cerberus.Validator(self.blast_schema)
        self.valid = self._validate_input(params)



    def _build_blast_schema(self):
        """

        :return:
        """
        schema = {}

        integer_parameters = ["freq-sd", "band", "block-size", "max-hsps", "min-score", "top", "min-orf",
                              "subject-cover", "query-cover", "max-target-seqs", "frameshift", "gapopen", "gapextend", ]
        for int_param in integer_parameters:
            schema[int_param] = {"type": "integer"}

        binary_parameters = ["algo", "comp-based-stats"]
        for binary_param in binary_parameters:
            schema[binary_param] = {"type": "binary", "min": 0, "max": 1}

        switches = ["sensitive", "more-sensitive"]
        for boolean_parameter in switches:
            schema[boolean_parameter] = {"type": "boolean", "required": False}

        float_parameters_0_100 = ["range-cover", "id"]
        for int_param in float_parameters_0_100:
            schema[int_param] = {"type": "number", "min": 0, "max": 100}

        float_parameters_0_1 = ["evalue"]
        for int_param in float_parameters_0_1:
            schema[int_param] = {"type": "float", "min": 0, "max": 1}

        return schema

    def _build_narrative_ui_schema(self):
        schema = dict()
        for nsp in self.narrative_parameters:
            schema[nsp] = {"type": "string"}
        schema["context"] = {"type": "dict"}
        return schema

    def _validate_input(self, params):
        """

        :param params:
        :return:
        """
        empty_params = []
        for item in params:
            if params[item] is None or params[item] == "":
                empty_params.append(item)

        for item in empty_params:
            del(params[item])

        for item in params.keys():
            if item in self.narrative_parameters:
                self.narrative_params[item] = params[item]
            else:
                self.blast_params[item] = params[item]

        if not self.narrative_ui.validate(self.narrative_params):
            raise ValidationException(self.narrative_ui.errors)
        if not self.blast_validator.validate(self.blast_params):
            raise ValidationException(self.blast_validator.errors)

        return True


