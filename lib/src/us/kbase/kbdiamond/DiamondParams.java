
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
    "output_feature_set_name",
    "ident_thresh",
    "e_value",
    "bitscore",
    "overlap_fraction",
    "maxaccepts",
    "output_extra_format"
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
    @JsonProperty("output_feature_set_name")
    private String outputFeatureSetName;
    @JsonProperty("ident_thresh")
    private Double identThresh;
    @JsonProperty("e_value")
    private Double eValue;
    @JsonProperty("bitscore")
    private Double bitscore;
    @JsonProperty("overlap_fraction")
    private Double overlapFraction;
    @JsonProperty("maxaccepts")
    private Double maxaccepts;
    @JsonProperty("output_extra_format")
    private String outputExtraFormat;
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

    @JsonProperty("output_feature_set_name")
    public String getOutputFeatureSetName() {
        return outputFeatureSetName;
    }

    @JsonProperty("output_feature_set_name")
    public void setOutputFeatureSetName(String outputFeatureSetName) {
        this.outputFeatureSetName = outputFeatureSetName;
    }

    public DiamondParams withOutputFeatureSetName(String outputFeatureSetName) {
        this.outputFeatureSetName = outputFeatureSetName;
        return this;
    }

    @JsonProperty("ident_thresh")
    public Double getIdentThresh() {
        return identThresh;
    }

    @JsonProperty("ident_thresh")
    public void setIdentThresh(Double identThresh) {
        this.identThresh = identThresh;
    }

    public DiamondParams withIdentThresh(Double identThresh) {
        this.identThresh = identThresh;
        return this;
    }

    @JsonProperty("e_value")
    public Double getEValue() {
        return eValue;
    }

    @JsonProperty("e_value")
    public void setEValue(Double eValue) {
        this.eValue = eValue;
    }

    public DiamondParams withEValue(Double eValue) {
        this.eValue = eValue;
        return this;
    }

    @JsonProperty("bitscore")
    public Double getBitscore() {
        return bitscore;
    }

    @JsonProperty("bitscore")
    public void setBitscore(Double bitscore) {
        this.bitscore = bitscore;
    }

    public DiamondParams withBitscore(Double bitscore) {
        this.bitscore = bitscore;
        return this;
    }

    @JsonProperty("overlap_fraction")
    public Double getOverlapFraction() {
        return overlapFraction;
    }

    @JsonProperty("overlap_fraction")
    public void setOverlapFraction(Double overlapFraction) {
        this.overlapFraction = overlapFraction;
    }

    public DiamondParams withOverlapFraction(Double overlapFraction) {
        this.overlapFraction = overlapFraction;
        return this;
    }

    @JsonProperty("maxaccepts")
    public Double getMaxaccepts() {
        return maxaccepts;
    }

    @JsonProperty("maxaccepts")
    public void setMaxaccepts(Double maxaccepts) {
        this.maxaccepts = maxaccepts;
    }

    public DiamondParams withMaxaccepts(Double maxaccepts) {
        this.maxaccepts = maxaccepts;
        return this;
    }

    @JsonProperty("output_extra_format")
    public String getOutputExtraFormat() {
        return outputExtraFormat;
    }

    @JsonProperty("output_extra_format")
    public void setOutputExtraFormat(String outputExtraFormat) {
        this.outputExtraFormat = outputExtraFormat;
    }

    public DiamondParams withOutputExtraFormat(String outputExtraFormat) {
        this.outputExtraFormat = outputExtraFormat;
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
        return ((((((((((((((((((((((((((("DiamondParams"+" [workspaceName=")+ workspaceName)+", inputQueryString=")+ inputQueryString)+", inputObjectRef=")+ inputObjectRef)+", targetObjectRef=")+ targetObjectRef)+", outputSequenceSetName=")+ outputSequenceSetName)+", outputFeatureSetName=")+ outputFeatureSetName)+", identThresh=")+ identThresh)+", eValue=")+ eValue)+", bitscore=")+ bitscore)+", overlapFraction=")+ overlapFraction)+", maxaccepts=")+ maxaccepts)+", outputExtraFormat=")+ outputExtraFormat)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
