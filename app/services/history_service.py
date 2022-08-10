from models.history import History

history_collection = History


async def add_history(new_history: History) -> History:
    history = await new_history.insert()
    return history


async def retrieve_history(obs_id: str) -> History:
    param = {"object_id": obs_id}
    history = await history_collection.find(param).to_list()
    if history:
        return history