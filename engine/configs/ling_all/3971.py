CONFIG = dict(
    num=3971, title='最大总价值', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分第 m 大价值 + 等差数列求和',
    tags=['二分算法', '难度分 2195'],
    code='''
class Solution:
    def maxTotalValue(self, value: list[int], decay: list[int], m: int) -> int:
        def check(low: int) -> bool:
            left_m = m
            for v, d in zip(value, decay):
                if v >= low:
                    left_m -= (v - low) // d + 1
                    if left_m < 0:  # 提前跳出循环
                        return True
            return False

        if not check(0):  # 可以选所有价值
            low = 0
        else:
            left, right = 0, max(value) + 1
            while left + 1 < right:
                mid = (left + right) // 2
                if check(mid):
                    left = mid
                else:
                    right = mid
            low = left

        ans = 0
        # 计算价值严格大于 low 的价值和，以及这些价值的个数
        for v, d in zip(value, decay):
            if v > low:
                k = (v - low - 1) // d + 1
                m -= k
                ans += (v * 2 - d * (k - 1)) * k
        ans //= 2  # 把除以 2 提到循环外面
        ans += m * low  # 剩余 m 次选的价值都是 low
        return ans % 1_000_000_007
''',
    call='Solution().maxTotalValue([6, 5, 4], [2, 1, 1], 4)',
    expect=19,
    views=[
        dict(type='array', var='value', label='value（蓝 = 当前遍历的下标）', cell=84, h=140,
             color=lambda S, i, x: 'blue' if S.get('v') == x else None),
        dict(type='array', var='decay', label='decay', cell=84, h=140,
             color=lambda S, i, x: 'blue' if S.get('d') == x and S.get('v') == S['value'][i] else None),
        dict(type='text', size=28, fn=lambda S: (
            f"二分第 m 大价值：`({S['left']}, {S['right']})` 开区间，`mid = {S['mid']}`" if 'mid' in S and 'left' in S and 'right' in S
            else (f"`low = {S['low']}`：先算价值 `> low` 的，剩下都等于 low" if 'low' in S else ''))),
        dict(type='text', size=28, fn=lambda S: (
            f"`m` 还剩 {S['m']}，累计 `ans = {S['ans']}`" if 'ans' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), ('low', 'low', 'purple'),
           ('left_m', 'left_m', 'orange'), ('m', 'm', 'cyan'), ('ans', 'ans', 'green')],
    max_steps=100,
    skip=['left_m = m', 'for v, d in zip', 'if v >= low', 'if v > low', 'ans = 0', 'return True'],
    captions={
        'left_m = m': '`left_m = m = {m}`：还需要凑够几个价值',
        'if v >= low': lambda S, B, r: (f'`v = {S.v} >= low = {S.low}` → 这个下标能选出不少于 low 的价值' if S.v >= S.low
                                        else f'`v = {S.v} < low = {S.low}` → 一次都选不了，跳过'),
        'left_m -= (v - low)': '`v = {v}` 最多选 `({v} - {low}) // {d} + 1` = =={(v-low)//d+1}== 次价值 ≥ low：`left_m` → {left_m}',
        'if left_m < 0': lambda S, B, r: (f'`left_m = {S.left_m} < 0`：价值 ≥ low 的已经超过 m 个 → 提前返回 True（low 还可以更大）' if S.left_m < 0
                                          else f'`left_m = {S.left_m} >= 0`：还没超过 m 个，继续看下一个下标'),
        'return True': '价值 `>= low` 的个数 ≥ m，说明 `low` 还可以更大 → True',
        'return False': '遍历完仍不足 m 个 → `low` 取大了 → False',
        'if not check(0)': '先试 `check(0)`：价值 ≥ 0 的个数不足 m 就全选（low = 0）；够了就要二分 low',
        'if check(mid)': '调用 `check({mid})`：价值 ≥ {mid} 的个数有没有 m 个？',
        'left, right = 0, max': '开区间二分：`left = 0` 一定满足，`right = max(value) + 1 = {right}` 一定不满足',
        'while left + 1 < right': lambda S, B, r: (f'`left + 1 = {S.left + 1} < right = {S.right}` → 区间 `({S.left}, {S.right})` 里还有候选' if S.left + 1 < S.right
                                                   else f'`left + 1 = {S.left + 1} = right` → 开区间空了，`left` 就是 low'),
        'mid = (left + right)': '取 `mid = ({left} + {right}) // 2` = =={mid}==：看价值 ≥ mid 的有没有 m 个',
        'left = mid': '`check({mid})` 为 True → ≥ mid 的价值够 m 个，low 至少是 mid：`left` → {left}',
        'right = mid': '`check({mid})` 为 False → mid 太大了：`right` → {right}',
        'low = left': '二分结束：==第 m 大的价值 low = {low}==',
        'ans = 0': '`ans = 0`：开始累计价值 ==严格大于 low== 的那些',
        'for v, d in zip(value, decay):': lambda S, B, r: (f'`v = {S.v}, d = {S.d}`' if 'v' in S else '遍历所有下标'),
        'if v > low': lambda S, B, r: (f'`v = {S.v} > low = {S.low}` → 它有一部分价值要全拿' if S.v > S.low
                                       else f'`v = {S.v} <= low = {S.low}` → 没有严格大于 low 的价值'),
        'k = (v - low - 1)': '价值 `> low` 即 `>= low + 1`，共选 `k = ({v} - {low} - 1) // {d} + 1` = =={k}== 次',
        'm -= k': '这 `{k}` 个价值已经拿走，`m` 还剩 {m} 个名额',
        'ans += (v * 2': '等差数列求和（先不除 2）：`(2·{v} - {d}·({k}-1)) · {k}`，`ans` → {ans}',
        'ans //= 2': '把除以 2 统一提到循环外：`ans = {ans}`',
        'ans += m * low': '剩下 `m = {m}` 次，价值都恰好等于 `low = {low}`：`ans += {m} * {low}` → {ans}',
        'return ans %': '`{ans} % (10^9+7)` = =={ret}==',
    },
    cards=dict(
        one_liner='二分第 m 大的价值，再用等差数列一次性求和',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['`value[i]` 是下标 i 的初始价值，每选一次下标 i，价值减少 `decay[i]`',
                 '最多选 m 次，求最大总价值，对 `10^9 + 7` 取模',
                 '示例：`value=[6,5,4], decay=[2,1,1], m=4` → `19`'],
        quote='第 m 小等价于：求最小的 x，满足 ≤ x 的数至少有 m 个。第 m 大等价于：求最大的 x，满足 ≥ x 的数至少有 m 个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['m 高达 `10^9`，用堆模拟太慢 → 转成「第 m 大价值」，==二分 low==',
              '价值 `>= low` 的个数：每个下标 `(v - low) // d + 1`，累加和 m 比较',
              '严格大于 low 的价值用等差数列求和；剩下的名额都按 low 计算'],
        summary=['时间 `O(n log U)`，空间 `O(1)`；`U = max(value)`',
                 '开区间二分：`check(mid)` 为 True 更新谁，最后就返回谁',
                 '总和不超过 `10^18`，Python 里最后再取模即可',
                 '题解还有一版小优化：先判断 `check(0)`，随机数据下 low 大概率是 0',
                 '同类题：二分题单 §2.6 第 K 小/大'],
    ),
)
