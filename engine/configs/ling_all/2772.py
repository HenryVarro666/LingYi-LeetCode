CONFIG = dict(
    num=2772, title='使数组中的所有元素都等于零', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组 + 贪心从左往右',
    tags=['灵神题单', '常用数据结构', '难度分 2029'],
    code='''
class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        d = [0] * (n + 1)
        sum_d = 0
        for i, x in enumerate(nums):
            sum_d += d[i]
            x += sum_d
            if x == 0: continue  # 无需操作
            if x < 0 or i + k > n: return False  # 无法操作
            sum_d -= x  # 直接加到 sum_d 中
            d[i + k] += x
        return True
''',
    call='Solution().checkArray([2,2,3,1,1,0], 3)',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（原数组；蓝 = 当前下标 i）', pointers={'i': 'blue'}, h=200),
        dict(type='text', fn=lambda S: (f"`nums[{S['i']}]` 原值 `{S['nums'][S['i']]}`，加上累计变化量后实际值 `{S['x']}`" if 'x' in S and 'i' in S and S.get('_line', 0) >= 9 else ''), h=60),
        dict(type='array', var='d', label='d（差分：d[i+k] 处把减量收回）', h=190, cell=90),
    ],
    watch=['i', 'x', ('sum_d', 'sum_d', 'blue')],
    captions={
        'd = [0]': '差分数组 `d`，长度 `n+1`：`d[i]` 记录「从 i 开始不再被减」的量',
        'sum_d = 0': '`sum_d` = 前面所有操作对当前位置的累计变化量（负数 = 被减掉）',
        'for i, x': lambda S, B, r: ('数组遍历完，中途没有返回 False' if 'i' in B and B.i == S.i else f'依次看 `nums[{S.i}] = {S.x}`'),
        'sum_d += d[i]': '先累加差分：前面操作累计到 `{i}` 位置的变化量 `sum_d = {sum_d}`',
        'x += sum_d': '`nums[i]` 的实际值：`{B.x} + ({sum_d})` 得 =={x}==',
        'if x == 0': lambda S, B, r: (f'实际值是 0：不用再减，看下一个' if S.x == 0 else f'实际值 `{S.x}` 不为 0：必须操作'),
        'if x < 0': lambda S, B, r: (f'`x = {S.x} < 0`：已经减过头，无法加回来 → `False`' if S.x < 0 else (f'`i + k = {S.i + S.k} > n = {len(S.nums)}`：后面不够 `k` 个数 → `False`' if S.i + S.k > len(S.nums) else f'`x = {S.x} > 0` 且 `i + k = {S.i + S.k} <= n`：可以从 `i` 起减 `{S.x}` 次')),
        'sum_d -= x': '从 `i` 起的 `k` 个数都减 `{x}`：`sum_d` 先减 `{x}` → {sum_d}',
        'd[i + k] += x': '到 `i+k` 位置这次操作结束：`d[{i + k}]` 加 `{x}`，把减量收回',
        'return True': '每个数都能减到 0 → `True`',
    },
    cards=dict(
        one_liner='最左边的非零数，只能靠从它开始的区间减掉',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次选长度为 `k` 的子数组，每个元素减 `1`，可操作任意次',
                 '问能否让整个数组变成全 `0`',
                 '示例：`nums=[2,2,3,1,1,0], k=3` → `true`'],
        quote='对于 nums[0]>0 的情况，必须把 nums[0] 到 nums[k-1] 都减去 nums[0]。然后思考 nums[1] 要怎么处理，依此类推。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左往右：当前数 `x > 0`，只有从它开始的区间能把它减到 `0`，减 `x` 次',
              '子数组同时减同一个数 → 差分数组：`d[i] -= x`，`d[i+k] += x`',
              '用 `sum_d` 累加差分，`nums[i] + sum_d` 就是当前实际值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`x < 0`：减过头了，无解；`i + k > n`：区间放不下，无解',
                 '`sum_d -= x` 直接并入累计量，省去单独写 `d[i]`',
                 '类似题：2528. 最大化城市的最小供电站数目'],
    ),
)
