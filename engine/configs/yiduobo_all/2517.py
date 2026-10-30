CONFIG = dict(
    num=2517, title='礼盒的最大甜蜜度', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 + 一趟贪心', tags=['灵神题单·二分算法', '难度分 2021'],
    code='''
class Solution(object):
    def maximumTastiness(self, price, k):

        price.sort()
        left = 0
        right = price[-1] - price[0]

        while left < right:
            mid = (left + right + 1) >> 1
            cnt = 1
            pre = 0
            now = 1
            while now < len(price):
                if price[now] - price[pre] >= mid:
                    pre = now
                    cnt += 1
                
                now += 1

            if cnt >= k:
                left = mid
            else:
                right = mid - 1

        return left
''',
    call='Solution().maximumTastiness([13,5,1,8,21,2], 3)',
    expect=8, max_steps=120,
    skip=['now += 1', 'while now < len', 'pre = 0', 'now = 1'],
    views=[
        dict(type='array', var='price', h=260, cell=96,
             label='price 排序后（绿 = pre 下标，黄 = now 下标）',
             pointers={'pre': 'green', 'now': 'yellow'},
             color=lambda S, i, v: 'green' if 'pre' in S and 'cnt' in S and i == S['pre'] else None),
        dict(type='text', h=70, fn=lambda S: (f"二分范围 `[{S['left']}, {S['right']}]`（闭区间），试 `mid = {S['mid']}`" if 'mid' in S else (f"二分范围 `[{S['left']}, {S['right']}]`" if 'right' in S else ''))),
        dict(type='text', h=70, fn=lambda S: (f"已选 `cnt = {S['cnt']}` 类，目标 `k = {S['k']}`" if 'cnt' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('cnt', 'cnt', 'green'), ('pre', 'pre', 'green'), ('now', 'now', 'yellow')],
    captions={
        'price.sort()': '先按价格从小到大排序 → `{price}`',
        'right = price[-1]': '上界 = 最贵 − 最便宜 = `{right}`（差再大也选不出）；下界 `left = 0`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：还没夹到答案，继续' if S.left < S.right else f'`left = right = {S.left}`：夹到了'),
        'mid = (': '取偏大的中点：`mid = ({left} + {right} + 1) >> 1 = {mid}`（==+1== 防止 `left = mid` 死循环）',
        'cnt = 1': '先选下标 0（最便宜的）：`cnt = 1`；`pre` 记最后选中的==下标==，`now` 从 1 往后找',
        'pre = 0': '`pre` 记已选的最后一颗糖果的==下标==',
        'now = 1': '从下标 1 开始往后找',
        'while now < len': lambda S, B, r: (f'`now = {S.now}`：看 `price[{S.now}]`' if S.now < len(S.price) else '糖果看完了'),
        'if price[now]': lambda S, B, r: (f'`{S.price[S.now]} - {S.price[S.pre]} = {S.price[S.now] - S.price[S.pre]} ≥ {S.mid}`：能选' if S.price[S.now] - S.price[S.pre] >= S.mid
                                       else f'`{S.price[S.now]} - {S.price[S.pre]} = {S.price[S.now] - S.price[S.pre]} < {S.mid}`：太近，不选'),
        'pre = now': '选 `price[{now}] = {price[now]}`，`pre` → {pre}',
        'cnt += 1': '`cnt` → {cnt}',
        'now += 1': '`now` → {now}',
        'if cnt >= k': lambda S, B, r: (f'`cnt = {S.cnt} ≥ k = {S.k}`：甜蜜度 {S.mid} 可行' if S.cnt >= S.k else f'`cnt = {S.cnt} < k = {S.k}`：甜蜜度 {S.mid} 选不够'),
        'left = mid': '可行 → 答案 ≥ {mid}：下界 `left = {left}`',
        'right = mid - 1': '不可行 → 答案 ≤ {mid} − 1：上界 `right = {right}`',
        'return left': '`left = right`：最大可行甜蜜度 ==`{left}`==',
    },
    cards=dict(
        one_liner='甜度越低越好满足：二分最大可行甜度',
        complexity='时间 `O(n log n + n log U)`，空间 `O(1)`',
        problem=['挑 `k` 类糖果装礼盒，甜度 = 任意两类价格差的最小值',
                 '求最大甜度',
                 '示例：`[13,5,1,8,21,2]`，`k=3` → `8`'],
        quote='礼盒的甜度越低，放糖果的门槛就越低，可放进去的糖果也就越多。根据这一点，就可以通过二分答案来寻找最大可行的甜度。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排序；上界取最贵减最便宜，下界 0',
              '对 `mid` 一趟遍历：`pre` 记最后选中的下标，差 ≥ mid 就选',
              '选够 `k` 类 → `left = mid`，否则 `right = mid - 1`'],
        summary=['时间 `O(n log n + n log U)`，`U` 为最大价差',
                 '闭区间二分：取中点要 `+1`，否则 `left = mid` 会死循环',
                 '`pre` 存的是下标，比较用 `price[now] - price[pre]`',
                 '原文已是 Python 3 可运行写法，未改动',
                 '对比灵神：灵神用开区间并把右端点收紧到 `(max−min)//(k−1)+1`'],
    ),
)
