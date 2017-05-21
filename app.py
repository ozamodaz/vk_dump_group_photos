from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlretrieve
import vk
session = vk.Session()
api = vk.API(session)

# If page has its own name shown in URL
# page_domain = 'spacespiceboy'

# If page only has id number
owner_id = -76907970

# Where to save photos
dload_folder = '/home/ozamodaz/Pictures/tst/'


def get_posts():

    def api_call(count, offset):
        if 'page_domain' in globals():
            return api.wall.get(domain=page_domain, count=count, offset=offset)
        elif 'owner_id' in globals():
            return api.wall.get(owner_id=owner_id, count=count, offset=offset)

    posts = []
    offset = 0
    total_posts = api_call(count=1, offset=0)[0]
    while len(posts) < total_posts:
        responce = api_call(count=100, offset=offset)[1:]
        posts.extend(responce)
        offset += 100
        print(len(posts))
    return posts


def get_pics(post):
    URLs = set()
    if post.get('attachments', None):
        for attach in post['attachments']:
            if attach['type'] == 'photo':
                URLs.update([attach['photo']['src_big']])
    return URLs


if __name__ == "__main__":
    posts = get_posts()
    pics = set()
    for post in posts:
        pics.update(get_pics(post))

    with ThreadPoolExecutor(max_workers=10) as executor:
        for pic in pics:
            dest = dload_folder + pic.rsplit('/', 1)[1]
            worker = executor.submit(urlretrieve, pic, dest)
