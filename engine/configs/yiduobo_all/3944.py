def _in_calc(S):
    return 'index' in S and 's' in S and 'p' in S and 'q' in S


def _seg(S, i, v):
    if not _in_calc(S) or 't' not in S:
        return None
    if i < S['p']:
        return 'purple'
    if i < S['index']:
        return 'green'
    if i < S['q']:
        return 'orange'
    return 'pink'


def _cost(S):
    p, ix, q, t, k, n, s, nums = S['p'], S['index'], S['q'], S['t'], S['k'], S['n'], S['s'], S['nums']
    return (s[p] + (k - t) * p) + (t * (ix - p) - (s[ix] - s[p])) + (s[q] - s[ix] - t * (q - ix)) + ((n - q) * (k + t) - (s[-1] - s[q]))


def _txt(S):
    if _in_calc(S) and 't' in S:
        return f"目标 `t = {S['t']}`：四段 绕0降到t / 直接加到t / 直接减到t / 绕k升到t，总代价 `c = {_cost(S)}`"
    if 'et1' in S:
        return f"even：最优 `t={S['et1']}` 代价 {S['ec1']}；odd：最优 `t={S['ot1']}` 代价 {S['oc1']}"
    return ''


def _best(S):
    if _in_calc(S) and 'c1' in S:
        return f"当前最优 `t1={S['t1']}, c1={S['c1']}`；次优 `t2={S['t2']}, c2={S['c2']}`"
    return ''


CONFIG = dict(
    num=3944, title='使数组变为模交替数组的最少操作次数 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='按奇偶分组 + 枚举目标余数 + 排序前缀和三指针',
    tags=[],
    code='''
class Solution(object):
    def minOperations(self, nums, k):
        
        r = [v % k for v in nums]
        odd = []
        even = []
        for index, v in enumerate(r):
            if index % 2 == 0:
                even.append(v)
            else:
                odd.append(v)

        even.sort()
        odd.sort()

        def calc(nums):
            if not nums:
                return None, 0, None, None

            s = [0]
            for v in nums:
                s.append(s[-1] + v)

            n = len(nums)
            index = 0
            p = 0
            q = 0
            c1, t1, c2, t2 = None, None, None, None
            for t in range(k):
                while index < n and nums[index] <= t:
                    index += 1

                while p < index and t - nums[p] > nums[p] + k - t:
                    p += 1

                if q < index:
                    q = index
                while q < n and nums[q] - t < k - nums[q] + t:
                    q += 1

                c = s[p] + (k - t) * p
                c += t * (index - p) - (s[index] - s[p])
                c += s[q] - s[index] - t * (q - index)
                c += (n - q) * (k + t) - (s[-1] - s[q])

                if c1 is None or c < c1:
                    t1, c1, t2, c2 = t, c, t1, c1
                elif c2 is None or c < c2:
                    t2, c2 = t, c
            
            return t1, c1, t2, c2

        et1, ec1, et2, ec2 = calc(even)
        ot1, oc1, ot2, oc2 = calc(odd)

        if et1 != ot1:
            return ec1 + oc1
        
        return min(ec1 + oc2, ec2 + oc1)
''',
    call='Solution().minOperations([1, 4, 7, 10], 3)',
    expect=2,
    views=[
        dict(type='array', var='nums', h=240, label='nums（紫 = 绕 0 下降，绿 = 直接加，橙 = 直接减，粉 = 绕 k 上升）',
             pointers={'p': 'purple', 'index': 'green', 'q': 'orange'},
             color=_seg),
        dict(type='array', var='s', h=140, label='s（前缀和，s[0] = 0）'),
        dict(type='text', size=26, h=70, fn=_txt),
        dict(type='text', size=28, h=60, fn=_best),
    ],
    watch=['t', 'index', 'p', 'q', 'c', ('c1', 'c1', 'green'), ('c2', 'c2', 'cyan')],
    skip=['while index < n', 'if index % 2 == 0', 'if q < index', 'for index, v in enumerate(r)', 'index += 1', 'q += 1', 'p += 1', 'c += ', 'odd = []', 'even = []', 'if not nums', 'return None, 0', 'for v in nums', 's.append', 'c1, c2, t1, t2', 'n = len(nums)', 'index = 0', 'p = 0', 'q = 0'],
    max_steps=110,
    captions={
        'r = [v % k': '只关心模 k 的结果：`r = {r}`，下面按下标奇偶拆成两组',
        'for index, v in enumerate(r)': '按下标奇偶分到 `even` / `odd`',
        'if index % 2 == 0': '`index = {index}` 是{"偶" if index % 2 == 0 else "奇"}数下标',
        'odd.append': '`index = {index}` 是奇数下标 → 放进 `odd`',
        'even.append': '`index = {index}` 是偶数下标 → 放进 `even`',
        'even.sort()': '`even = {even}` 排好序，方便用三个单调指针',
        'odd.sort()': '`odd = {odd}` 也排好序',
        's = [0]': '先做前缀和 `s`（`s[0] = 0`），后面求任意一段的和',
        'for t in range(k)': lambda S, B, r: (f'枚举目标余数 `t = {S.t}`：把所有数在环上挪到 t 的最小代价' if B.get('t') != S.t else 'k 个目标余数都枚举完了'),
        'while index < n and nums[index] <= t': '`index`：前面 `{index}` 个数 ≤ t，它们直接加上去就能到 t',
        'while p < index and t - nums[p] > nums[p] + k - t': '`p`：前 `{p}` 个数绕 0 下降更划算（环形公路上走反方向更近）',
        'if q < index': '`q` 不能落在 `index` 前面',
        'while q < n and nums[q] - t < k - nums[q] + t': '`q = {q}`：它之前的数直接减到 t，之后的绕 k 上升更近',
        'c = s[p] + (k - t) * p': lambda S, B, r: f'`t = {S.t}`：分界 `p={S.p}`、`index={S.index}`、`q={S.q}` 分出四段，代价相加 `c` = =={_cost(S)}==',
        'if c1 is None or c < c1': lambda S, B, r: f'`c = {S.c}` 比最优 `c1 = {B.c1}` 小吗？→ {"==是，更新最优，原最优退为次优==" if (B.c1 is None or S.c < B.c1) else "不是"}',
        'elif c2 is None or c < c2': lambda S, B, r: f'`c = {S.c}` 比次优 `c2 = {B.c2}` 小吗？→ {"==是，更新次优==" if (B.c2 is None or S.c < B.c2) else "不是"}',
        't1, c1, t2, c2 = t, c, t1, c1': '最优 → `t1 = {t1}, c1 = {c1}`；旧最优降为次优 `t2 = {t2}, c2 = {c2}`',
        't2, c2 = t, c': '次优 → `t2 = {t2}, c2 = {c2}`',
        'return t1, c1, t2, c2': '这组的最优/次优：`t1={t1}, c1={c1}, t2={t2}, c2={c2}`',
        'et1, ec1, et2, ec2 = calc(even)': '对 even 求最优与次优目标',
        'ot1, oc1, ot2, oc2 = calc(odd)': '对 odd 求最优与次优目标',
        'if et1 != ot1': '`et1 = {et1}`，`ot1 = {ot1}`：{"==最优目标不同，两边都取最优==" if et1 != ot1 else "==最优目标相同，但题目要求 x ≠ y，必须有一边退到次优=="}',
        'return ec1 + oc1': '返回 `ec1 + oc1 = {ec1} + {oc1} = {ret}`',
        'return min(ec1 + oc2': '二选一：`ec1 + oc2 = {ec1 + oc2}`，`ec2 + oc1 = {ec2 + oc1}` → 取小 =={ret}==',
    },
    cards=dict(
        one_liner='奇偶下标各选一个目标余数，且两个目标不能相同',
        complexity='时间 `O(n log n + k)`，空间 `O(n)`',
        problem=['一步操作可以把 `nums` 里任一元素 `+1` 或 `-1`',
                 '要使偶数下标的 `nums[i] % k` 全等于 `x`、奇数下标的全等于 `y`，且 ==x ≠ y==',
                 '求最少操作次数；本视频：`nums=[1,4,7,10], k=3` → `2`'],
        quote='对于一条环形公路，上面有若干点，找出最优与次优的两个位置，使得所有点到这两个位置的距离之和最小/次小。',
        quote_src='—— yiduobo 题解原文',
        idea=['先对 `k` 取模，按奇偶下标分成 `even`、`odd`，各自排序',
              '枚举目标 `t`：数轴首尾相接成环，排序后分四段走最短路；分界 `p/index/q` 单调右移，前缀和 `O(1)` 算代价',
              '各记最优、次优：若两边最优 `t` 相同，就有一边退到次优'],
        summary=['时间 `O(n log n + k)`，空间 `O(n)`',
                 '易错点：==次优位置不一定落在已有的点上==，所以直接枚举 `t = 0..k-1`',
                 '`x ≠ y`：本例两组最优目标都是 1，必须一边退到次优（代价 2）',
                 '对比灵神：灵神只指向 3937 的方法二，未展开'],
    ),
)
