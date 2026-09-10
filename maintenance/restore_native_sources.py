"""Recover only complete, checksum-matched original source files."""
import base64
import hashlib
import json
import lzma
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PREFIX_SHAS = '''26ff34ee126dbec628dffe4ec06ce05b3f0c3526
1661751a7f5c3807699fddaf4cc7494895d02f82
71081ae6ca8e431353194a32bf16531f3ee60732
91503bac9482a10b0e6b0687fb5be78b3e917db2
7caf269b2df2c55a682d8df10f399d2e42171070
6c44855cb2441900ba4e764593bfe962ec7823a8
d45228913bdfdac579db4988b2bc72670f41ebdb
8449d0572c92eda6a694ab2ccc9b6adecf647584
d0768a8e70d5312d303ce2c38969ba016f4834a6
e82ac228b62d1d1f8c9a4472414b2e07a8e2762e
d3d88d739fea49c9a49a373e488005105467d067
7930d0c897f817aa3c49ae3f4fb812f230cfcd1b
0295e55cf09c5877658cdfcef9d16f0493500098
8e09fcd9749e5f8e9d7d50470f80985fb6914204
e7a1be7eb050526a55d91d5402224df2fe61a6d4'''.split()
TAIL_SHAS = '''da6eb73e16cea14ef53fc09510e6ebf2ce47fdfe
70170dc53a1488ba2f63d44d3429869fc5e53ebe
8869c5a0c1e962326c6f36cccd8b37422d714eb7
1d425dba5091a53e775a7a93c6995139ecb1bbeb
f5bcc708dcda707f7da36ee678a0938d323fab08
a56bfb8f23d9c75ac46eb70471dae34dbf6f3aff
92f879762dc230d7d9061217c8ccc387dbf6b248
a59c345ca6126b35f1b7ecc6e62aafc4c580f2fa
50b105a5753390540cc80cdeea26c6790ac7ca15
bda59ac231e995119e201ea15c422df0ea287a50
a4842e378b1510dffc7d192b1e2a697e7ffe7b09'''.split()

def load(sha):
    req = urllib.request.Request(
        f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/git/blobs/{sha}',
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=60) as response:
        raw = base64.b64decode(json.load(response)['content'])
    if hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() != sha:
        raise ValueError('Source blob identity mismatch')
    return raw

if __name__ == '__main__':
    # Inspect available original source records; no partial Python file is written.
    prefix = bytearray(b''.join(load(sha) for sha in PREFIX_SHAS))
    prefix[122916:122921] = bytes([140, 125, 98, 239, 254])
    packed = bytes(prefix) + b''.join(load(sha) for sha in TAIL_SHAS)
    text = lzma.LZMADecompressor().decompress(packed).decode('utf-8', errors='ignore')
    decoder = json.JSONDecoder()
    pos, paths = 1, []
    while pos < len(text):
        try:
            while text[pos].isspace() or text[pos] == ',': pos += 1
            name, pos = decoder.raw_decode(text, pos)
            while text[pos].isspace() or text[pos] == ':': pos += 1
            value, pos = decoder.raw_decode(text, pos)
        except (ValueError, IndexError): break
        if name.startswith('src/masar/'):
            paths.append(name)
    print(json.dumps({'complete_original_source_records': paths, 'last_complete_position': pos, 'decoded_bytes': len(text)}))
