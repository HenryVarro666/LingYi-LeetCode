PENDING = (7, 8, 10, 11)  # 已经填了 nums1[p]，但 p 还没减一的那几行


def _filled(S, i):
    return i > S['p'] or (S.get('_line') in PENDING and i == S['p'])


def _slot_dim(S, i, v):
    # p1 < i <= p 是“空位”：里面的旧值已经没用了，可以随便覆盖
    return 'p' in S and S['p1'] < i <= S['p'] and not _filled(S, i)


def _slot_color(S, i, v):
    if 'p' in S and _filled(S, i):
        return 'green'
    return None


def _gap(S):
    if 'p' not in S:
        return ''
    holes = S['p'] - S['p1']
    if S.get('_line') in (7, 8):
        return '搬走 nums1 的一个数：==它原来的位置变成新空位==，空位数不变'
    if S.get('_line') in (10, 11):
        return '填入 nums2 的一个数：空位 −1，nums2 剩余也 −1'
    if S['p2'] < 0:
        return f"`p2 = -1`：nums2 填完了，剩下的 `nums1[0..{S['p1']}]` ==本来就在正确位置=="
    return f"空位个数 `p − p1 = {holes}` ==始终等于== nums2 剩余个数 `p2 + 1 = {S['p2'] + 1}`"


def _cmp(S, B, ret):
    p1, p2 = B.p1, B.p2
    if p2 < 0:
        return '`p2 < 0`：nums2 已经全部填入 → 结束'
    return f'nums2 还剩 `{p2 + 1}` 个元素没合并，继续'


def _if(S, B, ret):
    p1, p2 = B.p1, B.p2
    if p1 < 0:
        return '`p1 < 0`：nums1 已经没有数了 → 走 else，填 nums2'
    a, b = B.nums1[p1], B.nums2[p2]
    if a > b:
        return f'`nums1[{p1}] = {a} > nums2[{p2}] = {b}`：nums1 的更大 → 放到 `nums1[{B.p}]`'
    if a == b:
        return f'`{a} == {b}`：相等时规定放 nums2 的（只搬 nums2 更省事）'
    return f'`nums1[{p1}] = {a} < nums2[{p2}] = {b}`：nums2 的更大 → 走 else'


CONFIG = dict(
    num=88, title='合并两个有序数组', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='倒序双指针',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        p1, p2, p = m - 1, n - 1, m + n - 1
        while p2 >= 0:  # nums2 还有要合并的元素
            # 如果 p1 < 0，那么走 else 分支，把 nums2 合并到 nums1 中
            if p1 >= 0 and nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]  # 填入 nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]  # 填入 nums2[p2]
                p2 -= 1
            p -= 1  # 下一个要填入的位置
''',
    call='''nums1 = [1, 3, 6, 0, 0, 0]
Solution().merge(nums1, 3, [2, 4, 5], 3)
nums1''',
    expect=[1, 2, 3, 4, 5, 6],
    views=[
        dict(type='text', fn=_gap, h=60),
        dict(type='array', var='nums1', label='nums1（暗 = 空位，可以安全覆盖；绿 = 已就位）', cell=88,
             pointers={'p1': 'blue', 'p': 'yellow'}, color=_slot_color, dim=_slot_dim, h=230),
        dict(type='array', var='nums2', label='nums2（暗 = 已填入 nums1）', cell=88,
             pointers={'p2': 'pink'}, dim=lambda S, i, v: 'p2' in S and i > S['p2'], h=200),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), ('p', 'p', 'yellow')],
    captions={
        'p1, p2, p =': '三个指针都从==末尾==出发：`p1 = {p1}`，`p2 = {p2}`，`p = {p}`（下一个要填的位置）',
        'while p2 >= 0': _cmp,
        'if p1 >= 0 and': _if,
        'nums1[p] = nums1[p1]': '填入 nums1[p1]：`nums1[{p}] = {nums1[p]}`；==原位置变成新空位==，空位数不变',
        'p1 -= 1': '`p1` 左移 → {p1}',
        'nums1[p] = nums2[p2]': '填入 nums2[p2]：`nums1[{p}] = {nums1[p]}`',
        'p2 -= 1': '`p2` 左移 → {p2}',
        'p -= 1': '下一个要填入的位置：`p` → {p}',
    },
    cards=dict(
        one_liner='从后往前填最大的：搬走一个数就空出一个位置，永远不会错误覆盖',
        complexity='时间 `O(m + n)`，空间 `O(1)`',
        problem=['`nums1`、`nums2` 都按==非递减==排列，元素个数分别是 `m`、`n`',
                 '把 nums2 合并进 nums1（nums1 长度为 `m + n`，后 n 个是占位的 0）',
                 '示例：`[1,2,3,0,0,0], m = 3`，`[2,5,6], n = 3`',
                 '→ `[1,2,2,3,5,6]`',
                 '本视频：`[1,3,6,0,0,0]` 和 `[2,4,5]`'],
        quote='把 nums1 中的数字==移到另一个空位，又产生了一个新的空位，所以剩余空位的个数是不变的==，我们总是有空位可以让 nums2 的数字填入，不会发生错误覆盖。',
        quote_src='—— 灵茶山艾府题解：为什么倒序就一定能避免覆盖？',
        idea=['从左往右合并：nums2[0] 更小就会==直接覆盖== nums1[0] ✗',
              '从右往左：每次把两个末尾中==较大的==放到 `nums1[p]`',
              '`p2 < 0` 时 nums2 填完，nums1 剩下的数==本来就在正确位置==，不用动'],
        summary=['时间 `O(m + n)`，空间 `O(1)`',
                 '循环条件是 `p2 >= 0`：nums1 剩余元素无需移动（小优化）',
                 '`p1 < 0` 时只能填 nums2，所以 if 里要先判 `p1 >= 0`',
                 '相等时放 nums2 的：数组全相等时只需搬 nums2'],
    ),
)
