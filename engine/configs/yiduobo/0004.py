NUMS1, NUMS2 = [1, 4, 7, 9], [2, 3, 5, 6, 8, 10]


def _state(S):
    if 'k' not in S:
        return ''
    s = f"还要找第 k = =={S['k']}== 小（在没被舍去的数里）"
    if 'mid' in S and S['k'] > 1:
        s += f"   ·   mid = k // 2 = {S['k'] // 2}"
    if 'res' in S:
        s = f"第 k 小 res = =={S['res']}=="
    return s


def _p1(S):
    """nums1 side: the mid-th remaining number (hidden once res is known)"""
    return None if 'res' in S or 'mid' not in S else S['left1'] + S['mid'] - 1


def _p2(S):
    return None if 'res' in S or 'mid' not in S else S['left2'] + S['mid'] - 1


def _cmp(S, B, ret):
    i1, i2 = S.left1 + S.mid - 1, S.left2 + S.mid - 1
    x, y = S.nums1[i1], S.nums2[i2]
    if x < y:
        return f'`nums1[{i1}] = {x} < nums2[{i2}] = {y}`：nums1 这 {S.mid} 个数最极端也排不到第 k → ==全部舍去=='
    return f'`nums1[{i1}] = {x} ≥ nums2[{i2}] = {y}`：nums2 这 {S.mid} 个数排不到第 k → ==全部舍去=='


def _k1(S, B, ret):
    if S.k == 1:
        return '`k == 1`：第 1 小就是两个数组==当前第一个数==中较小的那个'
    return f'`k = {S.k}`：两个数组都没取空、k 也不是 1 → 进入 else，按 `mid = k // 2` 舍弃'


def _first(S, B, ret):
    x, y = S.nums1[S.left1], S.nums2[S.left2]
    if x > y:
        return f'`nums1[{S.left1}] = {x} > nums2[{S.left2}] = {y}` → 第 k 小是 `{y}`'
    return f'`nums1[{S.left1}] = {x} ≤ nums2[{S.left2}] = {y}` → 第 k 小是 `{x}`'


def _parity(S, B, ret):
    if (S.m + S.n) % 2 == 1:
        return f'`m + n = {S.m + S.n}` 是奇数 → 第 k 小就是中位数'
    return f'`m + n = {S.m + S.n}` 是偶数 → 还要第 k+1 小：==舍去前 k 小后，剩下数里最小的=='


CONFIG = dict(
    num=4, title='寻找两个正序数组的中位数', difficulty='Hard', category='二分查找',
    author='yiduobo', technique='求第 k 小 · 每次舍去 k/2 个数',
    code='''
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        m = len(nums1)
        n = len(nums2)
        k = (m + n + 1) // 2

        left1 = left2 = 0

        while True:
            if left1 == m:
                res = nums2[left2 + k - 1]
                left2 += k
                break
            elif left2 == n:
                res = nums1[left1 + k - 1]
                left1 += k
                break
            elif k == 1:
                if nums1[left1] > nums2[left2]:
                    res = nums2[left2]
                    left2 += 1
                    break
                else:
                    res = nums1[left1]
                    left1 += 1
                    break
            else:
                mid = k // 2
                if left1 + mid - 1 >= m:
                    left2 += mid
                elif left2 + mid - 1 >= n:
                    left1 += mid
                elif nums1[left1 + mid - 1] < nums2[left2 + mid - 1]:
                    left1 += mid
                else:
                    left2 += mid

                k -= mid

        if (m + n) % 2 == 1:
            return res * 1.0
        else:
            if left1 == m:
                return (res + nums2[left2]) * 0.5
            elif left2 == n:
                return (res + nums1[left1]) * 0.5
            else:
                return (res + min(nums1[left1], nums2[left2])) * 0.5
''',
    call=f'Solution().findMedianSortedArrays({NUMS1}, {NUMS2})',
    expect=5.5,
    views=[
        dict(type='text', fn=_state, size=27),
        dict(type='array', var='nums1', label='nums1', cell=100, h=230,
             pointers={'left1': 'blue', _p1: 'yellow'}, pointer_labels={_p1: '第 mid 个'},
             dim=lambda S, i, v: 'left1' in S and i < S['left1']),
        dict(type='array', var='nums2', label='nums2', cell=100, h=230,
             pointers={'left2': 'pink', _p2: 'yellow'}, pointer_labels={_p2: '第 mid 个'},
             dim=lambda S, i, v: 'left2' in S and i < S['left2']),
        dict(type='text', size=23, h=80, lines=2,
             text='灰色 = 已舍去（只移动左边界 `left1` / `left2`）\n黄箭头 = 两边各自剩余部分的第 mid 个数'),
    ],
    watch=[('k', 'k', 'yellow'), ('mid', 'mid'), ('left1', 'left1', 'blue'), ('left2', 'left2', 'pink'),
           ('res', 'res', 'green')],
    skip=['n = len(nums2)', 'while True', 'if left1 == m:', 'elif left2 == n:',
          'if left1 + mid - 1 >= m', 'elif left2 + mid - 1 >= n'],
    captions={
        3: '`m = {m}`，`n = {len(nums2)}`',
        5: lambda S, B, ret: f'`k = (m + n + 1) // 2 = {S.k}`：先求两个数组中==第 {S.k} 小==的数',
        7: '`left1 = left2 = 0`：用左边界表示==舍去了靠前的元素==，不用每次修改数组',
        18: _k1,
        19: _first,
        20: '`res = nums2[left2] = {res}`',
        21: '`left2 += 1` → `{left2}`：把它也舍去，剩下的最小值就是第 k+1 小',
        22: '`break`：第 k 小已求出',
        24: '`res = nums1[left1] = {res}`',
        25: '`left1 += 1` → `{left1}`：把它也舍去，剩下的最小值就是第 k+1 小',
        26: '`break`：第 k 小已求出',
        28: lambda S, B, ret: (f'`mid = k // 2 = {S.mid}`：两边剩余都够 {S.mid} 个（不是情况 4、5）→ 情况 6，比较两边的第 mid 个'
                               if S.left1 + S.mid - 1 < S.m and S.left2 + S.mid - 1 < S.n
                               else f'`mid = k // 2 = {S.mid}`：有一边剩余不足 {S.mid} 个 → 情况 4 / 5'),
        33: _cmp,
        34: '`left1 += mid` → `{left1}`：舍去 nums1 前面这 {mid} 个',
        36: '`left2 += mid` → `{left2}`：舍去 nums2 前面这 {mid} 个',
        38: '`k -= mid` → `k = {k}`：只需在剩下的数里找第 {k} 小，==规模减半==',
        40: _parity,
        41: '返回 `{ret}`',
        44: '`nums1` 已取空 → 第 k+1 小是 `nums2[left2]`，返回 `{ret}`',
        46: '`nums2` 已取空 → 第 k+1 小是 `nums1[left1]`，返回 `{ret}`',
        48: '第 k+1 小 = `min({nums1[left1]}, {nums2[left2]})`，中位数 = `({res} + 第 k+1 小) * 0.5` = =={ret}==',
    },
    cards=dict(
        one_liner='求第 k 小：每次比较两边第 k/2 个数，舍去较小那边的前 k/2 个',
        complexity='时间 `O(log(m + n))`，空间 `O(1)`',
        problem=['两个正序数组 `nums1`（长 m）和 `nums2`（长 n），返回合并后的==中位数==；要求 `O(log(m+n))`',
                 '示例：`[1,3]`, `[2]` → `2.0`；`[1,2]`, `[3,4]` → `2.5`'],
        before=[dict(heading='yiduobo 的六种情况（mid = k / 2）', lines=[
            '1、2：某个数组已取空 → 直接取另一个数组的第 k 个',
            '3：`k = 1` → 比较两个数组的第一个数',
            '4、5：某个数组剩余不足 mid 个 → 舍去另一个数组的前 mid 个',
            '6：比较两边第 mid 个数，==舍去较小那边的前 mid 个==，k 变成 `k − mid`'])],
        quote='若a[mid] < b[mid]……a[mid]不符合要求，==自然a[0]到a[mid]都不符合要求==。此时，我们舍去a[0]到a[mid]，得到newa，然后从newa和b中找第k - mid小的即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['令 `k = (m + n + 1) / 2`：m + n 为奇数求第 k 小，为偶数再求第 k + 1 小',
              '每次舍去的都是靠前的元素 → ==维护左边界== `left1 / left2` 即可',
              '第 k + 1 小：舍去前 k 小后，从 newa 和 newb 里再找最小的数'],
        result='返回 `5.5`：第 5 小是 5，第 6 小是 6 ✓',
        summary=['每轮 k 减半：时间 `O(log(m + n))`，空间 `O(1)`',
                 '原文为 Python 2 写法：`k` 和 `mid` 的整数除法 `/` 已改为 `//`，删去了 `"""type"""` 文档字符串',
                 '下标从 0 开始：剩余部分的第 mid 个数是 `left + mid - 1`',
                 '先判“取空”和 `k == 1`，再判“不足 mid 个”，顺序不能乱',
                 '对比灵神：他二分“第一组”的分割点，`O(log min(m, n))`'],
    ),
)
