_ACC = (45, 212, 191)


def _f_color(S, k, v):
    if 'i' not in S:
        return None
    i = S['i']
    if k == i:
        return 'green'
    if 'coin' in S and i >= S['coin'] and k == i - S['coin']:
        return 'blue'
    return None


def _cands(cv, S, B, box, T):
    if 'i' not in S or 'f' not in S:
        s = '`f[0] = 0`：0 块钱不用硬币；其余先设 `-1`（==凑不出==）' if 'f' in S and S['f'][0] == 0 else ''
    else:
        i, f, coins = S['i'], S['f'], S['coins']
        upto = coins.index(S['coin']) if 'coin' in S and S.get('coin') in coins and B.get('i') == i else -1
        parts = []
        for k, c in enumerate(coins[:upto + 1]):
            if i < c:
                parts.append(f'拿 {c}：太大')
            elif f[i - c] < 0:
                parts.append(f'拿 {c}：`f[{i - c}] = -1` 不可达')
            else:
                parts.append(f'拿 {c}：`f[{i - c}] + 1 = {f[i - c] + 1}`')
        s = f'`f[{i}] = min(f[{i} - coin]) + 1`　' + '；'.join(parts) if parts else f'`f[{i}]`：枚举每一种硬币，看从 `{i} - coin` 块转移过来'
    if s:
        cv.rich(box[0] + 22, box[1] + 8, s, box[2] - box[0] - 44, size=27, accent=_ACC, max_lines=2, line_gap=1.4)


def _legend(cv, S, B, box, T):
    x, y = box[0] + 24, (box[1] + box[3]) / 2
    for c, t in [('green', 'f[i]：正在算'), ('blue', 'f[i - coin]：从这里拿一枚 coin 过来'), (None, '暗格 = -1 凑不出')]:
        if c:
            cv.rect((x, y - 11, x + 22, y + 11), fill=T[c], r=5)
        else:
            cv.rect((x, y - 11, x + 22, y + 11), fill=(40, 45, 53), outline=T['border'], r=5)
        cv.text((x + 32, y), t, 22, T['muted'], anchor='lm')
        x += 32 + cv.tlen(t, 22) + 36


def _cap_if(S, B, ret):
    i, coin, f = S.i, S.coin, S.f
    if i < coin:
        return f'`i = {i} < {coin}`：这枚硬币比金额还大，用不了'
    p = f[i - coin]
    if p < 0:
        return f'`f[{i - coin}] = -1`：`{i - coin}` 块凑不出 → 不能从它拿一枚 `{coin}` 过来'
    if f[i] >= 0 and f[i] <= p + 1:
        return f'`f[{i}] = {f[i]}` 不比 `f[{i - coin}] + 1 = {p + 1}` 差 → ==不更新=='
    why = '还是 `-1`（第一次凑出）' if f[i] < 0 else f'= {f[i]} 更大'
    return f'`f[{i - coin}] = {p}` 可达，且 `f[{i}]` {why} → ==更新=='


CONFIG = dict(
    num=322, title='零钱兑换', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='背包 DP：外层金额、内层硬币',
    code='''
class Solution(object):
    def coinChange(self, coins, amount):
        f = [-1] * (amount + 1)
        f[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                if i >= coin and f[i - coin] >= 0 and (f[i] < 0 or f[i] > f[i - coin] + 1):
                    f[i] = f[i - coin] + 1

        return f[amount]
''',
    call='Solution().coinChange([2, 5], 9)',
    expect=3,
    views=[
        dict(type='custom', draw=_cands, h=80),
        dict(type='array', var='coins', label='coins（每种可以拿任意多次）',
             color=lambda S, k, v: 'orange' if 'coin' in S and v == S['coin'] else None, cell=96, h=170),
        dict(type='array', var='f', label='f[i] = 凑够 i 块钱最少要几个硬币（-1 = 凑不出）', color=_f_color,
             dim=lambda S, k, v: v == -1 and k != S.get('i'),
             pointers={'i': 'green', 'i - coin if i >= coin else None': 'blue'},
             pointer_labels={'i - coin if i >= coin else None': 'i-coin'}, cell=88, h=250),
        dict(type='custom', draw=_legend, h=50),
    ],
    watch=[('i', 'i', 'green'), ('coin', 'coin', 'orange'), ('f[i-coin]', 'f[i - coin] if i >= coin else None', 'blue'),
           ('f[i]', 'f[i]', 'green')],
    skip=['for coin in coins'],
    captions={
        'f = [-1]': '`f[i]` = 凑够 `i` 块钱最少几个硬币；先全设 `-1` 表示==凑不出==',
        'f[0] = 0': '边界：`f[0] = 0`，0 块钱不需要硬币',
        'for i in range': lambda S, B, ret: ('所有金额都算完了' if B.get('i') == S.i else
                                             f'算 `f[{S.i}]`：枚举每种硬币，看从 `{S.i} - coin` 块拿一枚过来' if S.i == 1 else
                                             f'算 `f[{S.i}]`'),
        'if i >= coin and': _cap_if,
        'f[i] = f[i - coin] + 1': '`{i - coin}` 块 + 一枚 `{coin}` = `{i}` 块：`f[{i}] = f[{i - coin}] + 1` = =={f[i]}==',
        'return f[amount]': '返回 `f[{amount}]` = =={ret}==（凑不出时就是初始的 `-1`）',
    },
    cards=dict(
        one_liner='凑 i 块钱 = 从 i - coin 块钱再拿一枚 coin：f[i] = min(f[i - coin]) + 1',
        complexity='时间 `O(amount · len(coins))`，空间 `O(amount)`',
        problem=['硬币面额 `coins`（每种无限枚），凑出总金额 `amount` 的==最少硬币数==',
                 '凑不出来返回 `-1`',
                 '示例：`[1,2,5], 11` → `3`；演示：`coins = [2,5], amount = 9` → `3`'],
        quote='f[i]表示凑够i块钱最少需要多少个硬币，那么就需要枚举每一种面值的硬币coin[j]，然后看做==从i - coin[j]块钱这个状态拿了coin[j]之后达成了i块钱==。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i] = min(f[i - coin[j]]) + 1`，要求 `i ≥ coin[j]`；边界 `f[0] = 0`',
              '用 `-1` 表示凑不出：只能从 `f[i - coin] ≥ 0` 的状态转移过来',
              '外层枚举金额 `i`，内层枚举硬币 → 两重循环'],
        after=[dict(heading='yiduobo 的进一步思考', lines=[
            '硬币能拿任意多次，理论上可以在==面值==上做优化',
            '例如 1、2、5：拿两个 1 不如一个 2；拿三个 2 不如 1 + 5',
            '先算出每种硬币最多拿几次也许能加速；作者说还没思路，先按最简单的实现',
        ])],
        summary=['时间 `O(amount · len(coins))`，空间 `O(amount)`',
                 '原文为 Python 2 写法：本题仅删去 docstring，其余未改',
                 '用 `-1` 表示凑不出：比较前要先判 `f[i] < 0`，否则 -1 会被当成「最少」',
                 '外层金额、内层硬币；求最少个数时，和「外层硬币」的顺序结果一样'],
    ),
)
