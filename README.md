# Custom Filter for Glyphs

This is the Custom Filter for [GlyphsApp](https://glyphsapp.com/), where each entry is a block
in Unicode 13.0. Some large and unnecessary blocks (e.g. CJK Unified Ideographs) are excluded.

## Build

To build your filter, run the following commands. Note that Python 3.9+ is required to support Unicode 13.0.

```sh
curl -o Blocks.txt https://unicode.org/Public/13.0.0/ucd/Blocks.txt
python3 build.py [--no-comment] 'CustomFilter <name>.plist'
```

Then place it next to your `.glyphs` file.

## License

Copyright (C) 2021 by Xiangdong Zeng.

Licensed under the [MIT](LICENSE) License.
