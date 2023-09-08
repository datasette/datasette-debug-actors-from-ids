from datasette.app import Datasette
from datasette import hookimpl
from datasette.plugins import pm
import pytest


@pytest.mark.asyncio
async def test_debug_actors_from_ids():
    ds = Datasette()
    await ds.invoke_startup()

    class ActorsFromIdsPlugin:
        __name__ = "ActorsFromIdsPlugin"

        @hookimpl
        def actors_from_ids(self, actor_ids):
            return {
                actor_id: {
                    "id": actor_id,
                    "name": "Name for {}".format(actor_id),
                }
                for actor_id in actor_ids
            }

    try:
        pm.register(ActorsFromIdsPlugin(), name="ActorsFromIdsPlugin")
        response = await ds.client.get("/-/debug-actors-from-ids?ids=1,2")
        assert response.status_code == 200
        assert response.json() == {
            "1": {"id": "1", "name": "Name for 1"},
            "2": {"id": "2", "name": "Name for 2"},
        }
    finally:
        pm.unregister(name="ReturnNothingPlugin")
