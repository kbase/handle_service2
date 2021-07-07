# handle_service release notes
=========================================

1.0.0
-----
* Merged handle_service (https://github.com/kbase/handle_service) and handle manager service(https://github.com/kbase/handle_mngr)


1.0.1
-----
* Raise error if handle id exists when persist_handle is called.


1.0.2
-----
* Make node type check non-case sensitive.

1.0.3
-----
* Support blobstore (https://github.com/kbase/blobstore).
* Switch to use Github action for tests.

1.0.4
-----
* create index for 'hid' on startup to speed up fetching
