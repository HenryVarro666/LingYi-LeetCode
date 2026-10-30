def _txt(S):
    if 'now' not in S:
        return '`now` = 窗口里相等下标对的个数；`now >= k` 才是好子数组'
    n, right, left = len(S['nums']), S['right'], S.get('left')
    if left is None:
        return f"`now = {S['now']}`，`right = {right}`"
    ln = S['_line']
    if S['now'] >= S['k']:
        return f"`now = {S['now']} >= k = {S['k']}`：[{left}, {right - 1}] 已经是好子数组"
    return f"`now = {S['now']} < k = {S['k']}`：还不够，right 继续右移（`right = {right}`）"


CONFIG = dict(
    num=2537, title='统计好子数组的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑窗 · 枚举左端点找最小 right',
    tags=['灵神题单', '难度分 1892'],
    code='''
class Solution(object):
    def countGood(self, nums, k):

        n = len(nums)
        right = 0
        now = 0
        res = 0
        cnt = {}
        for left in range(n):
            while right < n and now < k:
                freq = cnt.get(nums[right], 0)
                now += freq
                cnt[nums[right]] = freq + 1
                right += 1

            if now < k:
                break
            
            res += n - right + 1

            now -= (cnt[nums[left]] - 1)
            cnt[nums[left]] -= 1
        
        return res
''',
    call='Solution().countGood([3,1,4,3,2,2,4], 2)',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（框 = 窗口 [left, right)，right 指向下一个要加入的数）', cell=100, h=250,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right - 1')),
        dict(type='map', var='cnt', label='cnt（窗口内每个数的出现次数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=34),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('now', 'now', 'orange'), ('k', 'k'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'right = 0': '`right`：窗口右边界（开区间），==只会往右走，不回头==',
        'now = 0': '`now`：窗口里值相等的下标对数',
        'res = 0': '`res` 累计好子数组个数',
        'cnt = {}': '`cnt` 哈希表：窗口里每个数出现几次',
        'for left in range(n)': '固定左端点 `left = {left}`：找最小的 `right`，使 `[left, right)` 是好子数组',
        'while right < n and now < k': lambda S, B, ret: (
            f'`now = {S.now} < k = {S.k}` 且 `right = {S.right} < n`：窗口还不好，继续加入 `nums[{S.right}] = {S.nums[S.right]}`'
            if S.right < S.n and S.now < S.k else
            (f'`now = {S.now} >= k`：已经是好子数组，right 停下' if S.now >= S.k else f'`right = {S.right}` 到头了，没法再扩')),
        'freq = cnt.get': '`{nums[right]}` 之前在窗口里出现了 `{freq}` 次',
        'now += freq': '新加入的 `{nums[right]}` 与这 `{freq}` 个各成一对 → `now = {now}`',
        'cnt[nums[right]] = freq + 1': '`cnt[{nums[right]}]` = `{freq + 1}`',
        'right += 1': '`right` 右移到 `{right}`',
        'if now < k': lambda S, B, ret: (f'`now = {S.now} < k = {S.k}`：加到头也凑不够，往后的左端点更不行 → ==直接 break==' if S.now < S.k
                                         else f'`now = {S.now} >= k = {S.k}`：这个左端点可以继续算'),
        'res += n - right + 1': '右边界取 `right-1 ~ n-1` 都是好子数组，共 `n - right + 1 = {n} - {right} + 1` = `{n - right + 1}` 个 → `res = {res}`',
        'now -= (cnt[nums[left]] - 1)': '左端点要右移，丢掉 `nums[{left}] = {nums[left]}`：它在窗口里有 `{cnt[nums[left]]}` 个，少了 `{cnt[nums[left]] - 1}` 对 → `now = {now}`',
        'cnt[nums[left]] -= 1': '`cnt[{nums[left]}]` 减一 → `{cnt[nums[left]]}`',
        'return res': '返回 `{res}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='每个左端点找最小 right，右边全部合法',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组里至少有 `k` 对下标 `(i, j)`，`i < j` 且 `arr[i] == arr[j]` 的子数组是==好子数组==',
                 '统计 `nums` 里好子数组的个数',
                 '示例：`nums = [3,1,4,3,2,2,4], k = 2` → `4`'],
        quote='对于数组中的任意位置left，不妨设right为最小的，且满足子数组[left, right)为好子数组的下标，那么对于所有以left为左边界的子数组，只要其右边界大于等于right - 1，这就是一个好子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举==左端点== left，找最小的 right，右边都合法，贡献 `n - right + 1` 个',
              'left 右移时 right 只会右移 → 变长滑窗',
              '新数 `x` 在窗口里已有 `c` 个，就新增 `c` 对；去掉一个 `x`，少 `c-1` 对'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`right` 是开区间，所以贡献是 `n - right + 1`（right-1 也算）',
                 '`now < k` 时直接 `break`：后面的左端点只会更短',
                 '对比灵神：灵神枚举右端点、`ans += left`；yiduobo 枚举左端点、`res += n - right + 1`'],
    ),
)
