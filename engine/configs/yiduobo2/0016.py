NUMS = [5, -1, -4, 2, -1]
TARGET = 4


def _sgn(d):
    return '还差一点（和偏小）' if d > 0 else '超了（和偏大）'


def _cap_dup(S, B, ret):
    i, x = S.index, S.first_num
    if i > 0 and x == S.nums[i - 1]:
        return f'`{x}` 和前一个数相同：==重复的数只做一次 first_num== → 跳过'
    if i == 0:
        return f'固定 `first_num = {x}`，在它右边找另外两个数'
    return f'`{x}` 和前一个数 `{S.nums[i - 1]}` 不同 → 固定它为 first_num'


def _cap_min(S, B, ret):
    d, md = S.delta, B.min_delta
    if md is None:
        return f'第一次算出差值 → `min_delta = {d}`'
    if abs(d) < abs(md):
        return f'`|{d}| < |{md}|`：这次更接近 → ==更新 min_delta=='
    return f'`|{d}| ≥ |{md}|`：没有更接近，不更新'


def _cap_move(S, B, ret):
    d = S.delta
    if d > 0:
        return f'`delta = {d} > 0`：两数之和偏小 → `left` 右移到 {S.left + 1}，换个更大的数'
    return f'`delta = {d} ≤ 0`：两数之和偏大 → `right` 左移到 {S.right - 1}，换个更小的数'


def _row(S):
    if 'new_target' not in S:
        return f'目标：`target = {TARGET}`'
    md = S.get('min_delta')
    md_s = 'None' if md is None else f'{md}（对应和 {TARGET - md}）'
    return f"`new_target = target − first_num = {S['new_target']}`；最优差值 `min_delta = {md_s}`"


CONFIG = dict(
    num=16, title='最接近的三数之和', difficulty='Medium', category='双指针',
    author='yiduobo', technique='固定 first_num + 左右指针记录最小差值',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def threeSumClosest(self, nums, target):

        nums = sorted(nums)

        min_delta = None

        for index, first_num in enumerate(nums):
            if index > 0 and first_num == nums[index - 1]:
                continue
            left = index + 1
            right = len(nums) - 1
            new_target = target - first_num
            while left < right:
                now = nums[left] + nums[right]
                if now == new_target:
                    return target
                delta = new_target - now
                if min_delta is None or abs(delta) < abs(min_delta):
                    min_delta = delta
                if delta > 0:
                    left += 1
                else:
                    right -= 1

        return target - min_delta
''',
    call=f'Solution().threeSumClosest({NUMS}, {TARGET})',
    expect=3,
    skip=['right = len(nums) - 1', 'now = nums[left] + nums[right]', 'left += 1', 'right -= 1'],
    views=[
        dict(type='array', var='nums', label='nums（排序后；紫 = first_num，蓝/粉 = left/right）', h=240,
             pointers={'index': 'purple', 'left': 'blue', 'right': 'pink'},
             color=lambda S, i, v: ('purple' if i == S.get('index') else
                                    'blue' if i == S.get('left') and S.get('left', 0) < S.get('right', 0) else
                                    'pink' if i == S.get('right') and S.get('left', 0) < S.get('right', 0) else None),
             dim=lambda S, i, v: S.get('index') is not None and i < S['index']),
        dict(type='text', fn=_row, size=26, h=110, lines=2),
        dict(type='text', fn=lambda S: (f"两数之和 `now = {S['now']}`，差值 `delta = new_target − now = {S['new_target'] - S['now']}`"
                                        if 'now' in S and 'new_target' in S else ''), size=26, h=70),
        dict(type='text', fn=lambda S: '最后答案 = `target − min_delta`', size=24, h=56),
    ],
    watch=[('first_num', 'first_num', 'purple'), ('left', 'left', 'blue'), ('right', 'right', 'pink'),
           'now', 'delta', ('min_delta', 'min_delta', 'green')],
    captions={
        'nums = sorted(nums)': '先排序：`{nums}`，这样左右指针才能“偏小右移、偏大左移”',
        'min_delta = None': '`min_delta`：目前离 target ==最近的差值==（带符号），开始还没有',
        'for index, first_num': lambda S, B, r: (f'固定第一个数 `first_num = nums[{S.index}] = {S.first_num}`'
                                                 if S.get('index') != B.get('index') else '所有 first_num 都试过了'),
        'if index > 0 and': _cap_dup,
        'continue': '跳过这个重复的 first_num',
        'left = index + 1': '左右指针：`left = {left}` 从 first_num 右边开始，`right = {len(nums) - 1}` 从最右边开始',
        'right = len(nums) - 1': '`right = {right}`：从最右边开始',
        'new_target = target - first_num': '问题变成：找两个数，和最接近 `new_target = {target} − ({first_num}) = {new_target}`',
        'while left < right': lambda S, B, r: (f'`left = {B.left} < right = {B.right}`，继续' if B.left < B.right
                                               else f'`left = {B.left} ≥ right = {B.right}`：这个 first_num 无法继续移动'),
        'now = nums[left] + nums[right]': '两数之和 `now = {nums[left]} + {nums[right]} = {now}`',
        'if now == new_target': lambda S, B, r: ('正好等于 new_target → 直接返回 target' if S.now == S.new_target
                                                 else f'两数之和 `now = {S.nums[S.left]} + {S.nums[S.right]} = {S.now}` ≠ `{S.new_target}`：不能直接匹配'),
        'delta = new_target - now': '`delta = {new_target} − {now} = {delta}`：' + '{"正数 = 和偏小" if delta > 0 else "负数 = 和偏大"}',
        'if min_delta is None': _cap_min,
        'min_delta = delta': '`min_delta = {min_delta}`，对应三数之和 `{target - min_delta}`',
        'if delta > 0': _cap_move,
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'return target - min_delta': '三数之和 = `target − min_delta = {target} − ({min_delta})` = =={ret}==',
    },
    cards=dict(
        one_liner='固定 first_num，剩下两数用左右指针逼近 target − first_num，记录最小差值',
        complexity='时间 `O(n^2)`，空间 `O(1)`（不计排序）',
        problem=['从 `nums` 里选==三个不同下标==的数，使它们的和与 `target` 最接近，返回这个和',
                 '示例：`nums = [-1,2,1,-4], target = 1` → `2`（`-1+2+1`）',
                 f'本视频：`nums = {NUMS}`，`target = {TARGET}` → `3`'],
        quote='固定住first_num之后寻找另外两数，如果能直接匹配那么就返回结果，否则==记录下当前结果与目标的差值并更新最优解==，并移动left或right直到无法继续移动。',
        quote_src='—— yiduobo 题解原文',
        idea=['和 15 题相同：排序后固定 `first_num`，目标变成 `new_target = target − first_num`',
              '`delta = new_target − now`：正数说明和偏小 → `left` 右移；否则 `right` 左移',
              '只记差值 `min_delta`，最后答案就是 ==`target − min_delta`=='],
        summary=['时间 `O(n^2)`：外层 n 个 first_num × 内层双指针 n 步',
                 '`min_delta` 要带符号保存，最后才能还原出 `target − min_delta`',
                 '易错：`min_delta` 初始为 `None`；比较时用 `abs()` 比绝对值',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神直接存和 ans，并多了 break / continue 两个剪枝'],
    ),
)
