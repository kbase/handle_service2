import tempfile


def get_hid_counter(hid_counter_collection):
    """
    get current handle id counter
    """
    counter = hid_counter_collection.find_one({"_id": {"$eq": "hid_counter"}})

    if counter is not None:
        return counter.get("hid_counter")
    return 0


def create_temp_file(data_string):
    try:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(data_string)
            file_path = temp_file.name
        return file_path

    except Exception as e:
        raise ValueError("An error occurred:") from e
