# -*- coding: utf-8 -*-
#BEGIN_HEADER
#END_HEADER


class AbstractHandle:
    '''
    Module Name:
    AbstractHandle

    Module Description:
    A KBase module: AbstractHandle
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:Tianhao-Gu/handle_service2.git"
    GIT_COMMIT_HASH = "709e5996cac4f5bed5319f2841eb8d0bf04368f4"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.handleURL = config['handle-service-url']
        #END_CONSTRUCTOR
        pass


    def persist_handle(self, ctx, h):
        """
        The persist_handle writes the handle to a persistent store
        that can be later retrieved using the list_handles
        function.
        :param h: instance of type "Handle" -> structure: parameter "hid" of
           type "HandleId" (Handle provides a unique reference that enables
           access to the data files through functions provided as part of the
           HandleService. In the case of using shock, the id is the node id.
           In the case of using shock the value of type is shock. In the
           future these values should enumerated. The value of url is the
           http address of the shock server, including the protocol (http or
           https) and if necessary the port. The values of remote_md5 and
           remote_sha1 are those computed on the file in the remote data
           store. These can be used to verify uploads and downloads.),
           parameter "file_name" of String, parameter "id" of type "NodeId",
           parameter "type" of String, parameter "url" of String, parameter
           "remote_md5" of String, parameter "remote_sha1" of String
        :returns: instance of type "HandleId" (Handle provides a unique
           reference that enables access to the data files through functions
           provided as part of the HandleService. In the case of using shock,
           the id is the node id. In the case of using shock the value of
           type is shock. In the future these values should enumerated. The
           value of url is the http address of the shock server, including
           the protocol (http or https) and if necessary the port. The values
           of remote_md5 and remote_sha1 are those computed on the file in
           the remote data store. These can be used to verify uploads and
           downloads.)
        """
        # ctx is the context object
        # return variables are: hid
        #BEGIN persist_handle
        #END persist_handle

        # At some point might do deeper type checking...
        if not isinstance(hid, str):
            raise ValueError('Method persist_handle return value ' +
                             'hid is not type str as required.')
        # return the results
        return [hid]

    def hids_to_handles(self, ctx, hids):
        """
        Given a list of handle ids, this function returns a list of handles.
        This function is deprecated and replaced by fetch_handles_by.
        :param hids: instance of list of type "HandleId" (Handle provides a
           unique reference that enables access to the data files through
           functions provided as part of the HandleService. In the case of
           using shock, the id is the node id. In the case of using shock the
           value of type is shock. In the future these values should
           enumerated. The value of url is the http address of the shock
           server, including the protocol (http or https) and if necessary
           the port. The values of remote_md5 and remote_sha1 are those
           computed on the file in the remote data store. These can be used
           to verify uploads and downloads.)
        :returns: instance of list of type "Handle" -> structure: parameter
           "hid" of type "HandleId" (Handle provides a unique reference that
           enables access to the data files through functions provided as
           part of the HandleService. In the case of using shock, the id is
           the node id. In the case of using shock the value of type is
           shock. In the future these values should enumerated. The value of
           url is the http address of the shock server, including the
           protocol (http or https) and if necessary the port. The values of
           remote_md5 and remote_sha1 are those computed on the file in the
           remote data store. These can be used to verify uploads and
           downloads.), parameter "file_name" of String, parameter "id" of
           type "NodeId", parameter "type" of String, parameter "url" of
           String, parameter "remote_md5" of String, parameter "remote_sha1"
           of String
        """
        # ctx is the context object
        # return variables are: handles
        #BEGIN hids_to_handles
        #END hids_to_handles

        # At some point might do deeper type checking...
        if not isinstance(handles, list):
            raise ValueError('Method hids_to_handles return value ' +
                             'handles is not type list as required.')
        # return the results
        return [handles]

    def ids_to_handles(self, ctx, ids):
        """
        Given a list of ids, this function returns a list of handles.
        In case of Shock, the list of ids are shock node ids and this function the handles, which
              contains Shock url and related information.
        This function is deprecated and replaced by fetch_handles_by.
        :param ids: instance of list of type "NodeId"
        :returns: instance of list of type "Handle" -> structure: parameter
           "hid" of type "HandleId" (Handle provides a unique reference that
           enables access to the data files through functions provided as
           part of the HandleService. In the case of using shock, the id is
           the node id. In the case of using shock the value of type is
           shock. In the future these values should enumerated. The value of
           url is the http address of the shock server, including the
           protocol (http or https) and if necessary the port. The values of
           remote_md5 and remote_sha1 are those computed on the file in the
           remote data store. These can be used to verify uploads and
           downloads.), parameter "file_name" of String, parameter "id" of
           type "NodeId", parameter "type" of String, parameter "url" of
           String, parameter "remote_md5" of String, parameter "remote_sha1"
           of String
        """
        # ctx is the context object
        # return variables are: handles
        #BEGIN ids_to_handles
        #END ids_to_handles

        # At some point might do deeper type checking...
        if not isinstance(handles, list):
            raise ValueError('Method ids_to_handles return value ' +
                             'handles is not type list as required.')
        # return the results
        return [handles]

    def fetch_handles_by(self, ctx, params):
        """
        Given a list of elements, this function search elements with key_name column and returns a list of handles.
        :param params: instance of type "FetchHandlesParams" -> structure:
           parameter "elements" of list of String, parameter "key_name" of
           String
        :returns: instance of list of type "Handle" -> structure: parameter
           "hid" of type "HandleId" (Handle provides a unique reference that
           enables access to the data files through functions provided as
           part of the HandleService. In the case of using shock, the id is
           the node id. In the case of using shock the value of type is
           shock. In the future these values should enumerated. The value of
           url is the http address of the shock server, including the
           protocol (http or https) and if necessary the port. The values of
           remote_md5 and remote_sha1 are those computed on the file in the
           remote data store. These can be used to verify uploads and
           downloads.), parameter "file_name" of String, parameter "id" of
           type "NodeId", parameter "type" of String, parameter "url" of
           String, parameter "remote_md5" of String, parameter "remote_sha1"
           of String
        """
        # ctx is the context object
        # return variables are: handles
        #BEGIN fetch_handles_by
        #END fetch_handles_by

        # At some point might do deeper type checking...
        if not isinstance(handles, list):
            raise ValueError('Method fetch_handles_by return value ' +
                             'handles is not type list as required.')
        # return the results
        return [handles]

    def is_owner(self, ctx, arg_1):
        """
        Given a list of handle ids, this function determines if the underlying
        data is owned by the caller. If any one of the handle ids reference
        unreadable data this function returns false.
        :param arg_1: instance of list of type "HandleId" (Handle provides a
           unique reference that enables access to the data files through
           functions provided as part of the HandleService. In the case of
           using shock, the id is the node id. In the case of using shock the
           value of type is shock. In the future these values should
           enumerated. The value of url is the http address of the shock
           server, including the protocol (http or https) and if necessary
           the port. The values of remote_md5 and remote_sha1 are those
           computed on the file in the remote data store. These can be used
           to verify uploads and downloads.)
        :returns: instance of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN is_owner
        #END is_owner

        # At some point might do deeper type checking...
        if not isinstance(returnVal, int):
            raise ValueError('Method is_owner return value ' +
                             'returnVal is not type int as required.')
        # return the results
        return [returnVal]

    def delete_handles(self, ctx, handles):
        """
        The delete_handles function takes a list of handles
        and deletes them on the handle service server.
        :param handles: instance of list of type "Handle" -> structure:
           parameter "hid" of type "HandleId" (Handle provides a unique
           reference that enables access to the data files through functions
           provided as part of the HandleService. In the case of using shock,
           the id is the node id. In the case of using shock the value of
           type is shock. In the future these values should enumerated. The
           value of url is the http address of the shock server, including
           the protocol (http or https) and if necessary the port. The values
           of remote_md5 and remote_sha1 are those computed on the file in
           the remote data store. These can be used to verify uploads and
           downloads.), parameter "file_name" of String, parameter "id" of
           type "NodeId", parameter "type" of String, parameter "url" of
           String, parameter "remote_md5" of String, parameter "remote_sha1"
           of String
        :returns: instance of list of type "HandleId" (Handle provides a
           unique reference that enables access to the data files through
           functions provided as part of the HandleService. In the case of
           using shock, the id is the node id. In the case of using shock the
           value of type is shock. In the future these values should
           enumerated. The value of url is the http address of the shock
           server, including the protocol (http or https) and if necessary
           the port. The values of remote_md5 and remote_sha1 are those
           computed on the file in the remote data store. These can be used
           to verify uploads and downloads.)
        """
        # ctx is the context object
        # return variables are: hids
        #BEGIN delete_handles
        #END delete_handles

        # At some point might do deeper type checking...
        if not isinstance(hids, list):
            raise ValueError('Method delete_handles return value ' +
                             'hids is not type list as required.')
        # return the results
        return [hids]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
