
package us.kbase.kbuploadmethods;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: FileToConditionSetParams</p>
 * <pre>
 * required params:
 * staging_file_subdir_path: subdirectory file path
 * e.g.
 *   for file: /data/bulk/user_name/file_name
 *   staging_file_subdir_path is file_name
 *   for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
 *   staging_file_subdir_path is subdir_1/subdir_2/file_name
 * condition_set_name: output ConditionSet object name
 * workspace_id: workspace name/ID of the object
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "staging_file_subdir_path",
    "workspace_id",
    "condition_set_name"
})
public class FileToConditionSetParams {

    @JsonProperty("staging_file_subdir_path")
    private String stagingFileSubdirPath;
    @JsonProperty("workspace_id")
    private String workspaceId;
    @JsonProperty("condition_set_name")
    private String conditionSetName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("staging_file_subdir_path")
    public String getStagingFileSubdirPath() {
        return stagingFileSubdirPath;
    }

    @JsonProperty("staging_file_subdir_path")
    public void setStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
    }

    public FileToConditionSetParams withStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
        return this;
    }

    @JsonProperty("workspace_id")
    public String getWorkspaceId() {
        return workspaceId;
    }

    @JsonProperty("workspace_id")
    public void setWorkspaceId(String workspaceId) {
        this.workspaceId = workspaceId;
    }

    public FileToConditionSetParams withWorkspaceId(String workspaceId) {
        this.workspaceId = workspaceId;
        return this;
    }

    @JsonProperty("condition_set_name")
    public String getConditionSetName() {
        return conditionSetName;
    }

    @JsonProperty("condition_set_name")
    public void setConditionSetName(String conditionSetName) {
        this.conditionSetName = conditionSetName;
    }

    public FileToConditionSetParams withConditionSetName(String conditionSetName) {
        this.conditionSetName = conditionSetName;
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
        return ((((((((("FileToConditionSetParams"+" [stagingFileSubdirPath=")+ stagingFileSubdirPath)+", workspaceId=")+ workspaceId)+", conditionSetName=")+ conditionSetName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
