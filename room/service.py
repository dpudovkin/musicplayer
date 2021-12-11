import redis

from room.models import Song


class RedisService:
    __instance = None

    def __init__(self):
        if not RedisService.__instance:
            print(" __init__ method called..")
            self.redisClient = redis.Redis(host='localhost', port=6379, db=0)
        else:
            print("Instance already created:", self.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = RedisService()
        return cls.__instance

    def vote_next_song(self, room_group_name, username):
        key = f"vote{room_group_name}"
        count = self.redisClient.get(key)
        if count is None:
            self.redisClient.set(key, 1)
        else:
            self.redisClient.set(key, int(count) + 1)

        key = f"vote{room_group_name}{username}"
        self.redisClient.set(key, 1)

    def connect_user(self, room_group_name, username):
        key = f"users{room_group_name}"
        keyList = f"userList{room_group_name}"
        count = (self.redisClient.get(key))
        if count is None:
            self.redisClient.set(key, 1)
        else:
            self.redisClient.set(key, int(count) + 1)

        self.redisClient.lpush(keyList, username)

    def disconnect_user(self, room_group_name, username):
        key = f"users{room_group_name}"
        keyList = f"userList{room_group_name}"
        count = self.redisClient.get(key)
        if count is None:
            self.redisClient.set(key, 0)
        else:
            self.redisClient.set(key, int(count) - 1)

        userList = []
        while self.redisClient.llen(keyList) != 0:
            extract_name = self.redisClient.lpop(keyList)
            if str(extract_name.decode("utf-8")) != str(username):
                userList.append(extract_name)

        for name in userList:
            self.redisClient.lpush(keyList, name)

    def current_song_id(self, room_group_name):
        key = f"song{room_group_name}"
        songId = self.redisClient.get(key)
        return songId

    def update_current_src_id(self, room_group_name, songId):
        key = f"song{room_group_name}"
        self.redisClient.set(key, songId)

    def clear_voted(self, room_group_name):
        key = f"vote{room_group_name}"
        self.redisClient.set(key, 0)

    def turn_next(self, room_group_name):
        user_key = f"users{room_group_name}"
        vote_key = f"vote{room_group_name}"
        connectedUsers = int(self.redisClient.get(user_key))
        voted = int(self.redisClient.get(vote_key))
        if voted >= (connectedUsers+1) / 2:
            return True
        return False

    def all_users(self, room_group_name):
        keyList = f"userList{room_group_name}"
        resultList = []
        for i in range(self.redisClient.llen(keyList)):
            name = self.redisClient.lindex(keyList, i).decode("utf-8")
            resultList.append(str(name))
        return resultList

    def vote_count(self, room_group_name):
        key = f"vote{room_group_name}"
        count = self.redisClient.get(key)
        if count is None:
            return 0
        else:
            return int(count)

    def is_voted(self, room_group_name, username):
        key = f"vote{room_group_name}{username}"
        voted = self.redisClient.get(key)
        if voted is None:
            return False
        else:
            return 1 == int(self.redisClient.get(key))

    def reset_vote(self, room_group_name, username):
        key = f"vote{room_group_name}{username}"
        self.redisClient.set(key, 0)

# взаимодействие с моделями
class RepositoryService:
    __instance = None

    def __init__(self):
        if not RepositoryService.__instance:
            print(" __init__ method called..")
        else:
            print("Instance already created:", self.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = RepositoryService()
        return cls.__instance

    def next_song_id(self):
        # get only verified Song
        return Song.objects.filter(verified=True).order_by('?')[0].id

    def song_url(self, song_id):
        song = Song.objects.get(id=song_id)
        if song is None:
            return Song.objects.order_by('?')[0].url
        else:
            return song.audio_file.url

    def song(self, song_id):
        song = Song.objects.get(id=int(song_id))
        return song
