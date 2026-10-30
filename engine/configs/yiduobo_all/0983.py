DAYS = [1, 4, 6, 7, 8, 20]


def _cap_w(S, B, ret):
    return f'七日票：从第 `{S.days[S.pos_w]}` 天（下标 `pos_w = {S.pos_w}`）起买，刚好盖到今天 → 候选 `f[{S.pos_w}] + {S.costs[1]} = {S.f[S.pos_w] + S.costs[1]}`，取小后 `f[-1]` = =={S.f[-1]}=='


CONFIG = dict(
    num=983, title='最低票价', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP + 双指针',
    tags=['灵神题单·动态规划', '难度分 1786'],
    code='''
class Solution(object):
    def mincostTickets(self, days, costs):

        f = [0, min(costs)]
        pos_w = pos_m = 0
        for index in range(1, len(days)):
            f.append(f[-1] + costs[0])
            while days[pos_w] + 6 < days[index]:
                pos_w += 1
            f[-1] = min(f[-1], f[pos_w] + costs[1])
            while days[pos_m] + 29 < days[index]:
                pos_m += 1
            f[-1] = min(f[-1], f[pos_m] + costs[2])

        return f[-1]
''',
    call='Solution().mincostTickets([1,4,6,7,8,20], [2,7,15])',
    expect=11,
    views=[
        dict(type='array', var='days', label='days（出行日）', h=260, cell=80,
             pointers={'index': 'yellow', 'pos_w': 'blue', 'pos_m': 'pink'},
             window=('pos_w', 'index')),
        dict(type='text', size=26, h=80, fn=lambda S: f"今天 `days[{S['index']}] = {S['days'][S['index']]}`，七日票起点 `pos_w`，月票起点 `pos_m`" if 'index' in S else '三种买法：单日 / 七日 / 月票'),
        dict(type='array', var='f', label='f（f[i] = 覆盖前 i 个出行日的最低花费）', h=260, cell=80, pointers={'pos_w': 'blue', 'pos_m': 'pink'}),
    ],
    watch=[('index', 'index', 'yellow'), ('pos_w', 'pos_w', 'blue'), ('pos_m', 'pos_m', 'pink'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        'f = [0, min(costs)]': '`f[0] = 0`（没出行）；`f[1] = min(costs) = {min(costs)}`：只出行第一天，买最便宜的票',
        'for index in range': '枚举下标 `index = {index}`：第 `{days[index]}` 天要出行',
        'f.append(f[-1] + costs[0])': '先假设只买单日票：`f[{index+1}] = f[{index}] + {costs[0]}` = =={f[-1]}==',
        'while days[pos_w] + 6': '`days[pos_w] + 6 = {days[pos_w]+6}` {"<" if days[pos_w]+6 < days[index] else "≥"} `{days[index]}`：{"七日票盖不到今天，起点后移" if days[pos_w]+6 < days[index] else "这张七日票能盖到今天，停"}',
        'pos_w += 1': '`pos_w` 右移到 `{pos_w}`：days 递增，所以起点只会往右',
        'f[-1] = min(f[-1], f[pos_w] + costs[1])': _cap_w,
        'while days[pos_m] + 29': '`days[pos_m] + 29 = {days[pos_m]+29}` {"<" if days[pos_m]+29 < days[index] else "≥"} `{days[index]}`：{"月票盖不到今天，起点后移" if days[pos_m]+29 < days[index] else "这张月票能盖到今天，停"}',
        'pos_m += 1': '`pos_m` 右移到 `{pos_m}`',
        'f[-1] = min(f[-1], f[pos_m] + costs[2])': '月票：`f[{pos_m}] + {costs[2]}` 和当前比，取小 → `f[{index+1}] =` =={f[-1]}==',
        'return f[-1]': '覆盖全部出行日的最低花费 `f[-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='今天有三种买法：单日、七日、月票，取最省的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一年中要出行的日子是 `days`，三种票：1 天 / 7 天 / 30 天，价格 `costs`',
                 '求覆盖所有出行日的==最低花费==',
                 '示例：`days=[1,4,6,7,8,20]`，`costs=[2,7,15]` → `11`'],
        quote='令f[i]表示满足前days[i - 1]天的最低票价是多少……由于days是单调递增的，那么随着i的增大，w和m也必然是随之增大的，因此可以使用两个变量随着i一起向后递推。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]` 初值：只买单日票，`f[i-1] + costs[0]`',
              '七日票要发挥最大价值，必从某个出行日开始、盖到今天：`f[w] + costs[1]`',
              '月票同理。`days` 递增 → `w`、`m` 单调右移，用两个变量推进即可'],
        summary=['时间 `O(n)`：两个指针各只右移 `n` 次',
                 '易错：`+ 6` 和 `+ 29`（票含当天，共 7 / 30 天）',
                 '原文为 Python 2 写法；本题代码无需改动，直接可在 Python 3 运行',
                 '对比灵神：按天数 1..365 做 DP；这里按出行日下标做 DP'],
    ),
)
