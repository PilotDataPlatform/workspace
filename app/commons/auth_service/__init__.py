import httpx

from app.config import ConfigClass


async def get_project_users(container_code: str) -> list:
    users = []
    page = 0
    page_size = 25
    more_users = True
    roles = [f'{container_code}-' + i for i in ['admin', 'contributor', 'collaborator']]
    roles.append('platform-admin')
    while more_users:
        payload = {
            'role_names': roles,
            'status': 'active',
            'page': page,
            'page_size': page_size,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(ConfigClass.AUTH_SERVICE + 'admin/roles/users', json=payload)
        users += response.json().get('result')
        if ((page + 1) * page_size) > response.json()['total']:
            more_users = False
        page += 1
    return [i['username'] for i in users]
