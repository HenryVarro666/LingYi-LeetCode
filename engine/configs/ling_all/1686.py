CONFIG = dict(
    num=1686, title='石子游戏 VI', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='转换成 a+b 排序贪心',
    tags=['博弈论', '难度分 2001'],
    code='''
class Solution:
    def stoneGameVI(self, a: List[int], b: List[int]) -> int:
        pairs = sorted(zip(a, b), key=lambda p: -p[0] - p[1])
        diff = sum(x if i % 2 == 0 else -y for i, (x, y) in enumerate(pairs))
        return (diff > 0) - (diff < 0)
''',
    call='Solution().stoneGameVI([2,4,3,5], [1,6,7,1])',
    expect=1,
    views=[
        dict(type='array', var='a', label='a（Alice 的评价）', h=150),
        dict(type='array', var='b', label='b（Bob 的评价）', h=150),
        dict(type='array', var=lambda S: [f'{x}+{y}={x+y}' for x, y in S['pairs']] if 'pairs' in S else [],
             label='按 a+b 从大到小排好的石子（偶数位 Alice 拿，奇数位 Bob 拿）', cell=150, h=170,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='text', fn=lambda S: ('A−B = ==' + str(S['diff']) + '==' if 'diff' in S else '先把所有石子假设给 Bob：A−B = −sum(b)，Alice 每拿一颗 A−B 增加 a+b'), size=30),
    ],
    watch=[('diff', 'diff', 'green')],
    captions={
        'pairs = sorted': '把石子按 `a[i]+b[i]` ==从大到小==排序：Alice 拿走它，A−B 增加 a+b（自己得 a，还让 Bob 少得 b）：`{[x + y for x, y in pairs]}`',
        'diff = sum': '偶数位 Alice 拿 → `+a`，奇数位 Bob 拿 → `−b`，累加得 A−B = =={diff}==',
        'return': 'A−B = `{diff}`，大于 0 返回 1，小于 0 返回 −1，等于 0 返回 0 → =={ret}==',
    },
    cards=dict(
        one_liner='转换成「Bob 先全拿走，Alice 再抢」，按 a+b 排序交替取',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['Alice 先手，轮流取石子；同一颗石子两人评价不同：`a[i]` 与 `b[i]`',
                 '双方都最优，比较最后总分：Alice 赢返回 `1`，Bob 赢 `-1`，平局 `0`',
                 '示例：`a=[2,4,3,5]`，`b=[1,6,7,1]` → `1`'],
        quote='Alice 拿走 a[i]+b[i] 最大的石子最优。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 Bob 先把所有石子都拿走，A−B = −sum(b)',
              'Alice 拿走石子 i：A−B 增加 `a[i] − (−b[i]) = a[i]+b[i]`',
              '于是只剩一个变量 `c[i]=a[i]+b[i]`：双方都从大到小拿，Alice 拿偶数位'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '本质是「正难则反」：把两个变量合成一个 `a+b`',
                 '易错点：Bob 拿的是 `-y`，不是 `+y`；最后用 `(diff>0)-(diff<0)` 取符号',
                 '写法二：只对 `a+b` 排序，`diff = sum(s[::2]) - sum(b)`'],
    ),
)
