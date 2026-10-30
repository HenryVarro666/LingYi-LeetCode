TOPS = [2, 1, 2, 4, 2, 2]
BOTS = [5, 2, 6, 2, 3, 2]


def _col(S, i, v):
    if 'index' in S and i == S['index']:
        return 'blue'
    return None


def _info(S):
    if 'cnt_A' not in S:
        return '目标只有 `A[0]` 或 `B[0]`，一趟遍历同时统计两边'
    return (f"匹配 `A[0]={S['A'][0]}`：{'可行' if S['flag_A'] else '==不可行=='}，`cnt_A={S['cnt_A']}`，`both_A={S['both_A']}`　|　"
            f"匹配 `B[0]={S['B'][0]}`：{'可行' if S['flag_B'] else '==不可行=='}，`cnt_B={S['cnt_B']}`，`both_B={S['both_B']}`")


CONFIG = dict(
    num=1007, title='行相等的最少多米诺旋转', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历 · 翻转集合 R 与 both 计数',
    tags=['灵神题单·贪心与思维', '难度分 1541'],
    code='''
class Solution(object):
    def minDominoRotations(self, A, B):

        flag_A = flag_B = True
        cnt_A = cnt_B = 0
        both_A = both_B = 0

        for index in range(1, len(A)):
            if flag_A:
                if A[index] == A[0]:
                    if B[index] == A[0]:
                        both_A += 1
                elif B[index] == A[0]:
                    cnt_A += 1
                else:
                    flag_A = False

            if flag_B:
                if B[index] == B[0]:
                    if A[index] == B[0]:
                        both_B += 1
                elif A[index] == B[0]:
                    cnt_B += 1
                else:
                    flag_B = False

        res = len(A) + 1

        if flag_A:
            res = min(res, cnt_A, len(A) - both_A - cnt_A)
        
        if flag_B:
            res = min(res, cnt_B, len(A) - both_B - cnt_B)
        
        if res > len(A):
            res = -1

        return res
''',
    call=f'Solution().minDominoRotations({TOPS}, {BOTS})',
    expect=2,
    skip=['flag_A = flag_B', 'cnt_A = cnt_B', 'both_A = both_B', 'res = len(A) + 1'],
    views=[
        dict(type='array', var='A', label='A（蓝框 = 当前下标）', cell=96, h=190, color=_col, pointers={'index': 'blue'}),
        dict(type='array', var='B', label='B', cell=96, h=190, color=_col),
        dict(type='text', h=110, size=26, fn=_info),
    ],
    watch=[('index', 'index', 'blue'), ('cnt_A', 'cnt_A', 'blue'), ('both_A', 'both_A'), ('cnt_B', 'cnt_B', 'pink'),
           ('both_B', 'both_B'), ('res', 'res', 'green')],
    captions={
        'for index in range': lambda S, B, r: (f'下标 `index = {S.index}`：这张牌上 `{S.A[S.index]}`、下 `{S.B[S.index]}`，同时检查两个目标' if 'index' in S else '遍历完成，开始比较两个目标'),
        11: lambda S, B, r: (f'`B[{S.index}] = {S.B[S.index]}` 等于 `A[0]`：上下都是目标' if S.B[S.index] == S.A[0] else f'`B[{S.index}] = {S.B[S.index]}` ≠ `A[0]`：不是 both'),
        'if flag_A': lambda S, B, r: (('`A[0]` 这条路还没被否决，继续检查' if S.flag_A else '`A[0]` 这条路已经不可行，跳过') if S._line < 20 else ('`A[0]` 可行 → 计算它的代价' if S.flag_A else '`A[0]` 不可行 → 不参与比较')),
        'if A[index] == A[0]': lambda S, B, r: (f'`A[{S.index}] = {S.A[S.index]}` 等于 `A[0] = {S.A[0]}`：上半已匹配，不用翻' if S.A[S.index] == S.A[0]
                                                 else f'`A[{S.index}] = {S.A[S.index]}` ≠ `A[0] = {S.A[0]}`：上半没匹配，看下半'),
        'both_A += 1': '上下都等于 `A[0]`：无论 `A[0]` 翻不翻都不用转这张 → `both_A = {both_A}`',
        'elif B[index] == A[0]': lambda S, B, r: (f'下半 `B[{S.index}] = {S.B[S.index]}` = `A[0]`：翻这张就能匹配' if S.B[S.index] == S.A[0]
                                                   else f'下半 `B[{S.index}] = {S.B[S.index]}` 也 ≠ `A[0]`：翻不翻都匹配不了'),
        'cnt_A += 1': '这张必须翻（属于集合 R_A）→ `cnt_A = {cnt_A}`',
        'flag_A = False': '这张牌凑不出 `A[0]` → 匹配 `A[0]` ==不可行==',
        'if flag_B': lambda S, B, r: (('`B[0]` 这条路还没被否决，继续检查' if S.flag_B else '`B[0]` 这条路已经不可行，跳过') if S._line < 30 else ('`B[0]` 可行 → 计算它的代价' if S.flag_B else '`B[0]` 不可行 → 不参与比较')),
        'if B[index] == B[0]': lambda S, B, r: (f'`B[{S.index}] = {S.B[S.index]}` 等于 `B[0] = {S.B[0]}`：下半已匹配' if S.B[S.index] == S.B[0]
                                                 else f'`B[{S.index}] = {S.B[S.index]}` ≠ `B[0] = {S.B[0]}`：看上半'),
        'both_B += 1': '上下都等于 `B[0]` → `both_B = {both_B}`',
        'elif A[index] == B[0]': lambda S, B, r: (f'上半 `A[{S.index}] = {S.A[S.index]}` = `B[0]`：翻这张就能匹配' if S.A[S.index] == S.B[0]
                                                   else f'上半 `A[{S.index}] = {S.A[S.index]}` 也 ≠ `B[0]`：无法匹配'),
        'cnt_B += 1': '这张必须翻（属于集合 R_B）→ `cnt_B = {cnt_B}`',
        'flag_B = False': '这张牌凑不出 `B[0]` → 匹配 `B[0]` ==不可行==',
        'res = min(res, cnt_A': '匹配 `A[0]`：翻 R_A（`{cnt_A}` 次）或翻其余（`{len(A)} − {both_A} − {cnt_A} = {len(A) - both_A - cnt_A}` 次），取小 → `res = {res}`',
        'res = min(res, cnt_B': '匹配 `B[0]`：翻 R_B（`{cnt_B}` 次）或翻其余（`{len(A)} − {both_B} − {cnt_B}`），取小 → `res = {res}`',
        'if res > len(A)': lambda S, B, r: ('`res` 还是初始值 `len(A)+1`：两个目标都不可行 → 改成 `-1`' if S.res > len(S.A) else '`res` 有合法值，保留'),
        'return res': '最少旋转次数 `{res}`',
    },
    cards=dict(
        one_liner='目标只有 A[0] 或 B[0]：统计「必须翻的数量」，翻它或翻其余取小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每张多米诺上下各有一个 1–6 的数，可以旋转交换',
                 '求让某一排全相同的最少旋转次数，不行返回 `-1`',
                 '示例：`A=[2,1,2,4,2,2]`，`B=[5,2,6,2,3,2]` → `2`'],
        quote='对于情况1而言，就是A[0]之后部分骨牌执行翻转操作……我们也可以将除了R_A[0]之外的骨牌进行翻转，那么此时就得到了情况2，翻转的次数为==n - len(R_A[0]) - both_A[0]==。',
        quote_src='—— yiduobo 题解原文',
        idea=['匹配目标只有 `A[0]` 或 `B[0]`，各有「不翻首牌」「翻首牌」两种情况，互相对称',
              '`R` = 必须翻的牌的集合；`both` = 上下都等于目标的牌（不用翻）',
              '一种情况翻 `len(R)` 次，对称的情况翻 `n − len(R) − both` 次',
              '遍历时若遇到凑不出目标的牌，该目标不可行'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：对称情况的次数要减去 `both`，那些牌上下都是目标，哪边都不用翻',
                 '循环从 `index = 1` 开始，首牌自己不计入 `cnt` 和 `both`',
                 '`res` 初始为 `len(A) + 1`，最后大于 `len(A)` 就说明无解',
                 '原文已是 Python 3 可运行写法，代码未改'],
    ),
)
