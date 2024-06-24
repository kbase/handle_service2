# handle_service release notes
=========================================

## 1.0.7
* The MongoDB clients have been updated to the most recent version and the service tested against Mongo 7.
* Added the mongo-retrywrites configuration setting in deployment.cfg.templ, defaulting to false.
* Added the docker-compose file to start a handle service server in test mode.
* Added pipenv to handle dependencies.
* Removed Mongo setup from Dockerfile and converted test to run without `kb-sdk`.
* Fixed broken Lintly in GHA.
* Updated Python to 3.9.19.
* Modified MongoUtil to defer Mongo client initialization, preventing "MongoClient opened before fork" error with uwsgi prefork + threads.

## 1.0.6

* Added jitpack build for Java client

## 1.0.5
* Added threading locks around token cache access to fix a race condition that would throw a
  KeyError including the token in the error message and caused calls to `add_read_acl` to fail.
* Updated python to 3.8
* Updated tests to install mongo from a tarball to make future mongo matrixing in
  tests easier.

## 1.0.4
* create index for 'hid' on startup to speed up fetching
  (NOTE: please add a unique index on hid in the background prior to upgrade or the service will hang on startup until the index is built.
  "db.handle.createIndex({hid:1},{unique:1,background:1})")
* use only admin token provided in the deploy.cfg file for `add_read_acl` operation.
* Pin pymongo to 3.8.0 since deployed MongoDB doesn't support some of the latest pymongo features

## 1.0.3
* Support blobstore (https://github.com/kbase/blobstore).
* Switch to use Github action for tests.

## 1.0.2
* Make node type check non-case sensitive.

## 1.0.1
* Raise error if handle id exists when persist_handle is called.

## 1.0.0
* Merged handle_service (https://github.com/kbase/handle_service) and handle manager service(https://github.com/kbase/handle_mngr)

