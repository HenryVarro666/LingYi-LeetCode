def _txt(S):
    if 'start' not in S:
        return '枚举每个起点 `start`，向右一个个扩展终点 `end`，边加边判断'
    ln = S['_line']
    if ln in (6, 7, 8):
        return f"新的起点 `start = {S['start']}`：`s` 和 `length` 都从 0 重新累计"
    if 'end' not in S:
        return ''
    a, b = S['start'], S['end']
    seg = S['nums'][a:b + 1]
    base = f"`nums[{a}..{b}] = {seg}`：`s = {S['s']}`，`length = {S['length']}`"
    if ln in (13, 14, 15):
        ok = S['l'] <= S['length'] <= S['r'] and S['s'] > 0
        return base + ('，长度和和都符合' if ok else '')
    return base


def _cond(S, B, ret):
    ok_len = S.l <= S.length <= S.r
    if not ok_len:
        why = f'长度 `{S.length}` 不在 `[{S.l}, {S.r}]` 里'
        return f'{why} → ==不满足==，跳过'
    if S.s <= 0:
        return f'长度 `{S.length}` 合格，但和 `s = {S.s}` 不大于 0 → ==不满足==，跳过'
    return f'长度 `{S.length}` 在 `[{S.l}, {S.r}]`，和 `s = {S.s}` 大于 0 → ==满足==，可以拿来更新答案'


def _res_cond(S, B, ret):
    if S.res == -1:
        return '`res == -1`：还没有答案，直接记下这个正和'
    if S.res > S.s:
        return f'`res = {S.res} > s = {S.s}`：这个正和更小 → 更新'
    return f'`res = {S.res} ≤ s = {S.s}`：已有的答案更小，不更新'


def _win_c(S, i, v):
    if 'start' not in S or 'end' not in S:
        return None
    if S['start'] <= i <= S['end'] and S['_line'] >= 10:
        return 'blue' if i == S['end'] else 'cyan'
    return None


CONFIG = dict(
    num=3364, title='最小正和子数组', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='暴力枚举 · 起点固定、终点累加',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def minimumSumSubarray(self, nums, l, r):
        
        n = len(nums)
        res = -1
        for start in range(n):
            s = 0
            length = 0
            for end in range(start, n):
                s += nums[end]
                length += 1

                if l <= length <= r and s > 0:
                    if res == -1 or res > s:
                        res = s
        
        return res
''',
    call='Solution().minimumSumSubarray([5, -1, 2, -3], 2, 3)',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（框 = nums[start..end]，蓝 = 终点）', cell=96,
             pointers={'start': 'pink', 'end if _line in (9, 10, 11, 13, 14, 15) else None': 'blue'},
             pointer_labels={'end if _line in (9, 10, 11, 13, 14, 15) else None': 'end'},
             window=('start if _line in (9, 10, 11, 13, 14, 15) else None', 'end'), color=_win_c, h=230),
        dict(type='text', h=80, size=30, fn=lambda S: (f"长度范围 `l = {S['l']}` ~ `r = {S['r']}`，目前最小正和 `res = {S['res']}`" if 'res' in S else '要找长度在 `l ~ r`、和大于 0 的最小子数组和')),
        dict(type='text', h=120, size=28, fn=_txt),
    ],
    watch=[('start', 'start', 'pink'), ('end', 'end', 'blue'), ('s', 's', 'cyan'), ('length', 'length', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '数据规模很小（`n ≤ 100`），直接暴力枚举：`n = {n}`',
        'res = -1': '`res = -1`：没找到合法子数组就返回 -1，同时当作“还没有答案”的标记',
        'for start in': lambda S, B, r_: (f'枚举起点 `start = {S.start}`' if 'start' in S and ('start' not in B or S.start != B.start)
                                          else '所有起点都试完了'),
        's = 0': '起点换了，子数组和 `s` 清零',
        'length = 0': '子数组长度 `length` 也清零',
        'for end in': lambda S, B, r_: (f'终点 `end = {S.end}`：子数组变成 `nums[{S.start}..{S.end}]`' if B.length == 0 or S.end != B.end
                                        else '这个起点的终点都走完了'),
        's += nums[end]': '`s += nums[{end}]` → `s = {s}`：不用重算，沿用上一个终点的和',
        'length += 1': '长度加 1 → `length = {length}`',
        'if l <= length <= r and s > 0': _cond,
        'if res == -1 or res > s': _res_cond,
        'res = s': '`res = {res}`：目前最小的正和',
        'return res': lambda S, B, r_: (f'返回 `{S.res}`' if S.res != -1 else '没有合法子数组，返回 `-1`'),
    },
    max_steps=90,
    cards=dict(
        one_liner='数据范围小，枚举起点终点，边累加边判断',
        complexity='时间 `O(n^2)`，空间 `O(1)`',
        problem=['给 `nums` 和 `l`、`r`，找长度在 `l ~ r` 之间、和 ==大于 0== 的子数组',
                 '返回这些子数组里 ==最小的和==，不存在返回 `-1`',
                 '本视频：`[5,-1,2,-3], l=2, r=3` → `1`（`[-1,2]`）'],
        quote='本题的数据规模比较小，因此可以直接暴力枚举子数组的起点和终点并计算子数组和。若子数组长度达标，就用子数组和更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['外层枚举起点 `start`，内层终点 `end` 一路向右，`s` 随之累加',
              '`length` 同步加 1，只有 `l ≤ length ≤ r` 且 `s > 0` 才算候选',
              '`res` 初值 -1 兼作“没有答案”：为 -1 或更大时才替换成当前和'],
        summary=['时间 `O(n^2)`，空间 `O(1)`；`n ≤ 100` 完全够用',
                 '`res = -1` 是哨兵：判断 `res == -1 or res > s`，不能写成只看 `res > s`',
                 '和 `s` 必须严格大于 0，等于 0 不算',
                 '内层的和是累加得到的，不用每次重新求和',
                 '代码与原文一致，Python 3 可直接运行'],
    ),
)
