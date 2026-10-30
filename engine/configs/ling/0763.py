_SEG = ['green', 'cyan', 'purple', 'orange']


def _seg_of(S, k):
    """k 属于第几个已完成的片段（未完成返回 None）"""
    acc = 0
    for idx, ln in enumerate(S.get('ans') or []):
        if k < acc + ln:
            return idx
        acc += ln
    return None


def _color(S, k, v):
    g = _seg_of(S, k)
    return _SEG[g % 4] if g is not None else None


def _draw_letters(cv, S, B, box, T):
    """每个字母画成区间 [第一次出现, 最后一次出现]，和上面的字符串格子对齐"""
    x0, y0, x1, y1 = box
    s = S.get('s')
    if not s:
        return
    n = len(s)
    width = x1 - x0 - 40
    cell = min(88, width / n)
    sx = x0 + 20 + (width - cell * n) / 2
    cv.text((x0 + 18, y0 + 4), '每个字母的区间 [第一次, 最后一次]：片段必须把它整个包住', 24, T['muted'], bold=True)
    letters = list(dict.fromkeys(s))
    rowh = min(40, (y1 - y0 - 50) / len(letters))
    i = S.get('i', -1)
    for r, ch in enumerate(letters):
        pos = [k for k, c in enumerate(s) if c == ch]
        a, b = pos[0], pos[-1]
        y = y0 + 46 + r * rowh + rowh / 2
        g = _seg_of(S, a)
        if g is not None:
            c = T[_SEG[g % 4]]
        elif 'i' in S and S.get('c') == ch:
            c = T['yellow']
        elif a <= i:
            c = T['blue']
        else:
            c = T['border']
        cv.text((sx - 16, y), ch, 22, c, anchor='rm', bold=True, mono=True)
        cv.rect((sx + a * cell + cell * 0.3, y - 4, sx + b * cell + cell * 0.7, y + 4), fill=c, r=4)
        for k in pos:
            X = sx + k * cell + cell / 2
            cv.d.ellipse((X - 7, y - 7, X + 7, y + 7), fill=c)


CONFIG = dict(
    num=763, title='划分字母区间', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='合并区间',
    code='''
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last = {c: i for i, c in enumerate(s)}  # 每个字母最后出现的下标
        ans = []
        start = end = 0
        for i, c in enumerate(s):
            end = max(end, last[c])  # 更新当前区间右端点的最大值
            if end == i:  # 当前区间合并完毕
                ans.append(end - start + 1)  # 区间长度加入答案
                start = end + 1  # 下一个区间的左端点
        return ans
''',
    call='Solution().partitionLabels("abacbdedff")',
    expect=[5, 3, 2],
    views=[
        dict(type='string', var='s', cell=88, h=190, pointers={'i': 'yellow'}, window=('start', 'end'), color=_color),
        dict(type='map', var='last', h=96, font=22, fmt=lambda k, v: f'{k}:{v}'),
        dict(type='custom', h=300, draw=_draw_letters),
    ],
    watch=[('i', 'i', 'yellow'), 'c', ('start', 'start', 'cyan'), ('end', 'end', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'last = {c: i': '先算每个字母==最后出现的下标== `last`：同一字母后出现的下标会覆盖前面的',
        'ans = []': '`ans` 存每个片段的长度',
        'start = end = 0': '当前正在合并的区间 `[start, end]`（青框），从 `[0, 0]` 开始',
        'for i, c in enumerate(s)': lambda S, B, ret: ('遍历结束' if B.get('i') == S['i']
                                                       else f'`i = {S["i"]}`，字母 `{S["c"]}`'),
        'end = max(end, last[c])': lambda S, B, ret: (
            f'区间要包住所有 `{S["c"]}` → 右端点至少到 `last[{S["c"]!r}] = {S["last"][S["c"]]}`：`end = max({B["end"]}, {S["last"][S["c"]]}) = {S["end"]}`'
            + ('　==区间变长==' if S['end'] > B['end'] else '')),
        'if end == i': lambda S, B, ret: (
            f'`end == i == {S["i"]}`：区间里每个字母的最后一次出现都已包住 → ==合并完毕=='
            if S['end'] == S['i'] else f'`end = {S["end"]} > i = {S["i"]}`：后面还有必须包进来的字母，继续'),
        'ans.append(end - start + 1)': '区间 `[{start}, {end}]` 长度 `{end} - {start} + 1 = {ans[-1]}` 加入答案',
        'start = end + 1': '下一个区间从 `start = {start}` 开始',
        'return ans': '返回 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='每个字母是一个区间 [第一次, 最后一次]，把重叠的区间合并',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['把字符串 `s` 划分成尽量多的片段，==同一字母最多出现在一个片段中==',
                 '返回每个片段的长度',
                 '例：`"abacbdedff"` → `[5,3,2]`（`abacb` | `ded` | `ff`）'],
        quote='「同一字母最多出现在一个片段中」意味着，一个片段若要包含字母 a，那么所有的字母 a 都必须在这个片段中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字母 `a` 出现在下标 0、2 → 包含 `a` 的片段至少包含区间 `[0, 2]`',
              '区间里还有别的字母，它们的区间也得包进来 → ==合并区间==',
              '合并后的大区间不能再切开，所以它们的长度就是答案（片段最多）'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`（26 个小写字母）',
                 '`end == i` 才说明区间合并完毕；注意用 `max` 更新 `end`，不能直接赋值',
                 '实现上不用真的列出区间：`last[c]` 就是区间右端点，从左往右扫天然按左端点有序',
                 '相似题：56. 合并区间'],
    ),
)
