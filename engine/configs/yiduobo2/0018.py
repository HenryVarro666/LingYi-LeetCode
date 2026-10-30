NUMS = [1, 0, -1, 0, -2, 2]
TARGET = 0


def _ok(S, lo, hi):
    return lo <= S.get('_line', 0) <= hi


def _head(S):
    ln = S.get('_line', 0)
    if 'left_pos' not in S:
        return f'target = =={TARGET}=='
    if ln <= 18:
        return '预处理：`left_pos[i]` = 右边第一个不同数的位置，`right_pos[i]` = 左边第一个不同数的位置'
    if 'new_target' in S and _ok(S, 39, 52):
        return f"`new_target = {TARGET} − ({S['nums'][S['i']]}) − ({S['nums'][S['j']]}) = {S['new_target']}`：left/right 找两数之和 = =={S['new_target']}=="
    if _ok(S, 28, 54):
        return f"固定 `first = nums[{S['i']}] = {S['nums'][S['i']]}`、`second = nums[{S['j']}] = {S['nums'][S['j']]}`"
    return f"固定 `first = nums[{S['i']}] = {S['nums'][S['i']] if S['i'] < len(S['nums']) else '—'}`"


def _res(S):
    a = S.get('res')
    if not a:
        return '答案：（暂无）'
    return '答案：' + '，'.join(f'`{q}`' for q in a)


def _jump(name, S, B):
    if abs(S[name] - B[name]) > 1:
        return f'==直接跳==到 `{name} = {S[name]}`：一步跳过所有等于 `{S.nums[B[name]]}` 的数'
    return f'`{name}` → `{S[name]}`（`nums[{B[name]}] = {S.nums[B[name]]}` 没有重复，跳 1 格）'


def _c22(S, B, r):
    n, i = S.nums, S.i
    v = n[i] + n[i + 1] + n[i + 2] + n[i + 3]
    return (f'first 加紧挨着的三个数 = `{v} > {TARGET}`：后面只会更大 → ==break==' if v > TARGET
            else f'first 能凑出的最小和 `{v}` ≤ target，有希望')


def _c24(S, B, r):
    n, i = S.nums, S.i
    v = n[i] + n[-1] + n[-2] + n[-3]
    return (f'first 加最大的三个数 = `{v} < {TARGET}` → 这个 first 不行，跳到下一个不同的数' if v < TARGET
            else f'first 能凑出的最大和 `{v}` ≥ target，值得枚举 second')


def _c30(S, B, r):
    n, i, j = S.nums, S.i, S.j
    v = n[i] + n[j] + n[j + 1] + n[j + 2]
    return (f'first + second + 紧挨着的两个数 = `{v} > {TARGET}` → break' if v > TARGET
            else f'first + second 的最小和 `{v}` ≤ target')


def _c32(S, B, r):
    n, i, j = S.nums, S.i, S.j
    v = n[i] + n[j] + n[-1] + n[-2]
    return (f'first + second + 最大两个数 = `{v} < {TARGET}` → second 换下一个不同的数' if v < TARGET
            else f'first + second 的最大和 `{v}` ≥ target → 跑左右指针')


def _c41(S, B, r):
    n, l = S.nums, S.left
    v = n[l] + n[l + 1]
    return (f'剩下最小的两数之和 `{v} > {S.new_target}` → ==提前 break==' if v > S.new_target
            else f'剩下最小的两数之和 `{v}` ≤ new_target')


def _c43(S, B, r):
    n, rr = S.nums, S.right
    v = n[rr] + n[rr - 1]
    return (f'剩下最大的两数之和 `{v} < {S.new_target}` → ==提前 break==' if v < S.new_target
            else f'剩下最大的两数之和 `{v}` ≥ new_target')


def _c45(S, B, r):
    n = S.nums
    v = n[S.left] + n[S.right]
    if v == S.new_target:
        return f'`{n[S.left]} + {n[S.right]} = {v}` ==等于== new_target：找到一组！'
    return f'`{n[S.left]} + {n[S.right]} = {v}` ≠ `{S.new_target}`'


CONFIG = dict(
    num=18, title='四数之和', difficulty='Medium', category='双指针',
    author='yiduobo', technique='预处理 left_pos/right_pos 一步跳过重复',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def fourSum(self, nums, target):

        nums = sorted(nums)

        if len(nums) < 4:
            return []

        res = []
        left_pos = [i + 1 for i in range(len(nums))]
        right_pos = [i - 1 for i in range(len(nums))]

        for i in range(len(nums) - 2, -1, -1):
            if nums[i] == nums[i + 1]:
                left_pos[i] = left_pos[i + 1]
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                right_pos[i] = right_pos[i - 1]

        i = 0
        while i < len(nums) - 3:
            if nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break
            if nums[i] + nums[-1] + nums[-2] + nums[-3] < target:
                i = left_pos[i]
                continue

            j = i + 1
            while j < len(nums) - 2:
                if nums[i] + nums[j] + nums[j + 1] + nums[j + 2] > target:
                    break
                if nums[i] + nums[j] + nums[-1] + nums[-2] < target:
                    j = left_pos[j]
                    continue

                left = j + 1
                right = len(nums) - 1

                new_target = target - nums[i] - nums[j]
                while left < right:
                    if nums[left] + nums[left + 1] > new_target:
                        break
                    if nums[right] + nums[right - 1] < new_target:
                        break
                    if nums[left] + nums[right] == new_target:
                        res.append([nums[i], nums[j], nums[left], nums[right]])
                        left = left_pos[left]

                    elif nums[left] + nums[right] < new_target:
                        left = left_pos[left]
                    else:
                        right = right_pos[right]

                j = left_pos[j]
            i = left_pos[i]

        return res
''',
    call=f'Solution().fourSum({NUMS}, {TARGET})',
    expect=[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]],
    skip=['if len(nums) < 4', 'res = []', 'right = len(nums) - 1', 13, 14, 16, 17, 49],
    max_steps=52,
    views=[
        dict(type='text', fn=_head, size=25, h=70),
        dict(type='array', var='nums', label='nums（排序后；紫 = i，蓝 = j，绿/粉 = left/right）', h=240,
             pointers={'i': 'purple', 'j if 28 <= _line <= 54 else None': 'blue',
                       'left if 36 <= _line <= 52 else None': 'green', 'right if 37 <= _line <= 52 else None': 'pink'},
             pointer_labels={'j if 28 <= _line <= 54 else None': 'j', 'left if 36 <= _line <= 52 else None': 'left',
                             'right if 37 <= _line <= 52 else None': 'right'},
             color=lambda S, k, v: ('purple' if k == S.get('i') else
                                    'blue' if k == S.get('j') and _ok(S, 28, 54) else
                                    'green' if k == S.get('left') and _ok(S, 36, 52) else
                                    'pink' if k == S.get('right') and _ok(S, 37, 52) else None)),
        dict(type='array', var='left_pos', label='left_pos（右边第一个不同数的下标）', h=170, cell=70,
             color=lambda S, k, v: 'yellow' if S.get('_line') == 15 and k == S.get('i') else None),
        dict(type='array', var='right_pos', label='right_pos（左边第一个不同数的下标）', h=170, cell=70,
             color=lambda S, k, v: 'yellow' if S.get('_line') == 18 and k == S.get('i') else None),
        dict(type='text', fn=_res, size=24, h=60),
    ],
    watch=[('i', 'i', 'purple'), ('j', 'j', 'blue'), ('left', 'left', 'green'), ('right', 'right', 'pink'), 'new_target'],
    captions={
        'nums = sorted': '先排序：`{nums}`',
        'left_pos = [': '`left_pos[i]` 先设为 `i + 1`（默认右边紧挨着的就不同）',
        'right_pos = [': '`right_pos[i]` 先设为 `i − 1`',
        'left_pos[i] = left_pos[i + 1]': '`left_pos[{i}] = left_pos[{i + 1}] = {left_pos[i]}`：==从尾到头扫==，一串相同数共用同一个位置',
        'right_pos[i] = right_pos[i - 1]': '`right_pos[{i}] = right_pos[{i - 1}] = {right_pos[i]}`：==从头到尾扫==',
        'i = 0': '预处理完成，开始枚举 first：`i = 0`',
        'while i < len(nums) - 3': lambda S, B, r: (f'枚举 first：`i = {S.i}`，`nums[i] = {S.nums[S.i]}`' if S.i < len(S.nums) - 3 else f'`i = {S.i}`：后面不够 4 个数了，结束'),
        22: _c22,
        24: _c24,
        25: lambda S, B, r: _jump('i', S, B),
        'j = i + 1': '枚举 second：从 `j = i + 1 = {j}` 开始',
        'while j < len(nums) - 2': lambda S, B, r: (f'second：`j = {S.j}`，`nums[j] = {S.nums[S.j]}`' if S.j < len(S.nums) - 2 else f'`j = {S.j}`：second 枚举完'),
        30: _c30,
        32: _c32,
        33: lambda S, B, r: _jump('j', S, B),
        'left = j + 1': '左右指针：`left = j + 1 = {left}`，`right` 从最右 `{len(nums) - 1}` 开始',
        'new_target = ': lambda S, B, r: f'剩下两数之和要等于 `{S.target} − ({S.nums[S.i]}) − ({S.nums[S.j]})` = =={S.new_target}==',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，继续' if S.left < S.right else f'`left ≥ right`：这组 first/second 找完了'),
        41: _c41,
        43: _c43,
        45: _c45,
        'res.append': '记录 =={res[-1]}==',
        47: lambda S, B, r: _jump('left', S, B),
        49: lambda S, B, r: ('两数之和偏小 → left 右移' if S.nums[S.left] + S.nums[S.right] < S.new_target else '两数之和偏大 → right 左移'),
        50: lambda S, B, r: _jump('left', S, B),
        52: lambda S, B, r: _jump('right', S, B),
        54: lambda S, B, r: _jump('j', S, B),
        55: lambda S, B, r: _jump('i', S, B),
        42: '剩下的数凑不出 new_target → 换下一个 second',
        44: '剩下的数凑不出 new_target → 换下一个 second',
        23: '更大的 first 只会更大 → 结束',
        'return res': '返回全部 `{len(res)}` 个四元组',
    },
    cards=dict(
        one_liner='三数之和再套一层；用 left_pos/right_pos 一步跳过重复数',
        complexity='时间 `O(n^3)`，空间 `O(n)`（两个跳转数组）',
        problem=['在 `nums` 里找出所有==不重复==的四元组，四个下标互不相同，和等于 `target`',
                 '示例：`nums = [1,0,-1,0,-2,2], target = 0`',
                 '→ `[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]`'],
        quote='有了left_pos和right_pos，在后续的计算中，遇到需要移动first_num，second_num或是左右指针的时候，==无需再一位一位移动==，而是直接使用left_pos和right_pos进行移动即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['“果然人类的本质就是套娃”：排序后枚举 first、second，剩下两数用左右指针',
              '`left_pos[i]`：右边第一个 `!= nums[i]` 的位置；`right_pos[i]`：左边第一个不同的位置',
              '移动任何指针都用这两个数组==一步跳过整段重复==，自然不会产生重复答案'],
        after=[dict(heading='left_pos / right_pos 怎么算', lines=[
            '排序后 `[-2,-1,0,0,1,2]`：`left_pos = [1,2,4,4,5,6]`',
            '`nums[2] = nums[3] = 0`，它们的 left_pos 都是 4（下一个不同数的位置）',
            '==从尾到头==扫一遍得 left_pos，==从头到尾==扫一遍得 right_pos，各 `O(n)`',
        ])],
        summary=['时间 `O(n^3)`，空间 `O(n)`',
                 '四层都有剪枝：最小和 > target 就 break，最大和 < target 就跳过',
                 '易错：找到答案后只移动 left 即可，left 跳过重复后 right 会自然左移',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用 `x == nums[a-1]` 判重 + while 跳重复，不需要额外数组'],
    ),
)
