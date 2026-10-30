def _info(S):
    if 'h' not in S:
        return '把负数取绝对值：答案 = 非负数之和 − 第 k 小的「减数和」'
    popped = S.get('s')
    base = f"非负数之和 `sum = {S['sum']}`；堆里存 `(减数和, 下一个下标)`，堆顶最小"
    if popped is not None and S.get('_line', 0) >= 20:
        base = f"刚弹出的最小减数和 `s = {popped}`，下一个可选元素下标 `i = {S['i']}`；对应的子序列和 = {S['sum']} − {popped} = =={S['sum'] - popped}=="
    return base


CONFIG = dict(
    num=2386, title='找出数组的第 K 大和', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='转化为第 k 小 + 最小堆生成子序列和',
    tags=['常用数据结构', '难度分 2648'],
    code='''
class Solution:
    def kSum(self, nums: List[int], k: int) -> int:
        sum = 0
        for i, x in enumerate(nums):
            if x >= 0:
                sum += x
            else:
                nums[i] = -x
        nums.sort()

        h = [(0, 0)]  # 空子序列
        for _ in range(k - 1):
            s, i = heappop(h)
            if i < len(nums):
                # 在子序列的末尾添加 nums[i]
                heappush(h, (s + nums[i], i + 1))  # 下一个添加/替换的元素下标为 i+1
                if i:  # 替换子序列的末尾元素为 nums[i]
                    heappush(h, (s + nums[i] - nums[i - 1], i + 1))
        return sum - h[0][0]
''',
    call='Solution().kSum([2, 4, -2], 5)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（负数取绝对值后排序）', h=130, cell=80,
             color=lambda S, i, v: ('blue' if i == S.get('i') else 'pink' if i == S.get('i', 0) - 1 else None) if S.get('_line', 0) >= 13 and 'h' in S else None),
        dict(type='heap', var='h', h=240,
             fmt=lambda x: f'{x[0]}|{x[1]}'),
        dict(type='text', fn=_info, size=26, h=110),
    ],
    watch=[('sum', 'sum', 'green'), 'k', 's', 'i', ('已弹出', lambda S: S['_'] + 1 if '_' in S else '', 'orange')],
    captions={
        'sum += x': '`{x}` 非负 → 一定先选上：`sum` = {sum}（这是最大的子序列和）',
        'nums[i] = -x': '`{x}` 是负数：「加上负数」和「减去它的绝对值」效果一样 → 存成 `{-x}`',
        'nums.sort()': '排好序（全是非负数）：之后「添加」和「替换」都能让和变大',
        'h = [(0, 0)]': '堆里放入「空子序列」：减数和 `0`，下一个可选下标 `0`',
        'heappop(h)': '弹出堆顶 = 当前最小的减数和 `s = {s}`：它是第 `{_ + 1}` 小的减数和，用它来生成后继',
        'if i < len(nums)': lambda S, B, r: (f'`i = {S.i} < {len(S.nums)}`：还有元素可以添加/替换' if S.i < len(S.nums) else f'`i = {S.i}` 已到末尾，没有后继，不再入堆'),
        'heappush(h, (s + nums[i], i + 1))': '在末尾==添加== `nums[{i}] = {nums[i]}`：新减数和 `{s} + {nums[i]} = {s + nums[i]}`，下标变 {i + 1}',
        'heappush(h, (s + nums[i] - nums[i - 1]': '把末尾的 `nums[{i - 1}] = {nums[i - 1]}` ==替换==成 `nums[{i}] = {nums[i]}`：新减数和 `{s} + {nums[i]} − {nums[i - 1]} = {s + nums[i] - nums[i - 1]}`',
        'return sum - h[0][0]': '第 k 小的减数和是堆顶 `{h[0][0]}` → 答案 `{sum} − {h[0][0]} = =={ret}==`',
    },
    skip=['for _ in range(k - 1)', 'for i, x in enumerate(nums)', 'if x >= 0', 'if i:'],
    max_steps=80,
    cards=dict(
        one_liner='第 k 大和 = 非负数之和 − 第 k 小的「减数和」，用最小堆逐个生成',
        complexity='时间 `O(n log n + k log k)`，空间 `O(k)`',
        problem=['任选 `nums` 的一个子序列求和（空序列和为 0），求第 `k` 大的和',
                 '示例：`[2,4,-2], k=5` → `2`（和从大到小 6,4,4,2,2,0,0,-2）',
                 '`n` 到 `10^5`，但 `k ≤ 2000`'],
        quote='「减去非负数」和「加上负数」都相当于减去 |nums[i]|。sum 减去的数越小，nums 的子序列和就越大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['所有负数取绝对值，问题变成：第 `k` 小的子序列和（减数和）',
              '从空子序列出发，每个子序列可以「末尾添加下一个数」或「把末尾换成下一个数」，不重不漏',
              '这相当于在以空序列为根的树上跑 Dijkstra：出堆顺序就是和的从小到大'],
        after=[dict(heading='另一种写法', lines=['方法一：二分答案 + 暴搜子集，剪枝后每次 check 最多 `k` 次递归', '本视频是方法二：最小堆，只弹 `k-1` 次'])],
        summary=['先 `sum` 加所有非负数，负数取绝对值后排序',
                 '每个子序列只有两个后继：添加 `nums[i]`、替换成 `nums[i]`，下标统一变成 `i+1`',
                 '`if i:` 保证第一个元素不能做「替换」',
                 '循环 `k-1` 次后，堆顶就是第 `k` 小的减数和'],
    ),
)
