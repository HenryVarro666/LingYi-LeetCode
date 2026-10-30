NUMS = [1, 2, 2, 3]
K = 2
N = len(NUMS)


def _b(m):
    return format(m, f'0{N}b')


def _ncolor(E, i, v):
    cand = E.get('candidate')
    if cand is None:
        return None
    if E.get('index') == i and E.get('_line', 0) >= 17:
        return 'yellow'
    return None if i in cand else 'green'


def _ndim(E, i, v):
    return False


def _text(E):
    if 'part_s' not in E:
        return '目标：每个子集的和都等于 `sum / k`'
    if 'now' not in E or 'now_s' not in E:
        return f"每个子集的和必须是 `part_s = {E['part_s']}`"
    cand = E.get('candidate') or set()
    used = sum(NUMS) - sum(NUMS[i] for i in cand)
    full = (used - E['now_s']) // E['part_s'] if E['now_s'] != E['part_s'] else used // E['part_s']
    return f"`now = {_b(E['now'])}`（1 = 没用）；当前子集 `{E['now_s']}/{E['part_s']}`；已凑满 `{full}` 个"


def _cap_dfs_if(E, B, ret):
    if B.f[B.now] is None:
        return f'状态 `now = {_b(B.now)}` 第一次遇到 → 展开搜索'
    if B.f[B.now] is True:
        return f'`now = {_b(B.now)}`：所有数都用完了 → `f[0] = True`，==成功=='
    return f'状态 `now = {_b(B.now)}` 之前搜过，失败了 → 直接返回 `False`（==记忆化剪枝==）'


def _cap_cand_if(E, B, ret):
    i, s, p = E.index, E.now_s, E.part_s
    if s + E.nums[i] <= p:
        return f'`{s} + nums[{i}]({E.nums[i]}) = {s + E.nums[i]} ≤ {p}` → 可以放进当前子集'
    return f'`{s} + {E.nums[i]} = {s + E.nums[i]} > {p}` → 放不下，跳过'


def _cap_ret(E, B, ret):
    if ret is True:
        return '返回 ==True=='
    return f'这个状态无解 → 返回 `False`（`f[{_b(E.now)}] = False` 已记下）'


CONFIG = dict(
    num=698, title='划分为k个相等的子集', difficulty='Medium', category='回溯',
    author='yiduobo', technique='状压记忆化 + 回溯（473 火柴拼正方形的翻版）',
    tags=['字节30天'],
    code='''
class Solution(object):
    def canPartitionKSubsets(self, nums, k):
        n = len(nums)
        s = sum(nums)
        if s % k != 0:
            return False

        part_s = s // k

        f = [None] * (1 << n)
        f[0] = True

        return self.dfs((1 << n) - 1, f, n, nums, set(range(n)), 0, part_s)

    def dfs(self, now, f, n, nums, candidate, now_s, part_s):
        if f[now] is None:
            f[now] = False
            if now_s == part_s:
                now_s = 0
            for index in list(candidate):
                if now_s + nums[index] <= part_s:
                    candidate.remove(index)
                    if self.dfs(now - (1 << index), f, n, nums, candidate, now_s + nums[index], part_s):
                        return True
                    candidate.add(index)

        return f[now]
''',
    call=f'Solution().canPartitionKSubsets({NUMS}, {K})',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=60, size=26),
        dict(type='array', var='nums', label='nums（绿 = 已用，黄 = 当前尝试；now 从右数第 i 位对应 nums[i]）', cell=100,
             color=_ncolor, h=150),
        dict(type='set', var=lambda E: {_b(m) for m, v in enumerate(E['f']) if v is False} if isinstance(E.get('f'), list) else None,
             label='f[now] = False 的状态（正在搜，或已搜过且失败）', h=110, font=24),
        dict(type='calls', h=260, label='调用栈', hide=('f', 'n', 'nums', 'candidate', 'part_s')),
    ],
    watch=[('now', lambda E: _b(E['now']) if 'now' in E else None), ('now_s', 'now_s', 'yellow'), ('part_s', 'part_s', 'green'), ('index', 'index', 'yellow'),
           ('candidate', 'candidate')],
    skip=['n = len(nums)', 'f = [None]', 'candidate.remove(index)'],
    max_steps=70,
    captions={
        's = sum': '元素和 `s = {s}`',
        'if s % k != 0': '`{s} % {k} = 0`：能整除，才可能分成 `k` 份',
        'part_s = s // k': '每个子集的和 `part_s = {s} // {k} = {part_s}`（原文 `/`）',
        'f[0] = True': '`f[now]`：数的使用状态为 `now`（二进制，1 = 没用）时能否成功；`f[0] = True`：全用完就成功',
        'return self.dfs((1 << n) - 1': '从「全都没用」`now = {(1 << n) - 1:b}`、当前子集和 0 开始搜',
        'if f[now] is None': _cap_dfs_if,
        'f[now] = False': '先标成 `False`：如果后面没成功，它就保持失败',
        'if now_s == part_s': lambda E, B, ret: ('当前子集凑满了 → 开始凑下一个子集' if E.now_s == E.part_s
                                                 else f'当前子集还差 `{E.part_s - E.now_s}`'),
        'now_s = 0': '`now_s` 清零，凑下一个子集',
        'for index in list(candidate)': lambda E, B, ret: ('候选都试过了，都不行' if 'index' in B and B.index == E.index else
                                                           f'枚举还没用的数：`index = {E.index}`（`nums[{E.index}] = {E.nums[E.index]}`）'),
        'if now_s + nums[index] <= part_s': _cap_cand_if,
        'candidate.remove(index)': '用掉 `nums[{index}]`',
        'if self.dfs(now - (1 << index)': lambda E, B, ret: f'用掉 `nums[{B.index}]`，递归：`now` → `{_b(B.now - (1 << B.index))}`，子集和变成 `{B.now_s + B.nums[B.index]}`',
        'return True': '下一层成功了 → 一路返回 ==True==',
        'candidate.add(index)': '这条路不通 → ==回溯==，把 `nums[{index}]` 放回去',
        'return f[now]': _cap_ret,
        'return False': '不能整除 → `False`',
    },
    cards=dict(
        one_liner='用二进制 now 表示哪些数还没用，一个子集一个子集地凑',
        complexity='时间 `O(n · 2^n)`，空间 `O(2^n)`',
        problem=['能否把 `nums` 分成 `k` 个==非空子集==，且每个子集的和都相等？',
                 '示例：`[4,3,2,3,5,2,1]`，`k = 4` → `true`',
                 '演示：`[1,2,2,3]`，`k = 2` → `true`（`(1,3) (2,2)`）'],
        quote='这一题是473题的==翻版==。……有一个小小的区别是从正方形变成了正k边形，但是具体的做法还是一样。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个子集的和必须是 `part_s = sum / k`',
              '按顺序一个子集一个子集地凑：`now_s` 是当前子集的和，凑满 `part_s` 就清零',
              '状态只需要 `now`（哪些数还没用）：同一个 `now` 失败过就==不再重复搜=='],
        summary=['时间 `O(n · 2^n)`，空间 `O(2^n)`',
                 '为什么只用 `now` 做状态：用掉的数确定了，`now_s = 已用的和 % part_s` 也就确定了',
                 '剪枝：`now_s + nums[index] > part_s` 直接跳过',
                 '原文为 Python 2 写法，`part_s = s / k` 已改为 `//`，并删去类型说明文档字符串',
                 '同类题：473. 火柴拼正方形（`k = 4`）'],
    ),
)
