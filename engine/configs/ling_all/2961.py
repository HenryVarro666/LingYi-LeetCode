CONFIG = dict(
    num=2961, title='双模幂运算', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='内置快速幂 pow(a, b, m)',
    code='''
class Solution:
    def getGoodIndices(self, variables: List[List[int]], target: int) -> List[int]:
        return [i for i, (a, b, c, m) in enumerate(variables)
                if pow(pow(a, b, 10), c, m) == target]
''',
    call='Solution().getGoodIndices([[2,3,3,10],[3,3,3,1],[6,1,1,4],[39,3,1000,1000]], 2)',
    expect=[0, 2],
    views=[
        dict(type='table', var='variables', rows=['0', '1', '2', '3'], cols=['a', 'b', 'c', 'm'], h=300,
             color=lambda S, i, j, v: 'blue' if i == S.get('i') else None),
        dict(type='text', fn=lambda S: (f"`(({S['a']}^{S['b']} % 10)^{S['c']}) % {S['m']}` = `pow(pow({S['a']}, {S['b']}, 10), {S['c']}, {S['m']})` = =={pow(pow(S['a'], S['b'], 10), S['c'], S['m'])}==，目标 `{S['target']}`") if 'a' in S else ''),
    ],
    watch=['i', 'a', 'b', 'c', 'm', 'target'],
    captions={
        'enumerate': lambda S, B, ret: ('遍历结束，好下标：`{}`'.format(ret) if ret is not None else '取下标 `i = {}` 的 `a, b, c, m`'.format(S['i'])),
        'if pow': '先 `pow(a, b, 10)` = {pow(a, b, 10)}（只留末位），再 `pow(.., c, m)` = =={pow(pow(a, b, 10), c, m)}==，和 `target = {target}` 比 → =={"相等，好下标" if pow(pow(a, b, 10), c, m) == target else "不等，跳过"}==',
    },
    cards=dict(
        one_liner='三参数 pow 一步完成「幂 + 取模」，套两层就行',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['给 `[a, b, c, m]`，判断 `((a^b % 10)^c) % m == target`',
                 '满足的下标就是好下标，全部返回',
                 '示例：`[2,3,3,10]` → `(8)^3 % 10 = 2`'],
        quote='由于 b 和 c 都比较小，可以暴力循环计算。更快的做法是用快速幂。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pow(a, b, 10)` 在 Python 里就是快速幂，边乘边取模，不会爆大数',
              '外层再 `pow(x, c, m)`，注意先 %10 再取 m，==顺序不能换=='],
        summary=['时间 `O(n log U)`，U 是 b、c 的最大值',
                 '易错：不能把两层模数合并，题目规定先对 10 取模',
                 '`m = 1` 时结果恒为 0；暴力循环也能过，快速幂更快'],
    ),
)
