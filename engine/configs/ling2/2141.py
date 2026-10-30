N0 = 3  # 示例里的电脑数


def _done(S):
    """已经独占一台电脑的电池个数"""
    return N0 - S['n'] if 'n' in S else 0


def _color(S, i, v):
    if 's' not in S:
        return None
    k = _done(S)
    if i < k:
        return 'green'
    if i == k and S['_line'] in (5, 6, 7, 8):
        return 'yellow'
    return None


def _top(S):
    if 's' not in S:
        return '先排序：从电量最大的电池开始看'
    n, s = S['n'], S['s']
    return f'剩 `n = {n}` 台电脑、剩余电量 `s = {s}` → 至多供电 `s // n` = =={s // n}== 分钟'


def _if(S, B, ret):
    b, s, n = S.b, S.s, S.n
    x = s // n
    if b <= x:
        return f'`{b} <= {s} // {n} = {x}` 成立：剩下的电池==都不超过 {x}==，拼起来就能供电 {x} 分钟'
    return f'`{b} > {s} // {n} = {x}`：这个电池比平均值还大，多出的电用不上 → ==让它独占一台电脑=='


CONFIG = dict(
    num=2141, title='同时运行 N 台电脑的最长时间', difficulty='Hard', category='二分查找',
    author='灵茶山艾府', technique='排序 + 贪心（大电池独占）',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def maxRunTime(self, n: int, batteries: List[int]) -> int:
        batteries.sort(reverse=True)
        s = sum(batteries)
        for b in batteries:
            if b <= s // n:
                return s // n
            s -= b
            n -= 1
''',
    call='Solution().maxRunTime(3, [3, 12, 1, 10, 2])',
    expect=6,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='bars', var='batteries', h=480, color=_color,
             label='batteries（绿 = 已独占一台电脑，黄 = 当前电池 b）'),
        dict(type='text', size=26, fn=lambda S: (
            f'已独占：{_done(S)} 台电脑（各用 x 分钟，多余的电浪费）；剩下的小电池平均分给 {S["n"]} 台'
            if 's' in S else '')),
    ],
    watch=[('n', 'n', 'blue'), ('s', 's', 'cyan'), ('b', 'b', 'yellow'), ('s // n', 's // n', 'green')],
    captions={
        'batteries.sort': '从大到小排序 → `{batteries}`：==先处理电量最大的电池==',
        's = sum': '总电量 `s = {s}`：理论上至多供电 `s // n = {s // n}` 分钟',
        'for b in batteries': '取下一个（当前最大的）电池 `b = {b}`',
        'if b <= s // n': _if,
        'return s // n': '返回 `s // n` = =={ret}==',
        's -= b': '把这个电池和一台电脑一起拿走：`s = {B.s} − {b} = {s}`',
        'n -= 1': '问题缩减为 `{n}` 台电脑的子问题，平均值变成 `{s // n}`',
    },
    cards=dict(
        one_liner='大电池独占一台电脑，剩下的小电池拼起来平均分',
        complexity='时间 `O(m log m)`，空间 `O(1)`',
        problem=['`n` 台电脑，`batteries[i]` 是第 `i` 个电池能供电的分钟数',
                 '任意整数时刻都能换电池；一个电池==同一时刻只能给一台电脑==',
                 '求 n 台电脑==同时==运行的最长分钟数；示例：`n = 2, [3,3,3]` → `4`',
                 '本视频：`n = 3, [3,12,1,10,2]` → `6`'],
        quote='若该电池电量超过 x，则将其供给一台电脑，问题缩减为 n−1 台电脑的子问题。若该电池电量不超过 x，则其余电池的电量均不超过 x……可以给 n 台电脑供电 x 分钟。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['`x = s // n` 是理论上限；电量 `> x` 的电池只能用 x 分钟 → ==独占一台==',
              '电量都 `≤ x` 时：把电池==连成一条线，每隔 x 切一刀==，每段给一台电脑',
              '电池 < x，切到两段时放在前一台末尾、后一台开头，时间不会重叠'],
        summary=['时间 `O(m log m)`，瓶颈在排序；空间 `O(1)`',
                 '易错：不能直接返回 `sum // n`，大电池多出来的电==用不上==',
                 '每拿走一个电池，`s` 和 `n` 都变了，要重新算 `s // n`（它只会变小）',
                 '方法一：二分答案 x，检查 `n * x <= sum(min(b, x))`，`O(m log(S/n))`'],
    ),
)
