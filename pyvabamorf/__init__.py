import pyvabamorf.vabamorf as vm
import os
import atexit

if not vm.FSCInit():
    raise Exception('Could not initiate pyvabamorf library. FSCInit() returned false!')

@atexit.register
def terminate():
    vm.FCSTerminate()

PACKAGE_PATH = os.path.dirname(__file__)
DICT_PATH = os.path.join(PACKAGE_PATH, 'dct')

class PyVabamorf(object):

    def __init__(self, lexPath=DICT_PATH):
        self._analyzer = vm.Analyzer(lexPath)

    def _an_to_dict(self, an):
        '''Convert an analysis to dicti onary.'''
        return {'root': an.root.decode('utf-8'),
                'ending': an.ending.decode('utf-8'),
                'clitic': an.clitic.decode('utf-8'),
                'partofspeech': an.partofspeech.decode('utf-8'),
                'form': an.form.decode('utf-8')}

    def _sentence_to_utf8(self, sentence):
        '''Convert a sequence of unicode strings to a list of utf-8 encoded objects.'''
        result = []
        for word in sentence:
            assert isinstance(word, unicode)
            result.append(word.encode('utf-8'))
        return result

    def analyze(self, sentence):
        morfresult = self._analyzer.analyze(vm.StringVector(self._sentence_to_utf8(sentence)))
        result = []
        for word, analysis in morfresult:
            analysis = [self._an_to_dict(an) for an in analysis]
            result.append({'text': word.decode('utf-8'),
                           'analysis': analysis})
        return result