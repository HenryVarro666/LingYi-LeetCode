def _cur(S):
    if 'diff' not in S or 'num' not in S:
        return '先求原来的绝对差值和，再找「换掉一个数能少多少」'
    ms = S['sorted_nums1']
    p = S['p']
    mc = S['max_change']
    return f'当前 `nums2` 值 `{S["num"]}`，原差值 `diff = {S["diff"]}`；目前最大可减少 `max_change = ` =={mc}=='


CONFIG = dict(
    num=1818, title='绝对差值和', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='排序去重 + 双指针找最接近的数',
    tags=['灵神题单·二分算法'],
    code='''
class Solution(object):
    def minAbsoluteSumDiff(self, nums1, nums2):

        p = 0
        n = len(nums1)
        res = 0
        mod = 10 ** 9 + 7
        for index in range(n):
            res += abs(nums1[index] - nums2[index])
            if res >= mod:
                res -= mod
        
        max_change = 0
        sorted_nums1 = sorted(list(set(nums1)))
        for num, diff in sorted(zip(nums2, [abs(nums1[index] - nums2[index]) for index in range(n)])):
            if num <= sorted_nums1[0]:
                if abs(sorted_nums1[0] - num) < diff:
                    max_change = max(max_change, diff - abs(sorted_nums1[0] - num))
            elif num > sorted_nums1[-1]:
                if abs(sorted_nums1[-1] - num) < diff:
                    max_change = max(max_change, diff - abs(sorted_nums1[-1] - num))
            else:
                while p < len(sorted_nums1) and sorted_nums1[p] <= num:
                    p += 1
                if p < len(sorted_nums1) and abs(sorted_nums1[p] - num) < diff:
                    max_change = max(max_change, diff - abs(sorted_nums1[p] - num))
                if p > 0 and abs(sorted_nums1[p - 1] - num) < diff:
                    max_change = max(max_change, diff - abs(sorted_nums1[p - 1] - num))
        
        res = res - max_change
        if res < 0:
            res += mod

        return res
''',
    call='Solution().minAbsoluteSumDiff([1, 10, 4, 4], [9, 3, 5, 1])',
    expect=12,
    skip=['n = len(nums1)', 'mod = 10 ** 9 + 7', 8, 10, 31],
    max_steps=90,
    views=[
        dict(type='array', var='nums1', label='nums1（可以把其中一个数换成 nums1 里的另一个数）', cell=80, h=170),
        dict(type='array', var='nums2', label='nums2（黄 = 正在处理的位置）', cell=80, h=170,
             color=lambda S, i, v: 'yellow' if S.get('num') == v and 'diff' in S else None),
        dict(type='array', var='sorted_nums1', label='sorted_nums1（排序去重；p 指向第一个 > num 的数）', cell=80, h=190,
             pointers={'p': 'blue'},
             color=lambda S, i, v: 'green' if S.get('p') is not None and 'diff' in S and i == S['p'] - 1 and S.get('num') is not None and i >= 0 and False else None),
        dict(type='text', h=80, size=28, fn=_cur),
    ],
    watch=[('res', 'res', 'blue'), 'num', 'diff', 'p', ('max_change', 'max_change', 'green')],
    captions={
        'p = 0': '`p` 是 `sorted_nums1` 上的指针，只会往右走',
        'res = 0': '`res` 先累计原来的绝对差值和',
        9: '`res` += `|{nums1[index]} − {nums2[index]}|` → {res}',
        'max_change = 0': '`max_change`：换掉某一位后，总和最多能减少多少',
        'sorted_nums1 = sorted(list(set(nums1)))': '换的数只能来自 `nums1`：排序去重得 `{sorted_nums1}`',
        'for num, diff in sorted(zip': lambda S, B, ret: (
            '所有位置都处理完，循环结束' if 'num' in B and S.num == B.num and S.diff == B.diff else
            '把每一位的 `(nums2[i], 原差值)` 按 `nums2` 排序：要找的邻居也单调，`p` 只右移。当前 `({}, {})`'.format(S.num, S.diff)),
        'if num <= sorted_nums1[0]': lambda S, B, ret: (
            '`{} <= {}`（最小的数）：只能换成最小的数'.format(S.num, S.sorted_nums1[0]) if S.num <= S.sorted_nums1[0]
            else '`{} > {}`：不比最小的数小，看下一种情况'.format(S.num, S.sorted_nums1[0])),
        'elif num > sorted_nums1[-1]': lambda S, B, ret: (
            '`{} > {}`（最大的数）：只能换成最大的数'.format(S.num, S.sorted_nums1[-1]) if S.num > S.sorted_nums1[-1]
            else '`num` 落在中间，需要找左右两个邻居'),
        'while p < len(sorted_nums1) and sorted_nums1[p] <= num': lambda S, B, ret: (
            '`sorted_nums1[{}] = {} <= {}`：还不大于 num → `p` 右移'.format(S.p, S.sorted_nums1[S.p], S.num)
            if S.p < len(S.sorted_nums1) and S.sorted_nums1[S.p] <= S.num else
            ('`p = {}`：`sorted_nums1[p]` 是第一个 `> {}` 的数'.format(S.p, S.num) if S.p < len(S.sorted_nums1) else '`p` 越过末尾，右邻居不存在')),
        'p += 1': '`p` → {p}',
        'if p < len(sorted_nums1) and abs': lambda S, B, ret: (
            '右邻居 `{}`：`|{} − {}| = {}`，比 `diff = {}` {}'.format(
                S.sorted_nums1[S.p], S.sorted_nums1[S.p], S.num, abs(S.sorted_nums1[S.p] - S.num), S.diff,
                '小 → 值得换' if abs(S.sorted_nums1[S.p] - S.num) < S.diff else '不小 → 不换')
            if S.p < len(S.sorted_nums1) else '没有右邻居（`p` 越界）：跳过'),
        'if p > 0 and abs': lambda S, B, ret: (
            '左邻居 `{}`：`|{} − {}| = {}`，比 `diff = {}` {}'.format(
                S.sorted_nums1[S.p - 1], S.sorted_nums1[S.p - 1], S.num, abs(S.sorted_nums1[S.p - 1] - S.num), S.diff,
                '小 → 值得换' if abs(S.sorted_nums1[S.p - 1] - S.num) < S.diff else '不小 → 不换')
            if S.p > 0 else '没有左邻居（`p = 0`）：跳过'),
        'if abs(sorted_nums1[0] - num) < diff': '换成最小的数后差值 `{abs(sorted_nums1[0] - num)}`，原差值 `{diff}`',
        'if abs(sorted_nums1[-1] - num) < diff': '换成最大的数后差值 `{abs(sorted_nums1[-1] - num)}`，原差值 `{diff}`',
        'max_change = max': '`max_change = max({B.max_change}, 减少量)` = =={max_change}==',
        'res = res - max_change': '总和减去最大的减少量：`res` = `{B.res} − {max_change}` = =={res}==',
        'return res': '最小绝对差值和 `{ret}`',
    },
    cards=dict(
        one_liner='先求原总和，再找换掉哪一位能减得最多',
        complexity='时间 `O(n log n)`（排序），空间 `O(n)`',
        problem=['两个正整数数组 `nums1`、`nums2`，绝对差值和为 `sum(|nums1[i] − nums2[i]|)`',
                 '可以把 `nums1` 中==至多一个==元素替换成 `nums1` 中的任意元素，求最小的绝对差值和（对 `10^9+7` 取模）',
                 '本视频：`[1,10,4,4]`、`[9,3,5,1]` → `12`'],
        quote='设这个变换的位置为index，变换的目标为p，那么最终就是要求abs(nums1[index] - nums2[index]) - abs(nums1[p] - nums2[index])最大。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举换哪一位 `index`：要让新差值 `|nums1[p] − nums2[index]|` 尽量小 → `nums1[p]` 要最接近 `nums2[index]`',
              '`nums1` 排序后，最接近的数只可能是 `nums2[index]` 左右两个邻居',
              '把 `nums2` 连同差值一起排序，邻居位置单调不减，用双指针 `p` 代替二分'],
        summary=['最终答案 = 原总和 − 最大减少量 `max_change`',
                 '易错边界：`num` 不大于最小数，或大于最大数时，只有一个候选',
                 '只有新差值严格小于原差值才值得换，所以要判 `< diff`',
                 '原文用「排序 + 双指针」；也可以不排序 `nums2`，直接对每个 `nums2[i]` 二分',
                 '原文本身是 Python 3 可运行的写法，未做修改；题面库里没有，题意按 LeetCode 原题补写'],
    ),
)
