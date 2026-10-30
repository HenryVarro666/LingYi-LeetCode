CONFIG = dict(
    num=2517, title='礼盒的最大甜蜜度', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 排序贪心', tags=['灵神题单·二分算法', '难度分 2021'],
    code='''
class Solution:
    def maximumTastiness(self, price: List[int], k: int) -> int:
        def f(d: int) -> int:
            cnt = 1
            pre = price[0]  # 先选一个价格最小的糖果
            for p in price:
                if p - pre >= d:  # 可以选 p
                    cnt += 1
                    pre = p
            return cnt

        price.sort()
        left = 0
        right = (price[-1] - price[0]) // (k - 1) + 1
        while left + 1 < right:  # 开区间不为空
            # 循环不变量：
            # f(left) >= k
            # f(right) < k
            mid = (left + right) // 2
            if f(mid) >= k:
                left = mid  # 下一轮二分 (mid, right)
            else:
                right = mid  # 下一轮二分 (left, mid)
        return left  # 最大的满足 f(left) >= k 的数
''',
    call='Solution().maximumTastiness([13,5,1,8,21,2], 3)',
    expect=8, max_steps=120,
    views=[
        dict(type='array', var='price', h=250, cell=96,
             label='price 排序后（绿 = pre，上一个选的；黄 = 正在看的 p）',
             color=lambda S, i, v: ('yellow' if 'p' in S and v == S['p'] and S.get('_line') in (6, 7, 8, 9) else
                                    'green' if 'pre' in S and 'cnt' in S and v == S['pre'] else None)),
        dict(type='text', h=70, fn=lambda S: (f"开区间 `({S['left']}, {S['right']})`：`f(left) ≥ k`，`f(right) < k`" if 'right' in S and 'left' in S and isinstance(S.get('right'), int) else '')),
        dict(type='text', h=70, fn=lambda S: (f"试甜蜜度 `d = {S['d']}`：已选 `{S['cnt']}` 类，上一个选的价格 `pre = {S['pre']}`，目标 `k = {S['k']}`" if 'd' in S and 'cnt' in S and 'pre' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('d', 'd', 'cyan'), ('cnt', 'cnt', 'green'), ('pre', 'pre', 'orange')],
    captions={
        'cnt = 1': '`cnt` 计已选糖果数，先算上最小的那类',
        'pre = price[0]': '最小的价格一定能选：`pre = {pre}`（选它，后面能选的不会比不选少）',
        'if p - pre >= d': lambda S, B, r: (f'`{S.p} - {S.pre} = {S.p - S.pre} ≥ {S.d}`：间隔够了，==可以选 {S.p}==' if S.p - S.pre >= S.d
                                           else f'`{S.p} - {S.pre} = {S.p - S.pre} < {S.d}`：间隔不够，跳过 {S.p}'),
        'cnt += 1': '选中，`cnt` → {cnt}',
        'pre = p': '`pre` 更新为刚选的 `{pre}`，下一个要离它至少 `{d}`',
        'return cnt': '甜蜜度至少为 `{d}` 时，最多能选 ==`{cnt}`== 类',
        'price.sort()': '最小差只会出现在相邻价格之间：先排序 → `{price}`',
        'right = (': '右开端点：`({price[-1]} - {price[0]}) // ({k} - 1) + 1 = {right}`，再大必然选不够 `k` 类',
        'mid = (': '猜答案 `mid = ({left} + {right}) // 2 = {mid}`',
        'if f(mid)': '调用 `f({mid})`：甜蜜度至少 {mid} 时，最多能选几类？和 `k = {k}` 比',
        'left = mid': '`f({mid}) ≥ {k}`：甜蜜度 {mid} 做得到 → 答案 ≥ {mid}，`left = {left}`',
        'right = mid': '`f({mid}) < {k}`：{mid} 太苛刻 → 答案 < {mid}，`right = {right}`',
        'while left + 1 < right': lambda S, B, r: ('开区间 `(left, right)` 里还有数，继续二分' if S.left + 1 < S.right else f'`left + 1 = right`：开区间空了 → 答案就是 `left = {S.left}`'),
        'return left': '最大的满足 `f(left) ≥ k` 的数：==返回 {left}==',
    },
    cards=dict(
        one_liner='最大化最小值：二分甜蜜度，再贪心数最多能选几类',
        complexity='时间 `O(n log n + n log U)`，空间 `O(1)`',
        problem=['从 `price` 里挑 `k` 类不同糖果，甜蜜度 = 任意两类价格差的最小值',
                 '求最大的甜蜜度',
                 '示例：`[13,5,1,8,21,2]`，`k=3` → `8`（选 13、5、21）'],
        quote='如果题目要求「最大化最小值」或者「最小化最大值」，一般是二分答案。为什么？对于本题来说，甜蜜度越大，能选择的糖果越少，有单调性，所以可以二分答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定义 `f(d)`：甜蜜度至少为 d 时最多能选几类（注意是至少）',
              '排序后贪心：最小的一定选；价格 ≥ `pre + d` 才选',
              '`f(d) ≥ k` 就往大猜，否则往小猜；开区间写法 `check` 为真更新谁就返回谁'],
        summary=['时间 `O(n log n + n log U)`，`U = (最大 − 最小) / (k − 1)`',
                 '右开端点 `(max−min)//(k−1)+1` 一定选不出 k 类；左端点 0 一定可行',
                 '易错：`f(d)` 是「至少 d」不是「恰好 d」；`pre` 先取 `price[0]`',
                 '二分结果一定是某两个价格的差（反证：否则 `f(ans+1)` 也成立）',
                 '另一写法：用 `bisect_left(range(right), True, key=check)` 二分，本视频不展开'],
    ),
)
