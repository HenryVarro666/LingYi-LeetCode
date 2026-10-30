S0 = 'leetsco'
D0 = ['leet', 'co', 'leetco']


def _hit(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') not in (10, 11):
        return None
    return S['s'][j:i + 1] in S['words']


def _sc(S, k, v):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return None
    if j is not None and j <= k <= i and S.get('_line') in (10, 11):
        return 'green' if _hit(S) else 'yellow'
    if k == i:
        return 'blue'
    return None


def _fc(S, k, v):
    j = S.get('j')
    if S.get('i') is None:
        return None
    if k == len(S['f']) - 1 and k > 0:
        return 'yellow'
    if j is not None and k == j and _hit(S):
        return 'green'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None:
        return '`f[i]` = 前 `i` 个字符里最少有几个额外字符，`f[0] = 0`'
    if j is not None and S.get('_line') in (10, 11):
        sub = S['s'][j:i + 1]
        if sub in S['words']:
            return f'`s[{j}:{i + 1}] = "{sub}"` 出现在 dictionary 中 → `f[-1] = min(f[-1], f[{j}])`，`f[{j}]` = =={S["f"][j]}=='
        return f'`s[{j}:{i + 1}] = "{sub}"` 不是单词'
    return f'处理 `s[{i}]`：先放弃它，再尝试把它并入某个单词'


CONFIG = dict(
    num=2707, title='字符串中的额外字符', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP：枚举单词起点',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1736'],
    code='''
class Solution(object):
    def minExtraChar(self, s, dictionary):

        words = set(dictionary)
        n = len(s)
        f = [0]
        for i, char in enumerate(s):
            f.append(f[-1] + 1)
            for j in range(i + 1):
                if s[j : i + 1] in words:
                    f[-1] = min(f[-1], f[j])

        return f[-1]
''',
    call=f'Solution().minExtraChar({S0!r}, {D0!r})',
    expect=1,
    skip=['for j in range'],
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符 s[i]，黄/绿 = 正在检查的 s[j..i]）', h=150, cell=70,
             pointers={'j': 'pink', 'i': 'blue'}, color=_sc),
        dict(type='set', var='words', label='words', h=90, fmt=lambda x: f'"{x}"'),
        dict(type='text', fn=_formula, size=25, h=60),
        dict(type='array', var='f', label='f：f[k] = 前 k 个字符的最少额外字符数（黄 = 刚追加、正在更新的 f[-1]）', h=170, cell=70, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'words = set': '把字典转成集合，后面判断子串是不是单词很快',
        'f = [0]': '`f[0] = 0`：前 0 个字符是空串，没有额外字符',
        'for i, char in enumerate(s)': lambda S, B, r: (f'枚举 `s[{S.i}] = {S.char}`，它对应的结果要放在 `f[{S.i+1}]`' if S.get('i') != B.get('i')
                                                       else '`s` 里每个字符都处理完了'),
        'f.append(f[-1] + 1)': '方法 1：放弃 `s[{i}]`，当成额外字符 → `f[{i+1}] = f[{i}] + 1` = =={f[-1]}==',
        'if s[j : i + 1] in words': lambda S, B, r: (f'`s[{S.j}:{S.i+1}] = "{S.s[S.j:S.i+1]}"` ==出现==在 dictionary 中，可以从 `j = {S.j}` 起整段用掉'
                                                    if S.s[S.j:S.i+1] in S.words else f'`s[{S.j}:{S.i+1}] = "{S.s[S.j:S.i+1]}"` 不在 dictionary 中，这个起点 `j` 不行'),
        'f[-1] = min': '方法 2：`f[-1] = min({B.f[-1]}, f[{j}])` = =={f[-1]}==，单词前面剩 `f[{j}]` 个额外字符',
        'return f[-1]': '`f[-1]` 就是整串的答案：最少 =={ret}== 个额外字符',
    },
    cards=dict(
        one_liner='f[i] 表示前 i 个字符，放弃或并入某个单词',
        complexity='时间 `O(n^3)`，空间 `O(n)`',
        problem=['把 `s` 分成若干互不重叠、且在 `dictionary` 中出现过的子串',
                 '不在任何子串里的字符是额外字符，求最少有几个',
                 '示例：`"leetscode"`、`["leet","code","leetcode"]` → `1`（视频用更短的 `"leetsco"`）'],
        quote='令f[i]表示前i个字符中最少有几个额外字符，初始情况下f[0] = 0，也就是空串中没有额外字符。',
        quote_src='—— yiduobo 题解',
        idea=['一趟遍历，对 `s[i]` 有两种处理，结果都写进 `f[i+1]`',
              '放弃它：`f[i+1] = f[i] + 1`',
              '并入单词：枚举起点 `j`，`s[j:i+1]` 在字典中就取 `min(f[i+1], f[j])`'],
        summary=['时间：`i`、`j` 两层循环再加切片比较，`O(n^3)`；字典转集合是 `O(L)`',
                 '易错：`f[i + 1]` 对应前 `i+1` 个字符，起点 `j` 对应的是 `f[j]` 不是 `f[j-1]`',
                 '代码用 `f.append` 追加，所以 `f[-1]` 一直指向当前正在算的那格',
                 '原文代码无需修改即可在 Python 3 运行'],
    ),
)
