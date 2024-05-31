def get_hid_counter(hid_counter_collection):
    """
    get current handle id counter
    """
    counter = hid_counter_collection.find_one({"_id": {"$eq": "hid_counter"}})

    if counter is not None:
        return counter.get("hid_counter")
    return 0
