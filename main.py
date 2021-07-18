import os
import requests
from dotenv import load_dotenv
import pprint
from PIL import Image
from io import BytesIO


def search(key):
    """
    検索クエリからplace_idを取得する
    :param key: API key(.envファイルに記述して読み込む)
    :return: place_id: 検索結果の1番目の店のplace_id
    """
    # APIを叩く
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {
        'key': key,
        'input': 'ラーメン二郎新代田',
        'inputtype': 'textquery',
    }  # 検索クエリの設定(詳しくはPlace Search APIのドキュメント参照)
    res = requests.get(url=url, params=params)

    # 検索結果の1番目からplace_idを取得する
    dic = res.json()  # レスポンスのjsonをdict型にする
    print(dic)
    place_id = dic['candidates'][0]['place_id']
    return place_id


def get_place_details(key, place_id):
    """
    place_idをもとにその店の写真の参照キーのリストを返す
    :param key: API key
    :param place_id: お店のplace_id
    :return: photo_references: 写真の参照キーのリスト
    """
    # APIを叩く
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'key': key,
        'place_id': place_id,
    }  # 検索クエリの設定(詳しくはPlace Search APIのドキュメント参照)
    res = requests.get(url=url, params=params)

    dic = res.json()  # レスポンスのjsonをdict型にする
    pp = pprint.PrettyPrinter(indent=2)  # pprintでdictの中身をきれいに表示する
    pp.pprint(dic)

    # お店の詳細情報からphoto_referenceをすべて取得してリストに入れる
    photo_references = [photo['photo_reference'] for photo in dic['result']['photos']]
    return photo_references


def get_place_photo(key, photo_references):
    """
    photo_referenceからお店の写真を取得して表示する
    :param key: API key
    :param photo_references: 写真参照キーのリスト
    :return:photos: Imageオブジェクトのリスト
    """
    url = 'https://maps.googleapis.com/maps/api/place/photo'
    maxheight = 400
    photos = [] # お店の写真のImageオブジェクトのリスト
    # photo_referenceごとにAPIを叩いて画像を取得
    for photo_ref in photo_references:
        # APIを叩く
        params = {
            'key': key,
            'photoreference': photo_ref,
            'maxheight': maxheight,
        }
        res = requests.get(url=url, params=params)

        # 返ってきたバイナリをImageオブジェクトに変換
        photo = Image.open(BytesIO(res.content))
        print(photo.format)  # 写真フォーマットは固定ではないらしいので確認
        photos.append(photo)
    return photos


def main():
    # .envファイルからAPIkeyを読み込む
    load_dotenv()
    # API keyの値を取得
    key = os.environ['APIkey']
    print(key)
    # 「ラーメン二郎新代田」での検索結果を取得
    place_id = search(key)
    print(place_id)
    # place_idからphoto_references(写真の参照キーのリスト)を取得する
    photo_references = get_place_details(key, place_id)
    # 写真のリストを取得する
    photos = get_place_photo(key, photo_references)
    # 写真を1枚表示
    photos[0].show()


if __name__ == '__main__':
    main()
