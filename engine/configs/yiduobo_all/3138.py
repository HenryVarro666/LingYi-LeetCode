def _col(S, i, v):
    if 'length' not in S:
        return None
    L = S['length']
    if S.get('_line') in (8, 9, 10, 11) and 'index' in S and S['index'] <= i < S['index'] + L:
        return 'blue' if S.get('flag', True) else 'red'
    if 'freq' in S and i < L:
        return 'green'
    return None


def _txt(S):
    if 'length' not in S:
        return '`t` 的长度必须是 n 的约数；约数很少（10^5 内最多 128 个），逐个试'
    n = len(S['s'])
    if n % S['length']:
        return f"`length = {S['length']}`：{n} % {S['length']} ≠ 0，不是约数，换下一个"
    if 'freq' not in S:
        return f"`length = {S['length']}` 是约数，分成 {n // S['length']} 段"
    return f"模板 `freq = {dict(S['freq'])}`：后面每段的字母个数必须与它完全相同"


CONFIG = dict(
    num=3138, title='同位字符串连接的最小长度', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举约数 + 字母计数比较',
    tags=[],
    code='''
class Solution(object):
    def minAnagramLength(self, s):

        for length in range(1, len(s)):
            if len(s) % length == 0:
                freq = Counter(s[:length])
                flag = True
                for index in range(length, len(s), length):
                    if Counter(s[index : index + length]) != freq:
                        flag = False
                        break
                
                if flag:
                    return length
        
        return len(s)
''',
    call='Solution().minAnagramLength("aabbaa")',
    expect=3,
    skip=['flag = True'],
    views=[
        dict(type='string', var='s', label='s（绿 = 第一段模板，蓝 = 正在比较的段，红 = 不同位）', cell=90, color=_col, h=230),
        dict(type='map', var='freq', label='freq = 第一段的字母个数', fmt=lambda k, v: f"'{k}': {v}", h=160, font=34),
        dict(type='text', fn=_txt, size=28, h=120),
    ],
    watch=['length', 'index', 'flag'],
    captions={
        'for length in range': '试 `t` 的长度 `length = {length}`（只试到 `len(s) - 1`，最后兜底是 `len(s)`）',
        'if len(s) % length': lambda S, B, r: (f"`{len(S.s)} % {S.length} == 0` → 是约数，可能成立" if len(S.s) % S.length == 0 else f"`{len(S.s)} % {S.length} = {len(S.s) % S.length}` → 不是约数，==整除才能切成整段，跳过=="),
        'freq = Counter': '第一段 `{s[:length]}` 的字母个数 `{dict(freq)}` 当模板',
        'for index in range(length': '下一段从 `index = {index}` 开始',
        'if Counter': lambda S, B, r: (lambda c: f"段 `{S.s[S.index:S.index + S.length]}` 的字母个数 {dict(c)} " + ('与模板相同，继续看下一段' if c == S.freq else '≠ 模板 → ==不是同位字符串，这个长度失败=='))(Counter(S.s[S.index:S.index + S.length])),
        'flag = False': '有一段对不上，`flag = False`，==不用再比，break==',
        'if flag': lambda S, B, r: ('每段都与模板同位 → ==这个 length 就是最小的 t 长度==' if S.flag else '这个 length 失败，试更大的'),
        'return length': '返回最小的可行长度 =={ret}==（从小到小枚举，第一个成功的就是最小）'.replace('从小到小', '从小到大'),
        'return len(s)': '没有更短的，`t` 就是 `s` 本身，返回 {ret}',
    },
    cards=dict(
        one_liner='t 的长度必是 n 的约数：从小到大试，每段字母个数都一样就停',
        complexity='时间 `O(A·n)`（A 为 n 的约数个数，最多 128），空间 `O(1)`',
        problem=['`s` 由 `t` 和若干个 `t` 的同位字符串（重排）拼成',
                 '求 `t` 的最小长度，`t` 可以等于 `s`',
                 '示例：`"abba"` → `2`；`"cdef"` → `4`',
                 '演示用 `"aabbaa"`：`length=3` 时 `aab` 与 `baa` 同位 → `3`'],
        quote='t的长度必然是s长度的约数，而约数的增长速度其实是非常缓慢的……即使n的规模来到10^5，其中约数数目最多也不会很大。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度不整除 n 就切不成整段，直接排除',
              '约数少：从 1 到 n-1 暴力扫，只对约数做计数比较',
              '每段的 `Counter` 都等于第一段，就说明是同位字符串'],
        summary=['时间 `O(A·n)`：10^5 内约数最多 128 个（83160）',
                 '易错：`range(1, len(s))` 不含 `len(s)`，兜底 `return len(s)`',
                 '先找到的就是最小，所以从小到大枚举',
                 '原文为 Python 2 写法，代码未改，只保留原文 Counter 比较'],
    ),
)
