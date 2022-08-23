import sqlite3
import os
import platform
import calendar
import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class AmusedDB(object):

    def __init__(self):
        import configparser
        config = configparser.ConfigParser()
        current_os = platform.system().lower()

        if current_os.lower() == "windows":
            db_path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + '..' + os.path.sep + 'database' + os.path.sep
        else:
            #config.read('/var/www/webApp/webApp/mlconfig.ini')
            db_path = '/etc/amused/'

        self.db_f_name = 'amusedDB'
        self.db_dir_name = db_path
        self.db_full_f_name = self.db_dir_name + self.db_f_name + '.db'
        print('Database location:')
        print(self.db_full_f_name)
        self.conn = sqlite3.connect(self.db_full_f_name)


    def create_table(self, table_name):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string1 = 'CREATE TABLE IF NOT EXISTS ' \
                      + table_name \
                      + '(ID INTEGER PRIMARY KEY);'
        c.execute(sql_string1)
        conn.close()
        return

    def conn(self):
        return self.conn

    def insert_columns(self, table_name, columns):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        for column in columns:
            sql_string = 'ALTER TABLE ' + table_name + '  ADD COLUMN ' + column + ';'
            try:
                c.execute(sql_string)
            except sqlite3.Error as e:
                if not 'duplicate column name:' in e.args[0]:
                    print(e.args[0])
        conn.close()

    def select(self, sql_string):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def get_base_name(self):
        splitted = self.db_f_name.split('.')
        return splitted[0]

    def get_name(self):
        return self.db_f_name

    def execute(self, sql_string):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        c.execute(sql_string)
        conn.commit()
        conn.close()
        return

    def getCategories(self, language):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM categories WHERE categories_language = "' + language + '" ORDER BY categories_sort_order ASC'
        c.execute(sql_string)
        data = c.fetchall()
        return data

    def getLevels(self, language):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM levels WHERE levels_language = "' + language + '" ORDER BY levels_sort_order ASC'
        c.execute(sql_string)
        data = c.fetchall()
        return data

    def getBackgrounds(self, language):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM backgrounds WHERE backgrounds_language = "' + language + '" ORDER BY backgrounds_sort_order ASC'
        c.execute(sql_string)
        data = c.fetchall()
        return data

    def getVideos(self, categories_SO , levels_SO, backgrounds_SO):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()

        searchFilter = []
        searchString = ""

        if categories_SO > -1:
            r = "p"
            searchFilter.append("videos_category_SO = " + str(categories_SO))
        if levels_SO > -1:
            searchFilter.append("videos_level_SO = " + str(levels_SO))
        if backgrounds_SO > -1:
            searchFilter.append("videos_background_SO = " + str(backgrounds_SO))

        if len(searchFilter) > 0:
            searchString = "WHERE "

        moreThenOne = False

        for filter in searchFilter:
            if moreThenOne:
                searchString = searchString + ' AND '
            searchString = searchString + filter
            moreThenOne = True


        sql_string = 'SELECT * FROM videos  ' + searchString +' ORDER BY videos_level_SO'
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def getMusic(self, categories_SO):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        if int(categories_SO) > -1:
            searchString = " WHERE music_category_SO = " + categories_SO

        sql_string = 'SELECT * FROM Music ' + searchString
        c.execute(sql_string)

        data = c.fetchall()
        conn.close()
        return data

    def getPlaylists(self, user_ID):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        sql_string = 'SELECT * FROM playlists WHERE playlists_user_ID = ' + str(user_ID) \
                     + ' ORDER BY playlists_date_created ASC'
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def add2PlaylistItems(self, playlist_ID, video_ID, music_ID):
        conn = sqlite3.connect(self.db_full_f_name)
        sql_string = 'INSERT INTO playlist_items (playlist_items_playlist_ID, playlist_items_video_ID, ' \
                     'playlist_items_music_ID, playlist_items_sort_order) ' \
                     'VALUES (' + str(playlist_ID) + ', ' + str(video_ID) + ', ' + str(music_ID) + ', 1000)'
        self.execute(sql_string)
        return 'http200OK'

    def addMusic2PlaylistItems(self, playlist_ID, music_ID):
        conn = sqlite3.connect(self.db_full_f_name)
        sql_string = 'INSERT INTO playlist_music (playlist_music_playlist_ID,  ' \
                     'playlist_music_music_ID, playlist_music_sort_order) ' \
                     'VALUES (' + str(playlist_ID) + ', ' + str(music_ID) + ', 1000)'
        self.execute(sql_string)
        return 'http200OK'

    def addVideo2PlaylistItems(self, playlist_ID, video_ID):
        conn = sqlite3.connect(self.db_full_f_name)
        sql_string = 'INSERT INTO playlist_videos (playlist_videos_playlist_ID, ' \
                     'playlist_videos_video_ID, playlist_videos_sort_order) ' \
                     'VALUES (' + str(playlist_ID) + ', ' + str(video_ID) +  ', 1000)'
        self.execute(sql_string)
        return 'http200OK'

    def addPlayList(self, playlistUserID, playListName):

        date = datetime.datetime.utcnow()
        utc_time = calendar.timegm(date.utctimetuple())

        values = '(' + playlistUserID + ',"' + playListName + '",' + str(utc_time) + ')'
        sql_string = 'INSERT INTO playlists (playlists_user_ID, playlists_name, playlists_date_created) VALUES ' + values
        self.execute(sql_string)
        return 'http200OK'

    def removePlayList(self, playlistID):
        sql_string = 'DELETE FROM playlists WHERE ID = ' + str(playlistID)
        self.execute(sql_string)
        sql_string = 'DELETE FROM playlist_music WHERE playlist_music_playlist_ID = ' + str(playlistID)
        self.execute(sql_string)
        sql_string = 'DELETE FROM playlist_videos WHERE playlist_videos_playlist_ID = ' + str(playlistID)
        self.execute(sql_string)
        return 'http200OK'

    def editPlayListName(self, playlistID, playlistName):
        sql_string = 'UPDATE playlists set playlists_name = "' + playlistName + '" WHERE ID = ' + playlistID
        self.execute(sql_string)
        return 'http200OK'

    def removeFromPlayList(self, playlist_Item_ID, table_name):
        sql_string = 'DELETE FROM ' + table_name + ' WHERE ID = ' + str(playlist_Item_ID)
        self.execute(sql_string)
        return 'http200OK'

    def getPlaylistItems(self, playlist_ID):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()

        join_clause = ' JOIN videos ON videos.ID  = playlist_items_video_ID JOIN music ON music.ID = playlist_items_music_ID '
        sql_string = 'SELECT playlist_items.ID as pi_ID, *  FROM playlist_items' + join_clause + \
                     'WHERE playlist_items_playlist_ID = ' + str(playlist_ID) \
                     + ' ORDER BY playlist_items_sort_order ASC'
        c.execute(sql_string)
        data = c.fetchall()
        self.addSortOrderToPlayListItems(data)
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def getPlaylistItemsMusic(self, playlist_ID):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()

        join_clause = ' JOIN music ON music.ID  = playlist_music_music_ID ' \
            'JOIN categories ON categories.categories_sort_order = music.music_category_SO '

        sql_string = 'SELECT playlist_music.ID as pm_ID, *  FROM playlist_music' + join_clause + \
                     'WHERE playlist_music_playlist_ID = ' + str(playlist_ID) \
                     + ' ORDER BY playlist_music_sort_order ASC'
        c.execute(sql_string)
        data = c.fetchall()
        self.addSortOrderToPlayListItemsMusic(data)
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def addSortOrderToPlayListItemsMusic(self, plItems):

        so = 1
        for plItem in plItems:
            pi_id = plItem.get('pm_ID')
            sql_string = "UPDATE playlist_music SET playlist_music_sort_order = " + str(so) + " WHERE ID=" + str(pi_id)
            self.execute(sql_string)
            so = so + 1

    def getPlaylistItemsVideo(self, playlist_ID):
        conn = sqlite3.connect(self.db_full_f_name)
        conn.row_factory = dict_factory
        c = conn.cursor()

        join_clause = ' JOIN videos ON videos.ID  = playlist_videos_video_ID ' \
            'JOIN categories ON categories.categories_sort_order = videos.videos_category_SO ' \
            'JOIN backgrounds ON backgrounds.backgrounds_sort_order = videos.videos_background_SO '

        sql_string = 'SELECT playlist_videos.ID as pv_ID, *  FROM playlist_videos' + join_clause + \
                     'WHERE playlist_videos_playlist_ID = ' + str(playlist_ID) \
                     + ' ORDER BY playlist_videos_sort_order ASC'
        c.execute(sql_string)
        data = c.fetchall()
        self.addSortOrderToPlayListItemsVideo(data)
        c.execute(sql_string)
        data = c.fetchall()
        conn.close()
        return data

    def addSortOrderToPlayListItemsVideo(self, plItems):

        so = 1
        for plItem in plItems:
            pi_id = plItem.get('pv_ID')
            sql_string = "UPDATE playlist_videos SET playlist_videos_sort_order = " + str(so) + " WHERE ID=" + str(pi_id)
            self.execute(sql_string)
            so = so + 1

    def movePlaylistitemUp(self, itemID):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = "SELECT playlist_items_sort_order FROM playlist_items WHERE ID=" + str(itemID)
        c.execute(sql_string)
        data = c.fetchone()
        sort_order_orig = data[0]
        sql_string = "SELECT  playlist_items_sort_order, ID  FROM playlist_items WHERE playlist_items_sort_order < " + str(sort_order_orig) + " ORDER BY playlist_items_sort_order DESC LIMIT 1"
        c.execute(sql_string)
        data = c.fetchone()
        sort_order_other = data[0]
        id_other = data[1]
        sql_string = "UPDATE playlist_items SET playlist_items_sort_order=" + str(sort_order_other) + " WHERE ID=" + str(itemID)
        c.execute(sql_string)
        sql_string = "UPDATE playlist_items SET playlist_items_sort_order=" + str(sort_order_orig) + " WHERE ID=" + str(id_other)
        c.execute(sql_string)
        conn.close()

    def movePlaylistitemDown(self, itemID):
        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = "SELECT playlist_items_sort_order FROM playlist_items WHERE ID=" + str(itemID)
        c.execute(sql_string)
        data = c.fetchone()
        sort_order_orig = data[0]
        sql_string = "SELECT  playlist_items_sort_order, ID  FROM playlist_items WHERE playlist_items_sort_order < " + str(sort_order_orig) + " ORDER BY playlist_items_sort_order ASC LIMIT 1"
        c.execute(sql_string)
        data = c.fetchone()
        sort_order_other = data[0]
        id_other = data[1]
        sql_string = "UPDATE playlist_items SET playlist_items_sort_order=" + str(sort_order_other) + " WHERE ID=" + str(itemID)
        c.execute(sql_string)
        sql_string = "UPDATE playlist_items SET playlist_items_sort_order=" + str(sort_order_orig) + " WHERE ID=" + str(id_other)
        c.execute(sql_string)
        conn.close()


    def movePlaylistitem(self, itemID, tableName, direction):
        if direction == 'up':
            sortDir = 'DESC'
            compSign = '<'
        if direction == 'down':
            sortDir = 'ASC'
            compSign = '>'

        conn = sqlite3.connect(self.db_full_f_name)
        c = conn.cursor()
        sql_string = "SELECT " + tableName + "_sort_order, " + tableName + "_playlist_ID FROM " \
                     + tableName + " WHERE ID=" + str(itemID)
        c.execute(sql_string)
        data = c.fetchone()
        sort_order_orig = data[0]
        playlist_ID = data[1]
        sql_string = "SELECT " + tableName + "_sort_order, ID  FROM " + tableName + " WHERE " + tableName +\
                     "_sort_order " + compSign + " " + \
                     str(sort_order_orig) + " AND " + tableName + "_playlist_ID=" + str(playlist_ID) + \
                     " ORDER BY " + tableName + "_sort_order " + sortDir + " LIMIT 1"
        print(sql_string)
        c.execute(sql_string)
        data = c.fetchone()
        sort_order_other = data[0]
        id_other = data[1]
        conn.close()
        sql_string = "UPDATE " + tableName + " SET " + tableName + "_sort_order=" + str(sort_order_other) +\
                     " WHERE ID=" + str(itemID)

        self.execute(sql_string)
        sql_string = "UPDATE " + tableName + " SET " + tableName + "_sort_order=" + str(sort_order_orig) +\
                     " WHERE ID=" + str(id_other)
        self.execute(sql_string)


    def create_db(self):
        # ********************************************************
        table_name = 'videos'

        self.create_table(table_name)

        columns = ["videos_name TEXT DEFAULT ''",
                    "videos_category_SO INTEGER",
                    "videos_level_SO INTEGER",
                    "videos_background_SO INTEGER",
                    "videos_description TEXT",
                    "videos_duration INTEGER"]

        self.insert_columns(table_name, columns)

        # ********************************************************
        table_name = 'music'

        self.create_table(table_name)
        columns = ["music_filename TEXT DEFAULT ''",
                   "music_duration INTEGER",
                   "music_thumbnail TEXT",
                   "music_artist TEXT",
                   "music_name TEXT",
                   "music_category_SO integer"]

        self.insert_columns(table_name, columns)

        # ********************************************************
        table_name = 'categories'

        self.create_table(table_name)
        columns = ["categories_name TEXT DEFAULT ''",
                   "categories_language TEXT DEFAULT ''",
                   "categories_sort_order INTEGER"]

        self.insert_columns(table_name, columns)

        # ********************************************************
        table_name = 'levels'

        self.create_table(table_name)
        columns = ["levels_name TEXT DEFAULT ''",
                   "levels_language TEXT DEFAULT ''",
                   "levels_sort_order INTEGER"]

        self.insert_columns(table_name, columns)


        # ********************************************************
        table_name = 'backgrounds'

        self.create_table(table_name)
        columns = ["backgrounds_name TEXT DEFAULT ''",
                   "backgrounds_language TEXT DEFAULT ''",
                   "backgrounds_sort_order INTEGER"]

        self.insert_columns(table_name, columns)

        # ********************************************************
        table_name = 'users'

        self.create_table(table_name)
        columns = ["user_name TEXT DEFAULT ''",
                   "user_surname TEXT DEFAULT ''",
                   "user_password TEXT DEFAULT ''"]

        self.insert_columns(table_name, columns)

        # ********************************************************
        table_name = 'playlists'

        self.create_table(table_name)
        columns = ["playlists_user_ID INTEGER DEFAULT -1",
                   "playlists_name TEXT DEFAULT 'New list'",
                   "playlists_date_created INTEGER"]

        self.insert_columns(table_name, columns)

        # ********************************************************
        table_name = 'playlist_items'

        self.create_table(table_name)
        columns = ["playlist_items_playlist_ID INTEGER DEFAULT -1",
                   "playlist_items_music_ID INTEGER DEFAULT -1",
                   "playlist_items_sort_order INTEGER DEFAULT -1",
                   "playlist_items_video_ID INTEGER DEFAULT -1"]

        self.insert_columns(table_name, columns)


        # ********************************************************
        table_name = 'playlist_videos'

        self.create_table(table_name)
        columns = ["playlist_videos_playlist_ID INTEGER DEFAULT -1",
                   "playlist_videos_sort_order INTEGER DEFAULT -1",
                   "playlist_videos_video_ID INTEGER DEFAULT -1"]

        self.insert_columns(table_name, columns)

        # ********************************************************
        table_name = 'playlist_music'

        self.create_table(table_name)
        columns = ["playlist_music_playlist_ID INTEGER DEFAULT -1",
                   "playlist_music_sort_order INTEGER DEFAULT -1",
                   "playlist_music_music_ID INTEGER DEFAULT -1"]

        self.insert_columns(table_name, columns)


        # ********************************************************
        table_name = 'log'

        self.create_table(table_name)
        columns = ["log_playlist_item_ID INTEGER DEFAULT -1",
                   "log_time_stamp INTEGER DEFAULT -1"]

        self.insert_columns(table_name, columns)


    def populateDB(self):

        # self.execute('INSERT INTO categories (categories_name, categories_language, categories_sort_order) VALUES '
        #              '("Warming-up","EN",1)')
        # self.execute('INSERT INTO categories (categories_name, categories_language, categories_sort_order) VALUES '
        #              '("Strength exercises","EN",2)')
        # self.execute('INSERT INTO categories (categories_name, categories_language, categories_sort_order) VALUES '
        #              '("Static balance exercises","EN",3)')
        # self.execute('INSERT INTO categories (categories_name, categories_language, categories_sort_order) VALUES '
        #              '("Dynamic balance exercises","EN",4)')
        # self.execute('INSERT INTO categories (categories_name, categories_language, categories_sort_order) VALUES '
        #              '("Functional exercises","EN",5)')
        # self.execute('INSERT INTO categories (categories_name, categories_language, categories_sort_order) VALUES '
        #              '("Endurance exercises","EN",6)')
        # self.execute('INSERT INTO categories (categories_name, categories_language, categories_sort_order) VALUES '
        #              '("Flexibility exercises","EN",7)')
        #
        # self.execute('INSERT INTO levels (levels_name, levels_language, levels_sort_order) VALUES '
        #              '("Level 1","EN",1)')
        # self.execute('INSERT INTO levels (levels_name, levels_language, levels_sort_order) VALUES '
        #              '("Level 2","EN",2)')
        # self.execute('INSERT INTO levels (levels_name, levels_language, levels_sort_order) VALUES '
        #              '("Level 3","EN",3)')
        # self.execute('INSERT INTO levels (levels_name, levels_language, levels_sort_order) VALUES '
        #              '("Level 4","EN",4)')
        # self.execute('INSERT INTO levels (levels_name, levels_language, levels_sort_order) VALUES '
        #              '("Level 5","EN",5)')
        #
        #
        #
        #
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid1.mp4",1,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid2.mp4",1,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid3.mp4",1,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid4.mp4",1,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid5.mp4",1,1,1,946)')
        #
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid1.mp4",2,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid2.mp4",2,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid3.mp4",2,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid4.mp4",2,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid5.mp4",2,1,1,946)')
        #
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid1.mp4",3,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid2.mp4",3,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid3.mp4",3,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid4.mp4",3,1,1,946)')
        # self.execute('INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #              '("vid5.mp4",3,1,1,946)')
        #
        #
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid1.mp4",1,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid2.mp4",1,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid3.mp4",1,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid4.mp4",1,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid5.mp4",1,2,1,946)')
        #
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid1.mp4",2,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid2.mp4",2,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid3.mp4",2,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid4.mp4",2,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid5.mp4",2,2,1,946)')
        #
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid1.mp4",3,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid2.mp4",3,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid3.mp4",3,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid4.mp4",3,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid5.mp4",3,2,1,946)')
        #
        #

        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid1_s.mp4",3,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid3_s.mp4",3,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid4_s.mp4",3,2,1,946)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("vid5_s.mp4",3,2,1,946)')






        # self.execute('INSERT INTO backgrounds (backgrounds_name, backgrounds_language, backgrounds_sort_order) VALUES '
        #              '("White","EN",1)')
        # self.execute('INSERT INTO backgrounds (backgrounds_name, backgrounds_language, backgrounds_sort_order) VALUES '
        #              '("UHasselt","EN",2)')
        #
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #     "VALUES ('song1_s.mp3', 120, 'song1.jpg',1)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #         "VALUES ('song2_s.mp3', 120, 'song2.jpg',2)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #          "VALUES ('song3_s.mp3', 120, 'song3.jpg',3)")



        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song1.mp3', 120, 'song1.jpg',1)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song2.mp3', 120, 'song2.jpg',2)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song3.mp3', 120, 'song3.jpg',3)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song4.mp3', 120, 'song4.jpg',4)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song5.mp3', 120, 'song5.jpg',5)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song6.mp3', 120, 'song6.jpg',6)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song7.mp3', 120, 'song7.jpg',1)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song8.mp3', 120, 'song8.jpg',2)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song9.mp3', 120, 'song9.jpg',3)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song10.mp3', 120, 'song10.jpg',4)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song1.mp3', 120, 'song1.jpg',5)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song2.mp3', 120, 'song2.jpg',6)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song3.mp3', 120, 'song3.jpg',1)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song4.mp3', 120, 'song4.jpg',2)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song5.mp3', 120, 'song5.jpg',3)")
        # self.execute("INSERT INTO music (music_name, music_duration, music_thumbnail, music_category_SO) "
        #              "VALUES ('song6.mp3', 120, 'song6.jpg',4)")

        # self.execute("INSERT INTO users (user_name, user_surname, user_password) "
        #               " VALUES ('Geraerts', 'Marc', 'fb31233dd9a42ac96743aee5db7cda3044a2265bd1a25e2b8e00259804a1a2af')")

        # self.execute("INSERT INTO playlists (playlists_user_ID, playlists_name, playlists_date_created) "
        #              " VALUES (1, 'Marc1', 1653412078)")


        # self.execute("INSERT INTO playlist_items (playlist_items_playlist_ID, playlist_items_music_ID, playlist_items_video_ID, playlist_items_sort_order) "
        #              " VALUES (1, 1, 1,1)")
        # self.execute("INSERT INTO playlist_items (playlist_items_playlist_ID, playlist_items_music_ID, playlist_items_video_ID, playlist_items_sort_order) "
        #              " VALUES (1, 2, 2,2)")
        # self.execute("INSERT INTO playlist_items (playlist_items_playlist_ID, playlist_items_music_ID, playlist_items_video_ID, playlist_items_sort_order) "
        #              " VALUES (1, 3, 3,3)")






        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("Fietsen_funct2.mp4",5,2,1,103)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("Klappen in alle richtingen_opwarming2.mp4",1,2,1,63)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("Op 1 been staan_stat4.mp4",3,2,1,92)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("Polsen ronddraaien_lenigheid.mp4",7,2,1,35)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("Stappen met versnellingen_uith1.mp4",6,2,1,188)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("Traplopen_funct1.mp4",5,2,1,55)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("Uitvalspas naar voor_dynam2.mp4",4,2,1,51)')
        # self.execute(
        #     'INSERT INTO videos (videos_name, videos_category_SO, videos_level_SO, videos_background_SO, videos_duration) VALUES '
        #     '("Zwaaien_opwarming2.mp4",1,2,1,60)')









        return