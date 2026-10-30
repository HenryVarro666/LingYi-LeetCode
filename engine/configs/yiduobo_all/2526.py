def _out(S):
    if 'self.xs' not in S or 'self.k' not in S or 'self.cnt' not in S:
        return []
    xs, k, p = S['self.xs'], S['self.k'], S['self.pos']
    last = p if S['_line'] == 15 else p - 1
    res, c = [], 0
    for j in range(last + 1):
        c = c + 1 if xs[j] == 4 else 0
        res.append(c >= k)
    return res


def _txt(S):
    if 'self.cnt' not in S or 'num' not in S:
        return ''
    return f"`num = {S['num']}`，`value = {S['self.value']}`，当前 `cnt = {S['self.cnt']}`，`k = {S['self.k']}`"


CONFIG = dict(
    num=2526, title='找到数据流中的连续整数', difficulty='Medium', category='设计',
    author='yiduobo', technique='记录末尾连续 value 的次数 cnt', tags=[],
    code='''
class DataStream(object):

    def __init__(self, value, k):
        self.cnt = 0
        self.k = k
        self.value = value

    def consec(self, num):

        if num != self.value:
            self.cnt = 0
        else:
            self.cnt += 1
        
        return self.cnt >= self.k
''',
    setup='''xs = [4, 3, 4, 4, 4, 4, 3, 4]
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
    expect=[False, False, False, False, True, True, False, False],
    views=[
        dict(type='array', var='self.xs', label='数据流（绿 = value，粉 = 其他；蓝色箭头 = 刚到的数）', pointers={'self.pos': 'blue'}, cell=96, h=230,
             color=lambda S, i, v: 'green' if v == 4 else 'pink'),
        dict(type='text', fn=_txt, size=30, h=120),
        dict(type='array', var=_out, label='到目前为止 consec 的返回值', cell=96, h=200,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('num', 'num', 'blue'), ('cnt', 'self.cnt', 'orange'), ('k', 'self.k')],
    captions={
        4: '`cnt`：当前==最后连续==出现的 `value` 的次数，初始 0',
        'self.k = k': '记下 `k = {k}`',
        'self.value = value': '记下 `value = {value}`',
        'if num != self.value': '`{num}` 和 `value = {self.value}` 比：=={"不相等" if num != self.value else "相等"}==',
        11: '`num` 不是 value，连续中断：`cnt` 重置为 0',
        'self.cnt += 1': '`num` 是 value，连续又长一位：`cnt` → {self.cnt}',
        'return self.cnt >= self.k': lambda S, B, r: (f'`cnt = {S.self.cnt}` ≥ `k = {S.self.k}` → ==true==' if r
                                                      else f'`cnt = {S.self.cnt}` < `k = {S.self.k}` → ==false=='),
    },
    cards=dict(
        one_liner='cnt 记最后连续的 value 个数，每次只比 cnt 和 k',
        complexity='每次 `consec` 时间 `O(1)`，空间 `O(1)`',
        problem=['数据流逐个加入整数，每次问：最后 `k` 个是不是都等于 `value`',
                 '不足 `k` 个也返回 `false`',
                 '本视频：`value=4, k=3`，流 `[4,3,4,4,4,4,3,4]`'],
        quote='使用一个变量cnt记录当前最后连续出现的value的次数，对于每次consec操作，若添加的num等于value，那么就将cnt加上1，否则将cnt重置为0',
        quote_src='—— yiduobo 题解原文',
        idea=['不必保存历史，只保存「结尾连续 value 的次数」',
              '相等则 `cnt += 1`；不相等则整个连续段作废，`cnt = 0`',
              '于是每次操作只需判断 `cnt >= k`'],
        summary=['每次操作 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 风格，只是类写作 `class DataStream(object)`，Python 3 直接可跑',
                 '用 `>=`：连续次数超过 `k` 依然返回 true',
                 '对比灵神：灵神压成一行三目表达式；这里写成 if / else 两个分支',
                 '演示辅助：setup 里给方法包了一层，只多记 `self.xs`、`self.pos` 用来画图，作者代码未改'],
    ),
)
