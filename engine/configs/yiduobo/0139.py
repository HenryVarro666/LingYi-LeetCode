def _cap_if(S, B, ret):
    i, j, s = S.i, S.j, S.s
    seg = s[j:i]
    if j == 0:
        head = '`j == 0`：前面是空串，不用拆'
    elif S.f[j]:
        head = f'`f[{j}]` 非空：前 {j} 位能拆'
    else:
        return f'`f[{j}]` 是空的：前 {j} 位拆不开 → 跳过'
    if seg in S.word_set:
        return head + f'，且 `"{seg}"` ==在字典里== → 成立'
    return head + f'，但 `"{seg}"` 不在字典里 → 不行'


def _cap_for_i(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '二重循环结束：每个 `f[i]` 都记下了「能结尾在第 i 位的单词」'
    pre = '' if 'i' in B else '`f` 初始全是空列表（空 = 拆不开）。'
    return pre + f'考虑 `f[{S.i}]`：前 {S.i} 位 `"{S.s[:S.i]}"`，从 0 到 {S.i - 1} ==枚举分割点 j=='


def _text(S):
    if 'j' not in S or 'i' not in S:
        return '`f[i]`：前 i 位能拆分时，最后一个单词可能是哪些（空 = 拆不开）'
    i, j, s = S['i'], S['j'], S['s']
    ok = s[j:i] in S['word_set']
    left = '`j == 0`' if j == 0 else f"`f[{j}]` {'非空' if S['f'][j] else '为空'}"
    return f"分割点 `j = {j}`：{left}，`s[{j}:{i}]` = \"{s[j:i]}\" {'==∈ 字典==' if ok else '∉ 字典'}"


CONFIG = dict(
    num=139, title='单词拆分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='字符串 DP：枚举分割点',
    code='''
class Solution(object):
    def wordBreak(self, s, wordDict):
        word_set = set(wordDict)
        f = [[] for _ in range(len(s) + 1)]

        for i in range(1, len(s) + 1):
            for j in range(i):
                if (j == 0 or len(f[j]) > 0) and s[j : i] in word_set:
                    f[i].append(s[j : i])

        return len(f[len(s)]) > 0
''',
    call='Solution().wordBreak("season", ["sea", "seas", "son", "on"])',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='string', var='s', label='s', cell=130, min_slots=7, h=195,
             window=('j', 'i-1')),
        dict(type='array', var=lambda S: ['/'.join(w) if w else '·' for w in S['f']],
             label='f[i]：能结尾在第 i 位的单词（· = 空；黄 = 当前 i，蓝 = 分割点 j）',
             cell=130, h=240, pointers={'j': 'blue', 'i': 'yellow'},
             color=lambda S, i, v: 'yellow' if i == S.get('i') else
                                   ('blue' if i == S.get('j') else ('green' if v != '·' else None))),
        dict(type='set', var='word_set', label='word_set', h=110),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'blue'), ('f[i]', 'f[i]', 'green')],
    skip=['for j in range(i)', 'f = [[]'],
    captions={
        'word_set = set': '字典转成集合，判断 `s[j : i]` 在不在字典里更快',
        'for i in range': _cap_for_i,
        'if (j == 0': _cap_if,
        'f[i].append': lambda S, B, ret: ('空串' if S.j == 0 else f'前 {S.j} 位能拆') + f' + `"{S.s[S.j:S.i]}"` 是单词 → 记进 `f[{S.i}] = {S.f[S.i]}`'
                       + ('；==不 break，继续找==，140 题要用到所有单词' if len(S.f[S.i]) > 1 else ''),
        'return len': '`f[{len(s)}] = {f[len(s)]}` 非空 → 整个 s 能拆分，返回 =={ret}==',
    },
    cards=dict(
        one_liner='设 f[i] 表示 s 的前 i 位能否被拆分，枚举分割点 j',
        complexity='时间 `O(n³)`（`O(n²)` 个分割点 × 切片 `O(n)`），空间 `O(n²)`',
        problem=['给字符串 `s` 和字典 `wordDict`，问 `s` 能否拆成若干个字典里的单词',
                 '单词可以==重复使用==，也不必全部用上',
                 '示例：`"season"`，`["sea","seas","son","on"]` → `true`'],
        quote='设f[i]表示s的前i位能否被拆分，然后对于f[i]，我们从0到i - 1枚举分割点j。如果存在j满足==f[j]为True，且s[j : i]这一段在wordDict中==，那么当前的f[i]为True。',
        quote_src='—— yiduobo 题解原文',
        idea=['「又是经典的字符串 DP，老样子，设 `f[i]` 表示 s 的前 i 位怎么怎么样」',
              '分割点 j 把前 i 位切成「前 j 位」+「最后一段 `s[j:i]`」',
              '前 j 位能拆、最后一段是单词 → 前 i 位就能拆；`j == 0` 时前面是空串'],
        after=[dict(heading='顺手解决 140 题', lines=[
            '原文 `f[i]` 不存布尔值，而是==存下所有能结尾在第 i 位的单词==',
            '`f[n]` 非空 ⇔ 能拆分（139）；顺着 `f` 往回记忆化搜索 → 列出所有拆法（140）',
            '本例 `f[6] = ["son", "on"]`：`sea|son` 与 `seas|on` 两种拆法',
        ])],
        summary=['原文只给 140 题代码，139 参考==第一个二重循环==：只取这段，删 docstring，结尾改为返回 `f[len(s)]` 是否非空',
                 '易错：`j == 0` 要单独放行（空前缀），`f` 开 `len(s) + 1` 个',
                 '可优化：j 只需枚举到最长单词长度（灵神写法），`O(n³)` 降为 `O(nL²)`'],
    ),
)
