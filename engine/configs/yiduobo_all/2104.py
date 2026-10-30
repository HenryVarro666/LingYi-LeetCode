def _cont(S, B, ret):
    n = len(S.nums)
    i = S.index
    return (f'`nums[{i}] = {S.nums[i]}` 的贡献：`({S.left_max[i]}×{S.right_max[i]} − {S.left_min[i]}×{S.right_min[i]}) × {S.nums[i]}`'
            f' = {(S.left_max[i]*S.right_max[i]-S.left_min[i]*S.right_min[i])*S.nums[i]}，累计 =={S.res}==')

ROWS = [('left_max', 'cyan', '左·最大'), ('right_max', 'blue', '右·最大'), ('left_min', 'orange', '左·最小'), ('right_min', 'pink', '右·最小')]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(S['nums'])
    cell = 64
    rh = (y1 - y0) / 4
    sx = x0 + 230
    for r, (name, c, zh) in enumerate(ROWS):
        y = y0 + r * rh
        cv.text((x0 + 16, y + rh / 2), f'{name}', 26, T[c], anchor='lm', bold=True)
        cv.text((x0 + 16, y + rh / 2 + 26), zh + '：能延伸几格', 17, T['muted'], anchor='lm')
        arr = S.get(name)
        if arr is None:
            cv.text((sx, y + rh / 2), '（尚未创建）', 20, T['dim'], anchor='lm')
            continue
        ln = S.get('_line') or 0
        rev = (name == 'right_max' and ln < 55) or (name == 'right_min' and ln < 56)
        for k in range(n):
            if k < len(arr):
                i = (n - 1 - k) if rev else k
            else:
                continue
            X = sx + i * (cell + 8)
            cur = (i == S.get('index'))
            cv.rect((X, y + 8, X + cell, y + rh - 8), fill=T['panel2'], outline=T[c] if cur else T['border'], width=3, r=8)
            cv.text((X + cell / 2, y + rh / 2), arr[k], 30, T['text'], anchor='mm', bold=True)


def _info(S):
    ln = S.get('_line')
    if 'res' in S:
        return '第三趟：每个数的 ==最大值次数 − 最小值次数== 再乘它自己'
    if 'right_max' in S:
        return '第二趟（倒序）：右侧用 ==严格大于/小于==，和左侧错开；right 数组倒着填，最后 reverse'
    return '第一趟（正序）：栈里留着「还可能卡住后面的数」的下标；弹出后栈顶就是左侧的墙'


CONFIG = dict(
    num=2104, title='子数组范围和', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 · 每个数当最大/最小值的次数',
    tags=['灵神题单', '单调栈', '难度分 2000'],
    code='''
class Solution(object):
    def subArrayRanges(self, nums):

        n = len(nums)
        max_stack = [0]
        left_max = [1]
        min_stack = [0]
        left_min = [1]
        for index in range(1, n):
            while max_stack and nums[index] >= nums[max_stack[-1]]:
                max_stack.pop()
            
            if not max_stack:
                left_max.append(index + 1)
            else:
                left_max.append(index - max_stack[-1])

            max_stack.append(index)

            while min_stack and nums[index] <= nums[min_stack[-1]]:
                min_stack.pop()
            
            if not min_stack:
                left_min.append(index + 1)
            else:
                left_min.append(index - min_stack[-1])

            min_stack.append(index)

        max_stack = [n - 1]
        right_max = [1]
        min_stack = [n - 1]
        right_min = [1]
        for index in range(n - 2, -1, -1):
            while max_stack and nums[index] > nums[max_stack[-1]]:
                max_stack.pop()
            
            if not max_stack:
                right_max.append(n - index)
            else:
                right_max.append(max_stack[-1] - index)

            max_stack.append(index)

            while min_stack and nums[index] < nums[min_stack[-1]]:
                min_stack.pop()
            
            if not min_stack:
                right_min.append(n - index)
            else:
                right_min.append(min_stack[-1] - index)

            min_stack.append(index)

        right_max.reverse()
        right_min.reverse()

        res = 0
        for index in range(n):
            res += (left_max[index] * right_max[index] - left_min[index] * right_min[index]) * nums[index]
        
        return res
''',
    call='Solution().subArrayRanges([3, 1, 3])',
    expect=6
,    skip=['n = len(nums)', 'max_stack = [0]', 'left_max = [1]', 'min_stack = [0]', 'left_min = [1]', 'max_stack = [n - 1]', 'right_max = [1]', 'min_stack = [n - 1]', 'right_min = [1]', 'res = 0'],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, cell=90, h=200),
        dict(type='stack', var='max_stack', label='max_stack（找更大的墙）', h=125, font=26),
        dict(type='stack', var='min_stack', label='min_stack（找更小的墙）', h=125, font=26),
        dict(type='custom', draw=_draw, h=270),
        dict(type='text', fn=_info, size=22, h=50),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'while max_stack and nums[index] >= ': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` 大于等于栈顶 `{S.nums[S.max_stack[-1]]}`：栈顶被它盖住了，当不了墙 → 弹出' if S.max_stack and S.nums[S.index] >= S.nums[S.max_stack[-1]] else '栈空或栈顶更大：栈顶就是左侧第一堵「更大」的墙，停'),
        'while min_stack and nums[index] <= ': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` 小于等于栈顶 `{S.nums[S.min_stack[-1]]}`：栈顶被它压住了 → 弹出' if S.min_stack and S.nums[S.index] <= S.nums[S.min_stack[-1]] else '栈空或栈顶更小：栈顶就是左侧第一堵「更小」的墙，停'),
        'left_max.append(index + 1)': '左边没有墙：最大值可以一直延伸到数组开头，共 `{index + 1}` 个起点',
        'left_max.append(index - max_stack[-1])': '墙在下标 `{B.max_stack[-1]}`：起点只能在墙右边，共 `{index} − {B.max_stack[-1]}` = =={left_max[-1]}== 个',
        'left_min.append(index + 1)': '左边没有更小的墙：最小值可延伸到开头，共 `{index + 1}` 个起点',
        'left_min.append(index - min_stack[-1])': '墙在下标 `{B.min_stack[-1]}`：共 `{index} − {B.min_stack[-1]}` = =={left_min[-1]}== 个起点',
        'max_stack.append(index)': '当前下标入栈，栈里保持「从底到顶数值递减」',
        'min_stack.append(index)': '当前下标入栈，栈里保持「从底到顶数值递增」',
        'while max_stack and nums[index] > ': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` ==严格大于== 栈顶 `{S.nums[S.max_stack[-1]]}` → 弹出' if S.max_stack and S.nums[S.index] > S.nums[S.max_stack[-1]] else '右侧这里用 ==严格大于==：相等的数留着当墙，和左侧的 `>=` 错开'),
        'while min_stack and nums[index] < ': lambda S, B, r: (f'`nums[{S.index}] = {S.nums[S.index]}` ==严格小于== 栈顶 `{S.nums[S.min_stack[-1]]}` → 弹出' if S.min_stack and S.nums[S.index] < S.nums[S.min_stack[-1]] else '右侧用 ==严格小于==，相等的数留着当墙'),
        'right_max.append(n - index)': '右边没有墙：可以延伸到数组末尾，共 `{n - index}` 个终点',
        'right_max.append(max_stack[-1] - index)': '墙在下标 `{B.max_stack[-1]}`：终点只能在墙左边，共 =={right_max[-1]}== 个',
        'right_min.append(n - index)': '右边没有更小的墙：共 `{n - index}` 个终点',
        'right_min.append(min_stack[-1] - index)': '墙在下标 `{B.min_stack[-1]}`：共 =={right_min[-1]}== 个终点',
        'right_max.reverse()': '`right_*` 是从右往左追加的，翻转后下标才和 `nums` 对齐',
        'right_min.reverse()': '`right_min` 同样翻转',
        'res += ': _cont,
        'return res': '所有子数组的范围之和 =={ret}==',
    },
    cards=dict(
        one_liner='换个角度：每个数当了多少次最大值、多少次最小值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组的「范围」= ==最大值 − 最小值==，求所有子数组范围之和',
                 '示例：`[1,2,3]` → `4`；`[4,-2,-3,4,1]` → `59`',
                 '本视频用 `[3,1,3]`，含重复数字'],
        quote='既然是O(n)的做法，那么显然不可能是从子数组入手，而应该改成从每个数入手。',
        quote_src='—— yiduobo 题解原文',
        idea=['数 `v` 当最大值的子数组有 `左 × 右` 个，当最小值的也一样',
              '贡献 = (最大值次数 − 最小值次数) × `v`，全部加起来',
              '重复数字：一侧 `>=`，另一侧 `>`，保证每个子数组只算一次'],
        summary=['时间 `O(n)`，空间 `O(n)`，比 `O(n^2)` 暴力快',
                 '易错：最大值左用 `>=` 弹栈、右用 `>` 弹栈（最小值同理），否则重复数字被重复统计',
                 '`right_*` 是倒序追加的，最后要 `reverse()` 才和下标对齐',
                 '原文为 Python 2 风格，代码未做修改即可在 Python 3 运行'],
    ),
)
