CONFIG = dict(
    num=2488, title='统计中位数为 K 的子数组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='从 k 向两侧计数，两个哈希表配对',
    tags=['灵神题单·常用数据结构', '难度分 1999'],
    code='''
class Solution(object):
    def countSubarrays(self, nums, k):

        p = None
        for index, num in enumerate(nums):
            if num == k:
                p = index
                break
        
        left_cnt = {0 : 1}
        now = 0
        for index in range(p - 1, -1, -1):
            if nums[index] < k:
                now -= 1
            else:
                now += 1
            left_cnt[now] = left_cnt.get(now, 0) + 1
        
        right_cnt = {0 : 1}
        now = 0
        for index in range(p + 1, len(nums)):
            if nums[index] < k:
                now -= 1
            else:
                now += 1
            right_cnt[now] = right_cnt.get(now, 0) + 1

        res = left_cnt.get(0, 0) * right_cnt.get(0, 0)
        for cnt in left_cnt:
            if cnt > 0:
                res += left_cnt[cnt] * (right_cnt.get(-cnt, 0) + right_cnt.get(1 - cnt, 0))
        
        for cnt in right_cnt:
            if cnt > 0:
                res += right_cnt[cnt] * (left_cnt.get(-cnt, 0) + left_cnt.get(1 - cnt, 0))
        
        return res
''',
    call='Solution().countSubarrays([3,2,1,4,5], 4)',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（绿 = k 的位置 p；箭头 index = 当前扫描位置）', h=190,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if v == S['k'] else ('pink' if v < S['k'] else 'cyan')),
        dict(type='map', var='left_cnt', label='left_cnt：从 p 向左，“大于 − 小于”的差 → 次数', fmt=lambda kk, v: f'{kk}: {v}', h=150, font=30),
        dict(type='map', var='right_cnt', label='right_cnt：从 p 向右，差 → 次数', fmt=lambda kk, v: f'{kk}: {v}', h=150, font=30),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"累加答案：`res = {S['res']}`" if 'res' in S else (f"`now = {S['now']}`" if 'now' in S else ''))),
    ],
    watch=['p', 'now', 'cnt', ('res', 'res', 'green')],
    captions={
        'p = None': '`p` 记 `k` 的下标：合法子数组必须包含它',
        'p = index': '找到 `k = {k}`，`p = {p}`',
        'left_cnt = {0': '`left_cnt[d]`：从 p 向左延伸，“大于 k 的个数 − 小于 k 的个数”等于 d 的方案数；不延伸（d=0）算 1 种',
        'right_cnt = {0': '右边同理，`right_cnt` 也从 `{{0: 1}}` 开始',
        'now -= 1': '`nums[{index}] = {nums[index]}` 比 `k` 小 → `now = {now}`',
        'now += 1': '`nums[{index}] = {nums[index]}` 比 `k` 大 → `now = {now}`',
        'left_cnt[now] =': '左边差为 `{now}` 的方案数记为 `{left_cnt[now]}`',
        'right_cnt[now] =': '右边差为 `{now}` 的方案数记为 `{right_cnt[now]}`',
        'res = left_cnt.get(0': '左右都不延伸或差都为 0：`left[0] × right[0]` = =={res}==，对应 `[4]`',
        'res += left_cnt[cnt]': '左差 `{cnt}`，右边需要差 `{-cnt}`（奇数长）或 `{1-cnt}`（偶数长）→ `res = {res}`',
        'res += right_cnt[cnt]': '右差 `{cnt}`，左边需要差 `{-cnt}` 或 `{1-cnt}` → `res = {res}`',
        'return res': '一共 =={res}== 个',
    },
    cards=dict(
        one_liner='从 k 往两边各数一次，再让两边的差互补',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组是不重复的 1 到 n，求中位数等于 `k` 的子数组个数',
                 '偶数长度时取中间靠左的数',
                 '示例：`[3,2,1,4,5]`，`k=4` → 3'],
        quote='子数组中必须包含数字K。如果存在另一个以p为左边界，且比K小的数字的数量与比K大的数字的数量之差为-cnt或者-cnt + 1的子数组，这两个子数组拼起来就可以得到一个中位数为K的子数组。',
        quote_src='—— yiduobo 题解',
        idea=['中位数是 k → 子数组一定包含位置 `p`，大于 k 的个数比小于 k 的多 0 或 1',
              '从 `p` 向左、向右各扫一遍，记录“大 − 小”的差及次数',
              '左差 d 配右差 `−d`（奇数长）或 `1−d`（偶数长），乘起来累加'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：差为 0 的情况要单独算 `left[0] × right[0]`',
                 '易错点：只枚举 `cnt > 0` 的一侧，避免同一组合重复算',
                 '代码里 `now` 在 `< k` 以外都 `+1`，因为数不重复且遍历时不含 k 本身',
                 '同类：560 和为 K 的子数组'],
        after=[],
    ),
)
