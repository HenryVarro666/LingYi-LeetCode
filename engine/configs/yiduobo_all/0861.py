A0 = [[0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 0, 0]]


def _cur(S):
    if 'i' not in S or 'j' not in S:
        return None, None
    if 'res' in S:          # 第二个循环：i 是列，j 是行
        return S['j'], S['n'] - 1 - S['i']
    return S['i'], S['n'] - 1 - S['j']


def _color(S, r, c, v):
    if 'pow2' not in S:
        return None
    if 'res' not in S and 'num' in S and r < len(S['num']) and 'i' in S and r < S['i']:
        return 'green' if S['A'][r][0] == 1 else 'purple'
    return None


def _txt(S):
    if 'res' in S:
        return f"当前累计 `res = {S['res']}`（每列的 1 要尽量多）"
    if 'num' in S and 'pow2' in S:
        return f"`num` 是每行翻转后（首位保证为 1）的十进制值：{S['num']}"
    return ''


CONFIG = dict(
    num=861, title='翻转矩阵后的得分', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='先保证首列全 1，再按列翻转',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def matrixScore(self, A):

        m = len(A)
        n = len(A[0])
        pow2 = [1]
        for index in range(1, n):
            pow2.append(pow2[-1] + pow2[-1])
        
        num = []
        for i in range(m):
            num.append(0)
            for j in range(n):
                num[-1] += pow2[j] * A[i][n - j - 1]

            if A[i][0] == 0:
                num[-1] = pow2[-1] + pow2[-1] - 1 - num[-1]
        
        res = sum(num)
        for i in range(n):
            cnt = 0
            for j in range(m):
                if num[j] & pow2[i]:
                    cnt += 1
            if cnt < m - cnt:
                res += (m - cnt - cnt) * pow2[i]
            
        return res
''',
    call=f'Solution().matrixScore({A0})',
    expect=39,
    views=[
        dict(type='text', fn=_txt),
        dict(type='grid', var='A', label='A（每行是一个二进制数，左侧高位）', h=250, cell=64,
             cursors=[(lambda S: _cur(S)[0], lambda S: _cur(S)[1], 'blue')], color=_color),
        dict(type='array', var='pow2', label='pow2（2 的幂，pow2[j] 对应从右数第 j 位）', h=140),
        dict(type='array', var='num', label='num（每行翻转后的值）', h=140),
    ],
    watch=['i', 'j', 'cnt', ('res', 'res', 'green')],
    skip=['m = len', 'n = len', 'pow2 = [1]', 'pow2.append', 'num = []', 'num.append', 'cnt = 0'],
    max_steps=95,
    captions={
        'num[-1] +=': '把第 `{i}` 行当二进制数累加：`pow2[{j}] × A[{i}][{n - j - 1}]` → `num[{i}] = {num[-1]}`',
        'if A[i][0] == 0': lambda S, B, r: (f'第 `{S.i}` 行首位是 `0`：高位为 0 太亏，==整行翻转==' if S.A[S.i][0] == 0 else f'第 `{S.i}` 行首位已经是 `1`，不用翻'),
        'num[-1] = pow2[-1]': '翻转整行 = 全 1 的值 `2^n − 1` 减去当前值 → `num[{i}] = {num[-1]}`',
        'res = sum(num)': '首列全是 1 了，先算当前总分 `res = {res}`',
        'if num[j] & pow2[i]': lambda S, B, r: (f'第 `{S.j}` 行这一位是 `1`' if S.num[S.j] & S.pow2[S.i] else f'第 `{S.j}` 行这一位是 `0`'),
        'cnt += 1': '这一列 1 的个数 `cnt = {cnt}`',
        'if cnt < m - cnt': lambda S, B, r: (f'这一列 1 有 `{S.cnt}` 个、0 有 `{S.m - S.cnt}` 个：0 更多 → ==翻转这一列==' if S.cnt < S.m - S.cnt else f'这一列 1 有 `{S.cnt}` 个，不少于 0 的 `{S.m - S.cnt}` 个 → 不翻'),
        'res += (m - cnt - cnt)': '翻转后这一列多出 `{m - cnt - cnt}` 个 1，每个值 `{pow2[i]}` → `res = {res}`',
        'return res': '最大得分 `{ret}`',
    },
    cards=dict(
        one_liner='高位压倒一切：先让每行首位都是 1，再逐列让 1 多于 0',
        complexity='时间 `O(m·n)`，空间 `O(m + n)`',
        problem=['`m × n` 的 0/1 矩阵，每次可翻转一整行或一整列（0 ↔ 1）',
                 '每行按二进制数计分（左侧高位），总分是各行之和，求最大总分',
                 '本视频：`[[0,0,1,1],[1,0,1,0],[1,1,0,0]]` → `39`'],
        quote='由于最终计算得分时，是按照每一行来计算，且左侧为高位，因此我们应当保证每一行的首位为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['首位为 0 的行：直接翻转整行（翻首列等价于翻整行再翻其余列）',
              '之后每列提供的值相同，0 比 1 多就翻转该列',
              '不真的改矩阵：翻转一行/一列只需 “`2` 的幂和 − 当前值”'],
        summary=['时间 `O(m·n)`，空间 `O(m + n)`',
                 '易错点：第一列必须先处理，且第一列不会再被翻回去（首列 1 已占多数）',
                 '列翻转的收益 = `(m − 2·cnt) × 2^位`',
                 '原文为 Python 2 写法，代码无需改动'],
    ),
)
