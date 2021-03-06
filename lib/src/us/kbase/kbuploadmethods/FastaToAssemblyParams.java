
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
 * <p>Original spec-file type: FastaToAssemblyParams</p>
 * <pre>
 * required params:
 * staging_file_subdir_path: subdirectory file path
 * e.g. 
 *   for file: /data/bulk/user_name/file_name
 *   staging_file_subdir_path is file_name
 *   for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
 *   staging_file_subdir_path is subdir_1/subdir_2/file_name
 * assembly_name: output Assembly file name
 * workspace_name: workspace name/ID of the object
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "staging_file_subdir_path",
    "assembly_name",
    "workspace_name",
    "min_contig_length"
})
public class FastaToAssemblyParams {

    @JsonProperty("staging_file_subdir_path")
    private String stagingFileSubdirPath;
    @JsonProperty("assembly_name")
    private String assemblyName;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("min_contig_length")
    private Long minContigLength;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("staging_file_subdir_path")
    public String getStagingFileSubdirPath() {
        return stagingFileSubdirPath;
    }

    @JsonProperty("staging_file_subdir_path")
    public void setStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
    }

    public FastaToAssemblyParams withStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
        return this;
    }

    @JsonProperty("assembly_name")
    public String getAssemblyName() {
        return assemblyName;
    }

    @JsonProperty("assembly_name")
    public void setAssemblyName(String assemblyName) {
        this.assemblyName = assemblyName;
    }

    public FastaToAssemblyParams withAssemblyName(String assemblyName) {
        this.assemblyName = assemblyName;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public FastaToAssemblyParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("min_contig_length")
    public Long getMinContigLength() {
        return minContigLength;
    }

    @JsonProperty("min_contig_length")
    public void setMinContigLength(Long minContigLength) {
        this.minContigLength = minContigLength;
    }

    public FastaToAssemblyParams withMinContigLength(Long minContigLength) {
        this.minContigLength = minContigLength;
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
        return ((((((((((("FastaToAssemblyParams"+" [stagingFileSubdirPath=")+ stagingFileSubdirPath)+", assemblyName=")+ assemblyName)+", workspaceName=")+ workspaceName)+", minContigLength=")+ minContigLength)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
