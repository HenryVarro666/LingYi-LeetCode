def _pairs(s):
    return [(abs(ord(a) - ord(b))) for a, b in zip(s, s[1:])]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    n = len(s)
    cell = min(110, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    cv.text((x0 + 18, y0 + 4), '相邻字符 ASCII 码之差的绝对值', 26, T['muted'], bold=True)
    ys = y0 + 110
    for i, ch in enumerate(s):
        X = sx + i * cell
        cv.rect((X + 4, ys, X + cell - 4, ys + 70), fill=T['blue'] if False else (70, 76, 86), r=8)
        cv.text((X + cell / 2, ys + 35), ch, 40, T['text'], anchor='mm', bold=True)
        cv.text((X + cell / 2, ys + 92), ord(ch), 24, T['muted'], anchor='mt', mono=True)
    d = _pairs(s)
    done = len(d) if 'ans' in S and S.get('_line') and S['_line'] > 4 else 0
    for i, v in enumerate(d):
        X = sx + (i + 1) * cell
        cv.text((X, ys + 190), f'|Δ|={v}', 26, T['green'], anchor='mm', bold=True)
    cv.text((x0 + 18, ys + 260), '累加：' + ' + '.join(str(v) for v in d) + f' = {sum(d)}', 34, T['yellow'], bold=True)


CONFIG = dict(
    num=3110, title='字符串的分数', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='相邻元素 pairwise', tags=[],
    code='''
class Solution:
    def scoreOfString(self, s: str) -> int:
        return sum(abs(x - y) for x, y in pairwise(map(ord, s)))
''',
    call='Solution().scoreOfString("hello")',
    expect=13,
    views=[
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[],
    captions={
        'return sum': lambda S, B, r: f'`map(ord, s)` 转成 ASCII 码，`pairwise` 取相邻两个，`abs(x - y)` 求差，再 `sum` 累加 → =={r}==',
    },
    cards=dict(
        after=[dict(heading='拆开看 "hello"', lines=['`h=104, e=101, l=108, l=108, o=111`', '`|104−101| + |101−108| + |108−108| + |108−111|`', '`= 3 + 7 + 0 + 3 = 13`'])],
        one_liner='相邻字母 ASCII 码的绝对差，一路累加',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['分数 = 相邻字符 ASCII 码之差的绝对值之和', '示例：`"hello"` → `3+7+0+3 = 13`',
                 '示例：`"zaz"` → `25+25 = 50`'],
        quote='遍历字符串 s，累加相邻字母 ASCII 值的绝对差，即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`map(ord, s)` 把每个字符变成 ASCII 码', '`pairwise` 依次给出 (s[0],s[1])、(s[1],s[2])…', '生成器表达式求绝对差，交给 `sum`'],
        summary=['时间 `O(n)`，空间 `O(1)`', '`pairwise` 在 Python 3.10+ 才有，LeetCode 已预置',
                 '长度为 n 只有 n-1 对，不要多算'],
    ),
)
