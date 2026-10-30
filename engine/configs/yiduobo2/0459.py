CASES = ['abab', 'aba', 'abcabc']


def _scan(s):
    """模拟 (s + s).find(s, 1)：返回每个起点的 (起点, 第一个不匹配的位置 或 None)"""
    t = s + s
    n = len(s)
    rows = []
    for p in range(1, n + 1):
        bad = None
        for k in range(n):
            if t[p + k] != s[k]:
                bad = k
                break
        rows.append((p, bad))
        if bad is None:
            break
    return rows


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S.get('s')
    if not isinstance(s, str):
        return
    n = len(s)
    t = s + s
    cell = min(64, (x1 - x0 - 200) / (2 * n))
    sx = x0 + 150 + ((x1 - x0 - 180) - cell * 2 * n) / 2
    y = y0 + 40
    cv.text((x0 + 18, y0 + 4), "s + s（蓝 = 第一份 s，紫 = 第二份 s）；下面每行 = 从起点 p 开始和 s 比", 22, T['muted'], bold=True)
    # 顶部 s + s
    for i, ch in enumerate(t):
        X = sx + i * cell
        c = T['blue'] if i < n else T['purple']
        cv.rect((X + 3, y, X + cell - 3, y + cell - 6), fill=c, r=8)
        cv.text((X + cell / 2, y + (cell - 6) / 2), ch, 30, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, y + cell - 2), i, 16, T['dim'], anchor='mt', mono=True)
    cv.text((sx - 16, y + (cell - 6) / 2), 's+s', 24, T['text'], anchor='rm', bold=True)
    y += cell + 26
    rows = _scan(s)
    rh = min(cell, (y1 - y - 70) / max(1, len(rows)))
    for p, bad in rows:
        ok = bad is None
        trivial = ok and p == n
        for k, ch in enumerate(s):
            X = sx + (p + k) * cell
            if ok:
                c = T['muted'] if trivial else T['green']
            elif k < bad:
                c = (70, 110, 80)
            elif k == bad:
                c = T['red']
            else:
                c = None
            if c is None:
                cv.rect((X + 3, y, X + cell - 3, y + rh - 8), outline=T['border'], width=2, r=8)
                cv.text((X + cell / 2, y + (rh - 8) / 2), ch, 26, T['dim'], anchor='mm', bold=True)
            else:
                cv.rect((X + 3, y, X + cell - 3, y + rh - 8), fill=c, r=8)
                cv.text((X + cell / 2, y + (rh - 8) / 2), ch, 26, T['bg'], anchor='mm', bold=True)
        tag = f'p={p}'
        cv.text((sx - 16, y + (rh - 8) / 2), tag, 22, T['green'] if ok and not trivial else T['muted'], anchor='rm', bold=True)
        if not ok:
            cv.text((sx + (p + n) * cell + 14, y + (rh - 8) / 2), f'第 {bad} 位不等 ×', 20, T['red'], anchor='lm')
        elif trivial:
            cv.text((sx + (p + n) * cell + 14, y + (rh - 8) / 2), 'p == len(s)，平凡匹配', 20, T['muted'], anchor='lm')
        else:
            cv.text((sx + (p + n) * cell + 14, y + (rh - 8) / 2), f'匹配！p 在中间', 20, T['green'], anchor='lm', bold=True)
        y += rh
    p, bad = rows[-1]
    msg = (f"find 返回 `{p}` ≠ `len(s) = {n}` → `s` 由 `s[0:{p}]` = =={s[:p]}== 重复 {n // p} 次得到"
           if p != n else f"find 返回 `{p}` == `len(s)`：中间没有匹配 → ==不能==由子串重复得到")
    cv.rich(x0 + 22, y1 - 56, msg, x1 - x0 - 44, size=26, accent=T['yellow'], max_lines=1)


def _cap(S, B, ret):
    s = S.s
    n = len(s)
    p = (s + s).find(s, 1)
    if p != n:
        return f'`s = "{s}"`：`(s + s).find(s, 1) = {p}`，起点在 s 中间 → 返回 ==True=='
    return f'`s = "{s}"`：`(s + s).find(s, 1) = {p} == len(s)`，只找到了第二份 s → 返回 ==False=='


CONFIG = dict(
    num=459, title='重复的子字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='s + s 里找 s：起点在中间即可重复',
    tags=['字节30天'],
    code='''
class Solution(object):
    def repeatedSubstringPattern(self, s):
        return (s + s).find(s, 1) != len(s)
''',
    call='\n'.join([f'r{i} = Solution().repeatedSubstringPattern({c!r})' for i, c in enumerate(CASES[:-1])]
                   + [f'Solution().repeatedSubstringPattern({CASES[-1]!r})']),
    expect=True,
    views=[dict(type='custom', draw=_draw, h=600)],
    watch=[('s', 's'), ('len(s)', lambda S: len(S['s']) if 's' in S else None, 'cyan'),
           ('find', lambda S: (S['s'] + S['s']).find(S['s'], 1) if 's' in S else None, 'green')],
    captions={
        'return (s + s).find(s, 1)': _cap,
    },
    cards=dict(
        one_liner='把 s 复制一遍接在后面，若 s 在中间某处出现，就能由子串重复得到',
        complexity='时间取决于 `find`：朴素最坏 `O(n²)`，用 KMP 可做到 `O(n)`；空间 `O(n)`',
        problem=['判断非空字符串 `s` 能否由它的一个子串==重复多次==构成',
                 '示例：`"abab"` → `true`（`"ab"` 重复两次）',
                 '示例：`"aba"` → `false`；`"abcabcabcabc"` → `true`',
                 '本视频依次演示 `"abab"`、`"aba"`、`"abcabc"`（一行代码，每个例子一步）'],
        quote='直接将原始字符串s复制一遍，接在后面形成新串s\'，然后在s\'中找s。若存在一个s的起点不等于0，且不等于len(s)，==即这个起点在s中间==，那么这个字符串就可以由子串重复得到。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s + s` 里 s 一定出现在起点 `0` 和 `len(s)`，这两个是"平凡"的',
              '`find(s, 1)` 从起点 1 开始找，跳过起点 0',
              '找到的起点 `p < len(s)` → 可以重复；`p == len(s)` → 不行'],
        after=[dict(heading='为什么成立？（yiduobo 的证明）', chapter='④ 证明',
                    lines=['设起点为 `p`：`s` 与 `s\'[p : p + len(s)]` 一致',
                           '于是 `s[0:p]` = `s\'[p:2p]` = `s[p:2p]`',
                           '==逐个往后递推==：`s[p:2p]` = `s[2p:3p]` = …',
                           '所以 `s` 由 `s[0:p]` 重复构成（`p` 一定整除 `len(s)`）'])],
        result='三个例子：`"abab"` → True，`"aba"` → False，`"abcabc"` → True ✓',
        summary=['一行代码：`(s + s).find(s, 1) != len(s)`',
                 '`find` 的第二个参数 `1`：==从下标 1 开始找==，排除起点 0',
                 '起点 `len(s)` 一定能找到（第二份 s），所以 find 不会返回 -1',
                 '更严格的线性做法：KMP 求 `s + s` 去掉首尾后是否含 `s`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
