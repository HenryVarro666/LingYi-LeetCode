def _phase(S):
    """by highlighted line: 1 = building new_nums / double_set, 2 = a+a+b check, 3 = two pointers"""
    ln = S.get('_line', 0)
    if ln >= 27:
        return 3
    if ln >= 21:
        return 2
    if ln >= 13:
        return 1
    return 0


def _p(ph, name):
    def f(S):
        return S.get(name) if _phase(S) in ph else None
    return f


_P1 = _p((1,), 'index')
_P2 = _p((2,), 'index')
_FIRST = _p((3,), 'index')
_L = lambda S: S['left'] if _phase(S) == 3 and S.get('_line', 0) >= 29 else None
_R = lambda S: S['right'] if _phase(S) == 3 and S.get('_line', 0) >= 29 else None


def _live3(S):
    return _phase(S) == 3 and S.get('_line', 0) >= 29 and S['left'] <= S['right']


def _dup_color(S, i, v):
    if 'index' not in S or 'double_set' not in S:
        return None
    done = _phase(S) >= 2 or i <= S['index']
    if done and i > 0 and S['nums'][i] == S['nums'][i - 1]:
        return 'purple'
    return None


def _new_color(S, i, v):
    ph = _phase(S)
    if ph == 3 and i == S['index']:
        return 'yellow'
    if ph == 2 and i == S['index']:
        return 'yellow'
    return None


def _text(S):
    ph = _phase(S)
    if ph == 0:
        return '先排序，把重复的数和不重复的数分开'
    if ph == 1:
        i, a = S['index'], S['nums']
        if i > 0 and a[i] == a[i - 1]:
            return f"`nums[{i}] = {a[i]}` 与前一个相同 → `a + a = {2 * a[i]}` 记入 `double_set`"
        return f"`nums[{i}] = {a[i]}` 首次出现 → 放进 `new_nums`"
    if ph == 2:
        b = S['new_nums'][S['index']]
        hit = '在' if -b in S['double_set'] else '不在'
        return f"`b = {b}`：`-b = {-b}` =={hit}== `double_set` 中" + (' → 有 `a + a + b = 0` 的解' if hit == '在' else '')
    if S.get('_line', 0) < 29:
        return f"固定 `first_num = {S['first_num']}`，在它右边找两数之和 `{-S['first_num']}`"
    a, l, r, f = S['new_nums'], S['left'], S['right'], S['first_num']
    if l >= r:
        return f"`first_num = {f}`：`left ≥ right`，这一轮结束"
    s = a[l] + a[r]
    rel = '等于' if s == -f else ('小于' if s < -f else '大于')
    return f"两数之和 `{a[l]} + {a[r]} = {s}` =={rel}== `-first_num = {-f}`"


def _res_text(S):
    if 'res' not in S:
        return ''
    return 'res = ' + ('  '.join(f'`{t}`' for t in S['res']) if S['res'] else '`[]`')


def _dup_q(S, B, ret):
    i, a = S.index, S.nums
    if i > 0 and a[i] == a[i - 1]:
        return f'`nums[{i}] == nums[{i - 1}] = {a[i]}`：重复了'
    return f'`nums[{i}] = {a[i]}` 不是重复数字' if i > 0 else '`index = 0`，第一个数'


def _aab(S, B, ret):
    b = S.new_nums[S.index]
    if -b in S.double_set:
        return f'`-b = {-b}` 在 `double_set` 中 → `{-b // 2}` 是重复元素，`{-b // 2} + {-b // 2} + {b} = 0`'
    return f'`b = {b}`：`-b = {-b}` 不在 `double_set` 中'


def _two(S, B, ret):
    a, l, r, f = S.new_nums, S.left, S.right, S.first_num
    s = a[l] + a[r]
    if s == -f:
        return f'`{a[l]} + {a[r]} = {s} = -first_num`：找到一组！'
    return f'`{a[l]} + {a[r]} = {s}` ≠ `{-f}`'


def _two_lt(S, B, ret):
    a, l, r, f = S.new_nums, S.left, S.right, S.first_num
    s = a[l] + a[r]
    if s < -f:
        return f'`{s} < {-f}`：和偏小'
    return f'`{s} > {-f}`：和偏大'


CONFIG = dict(
    num=15, title='三数之和', difficulty='Medium', category='双指针',
    author='yiduobo', technique='先处理 a+a+b，再在去重数组上双指针',
    code='''
class Solution(object):
    def threeSum(self, nums):
        res = []

        if len(nums) < 3:
            return []

        double_set = set()
        nums = sorted(nums)

        zero_count = 0
        new_nums = []
        for index in range(len(nums)):
            if index > 0 and nums[index] == nums[index - 1]:
                double_set.add(nums[index] + nums[index])
            else:
                new_nums.append(nums[index])
            if nums[index] == 0:
                zero_count += 1

        for index in range(len(new_nums)):
            if -new_nums[index] in double_set:
                if new_nums[index] == 0 and zero_count < 3:
                    continue
                res.append([-new_nums[index] // 2, -new_nums[index] // 2, new_nums[index]])

        for index, first_num in enumerate(new_nums):
            left = index + 1
            right = len(new_nums) - 1
            while left < right:
                if new_nums[left] + new_nums[right] == -first_num:
                    res.append([first_num, new_nums[left], new_nums[right]])
                    left += 1
                elif new_nums[left] + new_nums[right] < -first_num:
                    left += 1
                else:
                    right -= 1
        return res
''',
    call='Solution().threeSum([-1,0,1,2,-1])',
    expect=[[-1, -1, 2], [-1, 0, 1]],
    views=[
        dict(type='text', fn=_text, size=27),
        dict(type='array', var='nums', pointers={_P1: 'yellow'}, pointer_labels={_P1: 'index'}, color=_dup_color,
             cell=80, h=195, label='nums（排序后；紫 = 重复出现的数）'),
        dict(type='array', var='new_nums', pointers={_P2: 'yellow', _FIRST: 'yellow', _L: 'blue', _R: 'pink'},
             pointer_labels={_P2: 'index', _FIRST: 'first', _L: 'left', _R: 'right'}, color=_new_color,
             window=(lambda S: S['left'] if _live3(S) else None, lambda S: S['right'] if _live3(S) else None),
             dim=lambda S, i, v: _phase(S) == 3 and i < S['index'],
             cell=80, h=245, label='new_nums（去重后的数组）'),
        dict(type='set', var='double_set', h=96, label='double_set（重复数 × 2，即 a + a）', font=26),
        dict(type='text', fn=_res_text, size=28),
    ],
    watch=['zero_count', ('first_num', 'first_num', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'res = []': '`res` 收集答案',
        'if len(nums) < 3': '不足 3 个数直接返回空；这里有 `{len(nums)}` 个',
        'double_set = set()': '`double_set`：记录==重复出现两次的数 × 2==',
        'nums = sorted(nums)': '排序 → `{nums}`',
        'zero_count = 0': '`zero_count`：数 0 的个数，专门处理 `0 + 0 + 0`',
        'new_nums = []': '`new_nums`：每个数只留一个',
        'for index in range(len(nums))': lambda S, B, r: (f'扫描 `nums[{S.index}] = {S.nums[S.index]}`'
                                                          if 'index' not in B or B.index != S.index else '扫描结束'),
        'if index > 0 and nums[index] == nums[index - 1]': _dup_q,
        'double_set.add': '记录 `{nums[index]} + {nums[index]} = {2 * nums[index]}`：以后遇到 `b = {-2 * nums[index]}`，就能凑成 `a + a + b = 0`',
        'new_nums.append(nums[index])': '首次出现 → 加入 `new_nums`：`{new_nums}`',
        'if nums[index] == 0': lambda S, B, r: ('是 0' if S.nums[S.index] == 0 else '不是 0'),
        'zero_count += 1': '`zero_count` → {zero_count}',
        'for index in range(len(new_nums))': lambda S, B, r: (f'枚举 `b = new_nums[{S.index}] = {S.new_nums[S.index]}`，检查 `a + a + b = 0`'
                                                              if B.index != S.index or S.index == 0 else '检查结束'),
        'if -new_nums[index] in double_set': _aab,
        'if new_nums[index] == 0 and zero_count < 3': '特例 `0 + 0 + 0`：要三个 0；这里 `b = {new_nums[index]}`，不是这个特例',
        'res.append([-new_nums': '记录 `a + a + b` 形式的解 `{res[-1]}`',
        'for index, first_num in': lambda S, B, r: (f'固定 `first_num = {S.first_num}`，在它右边找两数之和 `= {-S.first_num}`'
                                                    if 'first_num' not in B or B.index != S.index else '全部枚举完'),
        'left = index + 1': '`left = {left}`',
        'right = len(new_nums) - 1': '`right = {right}`',
        'if new_nums[left] + new_nums[right] == -first_num': _two,
        'res.append([first_num': '记录 `{res[-1]}`',
        33: '`left` 右移 → {left}；`new_nums` 无重复，不会再找到同一组',
        'elif new_nums[left] + new_nums[right] < -first_num': _two_lt,
        35: '和偏小 → `left` 右移到 {left}',
        'right -= 1': '和偏大 → `right` 左移到 {right}',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='重复的数单独凑 a+a+b，其余在去重数组上做两数之和',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['找出所有和为 `0` 的三元组 `[nums[i], nums[j], nums[k]]`，下标互不相同',
                 '答案中==不能有重复的三元组==',
                 '示例：`[-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`',
                 '本视频去掉了 `-4`：`[-1,0,1,2,-1]`，答案相同'],
        quote='当出现两个相同的数字时，只需要选一个作为first_num即可。这样一来可以优先计算解是==a + a + b== = 0形式的答案，然后在去除掉一个a之后再使用上面的方法计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后扫一遍：重复的数把 `a + a` 记进 `double_set`，首次出现的进 `new_nums`',
              '对每个 `b`：`-b` 在 `double_set` 中 → `[a, a, b]` 是解（`0+0+0` 要三个 0）',
              '`new_nums` 无重复：固定 `first_num`，用第 1 题的双指针找另外两个数'],
        summary=['时间 `O(n²)`：排序 + 每个 `first_num` 一趟双指针；去重后 n 变小一些',
                 '`new_nums` 没有重复值，双指针找到的三元组天然不重复',
                 '易错：`0 + 0 + 0` 只有 `zero_count ≥ 3` 才成立',
                 '原文为 Python 2：整数除法 `-new_nums[index] / 2` 已改为 `//`；删去了文档字符串'],
    ),
)
