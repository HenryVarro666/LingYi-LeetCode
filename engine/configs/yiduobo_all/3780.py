def _tbl(S):
    if 'third' not in S:
        return [[None] * 3 for _ in range(3)]
    return [list(S['first']), list(S['second']), list(S['third'])]


def _col(S, rr, cc, v):
    r = S.get('r')
    v0 = S.get('v')
    if r is not None and cc == r and S.get('_line', 0) in (11, 13, 15):
        return 'yellow' if v == v0 else 'blue'
    return None


def _txt(S):
    v, r = S.get('v'), S.get('r')
    if v is None or r is None or S.get('_line', 0) > 16:
        return '按余数分三组，每组只留最大、次大、第三大的数'
    return f'`v = {v}`，`{v} % 3 = {r}` → 放进余数 =={r}== 这一列'


def _combo(S):
    if S.get('_line', 0) >= 19 and 'res' in S:
        return f"当前答案 `res` = =={S['res']}=="
    return ''


CONFIG = dict(
    num=3780, title='能被 3 整除的三元组最大和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按模 3 余数分组 · 每组留前三大',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def maximumSum(self, nums):
        
        first = [None] * 3
        second = [None] * 3
        third = [None] * 3
        for v in nums:
            r = v % 3
            if first[r] is None or first[r] < v:
                first[r], second[r], third[r] = v, first[r], second[r]
            elif second[r] is None or second[r] < v:
                second[r], third[r] = v, second[r]
            elif third[r] is None or third[r] < v:
                third[r] = v
        
        res = 0
        for r in range(3):
            if third[r] is not None:
                res = max(res, first[r] + second[r] + third[r])
        
        if first[0] is not None and first[1] is not None and first[2] is not None:
            res = max(res, first[0] + first[1] + first[2])
        
        return res
''',
    call='Solution().maximumSum([4, 2, 3, 1, 7, 5, 6, 9])',
    expect=21,
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前 v）', cell=70, h=150, color=lambda S, i, v: 'yellow' if S.get('_line', 0) < 17 and v == S.get('v') else None),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='table', var=_tbl, label='每个余数里最大 / 次大 / 第三大（黄 = 刚放入的数）', h=300, cell=100,
             rows=lambda S: ['最大', '次大', '第三'], cols=lambda S: ['余 0', '余 1', '余 2'],
             color=_col, fmt=lambda v: '-' if v is None else str(v)),
        dict(type='text', fn=_combo, size=26, h=50),
    ],
    watch=[('v', 'v', 'yellow'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        'first = [None]': '三个数组：`first / second / third` 记录每个余数里==最大、次大、第三大==，`None` 表示还没有',
        'for v in nums': lambda S, B, r: (f'看 `v = {S.v}`' if S.get('_line') == 7 and 'res' not in S and S.get('v') != B.get('v') else '所有数都归过组了，遍历结束'),
        'r = v % 3': '`{v} % 3 = {r}`，它属于余数 `{r}` 这一组',
        'if first[r] is None': lambda S, B, r: (f'`v = {S.v}`：这组还没有数 → 直接成为最大' if B.first[S.r] is None else f'`v = {S.v}` 比这组最大的 `{B.first[S.r]}` 大吗？'),
        'first[r], second[r], third[r] = v': '`{v}` 成为新的最大，原最大、次大各后移一位：现在 first / second / third = `{first[r]}, {second[r]}, {third[r]}`',
        'elif second[r] is None': lambda S, B, r: (f'`v = {S.v}` 不比最大的大；这组还没有次大 → 它就是次大' if B.second[S.r] is None else f'`v = {S.v}` 不比最大的大，那比次大的 `{B.second[S.r]}` 大吗？'),
        'second[r], third[r] = v': '`{v}` 成为新的次大，原次大后移成第三大：`{second[r]}, {third[r]}`',
        'elif third[r] is None': lambda S, B, r: (f'`v = {S.v}` 不比前两大的大；这组还没有第三大 → 它就是第三大' if B.third[S.r] is None else f'`v = {S.v}` 不比前两大的大，那比第三大的 `{B.third[S.r]}` 大吗？'),
        'third[r] = v': '`{v}` 成为新的第三大：`third[{r}] = {third[r]}`',
        'res = 0': '`res = 0`：找不到三元组就返回 0',
        'for r in range(3)': '逐个余数检查（情况一、二、三）：同余的三个数之和必被 3 整除',
        'if third[r] is not None': lambda S, B, r: (f'余数 `{S.r}` 这一组凑齐三个数了吗？' + ('凑齐了' if S.third[S.r] is not None else '没有，跳过')),
        'res = max(res, first[r]': '三个同余数之和 `{first[r]} + {second[r]} + {third[r]}` = {first[r] + second[r] + third[r]}，更新 `res` = =={res}==',
        'if first[0] is not None': lambda S, B, r: ('情况四：余数 0、1、2 各取最大的一个，和也被 3 整除；三组都有数吗？'
                                                      + ('有' if None not in (S.first[0], S.first[1], S.first[2]) else '没有，跳过')),
        'res = max(res, first[0]': '余数 0、1、2 各取最大：`{first[0]} + {first[1]} + {first[2]}` = {first[0] + first[1] + first[2]}，`res` = =={res}==',
        'return res': '四种情况取最大，答案 =={res}==',
    },
    cards=dict(
        one_liner='三数之和被 3 整除，只有四种余数组合：同余 ×3，或 0、1、2 各一个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你正整数数组 `nums`，选==恰好三个==数，使它们的和能被 3 整除',
                 '返回最大和；不存在则返回 `0`',
                 '示例：`[4,2,3,1]` → `9`；本视频：`[4,2,3,1,7,5,6,9]`'],
        quote='首先考察哪些三元组之和是3的倍数。对于这类问题，通常可以基于余数进行考虑，一共有四种情况：……',
        quote_src='—— yiduobo 题解原文',
        idea=['余数组合：`0+0+0`、`1+1+1`、`2+2+2`、`0+1+2`，和都被 3 整除',
              '同余的情况只要每组最大的三个；余数各异只要每组最大的一个',
              '一趟遍历维护每个余数的 `first / second / third`，最后四种情况取最大'],
        summary=['时间 `O(n)`，空间 `O(1)`（只存 9 个数）',
                 '易错：插入新数时要把原来的最大、次大依次后移，别漏掉 `third`',
                 '`None` 表示该余数组数量不足，求和前必须判空',
                 '对比灵神：他用二维 0-1 背包 DP 通用地做；这里用余数分类，直接贪心'],
    ),
)
