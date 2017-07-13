# https://developer.oxforddictionaries.com/documentation
import json


# For a given json looks for key name and returns None if not there or an array
# of instantiated class_name of each element of array.
def _none_or_array(blob, name, item_class):
    if blob.get(name, None) is None:
        return None
    else:
        ret = []
        for i in blob[name]:
            ret.append(item_class(i))
        return ret


# Used for /search/ and /wordlist/
class word_list(object):
    def __init__(self, metadata=None, results=None):
        # Dict, arbitrary data provided by OUP
        self.metadata = metadata
        # Array of match
        self.results = results

    def __init__(self, blob):
        # metadata is unstructured
        self.metadata = blob.get('metadata', None)
        # Iterate through results
        self.results = _none_or_array(blob, 'results', match)


# /search Model 1
class match(object):
    def __init__(self, id=None, word=None, match_string=None, match_type=None,
                 region=None):
        # String, ID of word
        self.id = id
        # String, string used to match
        self.match_string = match_string
        # String, what the query matched i.e. 'headword', 'fuzzy', 'inflection'
        self.match_type = match_type
        # String
        self.region = region
        # String, realization in undercase
        self.word = word

    def __init__(self, blob):
        # Do required arguments first
        self.id = blob['id']
        self.word = blob['word']
        # Now optional
        self.match_string = blob.get('matchString', None)
        self.match_type = blob.get('matchType', None)
        self.region = blob.get('region', None)
        # Probably should do some type checking

    # look up this word
    def lookup(self):
        pass


class retrieve_entry(object):
    def __init__(self, metadata=None, results=None):
        # Dict, Additional information TODO: figure out what this is
        self.metadata = metadata
        # Array of Headword_entry
        self.results = results

    def __init__(self, blob):
        # metadata is unstructured
        self.metadata = blob.get('metadata', None)
        # Iterate through results
        self.results = _none_or_array(blob, 'results', headword_entry)

    def get_definitions(self):
        defs = []
        for result in self.results:
            defs.extend(result.get_definitions())
        return defs


class headword_entry(object):
    def __init__(self, id=None, language=None, lexical_entries=None, word=None,
                 pronunciations=None, type=None):
        # Unique identifier for word
        self.id = id
        # IANA language code
        self.language = language
        # Array of Lexical_entry (basically entries for each pos it takes, but
        # could be more)
        self.lexical_entries = lexical_entries
        # Array of pronunciations
        self.pronunciations = pronunciations
        # one of 'headword', 'inflection', or 'phrase'
        self.type = type
        # A given written or spoken realisation of an entry lowercased, this is
        # not necessarily the correct spelling since it's lowercased
        self.word = word

    def __init__(self, blob):
        # Do required arguments first
        self.id = blob['id']
        self.word = blob['word']
        self.language = blob['language']
        self.lexical_entries = _none_or_array(blob, 'lexicalEntries',
                                             lexical_entry)
        # Now optional
        self.pronunciations = _none_or_array(blob, 'pronunciations',
                                             pronunciation)
        self.type = blob.get('type', None)
        # Probably should do some type checking

    def get_definitions(self):
        defs = []
        for lexical_entry in self.lexical_entries:
            defs.extend(lexical_entry.get_definitions())
        return defs


class lexical_entry(object):
    def __init__(self, language=None, lexical_category=None, text=None,
                 derivative_of=None, entries=None, gramatical_features=None,
                 notes=None, pronunciations=None, variant_forms=None):
        # Array of Related_entry
        self.derivative_of = None
        # Array of Entry
        self.entries = entries
        # Array of Grammatical_feature
        self.gramatical_features = grammatical_features
        # String IANA language code
        self.language = language
        # String that is the lexical category (generally pos I think)
        self.lexical_category = lexical_category
        # TODO: what are notes?
        self.notes = notes
        # Array of Pronunciation
        self.pronunciations = pronunciations
        # realization of an entry
        self.text = text
        # Array of Variant_form which are interchangable depending on context
        self.variant_forms = variant_forms

    def __init__(self, blob):
        # Do required arguments first
        self.language = blob['language']
        self.text = blob['text']
        self.lexical_category = blob['lexicalCategory']
        # Now optional
        self.derivative_of = _none_or_array(blob, 'derivativeOf',
                                            related_entry)
        self.entries = _none_or_array(blob, 'entries', entry)
        self.gramatical_features = _none_or_array(blob, 'grammaticalFeatures',
                                                  grammatical_feature)
        self.notes = _none_or_array(blob, 'notes', categorized_text)
        self.pronunciations = _none_or_array(blob, 'pronunciations',
                                             pronunciation)
        self.variant_forms = _none_or_array(blob, 'variantForms', variant_form)
        # Probably should do some type checking

    def get_definitions(self):
        defs = []
        for entry in self.entries:
            defs.extend(entry.get_definitions())
        return defs


class entry(object):
    def __init__(self, etymologies=None, grammatical_features=None,
                 homograph_number=None, notes=None, pronunciations=None,
                 senses=None, variant_forms=None):
        # Array of strings
        self.etymologies = etymologies
        # Array of Grammatical_feature
        self.gramatical_features = gramatical_features
        # String, last two digits identify the homograph number
        self.homograph_number = homograph_number
        # Array of Categorized_text
        self.notes = notes
        # Array of Pronunciation
        self.pronunciations = pronunciations
        # Array of Sense
        self.senses = senses
        # Array of Variant_form
        self.variant_forms = variant_forms

    def __init__(self, blob):
        # No required arguments
        # Now optional
        self.etymologies = _none_or_array(blob, 'etymologies', str)
        self.gramatical_features = _none_or_array(blob, 'grammaticalFeatures',
                                                  grammatical_feature)
        self.homograph_number = blob.get('homographNumber', None)
        self.notes = _none_or_array(blob, 'notes', categorized_text)
        self.pronunciations = _none_or_array(blob, 'pronunciations',
                                             pronunciation)
        self.senses = _none_or_array(blob, 'senses', sense)
        self.variant_forms = _none_or_array(blob, 'variantForms', variant_form)
        # Probably should do some type checking

    def get_definitions(self):
        defs = []
        for sense in self.senses:
            defs.extend(sense.get_definitions())
        return defs


# A variation of the word in spelling or maybe pronunciation
# /entries/ Model 5
class variant_form(object):
    def __init__(self, text=None, regions=None):
        # String which is the form variation
        self.text = text
        # Array of strings which are regions the text occurs in
        self.regions = regions

    def __init__(self, blob):
        self.text = blob['text']
        self.regions = _none_or_array(blob, 'regions', str)


# TODO: figure out what this is
# /entries/ Model 4
class categorized_text(object):
    def __init__(self, text=None, type=None, id=None):
        # String
        self.text = text
        # String
        self.type = type
        # String
        self.id = id

    def __init__(self, blob):
        self.id = blob.get('id', None)
        self.text = blob['text']
        self.type = blob['type']


# /entries/ Model 2
class related_entry(object):
    def __init__(self, id=None, text=None, domains=None, language=None,
                 regions=None, registers=None):
        # Array of strings, (subject/discipline)
        self.domains = domains
        # String, word ID
        self.id = id
        # String, IANA language code
        self.language = language
        # Array of strings
        self.regions = regions
        # Array of strings
        self.registers = registers
        # String, related itself
        self.text = text

    def __init__(self, blob):
        # Required fields first
        self.id = blob['id']
        self.text = blob['text']
        # Now optional fields
        self.language = blob.get('language', None)
        self.regions = _none_or_array(blob, 'regions', str)
        self.registers = _none_or_array(blob, 'registers', str)


# TODO: figure out what this is
# /entries/ Model 3
class grammatical_feature(object):
    def __init__(self, text=None, type=None):
        # String
        self.text = text
        # String
        self.type = type

    def __init__(self, blob):
        self.text = blob['text']
        self.type = blob['type']


class sense(object):
    def __init__(self, cross_reference_markers=None, cross_references=None,
                 definitions=None, domains=None, examples=None, id=None,
                 notes=None, pronunciations=None, regions=None, registers=None,
                 subsenses=None, translations=None, variant_forms=None):
        # Array of strings, grouping of notes TODO: wat is this?
        self.cross_reference_markers = cross_reference_markers
        # Array of Cross_reference
        self.cross_references = cross_references
        # Array of strings
        self.definitions = definitions
        # Array of strings (subject/discipline)
        self.domains = domains
        # Array of Example
        self.examples = examples
        # String, unique id for sense
        self.id = id
        # Array of Categorized_text
        self.notes = notes
        # Array of Pronunciation
        self.pronunciations = pronunciations
        # Array of strings, regions where sense is found
        self.regions = regions
        # Array of strings
        self.registers = registers
        # Array of senses (ordered)
        self.subsenses = subsenses
        # Array of Translation
        self.translations = translations
        # Array of Variant_form
        self.variant_forms = variant_forms

    def __init__(self, blob):
        # No required fields
        # Now for optional fields
        self.cross_reference_markers = _none_or_array(blob,
                                                      'crossReferenceMarkers',
                                                      str)
        self.cross_references = _none_or_array(blob, 'crossReferences',
                                               cross_reference)
        self.definitions = _none_or_array(blob, 'definitions', str)
        self.domains = _none_or_array(blob, 'domains', str)
        self.examples = _none_or_array(blob, 'examples', example)
        self.id = blob.get('id', None)
        self.notes = _none_or_array(blob, 'notes', categorized_text)
        self.pronunciations = _none_or_array(blob, 'pronunciations',
                                             pronunciation)
        self.regions = _none_or_array(blob, 'regions', str)
        self.registers = _none_or_array(blob, 'registers', str)
        self.subsenses = _none_or_array(blob, 'subsenses', sense)
        self.translations = _none_or_array(blob, 'translations', translation)
        self.variant_forms = _none_or_array(blob, 'variantForms', variant_form)

    def get_definitions(self):
        defs = []
        for definition in self.definitions:
            defs.append(definition)
        if self.subsenses is not None:
            for subsense in self.subsenses:
                defs.extend(subsense.get_definitions())
        return defs


# /entries/ Model 7
# TODO: helper for getting senses
class example(object):
    def __init__(self, text=None, definitions=None, domains=None, notes=None,
                 regions=None, registers=None, sense_ids=None,
                 translations=None):
        # Array of strings, a list of statements of the exact meaning of a word
        self.definitions = definitions
        # Array of strings (subject/discipline)
        self.domains = domains
        # Array of Categorized_text
        self.notes = notes
        # Array of strings, regions of example (TODO: will this differ from
        # sense?)
        self.regions = regions
        # Array of strings
        self.registers = registers
        # Array of strings, sense_ids this example relates to
        self.sense_ids = sense_ids
        # String, the example itself
        self.text = text
        # Array of Translation
        self.translations = translations

    def __init__(self, blob):
        # Required fields first
        self.text = blob['text']
        # Now for optional fields
        self.definitions = _none_or_array(blob, 'definitions', str)
        self.domains = _none_or_array(blob, 'domains', str)
        self.notes = _none_or_array(blob, 'notes', categorized_text)
        self.regions = _none_or_array(blob, 'regions', str)
        self.registers = _none_or_array(blob, 'registers', str)
        self.senseIds = _none_or_array(blob, 'senseIds', str)
        self.translations = _none_or_array(blob, 'translations', translation)


# /entries/ Model 6
class cross_reference(object):
    def __init__(self, id=None, text=None, type=None):
        # String, word ID of the concurrence
        self.id = id
        # String, word of concurrence
        self.text = text
        # String, The type of relation between the two words. Possible values
        # are 'close match', 'related', 'see also', 'variant spelling', and
        # 'abbreviation' in case of crossreferences, or 'pre', 'post' in case
        # of collocates.
        self.type = type

    def __init__(self, blob):
        self.id = blob['id']
        self.text = blob['text']
        self.type = blob['type']


# /entries/ Model 8
class translation(object):
    def __init__(self, text=None, language=None, domains=None,
                 gramatical_features=None, notes=None, regions=None,
                 registers=None):
        # Array of strings, (subject/discipline)
        self.domains = domains
        # Array of Grammatical_feature
        self.gramatical_features = gramatical_features
        # String, IANA language code
        self.language = language
        # Array of Categorized_text
        self.notes = notes
        # Array of strings
        self.regions = regions
        # Array of strings
        self.registers = registers
        # String, translation itself
        self.text = text

    def __init__(self, blob):
        # Required fields first
        self.language = blob['language']
        self.text = blob['text']
        # Now optional fields
        self.domains = _none_or_array(blob, 'domains', str)
        self.gramatical_features = _none_or_array(blob, 'grammaticalFeatures',
                                                  str)
        self.notes = _none_or_array(blob, 'notes', categorized_text)
        self.regions = _none_or_array(blob, 'regions', str)
        self.registers = _none_or_array(blob, 'registers', str)


# /entries/ Model 1
class pronunciation(object):
    def __init__(self, audio_file=None, dialects=None, phonetic_notation=None,
                 phonetic_spelling=None, regions=None):
        # String, url of sound file.
        self.audio_file = audio_file
        # Array of strings, for local/regional variation
        self.dialects = dialects
        # String, alphabetic system to display phonetic spelling (IPA etc.)
        self.phonetic_notation = phonetic_notation
        # String, the phonetic spelling
        self.phonetic_spelling = phonetic_notation
        # Array of strings
        self.regions = regions

    def __init__(self, blob):
        # No required fields
        # Now for optional fields
        self.audio_file = blob.get('audioFile', None)
        self.dialects = _none_or_array(blob, 'dialects', str)
        self.phonetic_notation = blob.get('phoneticNotation', None)
        self.phonetic_spelling = blob.get('phonetic_spelling', None)
        self.regions = _none_or_array(blob, 'regions', str)
