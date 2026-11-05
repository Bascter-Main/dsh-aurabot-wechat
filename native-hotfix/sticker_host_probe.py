#!/usr/bin/env python3
"""Read a trusted-local message XML/JSON file; output only sticker CDN host diagnostics."""
import argparse
import html
import json
import re
import sys
from urllib.parse import urlsplit

ALLOWED = {"snsvideo.c2c.wechat.com", "wxapp.tc.qq.com", "emoji.qpic.cn", "mmbiz.qpic.cn", "vweixinf.tc.qq.com"}
ATTR = re.compile(r'\b(cdnurl|thumburl|encrypturl)\s*=\s*(["\'])(.*?)\2', re.I | re.S)

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", nargs="?", help="Local XML/JSON fixture; otherwise stdin")
    a = p.parse_args()
    if a.file:
        with open(a.file, "rb") as f:
            data = f.read(1_048_577)
    else:
        data = sys.stdin.buffer.read(1_048_577)
    if len(data) > 1_048_576:
        print("ERROR: input exceeds 1 MiB", file=sys.stderr)
        return 2
    s = data.decode("utf-8", "replace")
    try:
        o = json.loads(s)
        if isinstance(o, dict):
            for key in ("rawContent", "content", "body", "xml"):
                if isinstance(o.get(key), str):
                    s = o[key]
                    break
    except json.JSONDecodeError:
        pass
    fields = []
    for match in ATTR.finditer(html.unescape(s)):
        label = match.group(1).lower()
        try:
            u = urlsplit(html.unescape(match.group(3)))
            h = (u.hostname or "").lower()
            scheme = u.scheme.lower()
            port = u.port
            valid = h in ALLOWED and scheme in ("http", "https") and not u.username and not u.password and not u.fragment and (port is None or port == (443 if scheme == "https" else 80))
            fields.append({"field":label, "host":h, "scheme":scheme, "port":port, "patch_allowlisted":valid})
        except ValueError:
            fields.append({"field":label, "host":"<unparseable>", "patch_allowlisted":False})
    print(json.dumps({"urls_detected":len(fields),"sources":fields,"note":"No secret paths or query strings are printed. If zero URLs: provide original message XML, not normalized message body."},ensure_ascii=False,indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
