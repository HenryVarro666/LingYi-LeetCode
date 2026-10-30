def _out(S):
    if 'self.xs' not in S or 'self.k' not in S or 'self.cnt' not in S:
        return []
    xs, k, p = S['self.xs'], S['self.k'], S['self.pos']
    last = p if S['_line'] == 9 else p - 1
    res, c = [], 0
    for j in range(last + 1):
        c = c + 1 if xs[j] == 4 else 0
        res.append(c >= k)
    return res


def _txt(S):
    if 'self.cnt' not in S or 'num' not in S:
        return ''
    return f"当前 `cnt = {S['self.cnt']}`，要求 `k = {S['self.k']}`：{'==cnt ≥ k，最后 k 个都是 value==' if S['self.cnt'] >= S['self.k'] else '还不够 k 个'}"


CONFIG = dict(
    num=2526, title='找到数据流中的连续整数', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='计数器：遇到加一，否则清零', tags=[],
    code='''
class DataStream:
    def __init__(self, value: int, k: int):
        self.value = value
        self.k = k
        self.cnt = 0

    def consec(self, num: int) -> bool:
        self.cnt = 0 if num != self.value else self.cnt + 1
        return self.cnt >= self.k
''',
    setup='''xs = [4, 4, 4, 3, 4, 4, 4, 4]
_init, _consec = DataStream.__init__, DataStream.consec
def __init__(self, value, k):
    self.xs = list(xs)
    self.pos = -1
    _init(self, value, k)
def consec(self, num):
    self.pos += 1
    return _consec(self, num)
DataStream.__init__, DataStream.consec = __init__, consec''',
    call='''d = DataStream(4, 3)
out = []
for i, x in enumerate(xs):
    out.append(d.consec(x))
out''',
    expect=[False, False, True, False, False, False, True, True],
    views=[
        dict(type='array', var='self.xs', label='数据流（绿 = value，粉 = 其他；蓝色箭头 = 刚到的数）', pointers={'self.pos': 'blue'}, cell=96, h=230,
             color=lambda S, i, v: 'green' if v == 4 else 'pink'),
        dict(type='text', fn=_txt, size=30, h=120),
        dict(type='array', var=_out, label='到目前为止 consec 的返回值', cell=96, h=200,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('num', 'num', 'blue'), ('cnt', 'self.cnt', 'orange'), ('k', 'self.k')],
    captions={
        'self.value = value': '记下目标值 `value = {value}`',
        'self.k = k': '记下长度 `k = {k}`',
        5: '`cnt` 记录结尾连续等于 `value` 的个数，一开始为 0',
        'self.cnt = 0 if': lambda S, B, r: (f'`{S.num}` == value：连续长度加一 → `cnt = {S.self.cnt}`' if S.num == S.self.value
                                             else f'`{S.num}` ≠ value：连续被打断，`cnt` 清零'),
        'return self.cnt >= self.k': lambda S, B, r: (f'`cnt = {S.self.cnt}` ≥ `k = {S.self.k}` → =={r}==，最后 k 个都等于 value' if r
                                                      else f'`cnt = {S.self.cnt}` < `k = {S.self.k}` → =={r}==，还不够 k 个'),
    },
    cards=dict(
        one_liner='不存整个数据流，只数结尾连续出现了几个 value',
        complexity='每次 `consec` 时间 `O(1)`，空间 `O(1)`',
        problem=['`consec(num)` 加入一个数；若最后 `k` 个数都等于 `value` 返回 `true`',
                 '不足 `k` 个数时返回 `false`',
                 '本视频：`value=4, k=3`，流 `[4,4,4,3,4,4,4,4]`'],
        quote='用一个计数器 cnt 记录 value 的出现次数。遇到就加一，没遇到就重置为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['只关心==结尾连续==的 `value` 个数 `cnt`',
              '`num == value` 就 `cnt + 1`，否则清零',
              '`cnt >= k` 就说明最后 `k` 个全是 `value`；不足 `k` 个时 `cnt` 本来就小于 `k`'],
        summary=['每次操作 `O(1)`，空间 `O(1)`',
                 '一行三目：`num != value` 时清零，否则加一',
                 '用 `>=` 而不是 `==`：连续个数超过 `k` 也成立',
                 '不用单独处理「少于 k 个」：计数不够自然返回 false',
                 '演示辅助：setup 里给方法包了一层，只多记 `self.xs`、`self.pos` 用来画图，作者代码未改'],
    ),
)
