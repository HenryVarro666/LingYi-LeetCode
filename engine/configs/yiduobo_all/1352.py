def _txt(S):
    m = S.get('self.m')
    if m is None:
        return '`m[i]` = 上一个 0 之后的前缀乘积；粉 = `last_zero` 位置，蓝 = 最后 k 个数'
    lz = S['self.last_zero']
    if 'k' in S and S.get('_line') is not None:
        st = len(m) - S['k']
        return f'最后 `{S["k"]}` 个数 = `m[{st}..{len(m)-1}]`；起点 `len(m) − k = {st}`，`last_zero = {lz}`'
    return f'`m = {m}`，`last_zero = {lz}`'


CONFIG = dict(
    num=1352, title='最后K个数的乘积', difficulty='Medium', category='设计',
    author='yiduobo', technique='前缀乘积 · 遇 0 重置',
    tags=[],
    code='''
class ProductOfNumbers(object):

    def __init__(self):
        self.last_zero = -1
        self.m = [1]

    def add(self, num):
        if num == 0:
            self.last_zero = len(self.m)
            self.m.append(0)
        elif self.m[-1] == 0:
            self.m.append(num)
        else:
            self.m.append(self.m[-1] * num)

    def getProduct(self, k):

        print(len(self.m) - k)

        if self.last_zero >= len(self.m) - k:
            return 0
        elif self.last_zero == len(self.m) - k - 1:
            return self.m[-1]
        else:
            return self.m[-1] // self.m[len(self.m) - k - 1]
''',
    call='''p = ProductOfNumbers()
out = []
for x in (3, 0, 2, 5, 4):
    p.add(x)
out.append(p.getProduct(2))
out.append(p.getProduct(3))
out.append(p.getProduct(4))
out''',
    expect=[20, 40, 0],
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='self.m', label='m（前缀乘积，m[0]=1 是哨兵）',
             color=lambda S, i, v: ('pink' if i == S['self.last_zero'] else 'blue' if 'k' in S and i >= len(S['self.m']) - S['k'] else None),
             h=260),
        dict(type='calls', label='正在执行', h=120),
    ],
    watch=[('last_zero', 'self.last_zero', 'pink'), ('num', 'num', 'yellow'), ('k', 'k', 'blue')],
    captions={
        'self.last_zero = -1': '`last_zero = -1`：还没出现过 0',
        'self.m = [1]': '`m = [1]`：放一个 1 当哨兵，第一个数乘上它不变',
        'if num == 0': '新来的数是 `{num}`：是 0 吗？{"是" if num == 0 else "否"}',
        'self.last_zero = len(self.m)': '记下这个 0 将放在 `m[{last_zero}]`，之后的乘积都从它后面重新算',
        'self.m.append(0)': '`m` 末尾放 0：前缀乘积被 0 吃掉了',
        'elif self.m[-1] == 0': lambda S, B, r: ('`m[-1] = 0`：前一个是 0，不能再乘 → 从当前数重新开始' if S['self.m'][-1] == 0 or B['self.m'][-1] == 0
                                                else '`m[-1]` 不是 0，可以接着乘'),
        'self.m.append(num)': '重启：`m` 末尾直接放 `{num}`（不乘 0）',
        'self.m.append(self.m[-1] * num)': '`m` 末尾放 `{B["self.m"][-1]} × {num} = {self.m[-1]}`',
        'print(': '起点下标 `len(m) − k = {len(self.m) - k}`（原文调试用的 print）',
        'if self.last_zero >= len': lambda S, B, r: (f'`last_zero = {S["self.last_zero"]} ≥ {len(S["self.m"]) - S.k}`：最后 {S.k} 个数里有 0 → 乘积为 0'
                                                    if S['self.last_zero'] >= len(S['self.m']) - S.k
                                                    else f'`last_zero = {S["self.last_zero"]} < {len(S["self.m"]) - S.k}`：区间里没有 0'),
        'elif self.last_zero == len': lambda S, B, r: (f'`last_zero = {S["self.last_zero"]}` 恰好在区间前一位：前缀乘积正是从区间起点重启的'
                                                       if S['self.last_zero'] == len(S['self.m']) - S.k - 1
                                                       else '0 离区间更远，前缀乘积没被重置过'),
        23: '`m[-1]` 就是最后 {k} 个数的乘积：返回 =={ret}==',
        'return 0': '区间里有 0 → 返回 ==0==',
        'return self.m[-1] //': '`m[-1] ÷ m[{len(self.m) - k - 1}]` = `{self.m[-1]} ÷ {self.m[len(self.m) - k - 1]}` = =={ret}==（前缀乘积相除）',
    },
    cards=dict(
        one_liner='前缀乘积相除得到后 k 个数乘积；遇到 0 就重启前缀',
        complexity='`add` / `getProduct` 都是 `O(1)`，空间 `O(n)`',
        problem=['实现 `ProductOfNumbers`：`add(num)` 追加一个数，`getProduct(k)` 返回最后 `k` 个数的乘积',
                 '例：依次加入 `3,0,2,5,4`，`getProduct(2)` = `20`，`getProduct(3)` = `40`，`getProduct(4)` = `0`'],
        quote='若最后k个数中就有0，那么此时答案为0。为了处理这种情况，我们需要记录下最后一个0出现的位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`m[n-1] / m[n-k-1]` 就是后 k 个数的乘积，所以维护前缀乘积数组 `m`',
              '来了 0：记下位置，`m` 放 0；0 之后的第一个数不能再乘 0，直接放它自己',
              '`getProduct`：有 0 → 0；0 恰在区间前一位 → 直接取 `m[-1]`；否则做除法'],
        summary=['时间 `O(1)` 每次操作，空间 `O(n)`',
                 '易错：0 之后要重启前缀，否则除法会除以 0',
                 '`last_zero == len(m) − k − 1` 时区间正好从重启点开始，答案是 `m[-1]`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，`print x` 已改为 `print(x)`'],
    ),
)
