"""Rewrite PEP 701-style f-strings (same quote nested inside {...}, Python 3.12+) so they also parse on Python 3.10.

python pipeline/py310fix.py FILE...    # in place; prints FIXED/OK per file
Inside the {...} of an f'...' string, inner ' become " (and vice versa for f"..." strings).  Plain and triple-quoted
strings (e.g. the author's code block) are left untouched.
"""
import sys


def fix(src):
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == '#':
            j = src.find('\n', i)
            j = n if j < 0 else j
            out.append(src[i:j]); i = j; continue
        if c in '\'"':
            # find prefix letters already emitted
            k = len(out) - 1
            pre = ''
            while k >= 0 and len(out[k]) == 1 and out[k].isalpha() and len(pre) < 2:
                pre = out[k] + pre; k -= 1
            is_f = 'f' in pre.lower()
            if src.startswith(c * 3, i):
                j = src.find(c * 3, i + 3)
                j = n if j < 0 else j + 3
                out.append(src[i:j]); i = j; continue
            if not is_f:
                j = i + 1
                while j < n and src[j] != c and src[j] != '\n':
                    j += 2 if src[j] == '\\' else 1
                out.append(src[i:j + 1]); i = j + 1; continue
            # f-string with delimiter c
            other = '"' if c == "'" else "'"
            out.append(c); i += 1; depth = 0
            while i < n:
                ch = src[i]
                if depth == 0:
                    if ch == '\\':
                        out.append(src[i:i + 2]); i += 2; continue
                    if ch == c:
                        out.append(ch); i += 1; break
                    if src.startswith('{{', i):
                        out.append('{{'); i += 2; continue
                    if ch == '{':
                        depth = 1
                    out.append(ch); i += 1
                else:
                    if ch == '{':
                        depth += 1
                    elif ch == '}':
                        depth -= 1
                    out.append(other if ch == c else ch); i += 1
            continue
        out.append(c); i += 1
    return ''.join(out)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = open(p, encoding='utf-8').read()
        t = fix(s)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
        print('FIXED' if t != s else 'OK   ', p)
