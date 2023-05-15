import os

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.persistence.domain.database_song import DatabaseSong
from youtube_music_manager_server.persistence.music_persistence import MusicPersistence


class MusicPersistenceTest:

    @staticmethod
    @inject
    def test_database_has_been_created(app_settings: AppSettings = Provide['app_settings']) -> None:

        database_path = os.path.join(app_settings.persistence_settings.music_database_directory, 'music.db')

        assert os.path.isfile(database_path)

    @staticmethod
    def test_song_is_added(unit_tests_database_song: DatabaseSong, music_persistence: MusicPersistence) -> None:

        music_persistence.add_song(unit_tests_database_song)

    @staticmethod
    def test_song_is_returned(unit_tests_database_song: DatabaseSong, music_persistence: MusicPersistence) -> None:

        database_songs = music_persistence.get_all_songs()
        database_song = next((x for x in database_songs if x.id == unit_tests_database_song.id), None)

        assert database_song is not None
        assert isinstance(database_song, DatabaseSong)
        assert database_song.title == unit_tests_database_song.title
        assert database_song.artist == unit_tests_database_song.artist
        assert type(database_song.creation_date) == str
        assert database_song.creation_date == unit_tests_database_song.creation_date
        assert database_song.file == unit_tests_database_song.file

    @staticmethod
    def test_song_is_deleted(unit_tests_database_song: DatabaseSong, music_persistence: MusicPersistence) -> None:

        music_persistence.delete_song(unit_tests_database_song)

        assert not os.path.isfile(unit_tests_database_song.file)