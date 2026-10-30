COL = {0: 'red', 1: 'yellow', 2: 'blue'}


def _for_cap(S, B, ret):
    if 'index' in B and S.index == B.index:
        return '扫描结束'
    return f'扫描 `index = {S.index}`，`num = {S.num}`'


def _swap_in(S, B, ret):
    w1 = B.w + 1
    if w1 == S.index:
        return f'还没有蓝色：`nums[{S.index}] = nums[{w1}]` 是自己赋给自己'
    return f'把蓝色段最左边的 2（位置 `w + 1 = {w1}`）放到 `index = {S.index}`：`nums[{S.index}] = {S.nums[S.index]}`'


def _structure(S):
    r, w, idx = S.get('r'), S.get('w'), S.get('index')
    if r is None or w is None:
        return ''
    if idx is None:
        return f'`r = {r}`，`w = {w}`：三种颜色都还没有'
    def seg(a, b):
        return f'`[{a}, {b}]`' if a <= b else '空'
    return f'红 {seg(0, r)}　白 {seg(r + 1, w)}　蓝 {seg(w + 1, idx - 1)}　当前 `index = {idx}`'


CONFIG = dict(
    num=75, title='颜色分类', difficulty='Medium', category='技巧',
    author='yiduobo', technique='维护两段右边界 · 一趟扫描',
    code='''
class Solution(object):
    def sortColors(self, nums):
        r = -1
        w = -1

        for index, num in enumerate(nums):
            if num == 2:
                continue
            elif num == 1:
                nums[index] = nums[w + 1]
                nums[w + 1] = 1
                w += 1
            else:
                nums[index] = nums[w + 1]
                nums[w + 1] = nums[r + 1]
                nums[r + 1] = 0
                r += 1
                w += 1
        return nums
''',
    call='Solution().sortColors([1, 2, 0, 1, 2, 0])',
    expect=[0, 0, 1, 1, 2, 2],
    views=[
        dict(type='array', var='nums', label='nums', h=280, cell=120,
             pointers={'r': 'red', 'w': 'yellow', 'index': 'cyan'},
             window=(lambda S: 0 if 'index' in S else None, 'index'),
             color=lambda S, i, v: COL.get(v), dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='text', fn=lambda S: '红 = 0，黄 = 1（白色），蓝 = 2；`r` 红色段右边界，`w` 白色段右边界', size=26, h=90, lines=2),
        dict(type='text', fn=_structure, size=28, h=70),
        dict(type='text', fn=lambda S: '`0 0 0 (r) 1 1 1 (w) 2 2 2 (index)`：左边界由 `r + 1`、`w + 1` 算出', size=26, h=70),
    ],
    watch=[('index', 'index', 'cyan'), ('num', 'num'), ('r', 'r', 'red'), ('w', 'w', 'yellow')],
    captions={
        'r = -1': '`r`：红色（0）段的==右边界==，还没有红色 → `-1`',
        'w = -1': '`w`：白色（1）段的右边界 → `-1`；维护右边界，没有某种颜色时更方便',
        'for index, num in': _for_cap,
        'if num == 2': lambda S, B, ret: ('当前是蓝色 → 本来就排在最右边，==无事发生==' if S.num == 2
                                          else f'`{S.num}` 不是蓝色'),
        'continue': '`continue`，看下一个',
        'elif num == 1': lambda S, B, ret: ('当前是白色 → 把它和最左侧的 2 互换' if S.num == 1
                                            else '当前是红色 → 相当于两次交换'),
        'nums[index] = nums[w + 1]': _swap_in,
        'nums[w + 1] = 1': '`nums[{B.w + 1}] = 1`：白色段向右长一格',
        'nums[w + 1] = nums[r + 1]': lambda S, B, ret: (
            f'`nums[{B.w + 1}] = nums[{B.r + 1}]`：白色段最左的 1 挪到白色段末尾' if B.w > B.r
            else f'还没有白色：`nums[{B.w + 1}] = nums[{B.r + 1}]` 原地不动'),
        'nums[r + 1] = 0': '`nums[{B.r + 1}] = 0`：红色段向右长一格',
        'r += 1': '红色右边界后移：`r = {r}`',
        'w += 1': '白色右边界后移：`w = {w}`',
        'return nums': '一趟扫描完成，返回 `{ret}`',
    },
    cards=dict(
        one_liner='维护红、白两段的右边界，新来的数和段首交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组只含 `0, 1, 2`（红、白、蓝），==原地==排成 `0…0 1…1 2…2`',
                 '不能用库函数 sort；进阶：常数空间、一趟扫描',
                 '示例：`[2,0,2,1,1,0]` → `[0,0,1,1,2,2]`'],
        quote='对于bbb...bbba这种串，要将a放到b的左边，一个简单的思路就是==将a与最左侧的那个b进行交换==，这样就用O(1)的时间完成了段落的移动。',
        quote_src='—— yiduobo 题解',
        idea=['维护红色右边界 `r`、白色右边界 `w`，左边界用 `r+1`、`w+1` 算出',
              '白色：`nums[index]` 与 `nums[w+1]`（最左的 2）互换，`w += 1`',
              '红色：`index ← w+1 ← r+1 ← 0`，相当于两次交换，`r`、`w` 都后移'],
        result='一趟扫描完成：`[0,0,1,1,2,2]` ✓',
        summary=['时间 `O(n)` 一趟扫描，空间 `O(1)`',
                 '维护==右边界==、初值 `-1`：没有红色或白色时不用特判',
                 '红色的三次赋值顺序：先 `index`，再 `w+1`，最后 `r+1`',
                 '原文为 Python 2 写法：仅删去文档字符串，逻辑未改'],
    ),
)
