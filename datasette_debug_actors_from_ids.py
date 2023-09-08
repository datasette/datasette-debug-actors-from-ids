from datasette import hookimpl, Response


async def debug_actors_from_ids(request, datasette):
    # Must have view-instance permission
    await datasette.ensure_permissions(
        request.actor,
        ["view-instance"],
    )
    ids = (request.args.get("ids") or "").split(",")
    if not ids:
        return Response.html(
            "<h1>Must provide at least one actor ID</h1>",
            status=400,
        )
    actors = await datasette.actors_from_ids(ids)
    return Response.json(actors)


@hookimpl
def register_routes():
    return [(r"^/-/debug-actors-from-ids$", debug_actors_from_ids)]
