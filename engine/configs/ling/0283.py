def _color(S, i, v):
    if 'start0' not in S:
        return None
    if i < S['start0']:
        return 'green'
    return None


def _dim(S, i, v):
    return 'i' in S and i > S['i']


def _segments(S, B):
    a, s0, i = S['nums'], S['start0'], S['i']
    if B.get('nums') is not None and B['nums'] != a:      # just swapped: nums[start0] is now non-zero
        nz, pe = s0 + 1, i + 1
    elif B.get('start0') is not None and B['start0'] != s0:  # start0 += 1 finished processing nums[i]
        nz, pe = s0, i + 1
    else:
        nz, pe = s0, i
    return a[:nz], a[nz:pe], a[pe:]


def _draw_inv(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '循环不变量：[ 非零元素 | 零元素 | 尚未遍历 ]', 24, T['muted'], bold=True)
    if 'i' not in S:
        return
    segs = _segments(S, B)
    names = ['非零元素', '零元素', '尚未遍历']
    cols = [T['green'], T['purple'], T['dim']]
    x, y = x0 + 22, y0 + 44
    for name, vals, c in zip(names, segs, cols):
        txt = ', '.join(map(str, vals)) if vals else '空'
        w = max(130, cv.tlen(txt, 30, mono=True) + 40)
        cv.rect((x, y, x + w, y + 54), fill=T['panel2'], outline=c, width=3, r=10)
        cv.text((x + w / 2, y + 27), txt, 30, T['text'] if vals else T['dim'], anchor='mm', mono=True, bold=True)
        cv.text((x + w / 2, y + 62), name, 20, c if c != T['dim'] else T['muted'], anchor='mt')
        x += w + 16


def _if(S, B, ret):
    i, a = S.i, S.nums
    if a[i] == 0:
        return f'`nums[{i}] = 0` 是空位：不操作，空位区 `[start0, i]` 变长'
    return f'`nums[{i}] = {a[i]}` 非零 → 要放到最左边的空位 `start0 = {S.start0}`'


def _swap(S, B, ret):
    i, s0 = S.i, S.start0
    if i == s0:
        return f'`i == start0 = {i}`：前面还没有 0，==自己和自己交换==，相当于不动'
    return f'交换 `nums[{i}]` 和 `nums[{s0}]`：`{S.nums[s0]}` 填进最左空位，==原位置变成新的空位=='


CONFIG = dict(
    num=283, title='移动零', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='双指针 + 交换元素（循环不变量）',
    code='''
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        循环不变量：在循环过程中，nums 的数据分布始终如下图
        [ 非零元素 | 零元素 | 尚未遍历 ]
                    ^       ^
                    start0  i
        """
        start0 = 0
        for i in range(len(nums)):
            if nums[i]:
                nums[i], nums[start0] = nums[start0], nums[i]
                start0 += 1
''',
    call='''nums = [1, 0, 0, 3, 0, 12, 5]
Solution().moveZeroes(nums)
nums''',
    expect=[1, 3, 12, 5, 0, 0, 0],
    views=[
        dict(type='custom', draw=_draw_inv, h=150),
        dict(type='array', var='nums', pointers={'start0': 'pink', 'i': 'blue'}, color=_color, dim=_dim, h=300, cell=96,
             label='nums（绿 = 已就位的非零元素，暗 = 尚未遍历）'),
    ],
    watch=[('i', 'i', 'blue'), ('start0', 'start0', 'pink')],
    captions={
        'start0 = 0': '`start0` 指向==最左边的空位==（0）；开始时区间 `[start0, i−1]` 为空',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：看 `nums[{S.i}] = {S.nums[S.i]}`' if 'i' not in B or B.i != S.i
                                          else '遍历结束：`[start0, n−1]` 全是 0'),
        'if nums[i]:': _if,
        'nums[i], nums[start0] =': _swap,
        'start0 += 1': lambda S, B, r: (f'`start0` → {S.start0}：前面没有空位，`start0` 跟着 `i` 一起右移' if S.start0 > S.i
                                        else f'`start0` → {S.start0}：`[start0, i]` 仍全是空位，不变量保持'),
    },
    cards=dict(
        one_liner='把 0 看成空位，非零数依次换到最左边的空位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组中所有 `0` 移到末尾，==非零元素保持相对顺序==',
                 '必须==原地==修改，不能拷贝数组',
                 '示例：`[0,1,0,3,12]` → `[1,3,12,0,0]`',
                 '本视频：`[1,0,0,3,0,12,5]` → `[1,3,12,5,0,0,0]`'],
        quote='同时维护另一个下标 start0（初始值为 0），并==保证下标区间 [start0, i−1] 都是空位（0）==，且 start0 指向最左边的空位。',
        quote_src='—— 灵茶山艾府题解「方法二」',
        idea=['循环不变量：`[ 非零元素 | 零元素 | 尚未遍历 ]`',
              '遇到非零 `nums[i]`：和 `nums[start0]` 交换，`start0`、`i` 都加一',
              '遇到 0：只有 `i` 加一，空位区自然变长'],
        summary=['时间 `O(n)`，只遍历一次；空间 `O(1)`',
                 '开头没有 0 时 `i == start0`，自己和自己交换，不影响结果',
                 '方法一"原地栈"：非零数依次写到 `nums[stack_size]`，最后补 0（全 0 时要扫两遍）',
                 '同类：双指针原地修改（题单 §3.4）'],
        result='遍历结束：`nums = [1,3,12,5,0,0,0]`，原地完成',
    ),
)
