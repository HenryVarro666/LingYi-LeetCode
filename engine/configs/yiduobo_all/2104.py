def _top(S):
    if S['_line'] >= 58 and 'index' in S and 'left_max' in S:
        i = S['index']
        if S['_line'] == 60:
            lm, rm, ln, rn, x = S['left_max'][i], S['right_max'][i], S['left_min'][i], S['right_min'][i], S['nums'][i]
            return f"`({lm}×{rm} − {ln}×{rn}) × {x}` = ==`{(lm * rm - ln * rn) * x}`==（最大值次数 − 最小值次数）× 值"
    if S['_line'] <= 29:
        return '正序一趟：单调栈求每个数「向左能当最大/最小值」的延伸长度'
    if S['_line'] <= 57:
        return '逆序一趟：同样求「向右」的延伸长度'
    return '每个数的贡献 = (当最大值次数 − 当最小值次数) × 它的值'


def _ncolor(S, i, v):
    if 'index' in S and i == S['index']:
        return 'blue'
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if not nums:
        return
    n = len(nums)
    cur = S.get('index') if S['_line'] >= 9 else None
    lab_w = 250
    cell = min(110, (x1 - x0 - lab_w - 40) / n)
    sx = x0 + lab_w + 20
    rh = 62
    rows = [('nums', nums, False), ('left_max', S.get('left_max'), False),
            ('left_min', S.get('left_min'), False),
            ('right_max', S.get('right_max'), True),
            ('right_min', S.get('right_min'), True)]
    reversed_done = S['_line'] >= 55
    y = y0 + 50
    for k in range(n):
        cv.text((sx + k * cell + cell / 2, y - 6), k, 20, T['dim'], anchor='mb', mono=True)
    for name, arr, rev in rows:
        cv.text((x0 + 18, y + rh / 2), name, 24, T['muted'], anchor='lm', bold=True)
        for k in range(n):
            X = sx + k * cell
            cv.rect((X + 3, y + 3, X + cell - 3, y + rh - 3), fill=(38, 44, 54), r=8)
        if arr is not None:
            for j, v in enumerate(arr):
                col = n - 1 - j if (rev and not reversed_done) else j
                if not (0 <= col < n):
                    continue
                X = sx + col * cell
                fresh = len(arr) > 0 and j == len(arr) - 1 and S['_line'] < 55 and name != 'nums' and rev == (S['_line'] >= 34)
                cv.rect((X + 3, y + 3, X + cell - 3, y + rh - 3), fill=T['yellow'] if fresh else T['blue'], r=8, alpha=255 if fresh else 110)
                cv.text((X + cell / 2, y + rh / 2), v, 30, T['bg'] if fresh else T['text'], anchor='mm', bold=True)
        if name == 'nums' and cur is not None and 0 <= cur < n:
            X = sx + cur * cell
            cv.rect((X + 3, y + 3, X + cell - 3, y + rh - 3), fill=T['blue'], r=8)
            cv.text((X + cell / 2, y + rh / 2), nums[cur], 30, T['bg'], anchor='mm', bold=True)
        y += rh + 14
    y += 10
    for name in ('max_stack', 'min_stack'):
        st = S.get(name)
        cv.text((x0 + 18, y + 24), name + '（下标:值）', 24, T['muted'], anchor='lm', bold=True)
        if st is not None:
            for k, idx in enumerate(st):
                X = sx + k * 96
                cv.rect((X, y + 2, X + 88, y + 46), fill=T['purple'], r=8)
                cv.text((X + 44, y + 24), f'{idx}:{nums[idx]}', 26, T['bg'], anchor='mm', bold=True)
        y += 64


CONFIG = dict(
    num=2104, title='子数组范围和', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 · 每个数当最大值 − 当最小值的次数',
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
    call='Solution().subArrayRanges([1,3,2])',
    expect=5, max_steps=110,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='custom', draw=_draw, h=620),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'max_stack = [0]': lambda S, B, r: ('`max_stack` 存下标，栈里从底到顶的值递减；下标 0 先入栈' if 'right_max' not in S else '换成从右往左：`max_stack` 里先放最右边的下标 `n - 1`'),
        'left_max = [1]': '`left_max[0] = 1`：第 0 个数向左只有自己，延伸长度 1',
        'min_stack = [0]': lambda S, B, r: ('`min_stack` 同理，用来找左侧更小的' if 'right_min' not in S else '`min_stack` 也从 `n - 1` 开始'),
        'left_min = [1]': '`left_min[0] = 1`',
        'max_stack = [n - 1]': '换成从右往左：`max_stack` 里先放最右边的下标 `n - 1`',
        'right_max = [1]': '`right_max` 收集向右延伸长度，最右边的数是 1',
        'min_stack = [n - 1]': '`min_stack` 也从 `n - 1` 开始',
        'right_min = [1]': '`right_min` 同样先放 1',
        'for index in range(1, n)': lambda S, B, r: (f'正序处理 `index = {S.index}`' if S.index != B.get('index') else '正序扫完，左侧的四个数组都填好了'),
        'for index in range(n - 2': lambda S, B, r: (f'逆序处理 `index = {S.index}`' if S.index != B.get('index') else '逆序扫完，右侧的数组也填好了（顺序是反的）'),
        'while max_stack and nums[index] >= ': lambda S, B, r: (f'栈顶 `nums[{S.max_stack[-1]}] = {S.nums[S.max_stack[-1]]}` <= `{S.nums[S.index]}` → ==弹出==（它不再是 {S.index} 左边更大的那个）' if S.max_stack and S.nums[S.index] >= S.nums[S.max_stack[-1]] else ('栈空了，左边没有更大的数' if not S.max_stack else f'栈顶 `nums[{S.max_stack[-1]}] = {S.nums[S.max_stack[-1]]}` 更大，停止弹出')),
        'while min_stack and nums[index] <= ': lambda S, B, r: (f'栈顶 `nums[{S.min_stack[-1]}] = {S.nums[S.min_stack[-1]]}` >= `{S.nums[S.index]}` → ==弹出==' if S.min_stack and S.nums[S.index] <= S.nums[S.min_stack[-1]] else ('栈空了，左边没有更小的数' if not S.min_stack else f'栈顶 `nums[{S.min_stack[-1]}] = {S.nums[S.min_stack[-1]]}` 更小，停止弹出')),
        'while max_stack and nums[index] > ': lambda S, B, r: (f'栈顶 `nums[{S.max_stack[-1]}] = {S.nums[S.max_stack[-1]]}` < `{S.nums[S.index]}` → ==弹出==' if S.max_stack and S.nums[S.index] > S.nums[S.max_stack[-1]] else ('栈空了，右边没有 >= 它的数' if not S.max_stack else f'栈顶 `nums[{S.max_stack[-1]}] = {S.nums[S.max_stack[-1]]}` 不更小，停止弹出')),
        'while min_stack and nums[index] < ': lambda S, B, r: (f'栈顶 `nums[{S.min_stack[-1]}] = {S.nums[S.min_stack[-1]]}` > `{S.nums[S.index]}` → ==弹出==' if S.min_stack and S.nums[S.index] < S.nums[S.min_stack[-1]] else ('栈空了，右边没有 <= 它的数' if not S.min_stack else f'栈顶 `nums[{S.min_stack[-1]}] = {S.nums[S.min_stack[-1]]}` 不更大，停止弹出')),
        'if not max_stack': lambda S, B, r: (('`max_stack` 空 → ' + ('右边没有 >= 它的数，一直延伸到末尾' if S._line >= 34 else '左边没有更大的数，一直延伸到开头')) if not S.max_stack else ('`max_stack` 非空 → 栈顶就是最近的那个' + ('更大数（右侧）' if S._line >= 34 else '更大数（左侧）'))),
        'if not min_stack': lambda S, B, r: (('`min_stack` 空 → ' + ('右边没有 <= 它的数，一直延伸到末尾' if S._line >= 34 else '左边没有更小的数，一直延伸到开头')) if not S.min_stack else ('`min_stack` 非空 → 栈顶就是最近的那个' + ('更小数（右侧）' if S._line >= 34 else '更小数（左侧）'))),
        'left_max.append(index + 1)': '`left_max` 追加 `index + 1 = {index + 1}`：一直延伸到开头',
        'left_max.append(index - ': '`left_max` 追加 `{index} − {max_stack[-1]} = {left_max[-1]}`：到栈顶之间的起点个数',
        'left_min.append(index + 1)': '`left_min` 追加 `index + 1 = {index + 1}`',
        'left_min.append(index - ': '`left_min` 追加 `{index} − {min_stack[-1]} = {left_min[-1]}`',
        'right_max.append(n - index)': '`right_max` 追加 `n - index = {n - index}`：一直延伸到末尾',
        'right_max.append(max_stack[-1] - index)': '`right_max` 追加 `{max_stack[-1]} − {index} = {right_max[-1]}`',
        'right_min.append(n - index)': '`right_min` 追加 `n - index = {n - index}`',
        'right_min.append(min_stack[-1] - index)': '`right_min` 追加 `{min_stack[-1]} − {index} = {right_min[-1]}`',
        'max_stack.append(index)': '`{index}` 入 `max_stack`：`{max_stack}`',
        'min_stack.append(index)': '`{index}` 入 `min_stack`：`{min_stack}`',
        'right_max.reverse()': '`right_max` 是从右往左收集的，反转回按下标对齐：`{right_max}`',
        'right_min.reverse()': '`right_min` 反转：`{right_min}`',
        'res = 0': '`res` 累加每个数的贡献',
        'for index in range(n)': lambda S, B, r: ('全部处理完' if S.index == B.get('index') and S.index == len(S.nums) - 1 else f'处理 `nums[{S.index}]`'),
        'res += ': '`({left_max[index]}×{right_max[index]} − {left_min[index]}×{right_min[index]}) × {nums[index]} = {(left_max[index] * right_max[index] - left_min[index] * right_min[index]) * nums[index]}`，`res = {res}`',
        'return res': '所有数的贡献之和 `{res}`',
    },
    cards=dict(
        one_liner='不看子数组，看每个数：当最大值几次、当最小值几次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组的「范围」= 最大值 − 最小值，求所有子数组范围之和',
                 '示例：`[1,3,2]` → `5`',
                 '进阶：能否做到 `O(n)`'],
        quote='既然是O(n)的做法，那么显然不可能是从子数组入手，而应该改成从每个数入手。',
        quote_src='—— yiduobo 题解原文',
        idea=['数 `nums[i]` 在多少子数组里当最大值（次数 A）、当最小值（次数 B），贡献 `(A − B) × nums[i]`',
              '左边用 `>=` 弹栈、右边用 `>` 弹栈：重复数字不会重复计算',
              '次数 = 左延伸长度 × 右延伸长度，正序一趟、逆序一趟，各两个单调栈'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`right_*` 是逆序收集的，用之前必须 `reverse()`',
                 '易错：左右弹栈的比较符号一个带等号、一个不带，用来给重复数字去重',
                 '本视频示例很小，真实题解的每个贡献都是同一条公式',
                 '对比灵神：灵神只写一个函数算最大值，把数组取反再调用一次得到最小值；yiduobo 同时维护最大、最小两套栈'],
    ),
)
