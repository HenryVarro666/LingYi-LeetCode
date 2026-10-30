def _idx(S):
    if 'num' not in S or 'last_num' not in S:
        return None
    A = S['A']
    for k in range(1, len(A)):
        if A[k] == S['num'] and A[k - 1] == S['last_num']:
            return k
    return None


def _prev(S):
    k = _idx(S)
    return None if k is None else k - 1


CONFIG = dict(
    num=896, title='单调数列', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一次遍历 + 方向标记 flag',
    tags=[],
    code='''
class Solution(object):
    def isMonotonic(self, A):

        if len(A) <= 2:
            return True
        
        flag = None
        last_num = A[0]
        for num in A[1:]:
            if num == last_num:
                continue
            if flag is None:
                flag = num > last_num
            elif (num > last_num) != flag:
                return False
            last_num = num

        return True
''',
    call='Solution().isMonotonic([6, 5, 4, 4, 7])',
    expect=False,
    views=[
        dict(type='array', var='A', h=230, label='A（蓝 = last_num，黄 = 当前 num）',
             color=lambda S, i, v: 'yellow' if i == _idx(S) else ('blue' if i == _prev(S) else None)),
        dict(type='text', size=30, fn=lambda S: ('' if 'flag' not in S else
             '方向还没确定（flag = None）' if S['flag'] is None else
             ('方向：==递增==（flag = True）' if S['flag'] else '方向：==递减==（flag = False）'))),
    ],
    watch=['last_num', 'num', ('flag', 'flag', 'cyan')],
    captions={
        'len(A) <= 2': lambda S, B, r: f'长度 `{len(S.A)}` > 2 → 继续检查' if len(S.A) > 2 else '长度不超过 2，一定单调 → 直接返回',
        'flag = None': '`flag` 记录方向：`None` 还没定，`True` 递增，`False` 递减',
        'last_num = A[0]': '`last_num` 保存前一个数，从 `A[0] = {last_num}` 开始',
        'for num in A[1:]': '看下一个数 `num = {num}`，前一个是 `{last_num}`',
        'if num == last_num': lambda S, B, r: (f'`{S.num} == {S.last_num}` → 相等对递增递减都合法，跳过' if S.num == S.last_num else f'`{S.num} != {S.last_num}` → 要比较方向'),
        'continue': '相等不改变方向，直接看下一个数',
        'if flag is None': lambda S, B, r: ('`flag` 还是 `None` → 这是第一次出现不相等，由它定方向' if S.flag is None else f'`flag` 已定为 `{S.flag}`，要检查新方向是否一致'),
        'flag = num > last_num': '`{num} > {last_num}` 是 `{flag}` → 序列是=={"递增" if flag else "递减"}==的',
        'elif (num': lambda S, B, r: (f'`({S.num} > {S.last_num}) = {S.num > S.last_num}` 与 `flag = {S.flag}` 不同 → ==方向矛盾==' if (S.num > S.last_num) != S.flag else f'`({S.num} > {S.last_num}) = {S.num > S.last_num}` 与 `flag = {S.flag}` 一致 → 合法'),
        'return False': '方向和 `flag` 矛盾：先降后升，不是单调数列 → 返回 `False`',
        'last_num = num': '`last_num` 更新为 `{last_num}`，继续比较下一对',
        'return True': '整个数组都没有矛盾 → 返回 `True`',
    },
    cards=dict(
        one_liner='用 flag 记住方向，出现反向就不是单调',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数组单调递增（`A[i] <= A[j]`）或单调递减（`A[i] >= A[j]`）才算单调',
                 '给定整数数组 `A`，是单调的就返回 `true`，否则返回 `false`',
                 '示例：`[1,2,2,3]` → `true`；本视频：`[6,5,4,4,7]` → `false`'],
        quote='可以使用一个标记flag表示当前序列是递增还是递减的，初始化为空，然后从头开始往后遍历整个数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['相等的相邻数，递增递减都合法，直接跳过',
              '第一次出现不等：`flag` 为空，按大小关系设定方向',
              '之后每次不等：新方向和 `flag` 不一致，就返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '相等要 `continue`，且不能让相等的数把 `flag` 设成 `False`',
                 '`last_num` 在相等时不用更新（值本来就一样）',
                 '长度 ≤ 2 的数组一定单调，提前返回'],
    ),
)
