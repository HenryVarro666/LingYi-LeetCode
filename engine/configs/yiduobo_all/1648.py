def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inv = S.get('inventory')
    if not inv:
        return
    n = len(inv)
    now = S.get('now')
    p = S.get('p')
    cv.text((x0 + 18, y0 + 4), 'inventory（降序）：蓝色 = 已降到 now 的这一层，暗色 = 已卖掉的部分', 22, T['muted'], bold=True)
    cell = min(110, (x1 - x0 - 100) / n)
    sx = x0 + 50 + ((x1 - x0 - 100) - cell * n) / 2
    base, top = y1 - 120, y0 + 80
    vmax = max(max(inv), 1)
    sc = (base - top) / vmax
    live = now is not None and p is not None and len(inv) > 1 and inv[0] != 0 or (now is not None)
    for i, v in enumerate(inv):
        X = sx + i * cell
        bw = cell * 0.7
        bx0, bx1 = X + (cell - bw) / 2, X + (cell + bw) / 2
        cur = min(v, now) if now is not None else v
        # 已卖掉的部分（暗）
        if cur < v:
            cv.rect((bx0, base - v * sc, bx1, base - cur * sc), fill=(52, 58, 68), r=3)
        on_level = now is not None and v >= now and p is not None and i < p
        fill = T['blue'] if on_level else (110, 118, 130)
        if v == 0:
            cv.rect((bx0, base - 3, bx1, base), fill=fill, r=2)
        else:
            cv.rect((bx0, base - cur * sc, bx1, base), fill=fill, r=4)
        cv.text((X + cell / 2, base - v * sc - 4), v, 24, T['text'], anchor='mb', bold=True)
        cv.text((X + cell / 2, base + 6), i, 18, T['dim'], anchor='mt', mono=True)
    cv.line([(sx - 10, base), (sx + n * cell + 10, base)], T['border'], 2)
    if now is not None:
        y = base - now * sc
        cv.dashed((sx - 10, y), (sx + n * cell + 10, y), T['yellow'], 3)
        cv.text((sx - 14, y), f'now={now}', 22, T['yellow'], anchor='rm', bold=True)
    if p is not None and 0 <= p < n:
        X = sx + p * cell + cell / 2
        cv.tri_up(X, base + 34, 10, T['pink'])
        cv.text((X, base + 50), 'p', 24, T['pink'], anchor='mt', bold=True)


def _txt(S):
    if 'mul' not in S or 'now' not in S or 'p' not in S or len(S['inventory']) <= S['p']:
        return ''
    return f"最高层有 `mul = {S['mul']}` 种球，都是 `{S['now']}` 个；下一层 `inventory[p] = {S['inventory'][S['p']]}`；还要买 `orders = {S['orders']}` 个"


CONFIG = dict(
    num=1648, title='销售价值减少的颜色球', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='排序 + 一层一层卖 + 等差求和',
    tags=['贪心', '数学'],
    code='''
class Solution(object):
    def maxProfit(self, inventory, orders):

        inventory.append(0)
        inventory.sort(reverse=True)
        now = inventory[0]
        mul = 1
        p = 1
        mod = 10 ** 9 + 7
        res = 0
        while p < len(inventory):
            while p < len(inventory) and now == inventory[p]:
                mul += 1
                p += 1
            if (now - inventory[p]) * mul < orders:
                res += (now + inventory[p] + 1) * (now - inventory[p]) // 2 * mul
                res %= mod
                orders -= (now - inventory[p]) * mul
                mul += 1
                now = inventory[p]
                p += 1
            else:
                offset = orders // mul
                target = now - offset + 1
                res += (now + target) * offset // 2 * mul
                res += (target - 1) * (orders % mul)
                res %= mod
                return res
''',
    call='Solution().maxProfit([2,8,4,10,6], 20)',
    expect=110,
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='text', fn=_txt, h=80),
        dict(type='text', fn=lambda S: f"累计价值 `res = ` =={S['res']}==" if 'res' in S else '', h=50),
    ],
    watch=[('now', 'now', 'yellow'), ('mul', 'mul', 'blue'), ('p', 'p', 'pink'), 'orders', ('res', 'res', 'green')],
    max_steps=100,
    captions={
        4: '末尾补一个 `0`：最后一层也能「降到 0」，统一处理',
        5: '==从大到小排序==：价值等于当前剩余数量，永远先卖数量最多的',
        6: '`now = {now}`：当前最高的一层',
        7: '`mul` = 同在最高层的球种数（原文的 k），现在只有 1 种',
        8: '`p` 指向下一种球（下一层）',
        10: '`res` 累计总价值',
        11: lambda S, B, r: (f"`p = {S.p} < {len(S.inventory)}`，还有下一层" if S.p < len(S.inventory) else '所有层都处理完了'),
        12: lambda S, B, r: (f"`now = {S.now}` == `inventory[{S.p}] = {S.inventory[S.p]}` → 又有一种球在最高层" if S.p < len(S.inventory) and S.now == S.inventory[S.p]
                             else f"`inventory[{S.p}] = {S.inventory[S.p]}` ≠ `now = {S.now}` → 最高层的球种数确定了：`mul = {S.mul}`"),
        13: '最高层多一种：`mul = {mul}`',
        14: '`p` 后移一格，看下一种球',
        15: lambda S, B, r: (f"把 `{S.mul}` 种球从 `{S.now}` 都降到 `{S.inventory[S.p]}`，要买 `({S.now} − {S.inventory[S.p]}) × {S.mul} = {(S.now - S.inventory[S.p]) * S.mul}` 个"
                             + (f" `< orders = {S.orders}` → ==整层全买=="if (S.now - S.inventory[S.p]) * S.mul < S.orders else f" `≥ orders = {S.orders}` → ==够了，这一层只买一部分==")),
        16: '每种球 `{B.now}→{inventory[p]}` 的价值 `(m+n+1)(m−n)/2`，共 `{B.mul}` 种：`res = {res}`',
        17: '题目要求对 `10^9+7` 取模：`res = {res}`',
        18: '买掉了 `({B.now} − {inventory[p]}) × {mul}` 个：`orders` 还剩 =={orders}==',
        19: '下一层那种球也加入最高层：`mul = {mul}`',
        20: '最高层降到 `now = {now}`',
        21: '`p` 后移，准备看再下一层',
        23: '`orders // mul = {orders} // {mul} = {offset}`：这一层每种球轮流买 `{offset}` 个',
        24: '买完这些轮后每种球剩 `target − 1`：`target = now − offset + 1 = {target}`',
        25: '这 `mul` 种球各买 `now … target`：`(now+target)×offset/2×mul`，累计 `res = {res}`',
        26: '还剩 `orders % mul = {orders % mul}` 个，每个按 `target − 1 = {target - 1}` 的价值买：`res = {res}`',
        27: '取模：`res = {res}`',
        28: '买够了，总价值 =={res}==',
    },
    cards=dict(
        one_liner='先卖最多的那种球：一层一层把最高层压低，等差数列求和',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`inventory[i]` 是第 `i` 种颜色球的数量，卖一个球得到「当前这种球的剩余数量」那么多钱',
                 '一共卖 `orders` 个，求最大总价值（对 `10^9+7` 取模）',
                 '示例：`inventory=[2,8,4,10,6], orders=20` → `110`'],
        quote='对于当前数量最多的球，不妨设其有m个，且存在k种球都有m个，那么对于数量第二多的球n个而言，购买的顺序就应该是轮流买这k种球各一个，直到这k种球的数量都变为n为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['球数太大不能一个个模拟 → 排序后==成层==处理',
              '最高的 `k` 种球一起降到下一层 `n`：每种价值 `(m+n+1)(m−n)/2`，共买 `(m−n)×k` 个',
              '如果这一层买不完，`orders // k` 轮每种各买，剩余 `orders % k` 个再按一个更低价买'],
        summary=['时间 `O(n log n)`（排序）；原文说明可用快速选择降到 `O(n)`',
                 '原文为 Python 2 写法，`/` 用于整数除法的地方已改为 `//`',
                 '末尾补 `0`，让最后一层也能统一处理',
                 '易错：整层买完用的是 `<` 而不是 `<=`，刚好买完时走 else 分支',
                 '每步取模，防止结果溢出（Python 不会溢出，但要和题目取模一致）'],
    ),
)
