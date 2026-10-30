W = 4


def _bits(S):
    return [(S['n'] >> (W - 1 - i)) & 1 for i in range(W)]


def _top(S):
    n = S['n']
    return W - 1 - (n.bit_length() - 1) if n > 0 else None


def _pp(S):
    return S.get('p') if S['_line'] >= 10 else None


def _txt(S):
    n = S['n']
    if 'res' not in S:
        return f"`n` = `{n:0{W}b}`"
    return f"`n` = `{n:0{W}b}`；`res` = ==`{S['res']}`=="


CONFIG = dict(
    num=1611, title='使整数变为 0 的最少操作次数', difficulty='Hard', category='位运算',
    author='yiduobo', technique='从 0 倒推找规律 · 首尾配对 · 逐位正负交替',
    tags=['位运算', '贪心与思维'],
    code='''
class Solution(object):
    def minimumOneBitOperations(self, n):

        pow2 = [1]
        while pow2[-1] < n:
            pow2.append(pow2[-1] + pow2[-1])
        
        p = len(pow2) - 1
        res = 0
        flag = 1
        while n > 0:
            while p > 0 and pow2[p] > n:
                p -= 1
            
            res += flag * (pow2[p] + pow2[p] - 1)
            flag = -flag
            n -= pow2[p]

        return res
''',
    call='Solution().minimumOneBitOperations(13)',
    expect=9,
    views=[
        dict(type='text', fn=_txt, size=30, h=70),
        dict(type='array', var=_bits, label='n 的二进制（从高位到低位：8 4 2 1），蓝 = 当前最高位的 1', cell=84, h=190,
             pointers={_top: 'blue'}, pointer_labels={_top: 'top'},
             color=lambda S, i, v: 'green' if v else None, dim=lambda S, i, v: not v),
        dict(type='array', var='pow2', label='pow2（2 的幂表）', cell=84, h=190,
             pointers={_pp: 'pink'}, pointer_labels={_pp: 'p'}),
    ],
    watch=[('n', 'n', 'cyan'), ('p', 'p', 'pink'), ('flag', 'flag', 'purple'), ('res', 'res', 'green')],
    skip=['pow2 = [1]', 'p -= 1'],
    captions={
        'while pow2[-1] < n': lambda S, B, r: (f'`pow2[-1] = {S.pow2[-1]} < n = {S.n}`：还不够大，继续翻倍' if S.pow2[-1] < S.n
                                               else f'`pow2[-1] = {S.pow2[-1]} >= n = {S.n}`：2 的幂表够用了'),
        'pow2.append': '追加 `{pow2[-1]}`，表是 `{pow2}`',
        'p = len(pow2) - 1': '`p` 指向表末尾：`2^p = {pow2[p]}`',
        'res = 0': '`res` 累计答案',
        'flag = 1': '`flag` 是符号：奇数轮 `+`，偶数轮 `-`',
        'while n > 0': lambda S, B, r: (f'`n = {S.n} > 0`：还要拆最高位' if S.n > 0 else '`n = 0`：每一位都拆完'),
        'while p > 0 and pow2[p] > n': lambda S, B, r: (f'`2^{S.p} = {S.pow2[S.p]} > n = {S.n}`：太大，`p` 减一' if S.p > 0 and S.pow2[S.p] > S.n else f'`2^{S.p} = {S.pow2[S.p]} <= n = {S.n}`：这就是最大的 `2^k <= n`'),
        'res += flag': '`x` 与 `x - 2^k` 配对，步数之和是 `2^(k+1) - 1`：`res += {B.flag} × ({pow2[p]}×2 - 1)` → ==`{res}`==',
        'flag = -flag': '下一轮符号反过来：`flag = {flag}`（`2^(k+1)-1-y` 里的 `y` 带负号）',
        'n -= pow2[p]': '去掉最高位的 1：`n` → `{n}`',
        'return res': '最终答案 ==`{res}`==',
    },
    cards=dict(
        one_liner='首尾配对：x 与 x−2^k 的步数加起来是 2^(k+1)−1',
        complexity='时间 `O(log n)`，空间 `O(log n)`（`pow2` 表）',
        problem=['操作 1：翻转最低位；操作 2：若第 `i-1` 位是 1 且更低位全 0，翻转第 `i` 位',
                 '求把 `n` 变成 `0` 的最少操作次数',
                 '示例：`n = 3` → `2`；`n = 6` → `4`；本视频 `n = 13`'],
        quote='x与x- 2^k需要的步数分别为2^(k + 1) - 1 - y以及y。',
        quote_src='—— yiduobo 题解原文',
        idea=['直接分类推导想不清，改成从 `0000` 往后倒推，列出 4 位的 15 步',
              '头尾配对：`0000/1000` 是 0 和 15 步，`0001/1001` 是 1 和 14 步，加起来都是 `2^(k+1)-1`',
              '所以 `f(x) = 2^(k+1) - 1 - f(x - 2^k)`，逐位拆开就是奇数项加、偶数项减'],
        summary=['时间 `O(log n)`；`flag` 在 `+1/-1` 间交替',
                 '易错点：内层 `while p > 0 and pow2[p] > n` 要找最大的 `2^k <= n`',
                 '本题原文代码本身可在 Python 3 运行，未改动',
                 '对比灵神：他从最低位的 1 往上用 `lb×2-1-ans`，这里从最高位往下按符号累加，结果一样'],
    ),
)
