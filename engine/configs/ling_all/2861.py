def _txt(S):
    if 'mid' not in S or 'comp' not in S:
        return ''
    mid = S['mid']
    money = 0
    for s_, b_, c_ in zip(S['stock'], S['comp'], S['cost']):
        if s_ < b_ * mid:
            money += (b_ * mid - s_) * c_
    return f"造 `{mid}` 份需要花 `{money}`，预算 `{S['budget']}` → " + ('==够用==' if money <= S['budget'] else '==超预算==')


CONFIG = dict(
    num=2861, title='最大合金数', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='枚举机器 + 二分答案',
    tags=['二分算法', '难度分 1981'],
    code='''
class Solution:
    def maxNumberOfAlloys(self, n: int, k: int, budget: int, composition: List[List[int]], stock: List[int], cost: List[int]) -> int:
        ans = 0
        mx = min(stock) + budget
        for comp in composition:
            def check(num: int) -> bool:
                money = 0
                for s, base, c in zip(stock, comp, cost):
                    if s < base * num:
                        money += (base * num - s) * c
                        if money > budget:
                            return False
                return True

            left, right = ans, mx + 1
            while left + 1 < right:  # 开区间写法
                mid = (left + right) // 2
                if check(mid):
                    left = mid
                else:
                    right = mid
            ans = left
        return ans
''',
    call='Solution().maxNumberOfAlloys(2, 2, 6, [[2,1],[1,1]], [1,1], [2,2])',
    expect=2,
    views=[
        dict(type='table', var='composition', label='composition（每行 = 一台机器的配方，蓝色 = 当前 comp）', h=170, cell=80,
             color=lambda S, i, j, v: 'blue' if 'comp' in S and S['composition'][i] is S['comp'] else None),
        dict(type='array', var='stock', label='stock（库存）', h=130, cell=90),
        dict(type='array', var='cost', label='cost（单价）', h=130, cell=90),
        dict(type='text', fn=_txt, size=30, h=90),
        dict(type='text', fn=lambda S: f"二分开区间：`left = {S['left']}`（可行），`right = {S['right']}`（不可行）" if 'left' in S and 'right' in S else '', size=30, h=80),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('money', 'money', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'mx = min(stock)': '二分上界：每种金属最多买 `budget` 份，加上库存最少的那种 → `mx = {mx}`',
        'for comp in composition': '挨个机器判断，这台的配方 `comp = {comp}`',
        'money = 0': '`money` 累计这次要额外买金属的花费',
        'if s < base * num': lambda S, B, r: (f"需要 `{S.base}×{S.num}={S.base*S.num}`，库存 `{S.s}` → ==不够，要买=={S.base*S.num-S.s}份" if S.s < S.base * S.num else f"需要 `{S.base*S.num}`，库存 `{S.s}` → 够用，不用买"),
        'money += ': '额外花费 `({base}×{num} − {s}) × {c}`，累计 `money = {money}`',
        'if money > budget': lambda S, B, r: (f'`{S.money} > {S.budget}` → 超预算' if S.money > S.budget else f'`{S.money} ≤ {S.budget}` → 还在预算内'),
        'return False': '超预算 → 造不出 `{num}` 份，`check` 返回 `False`',
        'return True': '每种金属都买得起 → `check({num})` 为 `True`',
        'left, right = ans': '开区间左端点用当前 `ans`：小于等于 `ans` 的份数没意义；右端点 `{right}` 一定造不出',
        'while left + 1 < right': '`left + 1 < right`：开区间里还有数没试过' ,
        'mid = ': '`mid = ({left} + {right}) // 2 = {mid}`，试试造 `mid` 份',
        'if check(mid)': lambda S, B, r: ('`check(mid)` 成立 → 能造' if r else '`check(mid)` 不成立 → 造不出'),
        'left = mid': '能造 `{mid}` 份 → 答案至少是 `{mid}`，`left = {left}`',
        'right = mid': '造不出 `{mid}` 份 → 更多更造不出，`right = {right}`',
        'ans = left': '开区间二分结束，`left` 就是这台机器最多能造的份数 → `ans = {ans}`',
        'return ans': '所有机器里最多能造 `{ans}` 份',
    },
    skip=['def check'],
    max_steps=70,
    cards=dict(
        one_liner='造得越多越贵：每台机器各自二分最多能造几份',
        complexity='时间 `O(kn log U)`，空间 `O(1)`',
        problem=['`k` 台机器，每台有一份配方，造一份合金要每种金属各 `composition[i][j]` 份',
                 '有库存 `stock`，缺的按 `cost` 买，总花费不超过 `budget`；==只能用同一台机器==',
                 '示例：`budget=6`，配方 `[[2,1],[1,1]]`，库存 `[1,1]` → `2`'],
        quote='假设要制造 num 份合金，由于 num 越小，花费的钱越少，num 越多，花费的钱越多，可以据此二分猜答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一台机器：份数越多花费越多，==单调== → 二分答案',
              '`check(num)`：每种金属不够的部分按单价买，超预算就返回 False',
              '优化：左端点直接从当前 `ans` 开始，不可能更优的机器几乎不花时间'],
        summary=['时间 `O(kn log U)`，`U = min(stock) + budget`',
                 '开区间写法：`check(mid)` 为真就更新 `left`，最后返回 `left`，不用想加一减一',
                 '易错：库存够的金属不能算成负花费；右端点要 `mx + 1`',
                 '另一种写法用 `bisect_right(range, budget, key=f)` 一行完成二分'],
    ),
)
