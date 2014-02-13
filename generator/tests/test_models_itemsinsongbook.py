from django.test import TransactionTestCase
from django.test.utils import override_settings
from generator.models import *


class AddASong(TransactionTestCase):

    fixtures = ["test_data_1.json"]

    def setUp(self):        
        pass

    def test_add_song_to_songbook(self):
        
        # pre-conditions
        
        self.assertGreater(Songbook.objects.count(), 0)
        self.assertGreater(Song.objects.count(), 0)

        song = Song.objects.all()[0]
        songbook = Songbook.objects.get(id=1)

        self.assertEqual(songbook.items.count(), 0)

        # operations
        
        songbook.add(song)
        
        # verification
        
        sis = SongInSongbook.objects.get(song_id=song.id)
        self.assertIsNotNone(sis)
        
        self.assertEqual(sis.title, song.title)
        self.assertEqual(sis.slug, song.slug)
        self.assertEqual(sis.language, song.language)
        self.assertEqual(sis.capo, song.capo)
        
        ais = sis.artist
        self.assertIsNotNone(ais)
        
        self.assertEqual(ais.name, song.artist.name)
        self.assertEqual(ais.slug, song.artist.slug)
        
        fis = sis.file
        self.assertIsNotNone(fis)
        
        self.assertEqual(fis.file_path, song.file.file_path)
        self.assertEqual(fis.object_hash, song.file.object_hash)
        self.assertEqual(fis.commit_hash, song.file.commit_hash)
                
    @override_settings(DEBUG=True)
    def test_remove_song_from_songbook(self):
        
        # pre-conditions

        song = Song.objects.all()[0]
        songbook = Songbook.objects.get(id=1)

        self.assertEqual(ItemsInSongbook.objects.count(), 0)
        self.assertEqual(ArtistInSongbook.objects.count(), 0)
        self.assertEqual(FileInSongbook.objects.count(), 0)

        songbook.add(song)

        self.assertEqual(ArtistInSongbook.objects.count(), 1)
        self.assertEqual(FileInSongbook.objects.count(), 1)
        self.assertEqual(ItemsInSongbook.objects.count(), 1)
        
        # operation
        
        songbook.remove_song(song.id)
        
        self.assertEqual(ItemsInSongbook.objects.count(), 0)
        self.assertEqual(ArtistInSongbook.objects.count(), 0)
        self.assertEqual(FileInSongbook.objects.count(), 0)
        