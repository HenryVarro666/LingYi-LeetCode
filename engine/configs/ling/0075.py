COL = {0: 'red', 1: 'yellow', 2: 'blue'}


def _for_cap(S, B, ret):
    if 'i' in B and S.i == B.i:
        return '有序前缀已覆盖整个数组 → 排序完成'
    if S.i == 0:
        return f'`x = nums[0] = {S.x}`：插入空前缀'
    return f'把 `x = nums[{S.i}] = {S.x}` 插入有序前缀 `nums[0..{S.i - 1}]`'


CONFIG = dict(
    num=75, title='颜色分类', difficulty='Medium', category='技巧',
    author='灵茶山艾府', technique='O(1) 插入 · 插入排序',
    code='''
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        p0 = p1 = 0
        for i, x in enumerate(nums):
            nums[i] = 2
            if x <= 1:
                nums[p1] = 1
                p1 += 1
            if x == 0:
                nums[p0] = 0
                p0 += 1
''',
    call='''nums = [2, 0, 2, 1, 1, 0]
Solution().sortColors(nums)
nums''',
    expect=[0, 0, 1, 1, 2, 2],
    views=[
        dict(type='array', var='nums', label='nums', h=280, cell=120,
             pointers={'p0': 'red', 'p1': 'yellow', 'i': 'cyan'},
             window=(lambda S: 0 if 'i' in S else None, 'i'),
             color=lambda S, i, v: COL.get(v), dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='text', fn=lambda S: '红 = 0，黄 = 1，蓝 = 2；==青框== = 已排好序的前缀 `nums[0..i]`', size=26, h=60),
        dict(type='text', fn=lambda S: '`p0` = 0 的个数（下一个 0 写这里），`p1` = 0 和 1 的个数（下一个 1 写这里）', size=26, h=90, lines=2),
        dict(type='text', fn=lambda S: '插入 `x`：==倒着改==三个位置　`nums[i] = 2` → `nums[p1] = 1` → `nums[p0] = 0`', size=26, h=90, lines=2),
    ],
    watch=[('i', 'i', 'cyan'), ('x', 'x'), ('p0', 'p0', 'red'), ('p1', 'p1', 'yellow')],
    captions={
        'p0 = p1 = 0': '`p0`：前缀里 0 的个数；`p1`：前缀里 0 和 1 的个数。一开始前缀为空，都是 0',
        'for i, x in': _for_cap,
        'nums[i] = 2': lambda S, B, ret: ('“狸猫换太子”：不是插入，而是修改。先把末尾 `nums[0]` 改成 `2`' if S.i == 0
                                          else f'先把末尾 `nums[{S.i}]` 改成 `2`（相当于新增一个 2）'),
        'if x <= 1': lambda S, B, ret: (f'`x = {S.x} ≤ 1` → 还要把位置 `p1 = {S.p1}` 改成 1' if S.x <= 1
                                        else f'`x = 2` → 只改末尾就够了，插入完成'),
        'nums[p1] = 1': lambda S, B, ret: (f'前缀里没有 2：`nums[{B.p1}] = 1` 直接==覆盖==刚写的 2' if B.p1 == S.i
                                           else f'`nums[{B.p1}]` 原是第一个 2，改成 1（2 的段整体右移一格）'),
        'p1 += 1': '0 和 1 多了一个：`p1 = {p1}`',
        'if x == 0': lambda S, B, ret: (f'`x = 0` → 再把位置 `p0 = {S.p0}` 改成 0' if S.x == 0
                                        else f'`x = {S.x}` 不是 0，不用动 `p0`'),
        'nums[p0] = 0': lambda S, B, ret: (f'前缀里没有 1：`nums[{B.p0}] = 0` 直接==覆盖==刚写的 1' if B.p0 == S.p1 - 1
                                           else f'`nums[{B.p0}]` 原是第一个 1，改成 0（1 的段整体右移一格）'),
        'p0 += 1': '0 多了一个：`p0 = {p0}`',
    },
    cards=dict(
        one_liner='不让用 sort？插入排序，每次 O(1) 插入：改三个位置',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组只含 `0, 1, 2`（红、白、蓝），==原地==排成 `0…0 1…1 2…2`',
                 '不能用库函数 sort；进阶：常数空间、一趟扫描',
                 '示例：`[2,0,2,1,1,0]` → `[0,0,1,1,2,2]`'],
        before=[dict(heading='技巧：O(1) 插入元素', lines=[
            '有序数组 `[0,0,1,1,2,2]` 插入一个 0 → `[0,0,0,1,1,2,2]`',
            '竖着对比：==只有三个位置变了==：`a[2]` 1→0，`a[4]` 2→1，末尾新增 2',
            '`p0` = 0 的个数，`p1` = 0 和 1 的个数，末尾是 `i`'])],
        quote='实际上，我们可以「狸猫换太子」：==不是插入元素，而是修改元素==！',
        quote_src='—— 灵茶山艾府题解',
        idea=['没有 2 时第三步会出错？==倒过来算==：先改 `a[i]=2`，再 `a[p1]=1`，最后 `a[p0]=0`',
              '后写的会覆盖先写的，等价于“没有 2 的时候不改成 2”',
              '插入 1 跳过改 0；插入 2 只改 `a[i]`'],
        result='原地排序完成：`[0,0,1,1,2,2]` ✓',
        summary=['时间 `O(n)` 一趟扫描，空间 `O(1)`',
                 '关键：三次赋值的顺序必须是 ==2 → 1 → 0==，靠覆盖处理特殊情况',
                 '先用 `x` 记下 `nums[i]` 原值，因为 `nums[i]` 会被改掉',
                 '`p0 ≤ p1 ≤ i` 始终成立'],
    ),
)
