M = [[3, -2, 5], [-6, 4, -1], [8, 7, 9]]


def _pos(S):
    ln = S.get('_line')
    line, num = S.get('line'), S.get('num')
    if line is None or ln is None or ln < 6 or ln > 14:
        return None
    i = M.index(list(line))
    if ln == 6 or num is None or num not in line:
        return (i, None)
    return (i, list(line).index(num))


def _done(S, r, c):
    ln = S.get('_line') or 0
    if ln >= 16:
        return True
    p = _pos(S)
    if p is None:
        return False
    i, j = p
    if j is None:
        return r < i
    if (r, c) < (i, j):
        return True
    pre = sum(abs(M[a][b]) for a in range(3) for b in range(3) if (a, b) <= (i, j))
    return (r, c) == (i, j) and S.get('s') == pre


def _color(S, r, c, v):
    ln = S.get('_line') or 0
    if ln >= 16 and abs(v) == S.get('mi'):
        return 'orange'
    if _done(S, r, c):
        return 'purple' if v < 0 else 'green'
    if v < 0:
        return 'pink'
    return None


def _text(S, B):
    ln = S.get('_line') or 0
    if ln >= 19:
        return f"答案 = 绝对值之和 − 2 × mi = `45 − 2` = =={S['s']}=="
    if ln == 17:
        return f"遗留的负号给绝对值最小的格子：`{B['s']} − {S['mi']} − {S['mi']}` = =={S['s']}=="
    if ln == 16:
        return (f"负号 `cnt = {S['cnt']}` 个：两两负负得正后，==遗留 1 个==" if S['cnt'] % 2
                else f"负号 `cnt = {S['cnt']}` 个：可以全部消去")
    neg = [str(M[r][c]) for r in range(3) for c in range(3) if M[r][c] < 0 and _done(S, r, c)]
    if not neg:
        return '把所有负号==转移==到同一个格子，负负得正'
    return f"已收集的负号：{'，'.join(neg)} → 共 =={len(neg)}== 个（紫色格子）"


def _cap_line(S, B, ret):
    if S.get('line') is not None and (B.get('line') is None or list(S['line']) != list(B['line'])):
        return f"第 {M.index(list(S['line']))} 行 `{list(S['line'])}`"
    return '矩阵遍历完毕'


def _cap_num(S, B, ret):
    if 'num' in B and S['num'] == B['num']:
        return '这一行遍历完了'
    p = _pos(S)
    return f"格子 `({p[0]}, {p[1]})`：`num = {S['num']}`"


def _cap_abs(S, B, ret):
    n, mi = S.num, B.mi
    if abs(n) < mi:
        return f'`|{n}| = {abs(n)} < mi = {mi}` → 找到更小的绝对值'
    return f'`|{n}| = {abs(n)} ≥ mi = {mi}` → `mi` 不变'


CONFIG = dict(
    num=1975, title='最大方阵和', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='负号沿路径转移，集中到一个格子',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def maxMatrixSum(self, matrix):
        cnt = 0
        mi = 100001
        s = 0
        for line in matrix:
            for num in line:
                if abs(num) < mi:
                    mi = abs(num)
                if num < 0:
                    cnt += 1
                    s -= num
                else:
                    s += num

        if cnt % 2 == 1:
            s -= mi + mi

        return s
''',
    call=f'Solution().maxMatrixSum({M})',
    expect=43,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='grid', var='matrix', label='matrix（粉 = 负号，紫 = 负号已收集，绿 = 已累加，橙 = 遗留负号的落点）',
             cursors=[(lambda S: (_pos(S) or (None, None))[0], lambda S: (_pos(S) or (None, None))[1], 'yellow', 'num')],
             color=_color, cell=120, h=440),
    ],
    watch=[('num', 'num', 'yellow'), ('cnt', 'cnt', 'pink'), ('mi', 'mi', 'orange'), ('s', 's', 'green')],
    captions={
        'cnt = 0': '`cnt` 数负号个数',
        'mi = 100001': '`mi` 记最小绝对值：初值 `100001` 比任何 `|num| ≤ 10^5` 都大',
        's = 0': '`s` 累加每个格子的==绝对值==（假设负号都能消掉）',
        'for line in matrix': _cap_line,
        'for num in line': _cap_num,
        'if abs(num) < mi': _cap_abs,
        'mi = abs(num)': '更新最小绝对值：`mi` = =={mi}==',
        'if num < 0': lambda S, B, ret: (f'`{S.num} < 0` → 是负号' if S.num < 0 else f'`{S.num} ≥ 0` → 直接加'),
        'cnt += 1': '负号个数 `cnt` → {cnt}',
        's -= num': '减去负数 = 加上它的绝对值：`s -= ({num})` → `{s}`',
        's += num': '`s += {num}` → `{s}`',
        'if cnt % 2 == 1': lambda S, B, ret: (f'`cnt = {S.cnt}` 是奇数 → 负负得正后==最终遗留一个负号=='
                                               if S.cnt % 2 else f'`cnt = {S.cnt}` 是偶数 → 负号可以全部消去'),
        's -= mi + mi': '遗留的负号分配给绝对值最小的格子：`s` 先加过 `{mi}`，要变成 `−{mi}` → 减两次，=={s}==',
        'return s': '答案 = 绝对值之和 − 2 × mi = =={ret}==',
    },
    cards=dict(
        one_liner='负号可以沿路径转移：全部集中到一格，负负得正',
        complexity='时间 `O(n²)`，空间 `O(1)`',
        problem=['`n × n` 方阵，每次把==相邻==两个格子同时乘以 `-1`，可操作无数次',
                 '求操作后方阵元素和的==最大值==',
                 '示例：`[[1,-1],[-1,1]]` → `4`',
                 '本视频：`[[3,-2,5],[-6,4,-1],[8,7,9]]` → `43`'],
        quote='只需要随意画出一条从起始位置到结束位置的路径，然后延路径两两翻转相邻的格子，就能让起始位置的负号转移到结束位置了。',
        quote_src='—— yiduobo 题解原文',
        idea=['负号可以从任意格子==转移==到任意格子',
              '把所有负号都转移到同一个格子，利用负负得正消去',
              '偶数个 → 全部消去；奇数个 → 遗留一个，给绝对值最小的格子：答案 = 和 − 2·mi'],
        summary=['时间 `O(n²)`，空间 `O(1)`',
                 '`s` 直接累加绝对值：负数用 `s -= num`',
                 '易错：奇数时要减 `mi + mi`，不是只减一个 `mi`',
                 '`mi` 是全体格子的最小绝对值，可以落在正数格子上',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
