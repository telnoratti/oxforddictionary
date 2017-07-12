import unittest
import os
from oxforddictionary import client


api_url = "https://od-api.oxforddictionaries.com:443/api/v1/"


class test_client(unittest.TestCase):
    def setUp(self):
        self.c = client.client(os.environ['APP_ID'], os.environ['APP_KEY'])

    def test_url_gen(self):
        url = self.c._url("entries")
        self.assertEqual(url,
                         api_url + "entries/en")
        url = self.c._url("entries", word_id="spell")
        self.assertEqual(url,
                         api_url + "entries/en/spell")
        url = self.c._url("entries", source_lang="es", word_id="spell")
        self.assertEqual(url,
                         api_url + "entries/es/spell")
        url = self.c._url("entries", word_id="spell", filters={'examples':
                                                               None})
        self.assertEqual(url,
                         api_url + "entries/en/spell/examples")

    def test_filters_gen(self):
        f = self.c._filters({'examples': None})
        self.assertEqual(f, "examples")
        f = self.c._filters({'examples': None, 'lexicalCategory': 'Adjective'})
        self.assertEqual(f, "examples;lexicalCategory=Adjective")
        f = self.c._filters({'lexicalCategory': 'Adjective', 'register':
                             'informal', 'examples': None,
                             'grammaticalFeatures': 'Singular'})
        self.assertEqual(
            f,
            "lexicalCategory=Adjective;register=informal;examples;" +
            "grammaticalFeatures=Singular"
        )
        f = self.c._filters({})
        self.assertEqual(f, None)

    def test_client_init(self):
        self.assertIsNotNone(self.c)

    def test_inflection_search(self):
        results = self.c.search('spelling')
        self.assertEqual(len(results.results), 1)
        self.assertEqual(results.results[0].match_type, "inflection")

    def test_fuzzy_search(self):
        results = self.c.search('sppelling')
        self.assertEqual(len(results.results), 1)
        self.assertEqual(results.results[0].match_type, "fuzzy")

    def test_headword_search(self):
        results = self.c.search('spell')
        self.assertEqual(len(results.results), 1)

    def test_headword_search_multi(self):
        results = self.c.search('spell', limit=5)
        self.assertEqual(len(results.results), 5)

    def test_entries(self):
        entry = self.c.entries('spell')

if __name__ == '__main__':
    unittest.main()
