def _c1(S, k, v):
    if 'p1' not in S:
        return None
    return 'green' if k < S['p1'] else None


def _c2(S, k, v):
    if 'p2' not in S:
        return None
    return 'green' if k < S['p2'] else None


CONFIG = dict(
    num=1537, title='最大得分', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='双指针 · 类似二路归并',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def maxSum(self, nums1, nums2):

        n1 = len(nums1)
        n2 = len(nums2)
        p1 = p2 = 0
        s1 = s2 = 0
        cnt1 = cnt2 = 0
        res = 0
        mod = 10 ** 9 + 7
        while p1 < n1 and p2 < n2:
            if nums1[p1] == nums2[p2]:
                res += nums1[p1]
                if res >= mod:
                    res -= mod
                p1 += 1
                p2 += 1
                if cnt1 > cnt2 or (cnt1 == cnt2 and s1 > s2):
                    res += s1
                else:
                    res += s2
                
                if res >= mod:
                    res -= mod

                s1 = s2 = 0
                cnt1 = cnt2 = 0

            elif nums1[p1] < nums2[p2]:
                s1 += nums1[p1]
                p1 += 1
                if s1 >= mod:
                    cnt1 += 1
                    s1 -= mod
            else:
                s2 += nums2[p2]
                p2 += 1
                if s2 >= mod:
                    cnt2 += 1
                    s2 -= mod
                    
        while p1 < n1:
            s1 += nums1[p1]
            p1 += 1
            if s1 >= mod:
                cnt1 += 1
                s1 -= mod

        while p2 < n2:
            s2 += nums2[p2]
            p2 += 1
            if s2 >= mod:
                cnt2 += 1
                s2 -= mod

        if cnt1 > cnt2 or (cnt1 == cnt2 and s1 > s2):
            res += s1
        else:
            res += s2
        
        if res >= mod:
            res -= mod

        return res
''',
    call='Solution().maxSum([2, 4, 5, 8, 10], [4, 6, 8, 9])',
    expect=30,
    skip=['res -= mod', 'cnt1 = cnt2 = 0', 's1 = s2 = 0', 'n1 = len', 'n2 = len', 'mod = 10', 'if res >= mod', 'if s1 >= mod', 'if s2 >= mod', 'cnt1 += 1', 'cnt2 += 1', 's1 -= mod', 's2 -= mod'],
    views=[
        dict(type='array', var='nums1', label='nums1（蓝 = p1，绿 = 已走过）', h=210, cell=84, pointers={'p1': 'blue'}, color=_c1),
        dict(type='array', var='nums2', label='nums2（粉 = p2，绿 = 已走过）', h=210, cell=84, pointers={'p2': 'pink'}, color=_c2),
        dict(type='text', h=80, size=26, fn=lambda S: (
            f"本段累加：`s1` = =={S['s1']}==　`s2` = =={S['s2']}==　已结算 `res` = =={S['res']}==" if 's1' in S and 'res' in S else '两个有序数组，相同的值是「换路口」')),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), ('s1', 's1', 'blue'), ('s2', 's2', 'pink'), ('res', 'res', 'green')],
    captions={
        'p1 = p2 = 0': '两个指针从两个数组头部出发，像二路归并',
        's1 = s2 = 0': '`s1`、`s2`：两条路在当前路口之间各自的累加和',
        'cnt1 = cnt2 = 0': '`cnt` 记录累加和超过 `mod` 的次数：取模会破坏大小比较，所以要单独记',
        'while p1 < n1 and p2': lambda S, B, r: (f'`p1 = {S.p1}`，`p2 = {S.p2}` 都没到头 → 继续归并' if S.p1 < S.n1 and S.p2 < S.n2 else '有一个数组走完了 → 退出，处理另一个数组剩下的部分'),
        'if nums1[p1] == nums2[p2]': lambda S, B, r: (f'`{S.nums1[S.p1]} == {S.nums2[S.p2]}` → 相同值，==是换路口==' if S.nums1[S.p1] == S.nums2[S.p2]
                                                      else f'`{S.nums1[S.p1]} ≠ {S.nums2[S.p2]}` → 还没到路口，先走较小的那边'),
        'res += nums1[p1]': '路口的值本身只算一次：`res = {res}`',
        'p1 += 1': '`p1` → {p1}',
        'p2 += 1': '`p2` → {p2}',
        'if cnt1 > cnt2': lambda S, B, r: (f'两段中取累加和大的：`s1 = {S.s1}` 与 `s2 = {S.s2}`，选 =={"s1" if (S.cnt1 > S.cnt2 or (S.cnt1 == S.cnt2 and S.s1 > S.s2)) else "s2"}==（cnt 大的一定更大，一样再比 s）'),
        'res += s1': '选 `s1` 这一段：`res = {res}`',
        'res += s2': '选 `s2` 这一段：`res = {res}`',
        'elif nums1[p1] < nums2[p2]': lambda S, B, r: (f'`{S.nums1[S.p1]} < {S.nums2[S.p2]}`：`nums1` 这边更小 → 不可能是路口，先累加进 `s1`' if S.nums1[S.p1] < S.nums2[S.p2]
                                                       else f'`{S.nums1[S.p1]} > {S.nums2[S.p2]}`：`nums2` 这边更小 → 先累加进 `s2`'),
        's1 += nums1[p1]': '`s1 += {B.nums1[B.p1]}` → `s1 = {s1}`',
        's2 += nums2[p2]': '`s2 += {B.nums2[B.p2]}` → `s2 = {s2}`',
        'while p1 < n1:': lambda S, B, r: ('`nums2` 已走完，`nums1` 剩下的部分继续累加进 `s1`' if S.p1 < S.n1 else '`nums1` 也没有剩余了'),
        'while p2 < n2:': lambda S, B, r: ('`nums1` 已走完，`nums2` 剩下的部分继续累加进 `s2`' if S.p2 < S.n2 else '`nums2` 也没有剩余了'),
        'return res': '最大得分 =={ret}==',
    },
    cards=dict(
        one_liner='相同值是换路口：每两个路口之间，只走累加和更大的那一边',
        complexity='时间 `O(n1 + n2)`，空间 `O(1)`',
        problem=['两个严格递增数组 `nums1`、`nums2`，从任一个的开头走到结尾',
                 '走到两数组都有的值时，可以换到另一个数组继续走',
                 '得分 = 路径上所有不同值之和，求最大得分（对 `1e9+7` 取模）',
                 '本视频：`[2,4,5,8,10]` 与 `[4,6,8,9]` → `30`'],
        quote='按同值节点对数组进行划分，就得到若干互不相关的子数组，对于每一段子数组，则只需要选择其中和较大的那一侧。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个有序数组 → 用两个指针像二路归并，每次累加较小的一侧',
              '遇到相同值：把 `s1`、`s2` 中较大的加进答案，再把路口的值也加上，清零继续',
              '结尾剩下的部分同样取较大的一侧'],
        summary=['时间 `O(n1 + n2)`，空间 `O(1)`',
                 '易错：累加和对 `mod` 取模后不能直接比大小，所以用 `cnt1`、`cnt2` 记录取模次数',
                 '易错：相同的值只能算一次',
                 '原文中的代码在 Python 3 下可直接运行，未做修改；视频里为了简洁，取模相关的分支不单独讲'],
    ),
)
