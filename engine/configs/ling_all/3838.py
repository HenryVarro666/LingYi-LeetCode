W = [5, 3, 12, 14, 1, 2, 3, 2, 10, 6, 6, 9, 7, 8, 7, 10, 8, 9, 6, 9, 9, 8, 3, 7, 7, 2]


def _txt(S):
    if 'w' not in S:
        return ''
    if 's' in S and S['_line'] >= 8:
        s = S['s']
        return f"`w = {S['w']!r}`：权重和 `{s}`，`{s} % 26 = {s % 26}`，映射为 `z` 往前 {s % 26} 位 = =={chr(122 - s % 26)}=="
    return f"`w = {S['w']!r}`：把每个字母的权重加起来"


def _wcolor(S, i, v):
    w = S.get('w')
    if w is None or S['_line'] < 7:
        return None
    return 'blue' if chr(97 + i) in w else None


CONFIG = dict(
    num=3838, title='带权单词映射', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='模拟 · 减法映射',
    tags=[],
    code='''
class Solution:
    def mapWordWeights(self, words: List[str], weights: List[int]) -> str:
        ans = []
        ord_a = ord('a')
        ord_z = ord('z')
        for w in words:
            s = sum(weights[ord(ch) - ord_a] for ch in w)
            ans.append(chr(ord_z - s % 26))
        return ''.join(ans)
''',
    call=f'Solution().mapWordWeights(["abcd", "def", "xyz"], {W})',
    expect='rij',
    views=[
        dict(type='string', var='w', label='当前单词 w', cell=84, h=130),
        dict(type='array', var='weights', label='weights（a~z 的权重，蓝 = w 里出现的字母）', cell=36, h=150, index=False, color=_wcolor),
        dict(type='text', h=110, size=30, fn=_txt),
        dict(type='array', var='ans', label='ans（已映射的字符）', cell=84, h=150),
    ],
    watch=[('w', 'w', 'blue'), ('s', 's', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = []': '`ans` 收集每个单词映射后的字符',
        'ord_a = ord': '`ord_a = {ord_a}`：字母 `ch` 的权重下标就是 `ord(ch) - ord_a`',
        'ord_z = ord': '`ord_z = {ord_z}`：倒序映射要从 `z` 往前数',
        'for w in words': lambda S, B, r: (f'取下一个单词 `w = {S.w!r}`' if 'w' not in B or S.w != B.w or S.ans != B.ans else '所有单词处理完'),
        's = sum': '`w = {w!r}` 的字母权重（蓝色格）相加：`s = {s}`',
        'ans.append': '倒序映射 = `z` 减去 `s % 26`：`{s} % 26 = {s % 26}` → `{ans[-1]!r}`',
        'return': '把 `ans` 拼起来，返回 `{ret!r}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='倒序映射 = 用 `z` 减去权重和对 26 的余数',
        complexity='时间 `O(L)`，空间 `O(1)`',
        problem=['每个字母有权重，单词权重 = 字母权重之和',
                 '把权重对 26 取模，按 `0->z, 1->y, ..., 25->a` 映射成字母',
                 '示例：`["abcd","def","xyz"]` → `"rij"`'],
        quote='「将结果按字母倒序映射到一个小写英文字母」，相当于把 z 减去权重取模后的值：减 0 就是 z，减 1 就是 y …… 减 25 就是 a。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`weights[ord(ch) - ord_a]` 取字母权重，累加成 `s`',
              '倒序映射不用查表：`chr(ord_z - s % 26)`',
              '每个单词得到一个字符，按顺序拼接'],
        summary=['时间 `O(L)`，`L` 是所有单词长度之和；空间 `O(1)`',
                 '易错：先取模再映射；`0` 对应 `z`，不是 `a`',
                 '字符和数字互转：`ord` 与 `chr`，下标 = 字符 − `a`'],
    ),
)
