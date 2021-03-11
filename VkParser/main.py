import re
import vk
import string
import emoji
import configparser
import matplotlib.pyplot as plt
import pandas as pd

from postgres import Postgres


def get_posts(count=1, page='itis_kfu'):
    posts = {}
    for i in range(count // 100 + 1):
        posts.update(vkapi.wall.get(domain=page, offset=i * 100, count=count))
        count -= 100

    return posts


def save_posts(posts):
    psql = Postgres()
    for post in posts['items']:
        id = post['id']
        text = post['text']
        if psql.is_post_in(id):
            break

        if 'copy_history' in post:
            for nested_post in post['copy_history']:
                text += ' ' + nested_post['text']

        psql.add_post(text=text, vk_id=id)
    psql.close()


def clear_text(text):
    p_table = str.maketrans(dict.fromkeys(string.punctuation))
    d_table = str.maketrans(dict.fromkeys(b'1234567890'))

    text = re.sub(emoji.get_emoji_regexp(), r"", text)  # delete emojis
    text = text.translate(p_table)  # delete punctuation
    text = text.translate(d_table)  # delete digits

    return text


def count_words() -> dict:
    words_dict = {}
    psql = Postgres()
    text = psql.get_posts_text()

    for item in text:
        item = clear_text(item[0])

        for word in item.split():
            words_dict[word] = words_dict.get(word, 0) + 1

    psql.close()

    return words_dict


def save_n_words(word_dict: dict):
    psql = Postgres()
    words = []
    for item in word_dict.items():
        words.append(item)

    psql.save_words(words)

    psql.close()


def show_visualisation(word_dict: dict):
    df = pd.DataFrame.from_dict(word_dict, orient='index', columns=['count'])
    df = df.sort_values(by=['count']).tail(100)
    ax = df.plot(kind='bar', title='words distribution', figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("Words", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    plt.savefig('words_distr.png', dpi=1000)


def main():
    posts = get_posts(count=200)
    save_posts(posts)
    words_dict = count_words()
    save_n_words(words_dict)
    show_visualisation(word_dict=words_dict)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')

    session = vk.Session(access_token=config.get('vk', 'token'))
    vkapi = vk.API(session=session, v='5.85')

    psql = Postgres()
    psql.truncate_table('word')

    main()
