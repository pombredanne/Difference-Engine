from difflib import SequenceMatcher as SM

from .difference_engine import DifferenceEngine
from .ops import Insert, Persist, Remove


def parse_replace(a, b, a1, a2, b1, b2):
	yield Remove(a1, a2)
	yield Insert(b1, b2)

def parse_insert(a, b, a1, a2, b1, b2):
	yield Insert(b1, b2)

def parse_delete(a, b, a1, a2, b1, b2):
	yield Remove(a1, a2)

def parse_equal(a, b, a1, a2, b1, b2):
	assert a2 - a1 == b2 - b1
	yield Persist(a1, a2)

OP_PARSERS = {
	"replace": parse_replace,
	"insert": parse_insert,
	"delete": parse_delete,
	"equal": parse_equal
}

def parse_opcodes(opcodes, a, b):
	
	for opcode in opcodes:
		op, a_start, a_end, b_start, b_end = opcode
		
		parse = OP_PARSERS[op]
		for operation in parse(a, b, a_start, a_end, b_start, b_end):
			yield operation
	

def diff(a, b):
	opcodes = SM(None, a, b).get_opcodes()
	return parse_opcodes(opcodes, a, b)

class SequenceMatcher(DifferenceEngine):
	
	def __init__(self, last=None):
		self.last = last if last != None else []
	
	def process(self, tokens):
		delta = diff(self.last, tokens)
		
		return delta
		
	def serialize(self):
		return {'list': list(self.last)}
	
	@classmethod
	def deserialize(cls, doc):
		return cls(last=doc['last'])