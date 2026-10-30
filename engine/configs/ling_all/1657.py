S0, T0 = 'cabbba', 'abbccc'


def _cnt_txt(S):
    if 'cs' not in S:
        return '操作 1 = 随意洗牌；操作 2 = 交换两个字母的出现次数'
    a, b = sorted(S['cs'].values()), sorted(S['ct'].values()) if 'ct' in S else None
    if b is None:
        return ''
    ks = '一样' if S['cs'].keys() == S['ct'].keys() else '不同'
    return f'字符集合{ks}；出现次数的集合：s = `{a}`，t = `{b}`' + (' ==相同==' if a == b else ' 不同')


CONFIG = dict(
    num=1657, title='确定两个字符串是否接近', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='字符集合 + 出现次数的集合',
    tags=['灵神题单', '难度分 1530'],
    code='''
class Solution:
    def closeStrings(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        cs, ct = Counter(s), Counter(t)
        return cs.keys() == ct.keys() and Counter(cs.values()) == Counter(ct.values())
''',
    call=f'Solution().closeStrings("{S0}", "{T0}")',
    expect=True,
    views=[
        dict(type='string', var='s', label='s', cell=76),
        dict(type='string', var='t', label='t', cell=76),
        dict(type='map', var='cs', label='cs：s 中每个字符出现几次', fmt=lambda k, v: f'{k} × {v}'),
        dict(type='map', var='ct', label='ct：t 中每个字符出现几次', fmt=lambda k, v: f'{k} × {v}'),
        dict(type='text', fn=_cnt_txt, size=26),
    ],
    watch=[('len(s)', 'len(s)'), ('len(t)', 'len(t)')],
    captions={
        'if len(s) != len(t)': '两个操作都不改变长度：`{len(s)}` vs `{len(t)}` → ==长度一样==，继续',
        'cs, ct = Counter': '操作 1 能随意洗牌，位置不重要，只看==字符及出现次数==：`cs = {dict(cs)}`，`ct = {dict(ct)}`',
        'return': lambda S, B, ret: (
            f'字符集合：`{sorted(S.cs)}` vs `{sorted(S.ct)}` {"一样" if S.cs.keys() == S.ct.keys() else "不同"}；'
            f'次数的集合：`{sorted(S.cs.values())}` vs `{sorted(S.ct.values())}`（操作 2 可以==交换次数==）→ `{ret}`'),
    },
    cards=dict(
        one_liner='操作 1 是洗牌，操作 2 是交换出现次数',
        complexity='时间 `O(n+m)`，空间 `O(|Σ|)`',
        problem=['操作 1：交换任意两个字符；操作 2：把两种字符整体互换',
                 '问能否用这两个操作把 `word1` 变成 `word2`',
                 '示例：`"cabbba"` → `"abbccc"`，答案 `true`'],
        quote='把 s 看成是一叠扑克牌，我们可以随意洗牌。……所以「出现次数」也像操作 1 那样，是可以任意排列的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['操作 1 的本质：字符可以任意排列 → 只看每个字符出现几次',
              '操作 2 的本质：交换两个字符的出现次数，次数也能任意排列',
              '所以要同时满足：长度相同、字符集合相同、出现次数的集合相同'],
        after=[dict(heading='为什么次数能任意排列', lines=[
            '`a` 出现 2 次、`b` 出现 3 次：把 `a` 全变 `b`、`b` 全变 `a`',
            '等于交换了两个字符的出现次数，再配合 `c` 就能凑出任意排列',
            '所以次数的集合一样，就能用两种操作互相转化'])],
        result='字符集合都是 `{a,b,c}`，次数集合都是 `{1,2,3}` → True ✓',
        summary=['时间 `O(n+m)`，空间 `O(|Σ|)`',
                 '易错：次数集合要当==多重集==比较，`aabbbccc` 对应 `{2,3,3}`',
                 '易错：只比次数不比字符集合会错，`abc` 和 `def` 不接近',
                 '这里选的是写法二；写法一把三个条件连成一行 `and`，逻辑相同'],
    ),
)
