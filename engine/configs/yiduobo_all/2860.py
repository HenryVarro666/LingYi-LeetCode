def _info(S):
    if 'k' not in S:
        return '选 `k` 个学生 ⇔ ==第 k 小的数 < k，且第 k+1 小的数 > k=='
    k, a = S['k'], S['nums']
    ok = a[k - 1] < k and a[k] > k
    return (f'选 `k = {k}` 个：第 k 小 `nums[{k-1}] = {a[k-1]}` 要 < {k}，第 k+1 小 `nums[{k}] = {a[k]}` 要 > {k} → '
            + ('==好分组==' if ok else '不行'))


CONFIG = dict(
    num=2860, title='让所有学生保持开心的分组方法数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 · 第 k 小与第 k+1 小',
    tags=['灵神题单', '贪心与思维', '难度分 1626'],
    code='''
class Solution(object):
    def countWays(self, nums):

        nums.sort()
        res = 0
        if nums[0] > 0:
            res += 1
        if nums[-1] < len(nums):
            res += 1

        for k in range(1, len(nums)):
            if nums[k - 1] < k and nums[k] > k:
                res += 1
        return res
''',
    call='Solution().countWays([6, 0, 3, 3, 6, 7, 2, 7])',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=80),
        dict(type='array', var='nums', label='nums（排序后；绿 = 前 k 小，蓝箭头 = 第 k+1 小 nums[k]）',
             pointers={'k': 'blue'}, cell=96, h=280,
             color=lambda S, i, v: 'green' if ('k' in S and i < S['k']) else None,
             dim=lambda S, i, v: 'k' in S and i > S['k']),
    ],
    watch=[('k', lambda S: S.get('k'), 'blue'), ('res', lambda S: S.get('res'), 'green')],
    captions={
        'nums.sort()': '从小到大排序：选中的必然是==最小的 k 个==',
        'res = 0': '`res` 统计好分组的个数',
        'if nums[0] > 0': lambda S, B, r: (f'一个都不选（`k = 0`）：没有第 0 小，只需 `nums[0] = {S.nums[0]} > 0`' +
                                           ('，成立 → `res += 1`' if S.nums[0] > 0 else '，不成立')),
        'if nums[-1] < len(nums)': lambda S, B, r: (f'全选（`k = n = {len(S.nums)}`）：没有第 n+1 小，只需 `nums[-1] = {S.nums[-1]} < {len(S.nums)}`' +
                                                    ('，成立 → `res += 1`' if S.nums[-1] < len(S.nums) else '，不成立')),
        'for k in range': '枚举选 `k = {k}` 个学生',
        'if nums[k - 1] < k and': lambda S, B, r: (f'第 k 小 `{S.nums[S.k-1]} < {S.k}`？第 k+1 小 `{S.nums[S.k]} > {S.k}`？→ ' +
                                                    ('==都满足，好分组==' if S.nums[S.k-1] < S.k and S.nums[S.k] > S.k else '至少一个不满足')),
        'res += 1': '`res` = {res}',
        'return res': '一共 `{ret}` 种分组方法',
    },
    cards=dict(
        one_liner='选 k 人好不好：看第 k 小和第 k+1 小',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`nums[i]`：选中时人数要 ==严格大于== 它，没选时人数要 ==严格小于== 它',
                 '求让所有学生开心的选人方案数',
                 '本视频：`[6,0,3,3,6,7,2,7]` → `3`'],
        quote='只有当nums中第k小的数小于k，且第k + 1小的数大于k时，选中前k小的学生才是一个好的分组。',
        quote_src='—— yiduobo 题解原文',
        idea=['设选了 `k` 人：被选者的 `nums` 都 `< k`，没选者的都 `> k`',
              '排序后就是看 `nums[k-1] < k` 且 `nums[k] > k`',
              '`k = 0`（没有第 0 小）和 `k = n`（没有第 n+1 小）要单独判断'],
        result='运行结束，返回 `3`：选 1 个、4 个、全选',
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错：`k = 0` 看 `nums[0] > 0`，`k = n` 看 `nums[-1] < n`，别漏',
                 '循环 `k` 从 1 到 `n-1`，这样 `nums[k]` 不会越界',
                 '对比灵神：思路相同，灵神用 `pairwise` 把特判折进 `ans`，yiduobo 把两种特判单独写出来',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
