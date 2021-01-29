import sqlalchemy
import datetime
from pprint import pprint
# Запишем ссылку на нашу базу данных
db = 'postgresql://postgres:dimka4100141@localhost:5432/music'
# Подключимся к базе данных
engine = sqlalchemy.create_engine(db)
connection = engine.connect()
# Данные, которые будем передавать в базу данных
album = [(1, 'only noisia', 2017),
         (2, 'only Nero', 2019),
         (3, 'only BSE', 2015),
         (4, 'only Pendulum', 2018),
         (5, 'only Skrillex', 2019),
         (6, 'only 50 cent', 2006),
         (7, 'Classic', 1777),
         (8, 'only neurofunk', 2020)
         ]

albumartist = [(1, 1, 1),
                (2, 2, 2),
                (3, 3, 3),
                (4, 4, 4),
                (5, 5, 5),
                (6, 7, 6),
                (7, 8, 7),
                (8, 1, 8),
                (9, 3, 8)
                ]

artist = [(1, 'Noisia'),
         (2, 'Nero'),
         (3, 'Black Sun Empire'),
         (4, 'Pendulum'),
         (5, 'Skrillex'),
         (6, 'Flosstrodamus'),
         (7, '50 cent'),
         (8, 'Mozart')
         ]

collection = [
            (1, 'collection 1', 2020),
            (2, 'collection 2', 2019),
            (3, 'collection 3', 2018),
            (4, 'collection 4', 2017),
            (5, 'collection 5', 2016),
            (6, 'collection 6', 2015),
            (7, 'collection 7', 2014),
            (8, 'collection 8', 2020)
            ]
        
genre = [
        (1, 'neurofunk'),
        (2, 'DnB'),
        (3, 'Dubstep'),
        (4, 'Trap'),
        (5, 'Rap'),
        (6, 'Classic')
        ]

genresartists = [
                (1, 1, 1),
                (2, 1, 2),
                (3, 2, 2),
                (4, 3, 1),
                (5, 3, 2),
                (6, 4, 2),
                (7, 5, 3),
                (8, 6, 4),
                (9, 7, 5),
                (10, 8, 6)
                ]

track = [
        (1, 1, 'Dustup', '3:55'),
        (1, 2, 'Collaider', '4:22'),
        (1, 3, 'Mantra', '3:55'),
        (2, 4, 'Promises', '3:51'),
        (2, 5, 'Something Else', '2:6'),
        (2, 6, 'Do You Wanna', '10:11'),
        (3, 7, 'I Saw You', '0:0'),
        (3, 8, 'Immersion', '3:12'),
        (3, 9, 'Kepler', '6:9'),
        (4, 10, 'Crush', '8:3'),
        (4, 11, 'Driver', '1:13'),
        (4, 12, 'Nothing For Free', '6:15'),
        (5, 13, 'Bangarang', '4:59'),
        (6, 14, 'Candy shop', '3:11'),
        (7, 15, 'Turkish Rondo', '16:1'),
        (8, 16, 'neurofunk', '1:0'),
        (8, 17, 'my track', '5:46')
        ]

trackcollection = [
                    (1, 1, 1),
                    (2, 2, 1),
                    (3, 3, 1),
                    (4, 4, 2),
                    (5, 5, 2),
                    (6, 6, 2),
                    (7, 1, 3),
                    (8, 7, 3),
                    (9, 5, 4),
                    (10, 8, 5),
                    (11, 9, 6),
                    (12, 10, 7),
                    (13, 11, 8),
                    (14, 12, 1),
                    (15, 13, 3),
                    (16, 14, 5),
                    (17, 15, 7),
                    (18, 16, 2),
                    ]

# Запишем наименования таблиц и их содержиое в списки для обработки данныз в циклах
tables_name = ['trackcollection', 'albumartist', 'genresartists', 'collection', 'track', 'album', 'artist', 'genre']
tables = [trackcollection, albumartist, genresartists, collection, track, album, artist, genre]

# Удалим предыдущие значения в таблицах в базе данных, если они есть
for el in tables_name:
    connection.execute(f"DELETE FROM {el}")
# Развернем наши списки, так как запись в тааблицы базы данных идет в обратном порядке из-за связей таблиц
tables.reverse()
tables_name.reverse()
# Запишем значения в базу данных
for index, el in enumerate(tables_name):
    for i in tables[index]:
        connection.execute(f"""
                            INSERT INTO {el}
                                VALUES{str(i)}
                            """)

# Выведем результаты записи согласно условиям в задании

for i in genre:
    # print(x)
    output = connection.execute(f"""SELECT count(artistid) FROM genresartists
                        WHERE genreid = {i[0]};""").fetchall()
    
    print(f'В жанре {i[1]} {output[0][0]} исполнителей')
print()
# -------------------------------------------------------------------------------
date_1 = 2019
date_2 = 2020
output = connection.execute(f"""SELECT count(trackid) FROM track
                        JOIN album ON track.albumid = album.albumid
                        WHERE album.year BETWEEN {date_1} AND {date_2};""").fetchall()
print(f'Количество треков в альбомах, выпущенных с {date_1} по {date_2} - {output[0][0]} штук')
print()

# -------------------------------------------------------------------------------
for i in album:
    output = connection.execute(f"""SELECT AVG(time) FROM track
                        JOIN album ON track.albumid = album.albumid
                        WHERE album.albumid = {i[0]};""").fetchall()
    print(f'Средняя продолжительность треков в альбоме {i[1]} - {output[0][0]}')

print()
# -------------------------------------------------------------------------------
data_3 = 2020
output = connection.execute(f"""SELECT name FROM artist
                        WHERE name NOT IN (
                            SELECT name FROM artist
                            JOIN albumartist ON artist.artistid = albumartist.artistid
                            JOIN album ON albumartist.albumid = album.albumid
                            WHERE album.year = {data_3}
                        );""").fetchall()
print(f'Исполнители, которые не выпустили альбомы в {data_3} году:')
for i in output:
    print(i[0])
print()
# -------------------------------------------------------------------------------
name = 'Noisia'
output = connection.execute(f"""SELECT title FROM collection
                        WHERE title IN (
                            SELECT collection.title FROM collection
                            JOIN trackcollection ON collection.collectionid = trackcollection.collectionid
                            JOIN track ON trackcollection.trackid = track.trackid
                            JOIN album ON track.albumid = album.albumid
                            JOIN albumartist ON album.albumid = albumartist.albumid
                            JOIN artist ON albumartist.artistid = artist.artistid
                            WHERE artist.name = '{name}'
                        )
                        ;""").fetchall()
print(f'Коллекции, в которых выпустил свои треки исполнитель {name}')

for i in output:
    print(i[0])
print()
# -------------------------------------------------------------------------------    
output = connection.execute(f"""SELECT albumname FROM album
                        JOIN albumartist ON album.albumid = albumartist.albumid
                        JOIN genresartists ON albumartist.artistid = genresartists.artistid
                        GROUP BY albumname
                        HAVING COUNT(genresartists.genreid) > 1
                        ;""").fetchall()
print(f'Альбомы, в которых присутствуют исполнители более 1 жанра: ')
for i in output:
    print(i[0])
print()
# -------------------------------------------------------------------------------
print('Наименования треков, которые не входят в сборники:')
output = connection.execute(f"""SELECT title FROM track
                        WHERE trackid NOT IN (
                            SELECT trackid FROM trackcollection
                        )
                        ;""").fetchall()
for i in output:
    print(i[0])
print()
# -------------------------------------------------------------------------------

output = connection.execute(f"""SELECT artist.name, track.time FROM artist
                        JOIN albumartist ON artist.artistid = albumartist.artistid
                        JOIN track ON albumartist.albumid = track.albumid
                        WHERE track.time = (
                            SELECT MIN(track.time) FROM track
                        )
                        ;""").fetchall()
print('Исполнитель, написавший самый короткий трек:')
print(f"""{output[0][0]}
Длина трека составила {output[0][1]}""")
print()
# -------------------------------------------------------------------------------
output = connection.execute(f"""SELECT albumname FROM album
                        JOIN track ON album.albumid = track.albumid
                        GROUP BY albumname
                        HAVING COUNT(track.trackid) = (
                            SELECT MIN(count) FROM (
                            SELECT track.trackid, COUNT(track.trackid) as count FROM album
                            JOIN track ON album.albumid = track.albumid
                            GROUP BY track.trackid
                            ) as MINCOUNT
                        )
                        ;""").fetchall()
print('Названия альбомов, которые имеют наименьшее количество треков:')
for i in output:
    print(i[0])

# !количество исполнителей в каждом жанре;
# !количество треков, вошедших в альбомы 2019-2020 годов;
# !средняя продолжительность треков по каждому альбому;
# !все исполнители, которые не выпустили альбомы в 2020 году;
# !названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
# !название альбомов, в которых присутствуют исполнители более 1 жанра;
# !наименование треков, которые не входят в сборники;
# !исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
# !название альбомов, содержащих наименьшее количество треков.