/*
A KBase module: AbstractHandle
*/

module AbstractHandle {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /* Handle provides a unique reference that enables
       access to the data files through functions
       provided as part of the HandleService. In the case of using
       shock, the id is the node id. In the case of using
       shock the value of type is shock. In the future
       these values should enumerated. The value of url is
       the http address of the shock server, including the
       protocol (http or https) and if necessary the port.
       The values of remote_md5 and remote_sha1 are those
       computed on the file in the remote data store. These
       can be used to verify uploads and downloads.
    */
    typedef string HandleId;
    typedef string NodeId;

    typedef structure {
      HandleId hid;
      string file_name;
      NodeId id;
      string type;
      string url;
      string remote_md5;
      string remote_sha1;
    } Handle;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_handle_service2(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
