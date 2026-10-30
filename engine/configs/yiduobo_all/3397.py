_cnt = {}


def _forcap(var, n, key):
    def f(S, B, r):
        c = _cnt.get(key, 0) + 1
        _cnt[key] = c
        if c > n:
            return '遍历完所有元素，退出循环'
        return f'第 {c + 1} 个元素，取到 `{var} = {S.nums[c]}`' + ('（原值）' if False else '')
    return f


CONFIG = dict(
    num=3397, title='执行操作后不同元素的最大数量', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='排序 + 维护目标值 target',
    tags=['灵神题单', '难度分 1687'],
    code='''
class Solution(object):
    def maxDistinctElements(self, nums, k):
        
        nums.sort()
        res = 1
        target = nums[0] - k + 1
        for v in nums[1:]:
            if abs(v - target) <= k:
                target += 1
                res += 1
            elif v > target:
                target = v - k + 1
                res += 1
        
        return res
''',
    call='Solution().maxDistinctElements([4,4,4,4,4,5,9], 1)',
    expect=5,
    views=[
        dict(type='array', var='nums', h=190, label='nums（排序后）'),
        dict(type='text', h=130, fn=lambda S: ('下一个元素最理想的构造值 `target` 是 ==%s==' % S['target']) if 'target' in S else ''),
        dict(type='text', h=130, fn=lambda S: ('当前 `v = %s`，可达范围 `[%s, %s]`' % (S['v'], S['v'] - S['k'], S['v'] + S['k'])) if 'v' in S else ''),
    ],
    watch=['v', 'k', ('target', 'target', 'blue'), ('res', 'res', 'green')],
    captions={
        'for v in nums': _forcap('v', 6, 'y'),
        'nums.sort': '排序：从最小值开始，依次考虑每个元素',
        'res = 1': '最小值肯定能构造出一个值，`res = 1`',
        'target = nums[0]': '最小值减去 k，给后面的元素留足空间；下一个理想值 `target = {nums[0]} - {k} + 1 = {target}`',
        'if abs(v - target)': lambda S, B, r: (f'`|{S.v} - {S.target}| = {abs(S.v - S.target)} <= k = {S.k}`：`v` 能变成 `target`' if abs(S.v - S.target) <= S.k else f'`|{S.v} - {S.target}| = {abs(S.v - S.target)} > k = {S.k}`：`v` 够不着 `target`'),
        'target += 1': '`v` 变成 `target`，下一个理想值是 `target + 1 = {target}`',
        'res += 1': '多构造出一个不同的值：`res` → {res}',
        'elif v > target': lambda S, B, r: (f'`v = {S.v} > target = {S.target}`：`target` 太小够不着，但 `v-k` 没人用过' if S.v > S.target else f'`v = {S.v} <= target = {S.target}`：可用的值都被用完了，只能跳过'),
        'target = v - k + 1': '`v` 变成 `v - k`，下一个理想值 `target = {v} - {k} + 1 = {target}`',
        'return res': '最多有 =={ret}== 个不同元素',
    },
    max_steps=80,
    cards=dict(
        one_liner='从最小值开始构造，维护下一个元素的理想构造值',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每个元素最多可以加上一个 `[-k, k]` 内的整数',
                 '求操作后 `nums` 里 ==不同元素== 的最大数量',
                 '本视频：`[4,4,4,4,4,5,9]`、`k=1` → `5`'],
        quote='对于nums中的最小值first，很明显应该让first减去k，这样一来留给其他元素的操作空间会更大。',
        quote_src='—— yiduobo 题解原文',
        idea=['先从边界考虑：最小值减 k，下一个理想值 `target = first - k + 1`',
              '次小值 `v` 与 `target` 比较，分三种：`v < target - k` 跳过；`|v - target| <= k` 变成 `target`；`v > target + k` 变成 `v - k`',
              '每次构造成功 `res` 加一，并更新 `target`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`abs(v - target) <= k` 时 `target += 1`；否则 `v > target` 时 `target = v - k + 1`',
                 '`v < target - k` 的元素被跳过，不计数',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比灵神：灵神 `pre` 记录已占用的位置，用 `min/max` 写成一行；yiduobo 分三种情况讨论'],
    ),
)
