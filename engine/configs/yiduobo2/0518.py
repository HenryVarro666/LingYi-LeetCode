COINS = [1, 2, 5]
AMOUNT = 6


def _row_before(coin):
    """处理 coin 之前的 f（即二维的 f[i-1] 行）"""
    f = [1] + [0] * AMOUNT
    for c in COINS:
        if c == coin:
            break
        for j in range(c, AMOUNT + 1):
            f[j] += f[j - c]
    return f


def _color(S, k, v):
    if 'index' not in S or 'coin' not in S or S['_line'] != 8:
        return None
    if k == S['index']:
        return 'yellow'
    if k == S['index'] - S['coin']:
        return 'blue'
    return None


def _dim(S, k, v):
    return 'index' in S and 'coin' in S and S['_line'] == 8 and k > S['index']


def _formula(S, B):
    if 'index' in S and 'coin' in S and S['_line'] == 8:
        j, c = S['index'], S['coin']
        return (f'`f[{j}]` = 旧 `f[{j}]`（`f[i-1][{j}]` = {B["f"][j]}）+ `f[{j - c}]`（==本轮已更新==，`f[i][{j - c}]` = {S["f"][j - c]}）= =={S["f"][j]}==')
    if 'coin' in S:
        return f'硬币 `{S["coin"]}`：`index` 从 `{S["coin"]}` 到 `{AMOUNT}` ==从小到大=='
    return '`f[j]`：凑出面值 `j` 的方法数（二维 `f[i][j]` 滚动成一维）'


CONFIG = dict(
    num=518, title='零钱兑换 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='完全背包 · 滚动数组（正序）',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def change(self, amount, coins):

        f = [0] * (amount + 1)
        f[0] = 1
        for coin in coins:
            for index in range(coin, amount + 1):
                f[index] += f[index - coin]

        return f[amount]
''',
    call=f'Solution().change({AMOUNT}, {COINS})',
    expect=5,
    skip=['for index in range'],
    views=[
        dict(type='text', fn=_formula, size=26),
        dict(type='array', var='coins', label='coins（橙 = 当前硬币，每种可以用无限次）', cell=90, h=150,
             color=lambda S, k, v: 'orange' if S.get('coin') == v else None),
        dict(type='array', var=lambda S: _row_before(S['coin']) if 'coin' in S else None, h=150, cell=90,
             label='滚动前的旧行 f[i-1][j]（只用来对照，代码里没有）'),
        dict(type='array', var='f', label='f（黄 = f[index]，蓝 = f[index - coin]，暗 = 本轮还没更新）', cell=90, h=200,
             pointers={'index': 'yellow', 'index - coin': 'blue'}, color=_color, dim=_dim),
    ],
    watch=[('coin', 'coin', 'orange'), ('index', 'index', 'yellow'), ('index-coin', 'index - coin', 'blue')],
    captions={
        'f = [0] * (amount + 1)': '`f[j]`：用前 i 种硬币凑出面值 `j` 的方法数',
        'f[0] = 1': '`f[0] = 1`：面值 0 只有一种凑法（什么都不选）',
        'for coin in coins': lambda S, B, ret: (f'加入硬币 `coin = {S.coin}`：`f[i][j] = f[i-1][j] + f[i][j - {S.coin}]`'
                                                if B.get('coin') != S.coin else '所有硬币都处理完'),
        'f[index] += f[index - coin]': lambda S, B, ret: (
            f'`f[{S.index}] += f[{S.index - S.coin}]`：`{B.f[S.index]} + {S.f[S.index - S.coin]}` = =={S.f[S.index]}=='
            + ('（不带这枚 + 带上一枚）' if S.index < 2 * S.coin else '（`f[' + str(S.index - S.coin) + ']` 本轮已更新，可再带一枚）')),
        'return f[amount]': '凑出 `{amount}` 的方法数：`f[{amount}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[j] += f[j - coin]，j 必须从小到大',
        complexity='时间 `O(n·amount)`，空间 `O(amount)`',
        problem=['硬币面额 `coins`（==每种无限枚==），凑成总金额 `amount` 的==组合数==',
                 '凑不出返回 0；`[1,2]` 和 `[2,1]` 算同一种',
                 '示例：`amount = 5, coins = [1,2,5]` → `4`',
                 '本视频：`amount = 6, coins = [1,2,5]` → `5`'],
        quote='注意到这个状态转移方程是可以滚动的，于是可以写成 f[j] += f[j - coin[i]]。同时需要注意这里的==j循环必须从小到大==，即保证f[i][j - coin[i]]能在f[i][j]之前被处理到。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j] = f[i-1][j] + f[i][j - coin[i]]`：不用第 i 种，或带上一个 coin[i]',
              '滚动成一维：`f[j]` 的旧值就是 `f[i-1][j]`',
              '`j` 从小到大：`f[j - coin]` 已是本轮新值 = `f[i][j - coin]`，同一种硬币能用多次'],
        result='`f[6] = 5`：`1×6`、`2+1×4`、`2+2+1+1`、`2+2+2`、`5+1` ✓',
        summary=['时间 `O(n·amount)`，空间 `O(amount)`',
                 '易错：`j` 若从大到小，就变成每种硬币只能用一次（0-1 背包）',
                 '外层硬币、内层面值 → 组合数；交换两层循环会算成排列数',
                 '原文为 Python 2 风格，只删去了文档字符串',
                 '对比灵神：灵神先写记忆化搜索，再 1:1 翻译成二维递推，最后才压成一维'],
    ),
)
