import sys
import plistlib
import unicodedata
from collections import OrderedDict


class Blocks:
    MAX_BLOCK_LEN = 10000
    TO_BE_REMOVED_BLOCKS = [
        'CJK Unified Ideographs Extension A',
        'CJK Unified Ideographs',
        'High Surrogates',
        'High Private Use Surrogates',
        'Low Surrogates',
        'Private Use Area',
        'CJK Compatibility Ideographs',
        'CJK Unified Ideographs Extension B',
        'CJK Unified Ideographs Extension C',
        'CJK Unified Ideographs Extension D',
        'CJK Unified Ideographs Extension E',
        'CJK Unified Ideographs Extension F',
        'CJK Compatibility Ideographs Supplement',
        'CJK Unified Ideographs Extension G',
        'Supplementary Private Use Area-A',
        'Supplementary Private Use Area-B',
    ]
    XML_ESCAPES = {'&amp;': '&', '&lt;': '<', '&gt;': '>'}

    def __init__(self, file: str):
        self.blocks = OrderedDict()
        with open(file, 'r') as f:
            self._blocks = f.read()
        self.parse()
        self.sanitize()

    def parse(self):
        for line in self._blocks.splitlines():
            if not (line.startswith('#') or line == ''):
                range_str, name = line.split('; ')
                self.blocks[name] = self.parse_range(range_str)

    def parse_range(self, r: str):
        first, last = r.split('..')
        return range(int(first, 16), int(last, 16) + 1)

    def sanitize(self):
        # Remove some large and unnecessary blocks
        to_be_removed = set()
        for name, value in self.blocks.items():
            if name in self.TO_BE_REMOVED_BLOCKS or len(value) > self.MAX_BLOCK_LEN:
                to_be_removed.add(name)
        for name in to_be_removed:
            del self.blocks[name]
        # Convert the ranges into character lists
        for name, value in self.blocks.items():
            self.blocks[name] = {'name': name, 'list': self.to_char_list(value)}

    def to_char_list(self, r):
        res = []
        for i in r:
            c = chr(i)
            if not unicodedata.category(c) in ['Cc', 'Cn']:
                res.append(c)
        return res

    def to_plist(self, file: str, comment: bool = True):
        blocks_list = list(self.blocks.values())
        if comment:
            lines = plistlib.dumps(blocks_list, sort_keys=False).decode('utf8').splitlines()
            with open(file, 'w') as f:
                for line in lines:
                    if line.startswith('\t\t\t') and len(line) >= 12:
                        c = line[11]
                        if c == '&':
                            for k, v in self.XML_ESCAPES.items():
                                c = v if k in lines else c
                        line += '<!-- U+{0:04X} -->'.format(ord(c))
                    f.write(line + '\n')
        else:
            with open(file, 'wb') as f:
                plistlib.dump(blocks_list, f, sort_keys=False)


if __name__ == '__main__':
    if not unicodedata.unidata_version >= '15':
        print('Your Python does not support Unicode 13.0. Exit.')
        sys.exit()
    blocks = Blocks('Blocks.txt')
    if len(sys.argv) == 3 and sys.argv[1] == '--no-comment':
        blocks.to_plist(sys.argv[2], comment=False)
    else:
        blocks.to_plist(sys.argv[1])
