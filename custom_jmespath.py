import jmespath
import difflib
import unicodedata
import string


class CustomFunctions(jmespath.functions.Functions):
    """
        Custom functions that can be used as other jmespath functions in an extraction
    """
    @jmespath.functions.signature({'types': ['string']}, {'types': ['string']})
    def _func_approx(self, s1, s2):
        """
            Given strings and a threshold, return true if they are approximately equal
        """
        return self._func_belongs_to(s1, s2, 0.85)

    @jmespath.functions.signature({'types': ['string']})
    def _func_remove_accents(self, data):
        """
            Strips accents from a string
        """
        return ''.join(
            x for x in unicodedata.normalize('NFKD', data) if x in (string.ascii_letters + string.whitespace + "/[]-'" + string.digits)
        ).lower()

    @jmespath.functions.signature({'types': ['string']}, {'types': ['string']}, {'types': ['number']})
    def _func_belongs_to(self, word1, word2, cutoff):
        return len(difflib.get_close_matches(self._func_remove_accents(word1), [self._func_remove_accents(word2)], cutoff=cutoff)) > 0

    @jmespath.functions.signature(
        {'types': ['object', 'array', 'string', 'number', 'boolean']},
        {'types': ['string', 'number', 'array', 'boolean']},
        {'types': ['string', 'number', 'array', 'boolean']})
    def _func_replace(self, d, s1, s2):
        """
            Replaces a substring by another in an object, at first level
        """
        # replaces s1 by s2 in d, only at first level
        # if s1 is a list of strings, replaces each string of list s1 by the corresponding string of list s2
        if isinstance(s1, list):
            if not s1:
                return d
            else:
                d = self._func_replace(d, s1[0], s2[0])
                return self._func_replace(d, s1[1:], s2[1:])
        else:
            # s1 is a string/int/float/bool...
            if isinstance(d, list):
                return [self._func_replace(i, s1, s2) for i in d]
            elif isinstance(d, dict):
                for k in d:
                    d[k] = s2 if d[k] == s1 else d[k]
            else:
                d = s2 if d == s1 else d
            return d

    @jmespath.functions.signature(
        {'types': ['object', 'array', 'string', 'number', 'boolean']},
        {'types': ['string', 'number', 'array', 'boolean']},
        {'types': ['string', 'number', 'array', 'boolean']})
    def _func_replace_all(self, d, s1, s2):
        """
            Replaces a substring by another in an object, at all levels
        """
        # replaces s1 by s2 in d, at all levels
        if isinstance(s1, list):
            if not s1:
                return d
            else:
                d = self._func_replace_all(d, s1[0], s2[0])
                return self._func_replace_all(d, s1[1:], s2[1:])
        else:
            if isinstance(d, list):
                return [self._func_replace_all(i, s1, s2) for i in d]
            elif isinstance(d, dict):
                for k in d:
                    if isinstance(d[k], list) or isinstance(d[k], dict):
                        d[k] = self._func_replace_all(d[k], s1, s2)
                    elif d[k] == s1:
                        d[k] = s2
            else:
                d = s2 if d == s1 else d
            return d

    @jmespath.functions.signature({'types': ['array']}, {'types': ['string', 'number']})
    def _func_unique(self, l, key):
        """
            Removes multiple occurrences of a value for a given key in an array of dicts. Keeps the last one.
        """
        #in a list of dicts, each dict containing key as one of its keys, returns a list of dicts with key as a primary key
        return list({v[key]: v for v in l}.values())
