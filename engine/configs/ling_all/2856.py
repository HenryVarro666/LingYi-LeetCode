CONFIG = dict(
    num=2856, title='删除数对后的最小数组长度', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='众数 + 二分',
    tags=['灵神题单', '难度分 1750'],
    code='''
class Solution:
    def minLengthAfterRemovals(self, nums: List[int]) -> int:
        n = len(nums)
        x = nums[n // 2]
        max_cnt = bisect_right(nums, x) - bisect_left(nums, x)
        return max(max_cnt * 2 - n, n % 2)
''',
    call='Solution().minLengthAfterRemovals([1,2,2,2,2,3])',
    expect=2,
    views=[
        dict(type='text', size=30, fn=lambda S: (f"众数 `x = {S['x']}`，出现 `{S['max_cnt']}` 次" if 'max_cnt' in S else
                                                 f"有序数组：众数若过半，必定在中间 `nums[{S['n']//2}] = {S['x']}`" if 'x' in S else '')),
        dict(type='array', var='nums', label='nums（非递减）', h=260,
             pointers={'n // 2': 'blue'},
             color=lambda S, i, v: 'orange' if 'x' in S and v == S['x'] else None),
        dict(type='text', size=30, fn=lambda S: (
            f"`max_cnt*2 - n = {S['max_cnt']*2 - S['n']}`   `n % 2 = {S['n']%2}`   取较大者" if 'max_cnt' in S else '')),
    ],
    watch=['n', ('x', 'x', 'orange'), ('max_cnt', 'max_cnt', 'green')],
    captions={
        'n = len': '数组长度 `n = {n}`',
        'x = nums': '有序数组里，出现次数超过一半的数必定盖住中点 → 候选众数 `x = nums[{n // 2}] = {x}`',
        'max_cnt =': '二分找 `x` 的左右边界：`bisect_right - bisect_left` = `max_cnt` = {max_cnt}',
        'return max': lambda S, B, r: (f'`max_cnt*2 > n`（{S.max_cnt*2} > {S.n}）：其余 {S.n-S.max_cnt} 个数全和 x 消除，还剩 `{S.max_cnt*2-S.n}` 个 x → 答案 =={r}=='
                                       if S.max_cnt*2 > S.n else f'`max_cnt*2 <= n`：能配完，剩 `n % 2 = {S.n%2}` → 答案 =={r}=='),
    },
    cards=dict(
        one_liner='只看出现最多的数：它能消掉多少，剩下多少',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['非递减数组，每次选 `nums[i] < nums[j]` 两个数删掉',
                 '求任意次操作后数组最短长度',
                 '示例：`[2,3,4,4,4]` → `1`；本视频 `[1,2,2,2,2,3]` → `2`'],
        quote='如果 maxCnt·2 > n，其余所有 n-maxCnt 个数都要与 x 消除，所以最后剩下 maxCnt·2 - n 个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设出现最多的数 `x` 出现 `maxCnt` 次：`maxCnt*2 > n` 时剩 `maxCnt*2 - n` 个',
              '否则 n 为偶数剩 0，奇数剩 1',
              '数组有序，若 x 过半则必在 `nums[n//2]`，两次二分就得 `maxCnt`'],
        after=[dict(heading='为什么二分够了', lines=['只有过半的众数才可能让答案大于 1', '过半的数一定覆盖下标 `n // 2`', '不过半时，`max_cnt*2 - n` 为负，答案取 `n % 2`，所以拿错候选也不影响'])],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '`bisect_right - bisect_left` 就是 `x` 的出现次数',
                 '易错点：别忘了 `n % 2`，两两配完后可能剩 1 个',
                 '也可以遍历一遍统计最大频次，`O(n)`，答案公式相同'],
    ),
)
