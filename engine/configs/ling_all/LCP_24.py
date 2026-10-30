def _info(S):
    if 'left_sum' not in S:
        return 'b[i] = nums[i] − i：把「变成 x, x+1, x+2…」转成「都变成同一个 x」'
    L, R = S['left'], S['right']
    if not R:
        return f'左半（最大堆）和 =={S["left_sum"]}==　右半（最小堆）和 =={S["right_sum"]}=='
    return (f'左半和 `{S["left_sum"]}`　右半和 `{S["right_sum"]}`　右堆顶（中位数）`{R[0]}`　→ '
            f'右半 − 左半 = ==​{S["right_sum"] - S["left_sum"]}==')


CONFIG = dict(
    num='LCP 24', title='数字游戏', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='转成中位数 · 对顶堆',
    tags=['常用数据结构', '贪心与思维'],
    code='''
class Solution:
    def numsGame(self, nums: List[int]) -> List[int]:
        MOD = 1_000_000_007
        ans = [0] * len(nums)
        left = []  # 维护较小的一半，大根堆（小根堆取负号）
        right = []  # 维护较大的一半，小根堆
        left_sum = right_sum = 0
        for i, b in enumerate(nums):
            b -= i
            if i % 2 == 0:  # 前缀长度是奇数
                left_sum -= max(-left[0] - b, 0) if left else 0
                t = -heappushpop(left, -b)
                right_sum += t
                heappush(right, t)
                ans[i] = (right_sum - right[0] - left_sum) % MOD
            else:  # 前缀长度是偶数
                right_sum += max(b - right[0], 0)
                t = heappushpop(right, b)
                left_sum += t
                heappush(left, -t)
                ans[i] = (right_sum - left_sum) % MOD
        return ans
''',
    call='Solution().numsGame([1,1,1,2,3,4])',
    expect=[0, 1, 2, 3, 3, 3],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, h=185),
        dict(type='heap', var=lambda S: [-x for x in S['left']] if 'left' in S else [], label='left 较小一半（真实值）', top_color='blue', h=130),
        dict(type='heap', var='right', label='right 较大一半（最小堆）', top_color='pink', h=130),
        dict(type='array', var='ans', label='ans', h=165),
        dict(type='text', fn=_info, size=26, h=90),
    ],
    skip=['MOD =', 'ans = [0]', 'left_sum = right_sum'],
    watch=[('i', 'i', 'blue'), 'b', ('left_sum', 'left_sum', 'blue'), ('right_sum', 'right_sum', 'pink')],
    captions={
        'b -= i': '`b = nums[i] − i = {b}`：把「变成 x, x+1, x+2…」转成「都变成同一个 x」',
        'left_sum -= max': '右半要多出一个数：先把 `b` 放进 left。若 `b` 比 left 堆顶小，left 的和就变了，这里先把「会被顶出去的差值」扣掉',
        't = -heappushpop(left, -b)': '`b` 放进 left，再弹出 left 最大值 =={t}==：不管 `b` 大小，弹出的都是==当前的中位数候选==',
        'right_sum += t': '弹出的 `{t}` 归入右半：`right_sum` → {right_sum}',
        'heappush(right, t)': '`{t}` 压入 right；奇数个数时 right 比 left 多 1 个，==right 堆顶就是中位数，x = =={right[0]}==',
        'ans[i] = (right_sum - right[0] - left_sum)': '长度为奇数：去掉中位数 `{right[0]}`，右半和 − 左半和 = `{right_sum} − ({right[0]}) − ({left_sum})` = =={ans[i]}==',
        'right_sum += max': '偶数个：先把 `b` 放进 right。若 `b` 比 right 堆顶大，right 和增加差值，否则增加 0',
        't = heappushpop(right, b)': '`b` 放进 right，弹出 right 最小值 =={t}==，把它挪给 left，保证两半数量相等',
        'left_sum += t': '`{t}` 归入左半：`left_sum` → {left_sum}',
        'heappush(left, -t)': '`{t}` 压入 left（取负号存）；现在 left、right 个数相同',
        'ans[i] = (right_sum - left_sum)': '长度为偶数：右半和 − 左半和 = `{right_sum} − ({left_sum})` = =={ans[i]}==，再对 `MOD` 取模',
        'return ans': '每个前缀的最小操作数：`{ans}`',
    },
    cards=dict(
        one_liner='每个数减去下标，就变成「全部变成同一个数」：中位数贪心',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把前缀变成 `x, x+1, x+2, …`，每次只能把某个数加一或减一',
                 '对每个前缀 `0..i` 求最少操作数，答案对 `1e9+7` 取模',
                 '示例：`[1,1,1,2,3,4]` → `[0,1,2,3,3,3]`'],
        quote='定义 b_i = a_i − i，问题变成求 |b_0−x| + |b_1−x| + … 的最小值。这相当于在问：把 b_i 都变成同一个整数 x，最少要操作多少次？',
        quote_src='—— 灵茶山艾府题解',
        idea=['`b[i] = nums[i] − i`，目标序列 `x, x+1, …` 变成了统一的 `x`',
              '把所有数变成中位数最省；距离和 = ==右半之和 − 左半之和==（奇数个时先去掉中位数）',
              '前缀不断变长 → 用==对顶堆==动态维护中位数和两半的和'],
        summary=['时间 `O(n log n)`：每个元素常数次堆操作',
                 '奇数前缀：先进 left 再把最大值挪给 right，保证 right 堆顶 = 中位数',
                 '易错点：Python 只有小根堆，left 要存负号；`b` 可能为负，最后取模',
                 '对照 295 数据流的中位数：本题额外维护两半的和'],
    ),
)
