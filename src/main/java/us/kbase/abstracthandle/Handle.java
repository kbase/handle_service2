
package us.kbase.abstracthandle;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: Handle</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "hid",
    "file_name",
    "id",
    "type",
    "url",
    "remote_md5",
    "remote_sha1"
})
public class Handle {

    @JsonProperty("hid")
    private String hid;
    @JsonProperty("file_name")
    private String fileName;
    @JsonProperty("id")
    private String id;
    @JsonProperty("type")
    private String type;
    @JsonProperty("url")
    private String url;
    @JsonProperty("remote_md5")
    private String remoteMd5;
    @JsonProperty("remote_sha1")
    private String remoteSha1;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("hid")
    public String getHid() {
        return hid;
    }

    @JsonProperty("hid")
    public void setHid(String hid) {
        this.hid = hid;
    }

    public Handle withHid(String hid) {
        this.hid = hid;
        return this;
    }

    @JsonProperty("file_name")
    public String getFileName() {
        return fileName;
    }

    @JsonProperty("file_name")
    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public Handle withFileName(String fileName) {
        this.fileName = fileName;
        return this;
    }

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public Handle withId(String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("type")
    public String getType() {
        return type;
    }

    @JsonProperty("type")
    public void setType(String type) {
        this.type = type;
    }

    public Handle withType(String type) {
        this.type = type;
        return this;
    }

    @JsonProperty("url")
    public String getUrl() {
        return url;
    }

    @JsonProperty("url")
    public void setUrl(String url) {
        this.url = url;
    }

    public Handle withUrl(String url) {
        this.url = url;
        return this;
    }

    @JsonProperty("remote_md5")
    public String getRemoteMd5() {
        return remoteMd5;
    }

    @JsonProperty("remote_md5")
    public void setRemoteMd5(String remoteMd5) {
        this.remoteMd5 = remoteMd5;
    }

    public Handle withRemoteMd5(String remoteMd5) {
        this.remoteMd5 = remoteMd5;
        return this;
    }

    @JsonProperty("remote_sha1")
    public String getRemoteSha1() {
        return remoteSha1;
    }

    @JsonProperty("remote_sha1")
    public void setRemoteSha1(String remoteSha1) {
        this.remoteSha1 = remoteSha1;
    }

    public Handle withRemoteSha1(String remoteSha1) {
        this.remoteSha1 = remoteSha1;
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
        return ((((((((((((((((("Handle"+" [hid=")+ hid)+", fileName=")+ fileName)+", id=")+ id)+", type=")+ type)+", url=")+ url)+", remoteMd5=")+ remoteMd5)+", remoteSha1=")+ remoteSha1)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
