CONFIG = dict(
    num=1753, title='移除石子的最大得分', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='结论公式 min(s/2, s-m)',
    tags=['灵神题单', '难度分 1488'],
    code='''
class Solution:
    def maximumScore(self, a: int, b: int, c: int) -> int:
        s = a + b + c
        m = max(a, b, c)
        return min(s // 2, s - m)
''',
    call='Solution().maximumScore(4, 4, 6)',
    expect=7,
    views=[
        dict(type='text', size=34, fn=lambda S: f"三堆石子 `a={S['a']}`  `b={S['b']}`  `c={S['c']}`"),
        dict(type='bars', var=lambda S: [S['a'], S['b'], S['c']], label='三堆石子 (a, b, c)', h=300,
             color=lambda S, i, v: ('orange' if 'm' in S and v == S['m'] and i == [S['a'], S['b'], S['c']].index(S['m']) else None)),
        dict(type='text', size=32, fn=lambda S: (
            f"总数 `s = {S['s']}`，每回合拿走 2 颗 → 最多 `{S['s']//2}` 回合" if 's' in S and 'm' not in S else
            f"最大堆 `m = {S['m']}`，其余两堆共 `{S['s']-S['m']}` 颗" if 'm' in S and 'ret' not in S else '')),
        dict(type='text', size=32, fn=lambda S: (
            f"上界 `{S['s']//2}`（总数限制）  与  `{S['s']-S['m']}`（其余堆限制）取小" if 'm' in S else '')),
    ],
    watch=['a', 'b', 'c', ('s', 's', 'blue'), ('m', 'm', 'orange')],
    captions={
        's = a + b + c': '总石子数 `s = {a} + {b} + {c} = {s}`，每回合拿 2 颗，所以最多 `s // 2 = {s // 2}` 回合',
        'm = max': '最大的一堆 `m = {m}`：它每回合最多出 1 颗，要靠其余 `{s - m}` 颗来配对',
        'return min': '答案 = `min(s // 2, s - m)` = `min({s // 2}, {s - m})` = =={ret}==：两个上界里更紧的那个',
    },
    cards=dict(
        after=[dict(heading='再看两个例子', lines=['`2,4,6`：`s=12, m=6` → `min(6, 6) = 6`，最大堆刚好配完', '`1,8,8`：`s=17, m=8` → `min(8, 9) = 8`，别想着把第一堆也取空', '`1,1,10`：`s=12, m=10` → `min(6, 2) = 2`，最大堆太大，被 `s - m` 卡住']), dict(heading='为什么不会更大', lines=['每回合拿 2 颗，所以不超过 `s // 2`', '最大堆每回合最多出 1 颗，其余堆总共 `s - m` 颗', '两个上界都不能突破，原文再给出构造方案证明能取到'])],
        one_liner='最多回合数只被两件事卡住：总数的一半，和最大堆的搭档数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['三堆石子 `a, b, c`，每回合从两个不同的非空堆各取一颗，得 1 分',
                 '有两堆或以上为空时停止，求最大得分',
                 '示例：`a=4, b=4, c=6` → `7`'],
        quote='设 s = a+b+c，m = max(a,b,c)。定理：最大分数为 min(floor(s/2), s−m)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每回合拿走 2 颗，所以得分不超过 `s // 2`',
              '最大堆 `m` 的每一颗都要配一颗别堆的，所以不超过 `s - m`',
              '这两个上界永远能取到其中较小的一个（原文给了构造证明）'],
        summary=['时间 `O(1)`，空间 `O(1)`，没有任何模拟',
                 '易错点：只写 `s // 2` 会在最大堆特别大时算多，例如 `1,1,10` 只能得 2 分',
                 '同类题：「相邻不同」类贪心，都是比较最大值与其余之和'],
    ),
)
