from datetime import datetime

import requests
from collections import OrderedDict

from django.conf import settings
from social_core.exceptions import AuthForbidden
from urllib.parse import urlencode, urlunparse
from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    api_url = urlunparse(('https',
                      'api.vk.com',
                      '/method/users.get',
                      None,
                      urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_max_orig')),
                                            access_token=response['access_token'],
                                            v='5.92')),
                      None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if 'sex' in data:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
    if 'photo_max_orig' in data:
        photo_content = requests.get(data['photo_max_orig'])
        with open(f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg', 'wb') as photo_file:
            photo_file.write(photo_content.content)
    if 'about' in data:
        user.shopuserprofile.about_me = data['about']
    if 'bdate' in data:
        bdate = datetime.strptime(data['bdate'], "%d.%m.%Y")
        age = datetime.now().year - bdate.year
        if age < 18:
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    user.save()
