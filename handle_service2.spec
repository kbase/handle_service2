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

    /* The persist_handle writes the handle to a persistent store
       that can be later retrieved using the list_handles
       function.
    */
    funcdef persist_handle(Handle h) returns (HandleId hid) authentication required;

    /* Given a list of handle ids, this function returns a list of handles.
       This function is deprecated and replaced by fetch_handles_by.
    */
    funcdef hids_to_handles(list<HandleId> hids) returns(list<Handle> handles) authentication required;

    /* Given a list of ids, this function returns a list of handles.
       In case of Shock, the list of ids are shock node ids and this function the handles, which
             contains Shock url and related information.
       This function is deprecated and replaced by fetch_handles_by.
    */
    funcdef ids_to_handles(list<NodeId> ids) returns (list<Handle> handles) authentication required;

    typedef structure {
      list<string> elements;
      string key_name;
    } FetchHandlesParams;

    /* Given a list of elements, this function search elements with key_name column and returns a list of handles.
    */
    funcdef fetch_handles_by(FetchHandlesParams params) returns (list<Handle> handles) authentication required;

    /* Given a list of handle ids, this function determines if the underlying
       data is owned by the caller. If any one of the handle ids reference
       unreadable data this function returns false.
    */
    funcdef is_owner(list<HandleId>) returns(int) authentication required;

    /* The delete_handles function takes a list of handles
       and deletes them on the handle service server.
    */
    funcdef delete_handles(list<Handle> handles) returns (list<HandleId> hids) authentication required;

};
