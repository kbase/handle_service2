import logging
import traceback

from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError


MONGO_COLLECTION = 'handle'
MONGO_HID_COUNTER_COLLECTION = 'handle_id_counter'

class MongoUtil:

    _HID_COUNTER_ID = 'hid_counter'

    def _get_collection(self, mongo_host, mongo_port, mongo_database, mongo_collection,
                        mongo_user=None, mongo_password=None, mongo_authmechanism='DEFAULT'):
        """
        connect Mongo server and return a collection
        """

        if mongo_user:
            logging.info('mongo-user found in config file, configuring client for authentication using mech ' + str(mongo_authmechanism) )
            my_client = MongoClient(mongo_host, mongo_port,
                                    username=mongo_user, password=mongo_password,
                                    authSource=mongo_database,
                                    authMechanism=mongo_authmechanism)
        else:
            logging.info('no mongo-user found in config file, connecting without auth')
            my_client = MongoClient(mongo_host, mongo_port)

        try:
            my_client.server_info()  # force a call to server
        except ServerSelectionTimeoutError as e:
            error_msg = 'Connot connect to Mongo server\n'
            error_msg += 'ERROR -- {}:\n{}'.format(
                            e,
                            ''.join(traceback.format_exception(None, e, e.__traceback__)))
            raise ValueError(error_msg)

        # TODO: check potential problems. MongoDB will create the collection if it does not exist.
        my_database = my_client[mongo_database]
        my_collection = my_database[mongo_collection]

        return my_collection

    def increase_counter(self):

        query = {'_id': self._HID_COUNTER_ID}
        update = {'$inc': {self._HID_COUNTER_ID: 1}}

        return self.hid_counter_collection.find_one_and_update(filter=query,
                                                               update=update,
                                                               upsert=True,
                                                               return_document=ReturnDocument.AFTER)['hid_counter']

    def __init__(self, config):
        self.mongo_host = config['mongo-host']
        self.mongo_port = int(config['mongo-port'])
        self.mongo_database = config['mongo-database']
        self.mongo_user = config['mongo-user']
        self.mongo_pass = config['mongo-password']
        self.mongo_authmechanism = config['mongo-authmechanism']

        self.handle_collection = self._get_collection(self.mongo_host, self.mongo_port,
                                                      self.mongo_database, MONGO_COLLECTION,
                                                      self.mongo_user, self.mongo_pass,
                                                      self.mongo_authmechanism)
        # create index on startup to speed up fetching
        self.handle_collection.create_index('hid', unique=True)

        self.hid_counter_collection = self._get_collection(self.mongo_host, self.mongo_port,
                                                           self.mongo_database,
                                                           MONGO_HID_COUNTER_COLLECTION,
                                                           self.mongo_user, self.mongo_pass,
                                                           self.mongo_authmechanism)

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)

    def find_in(self, elements, field_name, projection={'_id': False}, batch_size=1000):
        """
        return cursor that contains docs which field column is in elements
        """
        logging.info('start querying MongoDB')

        try:
            result = self.handle_collection.find({field_name: {'$in': elements}},
                                                 projection=projection, batch_size=batch_size)
        except Exception as e:
            error_msg = 'Connot query doc\n'
            error_msg += 'ERROR -- {}:\n{}'.format(
                            e,
                            ''.join(traceback.format_exception(None, e, e.__traceback__)))
            raise ValueError(error_msg)

        return result

    def insert_one(self, doc):
        """
        insert a doc into collection
        """
        logging.info('start inserting document')

        try:
            self.handle_collection.insert_one(doc)
        except Exception as e:
            error_msg = 'Connot insert doc\n'
            error_msg += 'ERROR -- {}:\n{}'.format(
                            e,
                            ''.join(traceback.format_exception(None, e, e.__traceback__)))
            raise ValueError(error_msg)

        return True

    def update_one(self, doc):
        """
        update a doc
        """
        logging.info('start updating document')

        try:
            update_filter = {'hid': doc.get('hid')}
            update = {'$set': doc}
            self.handle_collection.update_one(update_filter, update)
        except Exception as e:
            error_msg = 'Connot update doc\n'
            error_msg += 'ERROR -- {}:\n{}'.format(
                            e,
                            ''.join(traceback.format_exception(None, e, e.__traceback__)))
            raise ValueError(error_msg)

        return True

    def delete_one(self, doc):
        """
        delete a doc
        """
        logging.info('start deleting document')

        try:
            delete_filter = {'hid': doc.get('hid')}
            self.handle_collection.delete_one(delete_filter)
        except Exception as e:
            error_msg = 'Connot delete doc\n'
            error_msg += 'ERROR -- {}:\n{}'.format(
                            e,
                            ''.join(traceback.format_exception(None, e, e.__traceback__)))
            raise ValueError(error_msg)

        return True

    def delete_many(self, docs):
        """
        delete a docs
        """
        logging.info('start deleting documents')

        try:
            hids_to_delete = list(set([doc.get('hid') for doc in docs]))
            delete_filter = {'hid': {'$in': hids_to_delete}}
            result = self.handle_collection.delete_many(delete_filter)
        except Exception as e:
            error_msg = 'Connot delete docs\n'
            error_msg += 'ERROR -- {}:\n{}'.format(
                            e,
                            ''.join(traceback.format_exception(None, e, e.__traceback__)))
            raise ValueError(error_msg)
        else:
            deleted_count = result.deleted_count

        return deleted_count
