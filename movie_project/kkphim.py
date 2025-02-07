import requests
import json
import mysql.connector

# Kết nối đến MySQL
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="movieweb",
    port=3307,
    collation='utf8mb4_general_ci'
)
cur = cnx.cursor(buffered=True)

name = input("name: ")

# API tìm kiếm phim
rqSearch = f"https://phimapi.com/v1/api/tim-kiem?keyword={name}"
gS = requests.get(rqSearch)
joS = gS.json()

# Định nghĩa câu lệnh SQL để chèn tập phim
insert_episode_query = """
INSERT INTO movielink (movieID, episode, link) 
VALUES (%s, %s, %s)
"""

# Lặp qua các kết quả tìm kiếm
for item in joS.get('data', {}).get('items', []):
    print(item['origin_name'])

    rqMovieSlug = f"https://phimapi.com/phim/{item['slug']}"
    gM = requests.get(rqMovieSlug)
    joM = gM.json()

    # Kiểm tra dữ liệu hợp lệ
    if 'episodes' not in joM or not joM['episodes']:
        continue

    eps = joM['episodes'][0]['server_data']
    filmInfo = joM['movie']

    # Xác định loại phim
    type = "TV Series" if len(eps) > 1 else "Movie"
    genre = " - ".join([cate['name'] for cate in filmInfo.get('category', [])])

    # Câu lệnh SQL để chèn thông tin phim
    insert_info_query = """
    INSERT INTO movieinfo 
    (`name`, `Status`, `duration`, `type`, 
    `publishYear`, `Language`, `Genre`, 
    `national`, `thumbnailImg`, `coverImg`, `requiredAge`, `content`) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    insert_values = (
        filmInfo.get('origin_name', ''),
        filmInfo.get('status', ''),
        filmInfo.get('time', ''),
        type,
        filmInfo.get('year', 0),
        filmInfo.get('lang', ''),
        genre,
        filmInfo.get('country', [{}])[0].get('name', ''),
        filmInfo.get('thumb_url', ''),
        filmInfo.get('poster_url', ''),
        16,
        filmInfo.get('content', '')
    )

    cur.execute(insert_info_query, insert_values)
    cnx.commit()

    # Lấy ID phim vừa chèn
    cur.execute("SELECT movieID FROM movieinfo WHERE name = %s ORDER BY movieID DESC", (filmInfo['origin_name'],))
    result = cur.fetchone()
    if result:
        movieID = result[0]
    else:
        continue  # Bỏ qua nếu không tìm thấy ID

    # Chèn dữ liệu tập phim (sử dụng câu lệnh SQL đã tách riêng)
    for ep in eps:
        cur.execute(insert_episode_query, (movieID, ep['name'], ep['link_m3u8']))

    cnx.commit()

cnx.close()
