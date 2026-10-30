def _days(S):
    n = S['n']
    return [i // 7 + i % 7 + 1 for i in range(n)]


def _color(S, i, v):
    if 'r' not in S:
        return None
    w = S['w']
    return 'blue' if i < w * 7 else 'pink'


def _text(S):
    if 'r' not in S:
        return '每天存的钱：每周一比上周一多 1 元，周内逐日加 1'
    D, w, r = S['D'], S['w'], S['r']
    if 'base' in S:
        return ''
    a = w * D * (w + D) // 2
    b = r * (w * 2 + r + 1) // 2
    return f'整周：`w·D·(w+D)/2 = {w}×{D}×({w}+{D})/2` = =={a}==　　零头：`r(2w+r+1)/2 = {r}×(2×{w}+{r}+1)/2` = =={b}=='


CONFIG = dict(
    num=1716, title='计算力扣银行的钱', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='等差数列求和 O(1)',
    tags=['灵神题单', '难度分 1295'],
    code='''
class Solution:
    def totalMoney(self, n: int) -> int:
        D = 7
        w, r = divmod(n, D)
        return (w * D * (w + D) + r * (w * 2 + r + 1)) // 2
''',
    call='Solution().totalMoney(20)',
    expect=96,
    views=[
        dict(type='array', var=_days, color=_color, h=260, cell=60, label='第 1~n 天每天存入的钱（蓝 = 完整的 w 周，粉 = 最后 r 天）'),
        dict(type='text', fn=_text, h=120, size=30),
    ],
    watch=['n', ('D', 'D'), ('w', 'w', 'blue'), ('r', 'r', 'pink')],
    captions={
        'D = 7': '一周的天数 `D = 7`',
        'divmod': '`divmod({n}, {D})`：存满了 `w = {w}` 周，还多出 `r = {r}` 天',
        'return': '整周 `w·D·(w+D)/2` 加零头 `r(2w+r+1)/2`：`({w}×{D}×({w}+{D}) + {r}×({w}×2+{r}+1)) // 2` = =={ret}==',
    },
    cards=dict(
        one_liner='整周是等差数列，零头也是等差数列，两段求和',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每天存钱：周一存 1 元，周二到周日每天比前一天多 1 元',
                 '之后每个周一，都比 ==上一个周一== 多存 1 元',
                 '求第 `n` 天结束时一共存了多少，示例 `n = 20` → `96`'],
        quote='第二周每天存的钱都比 D 天前多 1，所以第二周存的钱数为 base + D。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第 1 周共 `base = 28`，第 2 周多 `D`，第 3 周多 `2D`……：公差为 `D`',
              '`w` 周之和化简为 `w·D·(w+D)/2`',
              '剩下 `r` 天是 `(w+1) + … + (w+r)`，再套等差数列公式'],
        after=[dict(heading='验算 n = 20', lines=['`w = 2`，`r = 6`','整周：`2×7×(2+7)/2 = 63`','零头：`6×(2×2+6+1)/2 = 33`','合计 `63 + 33 = 96`，与示例一致'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：零头那 `r` 天的起点是 `w+1`，不是 1',
                 '`n` 只有 1000，直接模拟也能过，公式是 O(1) 的优化',
                 '最后的 `// 2` 一定能整除，因为两部分各自都是整数和的 2 倍'],
    ),
)
