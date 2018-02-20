
package us.kbase.kbdiamond;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: Diamond_Params</p>
 * <pre>
 * Diamond Input Params
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_query_string",
    "input_object_ref",
    "target_object_ref",
    "output_sequence_set_name",
    "id",
    "evalue",
    "min-score"
})
public class DiamondParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_query_string")
    private String inputQueryString;
    @JsonProperty("input_object_ref")
    private String inputObjectRef;
    @JsonProperty("target_object_ref")
    private String targetObjectRef;
    @JsonProperty("output_sequence_set_name")
    private String outputSequenceSetName;
    @JsonProperty("id")
    private Double id;
    @JsonProperty("evalue")
    private Double evalue;
    @JsonProperty("min-score")
    private Long minScore;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public DiamondParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_query_string")
    public String getInputQueryString() {
        return inputQueryString;
    }

    @JsonProperty("input_query_string")
    public void setInputQueryString(String inputQueryString) {
        this.inputQueryString = inputQueryString;
    }

    public DiamondParams withInputQueryString(String inputQueryString) {
        this.inputQueryString = inputQueryString;
        return this;
    }

    @JsonProperty("input_object_ref")
    public String getInputObjectRef() {
        return inputObjectRef;
    }

    @JsonProperty("input_object_ref")
    public void setInputObjectRef(String inputObjectRef) {
        this.inputObjectRef = inputObjectRef;
    }

    public DiamondParams withInputObjectRef(String inputObjectRef) {
        this.inputObjectRef = inputObjectRef;
        return this;
    }

    @JsonProperty("target_object_ref")
    public String getTargetObjectRef() {
        return targetObjectRef;
    }

    @JsonProperty("target_object_ref")
    public void setTargetObjectRef(String targetObjectRef) {
        this.targetObjectRef = targetObjectRef;
    }

    public DiamondParams withTargetObjectRef(String targetObjectRef) {
        this.targetObjectRef = targetObjectRef;
        return this;
    }

    @JsonProperty("output_sequence_set_name")
    public String getOutputSequenceSetName() {
        return outputSequenceSetName;
    }

    @JsonProperty("output_sequence_set_name")
    public void setOutputSequenceSetName(String outputSequenceSetName) {
        this.outputSequenceSetName = outputSequenceSetName;
    }

    public DiamondParams withOutputSequenceSetName(String outputSequenceSetName) {
        this.outputSequenceSetName = outputSequenceSetName;
        return this;
    }

    @JsonProperty("id")
    public Double getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(Double id) {
        this.id = id;
    }

    public DiamondParams withId(Double id) {
        this.id = id;
        return this;
    }

    @JsonProperty("evalue")
    public Double getEvalue() {
        return evalue;
    }

    @JsonProperty("evalue")
    public void setEvalue(Double evalue) {
        this.evalue = evalue;
    }

    public DiamondParams withEvalue(Double evalue) {
        this.evalue = evalue;
        return this;
    }

    @JsonProperty("min-score")
    public Long getMinScore() {
        return minScore;
    }

    @JsonProperty("min-score")
    public void setMinScore(Long minScore) {
        this.minScore = minScore;
    }

    public DiamondParams withMinScore(Long minScore) {
        this.minScore = minScore;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((("DiamondParams"+" [workspaceName=")+ workspaceName)+", inputQueryString=")+ inputQueryString)+", inputObjectRef=")+ inputObjectRef)+", targetObjectRef=")+ targetObjectRef)+", outputSequenceSetName=")+ outputSequenceSetName)+", id=")+ id)+", evalue=")+ evalue)+", minScore=")+ minScore)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
