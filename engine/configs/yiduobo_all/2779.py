NUMS = [4, 6, 1, 2]
K = 2


def _cnt_color(S, i, v):
    if 'target' in S and 'left' in S and 'right' in S and S['left'] == max(0, S['target'] - K):
        if S['left'] <= i <= S['right']:
            return 'orange' if i == S['right'] else 'blue'
        if S['left'] > 0 and i == S['left'] - 1:
            return 'purple'
    return None


def _top(S):
    if 'cnt' not in S:
        return '目标值 target 只可能在 `[0, max(nums)]` 之间 → ==暴力枚举 target=='
    if 'target' not in S:
        if 'v' in S and S.get('_line') in (8, 9):
            return '把计数数组原地变成==前缀和==：`cnt[v]` = 值 `≤ v` 的数的个数'
        return '计数：`cnt[v]` = 值等于 v 的数的个数（类似桶排）'
    if 'right' not in S or S['left'] != max(0, S['target'] - K) or S['right'] != min(S['ma'], S['target'] + K):
        return f"target = `{S['target']}`：值在 `[target − k, target + k]` 的数都能变成它"
    t, l, r, c = S['target'], S['left'], S['right'], S['cnt']
    if l > 0:
        return f"target = `{t}`：值在 `[{l}, {r}]` 的个数 = `cnt[{r}] − cnt[{l - 1}] = {c[r]} − {c[l - 1]} = {c[r] - c[l - 1]}`"
    return f"target = `{t}`：值在 `[0, {r}]` 的个数 = `cnt[{r}] = {c[r]}`"


CONFIG = dict(
    num=2779, title='数组的最大美丽值', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举目标值 + 前缀和计数',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def maximumBeauty(self, nums, k):

        ma = max(nums)

        cnt = [0] * (ma + 1)
        for v in nums:
            cnt[v] += 1
        for v in range(1, ma + 1):
            cnt[v] += cnt[v - 1]

        res = 0
        for target in range(ma + 1):
            left = max(0, target - k)
            right = min(ma, target + k)

            if left > 0:
                res = max(res, cnt[right] - cnt[left - 1])
            else:
                res = max(res, cnt[right])

        return res
''',
    call=f'Solution().maximumBeauty({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='array', var='nums', label='nums', cell=96, h=180),
        dict(type='array', var=lambda S: S.get('cnt') or [], label='cnt（下标 = 数值；蓝/橙 = [left, right]，紫 = cnt[left − 1]）',
             pointers={'v if _line <= 10 else None': 'pink', 'target': 'green'},
             pointer_labels={'v if _line <= 10 else None': 'v'}, color=_cnt_color, cell=96, h=260),
    ],
    watch=['ma', ('target', 'target', 'green'), ('left', 'left', 'blue'), ('right', 'right', 'orange'), ('res', 'res', 'green')],
    captions={
        'ma = max(nums)': '最大值 `ma = {ma}`：数值范围和 n 同量级，可以直接开数组',
        'cnt = [0] *': '计数数组 `cnt`，长度 `ma + 1 = {ma + 1}`',
        'for v in nums': lambda S, B, r: ('统计完毕' if 'v' in B and B.v == S.v else f'统计 `v = {S.v}`'),
        'cnt[v] += 1': '`cnt[{v}]` → {cnt[v]}',
        'for v in range(1': lambda S, B, r: ('前缀和完成' if B.get('v') == S.v else f'前缀和：处理 `cnt[{S.v}]`'),
        'cnt[v] += cnt[v - 1]': '`cnt[{v}] += cnt[{v - 1}]` → `{cnt[v]}`：值 ≤ {v} 的数有 {cnt[v]} 个',
        'res = 0': '`cnt = {cnt}`；`res = 0`，开始枚举目标值',
        'for target in': lambda S, B, r: (f'枚举目标值 `target = {S.target}`' if 'target' not in B or B.target != S.target
                                          else '枚举结束'),
        'left = max(0': '能变成 {target} 的最小值 `max(0, {target} − {k})` = `{left}`',
        'right = min(ma': '能变成 {target} 的最大值 `min({ma}, {target} + {k})` = `{right}`',
        'if left > 0': lambda S, B, r: (f'`left = {S.left} > 0`：用 `cnt[{S.right}] − cnt[{S.left - 1}]`' if S.left > 0
                                        else '`left = 0`：没有 `cnt[-1]`，直接用 `cnt[right]`'),
        'res = max(res, cnt[right] - cnt[left - 1])': '`res = max({B.res}, {cnt[right]} − {cnt[left - 1]})` = =={res}==',
        'res = max(res, cnt[right])': '`res = max({B.res}, {cnt[right]})` = =={res}==',
        'return res': '最大美丽值 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='直接枚举最终相等的那个值，用前缀和数出能变成它的数',
        complexity='时间 `O(n + U)`，空间 `O(U)`（U = max(nums)）',
        problem=['每个下标至多操作一次：把 `nums[i]` 换成 `[nums[i]−k, nums[i]+k]` 中的数',
                 '美丽值 = 由==相等元素==组成的最长子序列长度，求最大值',
                 '示例：`[4,6,1,2], k = 2` → `3`'],
        quote='对于一个目标数值target，只有数值在==target - k到target + k之间==的数才能变成target……就是cnt[target + k] - cnt[target - k - 1]。',
        quote_src='—— yiduobo 题解原文',
        idea=['数值和 k 与 n 同量级 → ==暴力枚举== target ∈ `[0, max]`',
              '计数数组 `cnt` 再原地转成前缀和',
              '区间 `[target−k, target+k]` 内的个数 = 前缀和相减'],
        summary=['时间 `O(n + U)`，空间 `O(U)`，不用排序',
                 '`target − k`、`target + k` 都可能越界：用 `max(0, …)`、`min(ma, …)` 截断',
                 '`left = 0` 时没有 `cnt[left − 1]`，要单独处理',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未改动',
                 '对比灵神：灵神排序后滑窗找 `y − x ≤ 2k`；这里按值域计数'],
    ),
)
