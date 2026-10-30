def _info(S):
    if 'diff' not in S:
        return ''
    t = f"假设剩下的最小值是 `nums1` 里的某个 `v`：`diff = nums2[0] − v = {S['diff']}`"
    if 'x' in S and 'p' in S and S['p'] < len(S['nums1']):
        t += f"；比较 `{S['x']} − nums1[{S['p']}] = {S['x'] - S['nums1'][S['p']]}` 与 `diff = {S['diff']}`"
    return t


def _while(S, B, ret):
    if S.p >= len(S.nums1):
        return f'`p = {S.p}` 已走出 `nums1`：没有数能配上 `{S.x}` → 这个 diff 行不通'
    d = S.x - S.nums1[S.p]
    if d != S.diff:
        return f'`{S.x} − nums1[{S.p}] = {d}` ≠ `diff = {S.diff}` → 这个数当作被删掉，`p` 右移'
    return f'`{S.x} − nums1[{S.p}] = {d}` == `diff` → ==配上了=='


CONFIG = dict(
    num=3132, title='找出与数组相加的整数 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='三种最小值 + 贪心判子序列',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1620'],
    code='''
class Solution(object):
    def minimumAddedInteger(self, nums1, nums2):

        nums1.sort()
        nums2.sort()
        res = None
        for p, v in enumerate(nums1[:3]):
            diff = nums2[0] - v
            flag = True
            for x in nums2:
                while p < len(nums1) and x - nums1[p] != diff:
                    p += 1
                if p == len(nums1):
                    flag = False
                    break
                
                p += 1
            
            if flag and (res is None or res > diff):
                res = diff
        
        return res
''',
    call='Solution().minimumAddedInteger([2,5,6,7,8,10], [3,4,5,8])',
    expect=-2,
    views=[
        dict(type='array', var='nums1', label='nums1（已排序）', pointers={'p': 'blue'}, h=250,
             dim=lambda S, i, v: 'p' in S and 'x' in S and i < S['p']),
        dict(type='array', var='nums2', label='nums2（已排序，x 为当前要配的数）', h=210,
             color=lambda S, i, v: 'yellow' if 'x' in S and v == S['x'] else None),
        dict(type='text', fn=_info, size=26, h=130),
    ],
    watch=[('p', 'p', 'blue'), ('diff', 'diff', 'orange'), ('x', 'x', 'yellow'), ('flag', 'flag', 'purple'), ('res', 'res', 'green')],
    captions={
        'nums1.sort()': '先排序：每个数加同一个 x 不改变顺序',
        'nums2.sort()': '`nums2` 也排序，之后只需要一趟贪心匹配',
        'res = None': '`res` 记录目前可行的最小 `diff`',
        'for p, v in enumerate': lambda S, B, r: ('前三小都试完了' if B.get('v') == S.v else f'删除后 `nums1` 的最小值只可能是前三小之一：试 `v = {S.v}`（原下标 {S.p}）'),
        'diff = nums2[0]': '剩下的最小值 `{v}` 对应 `nums2[0] = {nums2[0]}` → `diff = {diff}`',
        'for x in nums2': lambda S, B, r: ('`nums2` 每个数都配上了伙伴 → 这个 `diff` ==可行==' if B.get('x') == S.x == S.nums2[-1] else f'依次给 `nums2` 的每个数 `x = {S.x}` 在 `nums1` 里找伙伴'),
        'while p < len': _while,
        'p += 1': lambda S, B, r: (f'`p` → {S.p}', f'`p` → {S.p}')[0],
        'if p == len(nums1)': lambda S, B, r: (f'`p == len(nums1)`：`{S.x}` 没找到伙伴 → `diff = {S.diff}` ==不可行==' if S.p == len(S.nums1)
                                               else f'`p = {S.p} < {len(S.nums1)}`：找到了 `nums1[{S.p}]`'),
        'flag = False': '`flag = False`，放弃这个 `diff`',
        'if flag and': lambda S, B, r: (f'`flag = {S.flag}`，`res = {S.res}`，`diff = {S.diff}` → '
                                         + ('==更新答案==' if S.flag and (S.res is None or S.res > S.diff) else '不更新')),
        'res = diff': '`res = diff = {res}`',
        'return res': '三种情况都试完，最小的可行 `x` 是 ==`{res}`==',
    },
    cards=dict(
        one_liner='删完后的最小值只有三种可能，逐个试一遍',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`nums1` 比 `nums2` 多两个数：删掉两个数，其余每个数加上同一个 `x`，要和 `nums2` 相等',
                 '返回最小的 `x`',
                 '视频示例：`[2,5,6,7,8,10]`、`[3,4,5,8]` → `-2`'],
        quote='那么在这里就只需要分别检测这三种情况，对于每种情况，先计算出对应的x，然后将nums1中的所有元素都减去x，再检测nums2是否为nums1的子序列即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['确定删除后剩下的最小值，`x` 就等于 `nums2` 最小值减去它',
              '剩下最小值要么是原最小、次小、第三小：只有三种 `diff`',
              '对每个 `diff`：排序后一趟扫描，尽量匹配，匹配不上就说明不可行',
              '三个都试，取最小的可行 `diff`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`for p, v in enumerate(...)` 里的 `p` 被内层当作指针改写，每轮从该 `v` 的下标开始匹配',
                 '与灵神不同：不倒着枚举提前返回，而是三种都试、取最小的 `diff`',
                 '原文为 Python 2 写法，本题无需改动，可直接在 Python 3 运行'],
    ),
    skip=['flag = True', 'break'],
    max_steps=90,
)
