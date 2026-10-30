CONFIG = dict(
    num=1033, title='移动石子直到连续', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='三次交换排序 + 逐情况讨论', tags=['灵神题单', '贪心与思维', '难度分 1421'],
    code='''
class Solution(object):
    def numMovesStones(self, a, b, c):

        if a > b:
            a, b = b, a
        if a > c:
            a, c = c, a
        if b > c:
            b, c = c, b
        
        ma = c - a - 2
        if a == b - 1:
            if c == b + 1:
                mi = 0
            else:
                mi = 1
        elif c == b + 1:
            mi = 1
        elif a == b - 2 or c == b + 2:
            mi = 1
        else:
            mi = 2
        
        return [mi, ma]
''',
    call='Solution().numMovesStones(5, 1, 2)',
    expect=[1, 2],
    views=[
        dict(type='text', fn=lambda S: f"`a={S['a']}, b={S['b']}, c={S['c']}`" + (f"，最多 `c-a-2 = {S['ma']}`" if 'ma' in S else '') + (f"，最少 `{S['mi']}`" if 'mi' in S else '')),
        dict(type='array', var=lambda S: [S['a'], S['b'], S['c']], label='三枚石子的位置', h=260, cell=120,
             color=lambda S, i, v: ['blue', 'yellow', 'pink'][i]),
    ],
    watch=[('a', 'a', 'blue'), ('b', 'b', 'yellow'), ('c', 'c', 'pink'), ('mi', 'mi', 'green'), ('ma', 'ma', 'orange')],
    captions={
        'a, b = b, a': '`a > b` 不满足大小关系，交换：`a={a}, b={b}`',
        'a, c = c, a': '`a > c`，交换：`a={a}, c={c}`',
        'b, c = c, b': '`b > c`，交换：`b={b}, c={c}`',
        'ma = ': '最多：a、c 之间的空位共 `c - a - 2 = {ma}`，每步至少少一个空位，所以最多 =={ma}== 步',
        'if a == b - 1': '`a == b-1`（{a} == {b-1}）？a、b 是否已经相邻',
        'mi = 0': '三颗石子已连续，无需移动：`mi = 0`',
        'mi = 1': '只需一步：`mi = 1`',
        'mi = 2': '两段空隙都得填：a 移到 b-1，c 移到 b+1，`mi = 2`',
        'return': '返回 `[mi, ma]` = =={ret}==',
    },
    cards=dict(
        one_liner='先排成 a<b<c，再把最少步数的情形一个个列出来',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['三枚石子在数轴上，每次把最左或最右的石子挪到两端之间的空位',
                 '求使三枚石子连续的最少和最多移动次数',
                 '示例：`a=1, b=2, c=5` → `[1, 2]`'],
        quote='每一次移动，a到c之间的距离至少要减少1。那么初始情况下，a到c之间的距离为c - a + 1，另外还需要去除a、b、c这三个位置，因此实际上空闲的距离就是c - a - 2。',
        quote_src='—— yiduobo 题解',
        idea=['最多：空闲位置共 `c-a-2` 个，每步只占掉一个',
              '最少按 6 种情形分：已连续 0；a、b 或 b、c 相邻 1；间隔为 2 也是 1；其余 2'],
        summary=['先把 a、b、c 交换成有序，石子名字不影响结果',
                 '间隔为 2 的情形（a == b-2 或 c == b+2）把石子放进缝里，1 步',
                 '两边空隙都大于 2 时，只能 a→b-1、c→b+1 共 2 步',
                 '原文条件按先后顺序判断，顺序不能乱'],
    ),
)
