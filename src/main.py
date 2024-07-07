import asyncio
from steamid.resolve_custom_id import resolve_custom_id


async def main():
    id = "gabelogannewell"
    print(f'Resolving custom steam id "{id}"')
    id_64 = await resolve_custom_id(id)
    print(f'Resolved custom steam id "{id}" to the steamid64: {id_64}')


asyncio.run(main())
