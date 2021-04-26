from dragonfly import *
import 

grammar = Grammar("firefox")

class DictationCommandRule(MappingRule):
    mapping = {
        "navigate":   Key('c-l'),
    }
    extras = [  ]
    export=False
    context=AppContext(title='mozilla firefox')

grammar.add_rule(DictationCommandRule())
grammar.load()
