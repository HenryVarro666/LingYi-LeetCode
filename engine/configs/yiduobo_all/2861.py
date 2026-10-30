CONFIG = dict(
    num=2861, title='最大合金数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='枚举机器 + 二分合金数',
    tags=['二分算法', '难度分 1981'],
    code='''
class Solution(object):
    def maxNumberOfAlloys(self, n, k, budget, composition, stock, cost):

        res = 0
        for index in range(k):
            left = 0
            right = budget + max(stock)
            while left < right:
                mid = (left + right + 1) // 2
                need = [x * mid for x in composition[index]]
                buy = [max(0, x - y) for x, y in zip(need, stock)]
                tot_cost = sum([x * y for x, y in zip(buy, cost)])
                if tot_cost <= budget:
                    left = mid
                else:
                    right = mid - 1
            
            res = max(res, left)
        
        return res
''',
    call='Solution().maxNumberOfAlloys(2, 2, 6, [[2,1],[1,1]], [1,1], [2,2])',
    expect=2,
    views=[
        dict(type='table', var='composition', label='composition（蓝 = 当前机器 index）', h=170, cell=80,
             color=lambda S, i, j, v: 'blue' if 'index' in S and i == S['index'] else None),
        dict(type='array', var='stock', label='stock', h=120, cell=70),
        dict(type='array', var='need', label='need = 配方 × mid', h=120, cell=70, color=lambda S, i, v: 'blue'),
        dict(type='array', var='buy', label='buy = 还要买几份', h=120, cell=70, color=lambda S, i, v: 'orange' if v > 0 else None),
        dict(type='text', h=80, size=30, fn=lambda S: (f"二分区间 `[{S['left']}, {S['right']}]`，当前 `mid = {S['mid']}`" if 'mid' in S and 'left' in S else (f"二分区间 `[{S['left']}, {S['right']}]`" if 'left' in S else ''))),
    ],
    watch=[('index', 'index', 'purple'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('tot_cost', 'tot_cost', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录目前最多能造的合金数',
        'for index in range': '考察第 `{index}` 台机器，配方 `{composition[index]}`',
        'left = 0': '二分下界：造 0 份一定行',
        'right = budget + max': '二分上界：每件最便宜 1 元，最多 `budget + max(stock) = {right}`',
        'while left < right': lambda S, B, r: (f'`{S.left} < {S.right}`：答案还在区间里' if S.left < S.right else f'`left == right = {S.left}`：这台机器最多造 `{S.left}` 份'),
        'mid = ': '取上中位数 `({left} + {right} + 1) // 2 = {mid}`（`left = mid` 会往上走，所以要 +1 防死循环）',
        'need = ': '造 `{mid}` 份，每种金属共需要 `{need}`',
        'buy = ': '减去库存，不够的才要买：`buy = {buy}`',
        'tot_cost = ': '按单价 `{cost}` 算：`tot_cost = {tot_cost}`',
        'if tot_cost <= budget': lambda S, B, r: (f'`{S.tot_cost} <= {S.budget}` → ==买得起=={S.mid}份' if S.tot_cost <= S.budget else f'`{S.tot_cost} > {S.budget}` → ==超预算=={S.mid}份'),
        'left = mid': '买得起 → 至少能造 `{mid}` 份，`left = {left}`',
        'right = mid - 1': '超预算 → 至多 `{mid} − 1`，`right = {right}`',
        'res = max(res, left)': '这台机器最多 `{left}` 份 → `res = max({B.res}, {left}) = {res}`',
        'return res': '所有机器里最多造 `{res}` 份',
    },
    max_steps=75,
    cards=dict(
        one_liner='合金必须同一台机器造：逐台二分最多造几份',
        complexity='时间 `O(k·n·log(budget))`，空间 `O(n)`',
        problem=['`k` 台机器，每台造一份合金要各种金属若干份；有库存 `stock`，缺的按 `cost` 买',
                 '总花费不超过 `budget`，==所有合金由同一台机器造==，求最多造几份',
                 '本视频：`budget=6`，配方 `[[2,1],[1,1]]`，库存 `[1,1]`，单价 `[2,2]` → `2`'],
        quote='题目要求所有合金都由一台机器完成，那么在这里就没有调度这一说了，只需遍历每台机器，计算当前机器可以生产的最大合金数，取其中的最大值作为最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用调度：每台机器单独算，取最大',
              '单台机器造得越多越难 → 二分合金数，下界 0，上界 `budget + max(stock)`',
              '对每个 mid：算需要量 `need`、要买量 `buy`、花费 `tot_cost`，和预算比'],
        summary=['时间 `O(k·n·log(budget))`',
                 '`mid = (left + right + 1) // 2` 上取整，配合 `left = mid` 避免死循环',
                 '`buy` 要和 0 取 `max`，库存多的不能算负花费',
                 '原文为 Python 2 写法，`/` 是整数除法，已改为 `//`',
                 '对比灵神：灵神用开区间并让左端点从 `ans` 起步，yiduobo 每台机器从 0 开始'],
    ),
)
