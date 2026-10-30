N0 = '0110'


def _T(L, n):
    """left/right 列表 -> 2 行 n 列（行：变成 0 / 变成 1），没算到的格子留空"""
    r0 = [l[0] for l in L] + [''] * (n - len(L))
    r1 = [l[1] for l in L] + [''] * (n - len(L))
    return [r0, r1]


def _left(S):
    return _T(S['left'], len(S['s'])) if 'left' in S else [[''] * len(S['s'])] * 2


def _right(S):
    n = len(S['s'])
    R = S.get('right', [])
    if S.get('_line', 0) >= 20:   # reverse() 之后与下标对齐
        return _T(R, n)
    # 建表时 right 是倒序追加的（right[0] 对应下标 n-1）：先按倒序放到右侧
    k = len(R)
    return [[''] * (n - k) + [l[0] for l in R[::-1]], [''] * (n - k) + [l[1] for l in R[::-1]]]


def _txt(S):
    if 'cut_pos' in S:
        c = S['cut_pos']
        return f"切点 `{c}`：前缀 `s[0..{c}]` + 后缀 `s[{c+1}..]`，当前最小 `res = {S['res']}`"
    if 'right' in S and 'index' in S:
        return '后缀同理（对称）：`right[i][v]` = 把 `s[i..]` 全变成 `v` 的最小成本'
    if 'left' in S and 'index' in S:
        return '`left[i][v]` = 只用前缀翻转，把 `s[0..i]` 全变成 `v` 的最小成本'
    return '前缀翻转区间与后缀翻转区间不会重叠 → 枚举切点，前缀/后缀各自 DP'


CONFIG = dict(
    num=2712, title='使所有字符相等的最小成本', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='前后缀 DP · 枚举切点',
    tags=['灵神题单', '贪心与思维', '难度分 1791'],
    code='''
class Solution(object):
    def minimumCost(self, s):

        n = len(s)
        left = [[int(s[0]), 1 - int(s[0])]]
        for index in range(1, len(s)):
            char = s[index]
            if char == '0':
                left.append([left[-1][0], left[-1][0] + index + 1])
            else:
                left.append([left[-1][1] + index + 1, left[-1][1]])
        
        right = [[int(s[-1]), 1 - int(s[-1])]]
        for index in range(len(s) - 2, -1, -1):
            char = s[index]
            if char == '0':
                right.append([right[-1][0], right[-1][0] + len(s) - index])
            else:
                right.append([right[-1][1] + len(s) - index, right[-1][1]])
        right.reverse()
        
        res = min(min(left[-1]), min(right[0]))
        for cut_pos in range(len(s) - 1):
            res = min(res, left[cut_pos][0] + right[cut_pos + 1][0], left[cut_pos][1] + right[cut_pos + 1][1])
        
        return res
''',
    call="Solution().minimumCost('0110')",
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var='s', h=230, label='s',
             pointers={'index': 'blue', 'cut_pos': 'pink'}),
        dict(type='table', var=_left, label='left[i]：前缀 s[0..i] 变成 0 / 1 的最小成本', h=170, cell=64,
             rows=['变0', '变1'], cols=lambda S: list(range(len(S['s'])))),
        dict(type='table', var=_right, label='right[i]：后缀 s[i..] 变成 0 / 1 的最小成本', h=170, cell=64,
             rows=['变0', '变1'], cols=lambda S: list(range(len(S['s'])))),
    ],
    watch=[('index', 'index', 'blue'), ('cut_pos', 'cut_pos', 'pink'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {len(s)}`',
        'left = [[': '边界：`s[0]` 本身是 `{s[0]}`，变成它自己成本 0，变成另一个要翻一次，成本 1',
        'char = s[index]': '看 `s[{index}] = {char}`',
        'if char': lambda S, B, r: '`char = %s`：%s' % (S.char, ('本来就是 0，变 0 无需操作；变 1 要先把%s都变 0，再翻整个%s' if S.char == '0' else '本来就是 1，变 1 无需操作；变 0 要先把%s都变 1，再翻整个%s') % (('左边', '前缀') if S['_line'] < 13 else ('右边', '后缀'))),
        'left.append': '`left[{index}] = {left[-1]}`（变 0, 变 1 的最小成本）',
        'right = [[': '后缀边界：`s[-1] = {s[-1]}`',
        'right.append': '`right` 追加一项 `{right[-1]}`（对应下标 {index}，建表是倒序放入的）',
        'right.reverse': '`right` 倒过来，使 `right[i]` 对应 `s[i..]`',
        'res = min(min': '不切分（整串都用前缀翻或都用后缀翻）：`res = {res}`',
        'for cut_pos': '枚举切点 `cut_pos`：前缀 `[0..cut_pos]` 与后缀 `[cut_pos+1..]` 变成同一个数',
        'res = min(res': '切点 `{cut_pos}`：变 0 = `{left[cut_pos][0]} + {right[cut_pos + 1][0]}`，变 1 = `{left[cut_pos][1]} + {right[cut_pos + 1][1]}` → `res = {res}`',
        'return res': '所有切点枚举完，最小成本 ==res = {res}==',
    },
    cards=dict(
        one_liner='前缀翻转和后缀翻转不重叠：前后缀各做 DP，再枚举切点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制串，可翻转一个前缀或后缀，代价是翻转的长度',
                 '求把整串变成全 0 或全 1 的最小代价',
                 '本视频：`"0110"` → `2`'],
        quote='所有对前缀翻转的区间与所有对后缀翻转的区间是不可能重叠的，因为对于重叠的区间，翻转两次相当于没有翻转，相当于浪费了两倍重叠长度的代价。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left[i][v]`：只靠前缀翻转把 `s[0..i]` 变成 `v` 的最小成本；`right` 对称',
              '`s[i]` 已是目标：沿用 `left[i-1]`；不是：先把左边变成它，再翻整段前缀，加 `i+1`',
              '枚举切点 `cut_pos`，取 `left+right` 在 0/1 两种目标下的较小值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`right` 是倒序追加的，最后要 `reverse()` 才和下标对齐',
                 '别忘了不切分的情况：`min(left[-1], right[0])`',
                 '原文为 Python 2 风格，代码未做改动',
                 '对比灵神：灵神发现相邻不同处互相独立，直接累加 `min(i, n-i)`，`O(1)` 空间'],
    ),
)
