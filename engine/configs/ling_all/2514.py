def _txt(S):
    if 'mul' not in S:
        return '先算每个单词的排列数，再相乘；相同字母不区分'
    return f"分子 `ans` = 各位置 i 的连乘 = =={S['ans']}==　分母 `mul` = 各字母次数阶乘的积 = =={S['mul']}=="


CONFIG = dict(
    num=2514, title='统计同位异构字符串数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='多重集排列 · 费马小定理',
    tags=['灵神题单', '数学算法', '难度分 2070'],
    code='''
class Solution:
    def countAnagrams(self, s: str) -> int:
        MOD = 10 ** 9 + 7
        ans = mul = 1
        for s in s.split():
            cnt = Counter()
            for i, c in enumerate(s, 1):
                cnt[c] += 1
                mul = mul * cnt[c] % MOD
                ans = ans * i % MOD
        return ans * pow(mul, -1, MOD) % MOD
''',
    call='Solution().countAnagrams("too hot")',
    expect=18,
    views=[
        dict(type='string', var='s', label='当前单词 s（蓝箭头 = 第 i 个字母）', cell=100, h=190,
             pointers={'i - 1': 'blue'}),
        dict(type='map', var='cnt', label='cnt：当前单词里各字母出现次数', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
        dict(type='text', h=110, size=30, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c'), ('mul', 'mul', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'MOD = ': '答案要对 `{MOD}` 取模',
        'ans = mul = 1': '`ans` 累乘分子（n!），`mul` 累乘分母（各字母次数的阶乘），都从 1 开始',
        'for s in s.split()': lambda S, B, ret: (f'每个单词互相独立 → 取出单词 `{S.s!r}`，用乘法原理把各单词的方案数乘起来'
                                                  if S.get('s') != B.get('s') or 's' not in B else '所有单词处理完毕'),
        'cnt = Counter()': '新单词，次数表清空',
        'for i, c in enumerate(s, 1)': lambda S, B, ret: ('这个单词的字母都处理完了' if B.get('s') == S.s and B.get('i') == S.i and B.get('c') == S.c
                                                          else f'`i = {S.i}`：单词里第 {S.i} 个字母 `{S.c!r}`（`i` 从 1 开始，正好是 n! 里的乘数）'),
        'cnt[c] += 1': '`{c!r}` 已出现 `{cnt[c]}` 次',
        'mul = ': '分母：`x!` 可以拆成 1×2×…×x，这是第 `{cnt[c]}` 次出现，乘上 `{cnt[c]}` → `mul = {mul}`',
        'ans = ': '分子：n! = 1×2×…×n，乘上 `i = {i}` → `ans = {ans}`',
        'return': '`ans / mul` 用费马小定理：`pow(mul, -1, MOD)` 是 `mul` 的乘法逆元 → 返回 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='单词互相独立：n! 除以每种字母次数的阶乘，再连乘',
        complexity='时间 `O(n + log M)`，空间 `O(|Σ|)`',
        problem=['单词内字母可以任意重排，单词之间位置不变，求不同的同位异构字符串个数（对 `10^9+7` 取模）',
                 '示例：`"too hot"` → `18`（`too` 有 3 种，`hot` 有 6 种）',
                 '`"aa"` → `1`'],
        quote='每个单词自己是互相独立的，因此分别计算每个单词的同位异构字符串的数目，再用乘法原理相乘。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长 n 的单词全排列 `n!`，相同字母不区分，要除以每种字母次数 `x!`',
              '分子分母分开累乘，最后用==费马小定理==除：`pow(mul, -1, MOD)`',
              '巧妙处：`i` 从 1 数到 n 就是分子；`cnt[c]` 从 1 数到 x 就是分母'],
        summary=['时间 `O(n + log M)`，空间 `O(26)`',
                 '取模后不能直接除，要乘分母的逆元；`pow(x, -1, MOD)` 需 Python 3.8+',
                 '所有单词共用同一个 `ans` 和 `mul`，不需要每个单词单独求逆元',
                 '同类题：组合数取模（灵神数学题单 2.2 组合计数）'],
    ),
)
