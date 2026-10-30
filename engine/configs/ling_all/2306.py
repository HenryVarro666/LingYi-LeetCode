IDEAS = ["coffee", "donuts", "time", "toffee"]


def _key(S, st):
    for k, v in S['groups'].items():
        if v is st:
            return k
    return '?'


def _fmt(v):
    return '{' + ','.join(sorted(v)) + '}'


def _txt(S):
    if 'a' not in S or 'b' not in S:
        return '按首字母分组，组里只存去掉首字母后的字符串'
    a, b = S['a'], S['b']
    ka, kb = _key(S, a), _key(S, b)
    s = f"`{ka}` 组 {_fmt(a)}　`{kb}` 组 {_fmt(b)}"
    if 'm' in S:
        s += f"\n交集 {_fmt(a & b)}，`m = {S['m']}`"
    return s


CONFIG = dict(
    num=2306, title='公司命名', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='按首字母分组 · 集合交集',
    tags=['灵神题单·数学算法', '难度分 2305'],
    code='''
class Solution:
    def distinctNames(self, ideas: List[str]) -> int:
        groups = defaultdict(set)
        for s in ideas:
            groups[s[0]].add(s[1:])  # 按照首字母分组

        ans = 0
        for a, b in combinations(groups.values(), 2):  # 枚举所有组对
            m = len(a & b)  # 交集的大小
            ans += (len(a) - m) * (len(b) - m)
        return ans * 2  # 乘 2 放到最后
''',
    call='Solution().distinctNames(["coffee","donuts","time","toffee"])',
    expect=6,
    setup='from itertools import combinations',
    views=[
        dict(type='map', var='groups', fmt=lambda k, v: f'{k} → {_fmt(v)}', label='groups：首字母 → 去掉首字母后的字符串集合', h=250),
        dict(type='text', fn=_txt, size=30, h=180),
    ],
    watch=['m', ('ans', 'ans', 'green')],
    captions={
        'groups = defaultdict': '`groups`：首字母 → 后缀集合',
        'groups[s[0]].add': '`{s}` 放进 `{s[0]}` 组，只存后缀 `{s[1:]}`',
        'ans = 0': '`ans` 先累计「A 选一个、B 选一个」的对数，最后再乘 2（谁在左谁在右）',
        'for a, b in combinations': lambda S, B, r: ('三组两两配对都枚举完了' if ('a' in B and S.a == B.a and S.b == B.b) else f'取一对首字母不同的组：`{_key(S, S.a)}` 组 × `{_key(S, S.b)}` 组（同组内不能换，换了字符串不变）'),
        'm = len(a & b)': lambda S, B, r: (f'共有后缀 {_fmt(S.a & S.b)}：这些名字换首字母会撞上对方已有的名字，不能选，`m = {S.m}`' if S.m else f'两组没有共有后缀，`m = 0`：谁和谁都能换'),
        'ans += ': lambda S, B, r: f'A 去掉共有后缀剩 `{len(S.a)} − {S.m}` 个，B 剩 `{len(S.b)} − {S.m}` 个 → 乘法原理 `{(len(S.a) - S.m) * (len(S.b) - S.m)}` 对，`ans = {S.ans}`',
        'return ans': '每一对有先后两种顺序：`ans × 2` = =={ret}==',
    },
    cards=dict(
        one_liner='按首字母分组，两组之间减去共有后缀，再乘 2',
        complexity='时间 `O(nm|Σ|)`，空间 `O(nm+|Σ|)`',
        problem=['从 `ideas` 选两个不同名字，交换首字母',
                 '==两个新名字都不在 ideas 里==，才算一个有效公司名字（谁在前算不同）',
                 '示例：`["coffee","donuts","time","toffee"]` → `6`'],
        quote='第一组的 ac 无法和第二组的任何字符串交换，因为交换后会得到 bc，它在 ideas 中。其余字符串对可以交换首字母。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同首字母的两个名字，交换后不变，必然在 ideas 里 → 只看不同首字母的组对',
              '组 A、B 里==共有的后缀==换首字母会撞车，不能选',
              '合法对数 `2·(|A|−|A∩B|)·(|B|−|A∩B|)`，枚举所有组对累加'],
        after=[dict(heading='另一种写法', lines=['方法二：按后缀分组，遍历时直接累加 `intersection[a][b]`', '不用显式求集合交，时间 `O(n(m+|Σ|)+|Σ|²)`', '这里演示方法一，因为组对只有 3 个，看得最清楚'])],
        summary=['时间 `O(nm|Σ|)`，空间 `O(nm+|Σ|)`',
                 '只有一半顺序：代码里先不乘 2，最后统一 `ans * 2`',
                 '必须存「去掉首字母」的后缀，否则看不出共有部分',
                 '只有同后缀才会撞车，所以交集大小就是被禁用的名字数'],
    ),
)
