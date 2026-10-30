_SEG = ['green', 'cyan', 'purple', 'orange']


def _color(S, k, v):
    acc = 0
    for idx, ln in enumerate(S.get('res') or []):
        if k < acc + ln:
            return _SEG[idx % 4]
        acc += ln
    return None


def _info(S):
    if 'r' not in S or 'pos' not in S or S['l'] >= len(S['S']):
        return '区间 `[l, r]`（青框）：`r` 必须够到区间里每个字符的 `last_pos`'
    l, r, pos, s, lp = S['l'], S['r'], S['pos'], S['S'], S['last_pos']
    if pos < len(s) and pos < r:
        return f'区间 `[{l}, {r}]`，检查 `S[{pos}] = {s[pos]!r}`，它最后出现在 `{lp[s[pos]]}`'
    return f'区间 `[{l}, {r}]`'


CONFIG = dict(
    num=763, title='划分字母区间', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='预处理 last_pos + 逐段扩展右边界',
    code='''
class Solution(object):
    def partitionLabels(self, S):
        last_pos = {}
        for index, char in enumerate(S):
            last_pos[char] = index

        l = 0
        res = []
        while l < len(S):
            r = last_pos[S[l]]
            pos = l + 1
            while pos < r:
                if last_pos[S[pos]] > r:
                    r = last_pos[S[pos]]
                pos += 1
            res.append(r - l + 1)
            l = r + 1

        return res
''',
    call='Solution().partitionLabels("abacbdedff")',
    expect=[5, 3, 2],
    views=[
        dict(type='text', h=52, size=26, fn=_info),
        dict(type='string', var='S', cell=88, h=250, color=_color,
             pointers={'l': 'blue', 'r': 'pink', 'pos': 'yellow'}, window=('l', 'r')),
        dict(type='map', var='last_pos', label='last_pos：每个字母最后出现的位置', h=100, font=22, fmt=lambda k, v: f'{k}:{v}'),
        dict(type='text', h=60, size=28, fn=lambda S: f'已划分的长度 `res = {S["res"]}`' if 'res' in S else ''),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('pos', 'pos', 'yellow')],
    skip=['for index, char in enumerate(S)', 'last_pos[char] = index'],
    captions={
        'last_pos = {}': '先从头到尾扫一趟，==预处理出每个字母最后出现的位置== `last_pos`',
        'l = 0': '预处理完成（见下方 `last_pos`）。左边界 `l` 从 0 开始',
        'res = []': '`res` 存每段的长度',
        'while l < len(S)': lambda S, B, ret: (f'`l = {S["l"]} < {len(S["S"])}`：从 `l` 开始划分新的一段' if S['l'] < len(S['S'])
                                               else '`l` 到末尾了，划分结束'),
        'r = last_pos[S[l]]': '`S[l] = {S[l]!r}`：必须把 `l` 到它最后出现的位置都划进来 → `r = last_pos[{S[l]!r}] = {r}`',
        'pos = l + 1': '`pos = {pos}`：逐个检查 `l + 1` 到 `r` 之间的字符',
        'while pos < r': lambda S, B, ret: (f'`pos = {S["pos"]} < r = {S["r"]}`：还有字符没检查' if S['pos'] < S['r']
                                            else f'`pos = {S["pos"]}` 到了 `r = {S["r"]}`：区间里的字符都满足条件'),
        'if last_pos[S[pos]] > r': lambda S, B, ret: (
            f'`{S["S"][S["pos"]]}` 最后出现在 `{S["last_pos"][S["S"][S["pos"]]]}` > `r = {S["r"]}` → ==r 要往右移==' if S['last_pos'][S['S'][S['pos']]] > S['r']
            else f'`{S["S"][S["pos"]]}` 最后出现在 `{S["last_pos"][S["S"][S["pos"]]]}` ≤ `r = {S["r"]}`：已经在区间里'),
        'r = last_pos[S[pos]]': '`r` 右移到 `{r}`',
        'pos += 1': '`pos` → `{pos}`',
        'res.append(r - l + 1)': '`[{l}, {r}]` 是一个合法的划分，长度 `{r} - {l} + 1 = {res[-1]}`',
        'l = r + 1': '从 `l = r + 1 = {l}` 开始继续划分',
        'return res': '返回 `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='先记下每个字母最后出现的位置，再一段一段地把右边界往右推',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['把字符串划分成尽量多的片段，==同一字母最多出现在一个片段中==',
                 '返回每个片段的长度',
                 '例：`"abacbdedff"` → `[5,3,2]`（`abacb` | `ded` | `ff`）'],
        quote='如果我们从头到尾进行划分的话，只需要关注每个字母最后一次出现的位置last_pos。那么可以首先从头到尾进行一趟扫描，预处理出每个字母最后出现的位置。',
        quote_src='—— yiduobo 题解',
        idea=['先令 `r = last_pos[S[l]]`：`S[l]` 的所有出现都得划进来',
              '逐个检查 `l+1` 到 `r` 的字符，谁最后出现的位置大于 `r`，就把 `r` ==往右移==到那里',
              '`[l, r]` 都满足条件后就是一个合法划分，再从 `l = r + 1` 继续'],
        summary=['时间 `O(n)`：每个字符只被检查一次；空间 `O(|Σ|)`',
                 '内层 `while pos < r` 每轮都重新读 `r`，`r` 变大后会继续检查',
                 '与灵神写法本质相同：灵神用一个 for + `end == i` 判断，这里是两层 while',
                 '只删去了 `"""type ..."""` 文档字符串，其余照搬（兼容 Python 3）'],
    ),
)
