N = 13
_STATES = [list(range(1, N + 1))]
while len(_STATES[-1]) > 1:
    _k = len(_STATES)
    _STATES.append(_STATES[-1][::2] if _k % 2 == 1 else _STATES[-1][::-1][::2][::-1])


def _r(S):
    d = S.get('d')
    if d is None:
        return 0
    r = d.bit_length() - 1
    if S['_line'] in (8, 15):
        r -= 1
    return max(0, min(r, len(_STATES) - 1))


def _seq(S):
    return _STATES[_r(S)]


def _dim(S, i, v):
    L = len(_seq(S))
    if L <= 1:
        return False
    if S['_line'] in (7, 8):
        return i % 2 == 1
    if S['_line'] in (13, 14, 15):
        return (L - 1 - i) % 2 == 1
    return False


def _top(S):
    if 'd' not in S:
        return ''
    ln = S['_line']
    op = '操作 1（从左删）' if ln in (7, 8, 9, 10) else '操作 2（从右删）' if ln in (13, 14, 15, 16) else ''
    return f"首项 `a = {S['a']}`，公差 `d = {S['d']}`，项数 `cnt = {S['cnt']}`" + (f'　→　{op}' if op else '')


CONFIG = dict(
    num=3782, title='交替删除操作后最后剩下的整数', difficulty='Hard', category='位运算',
    author='yiduobo', technique='维护 首项 / 公差 / 项数',
    tags=['灵神题单', '位运算', '难度分 2074'],
    code='''
class Solution(object):
    def lastInteger(self, n):
        
        a = 1
        d = 1
        cnt = n
        while cnt > 1:
            d += d
            cnt = (cnt + 1) // 2
            if cnt == 1:
                break
            
            if cnt % 2 == 0:
                a += d
            d += d
            cnt = (cnt + 1) // 2
        
        return a
''',
    call='Solution().lastInteger(13)',
    expect=9,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var=_seq, label='当前剩下的数（蓝 = 首项 a，灰 = 这次操作要删掉的）', cell=84, h=300,
             dim=_dim, color=lambda S, i, v: 'blue' if v == S.get('a') else None),
    ],
    watch=[('a', 'a', 'blue'), ('d', 'd', 'yellow'), ('cnt', 'cnt', 'pink')],
    captions={
        'a = 1': '`a` 是首项，一开始是 1',
        'd = 1': '`d` 是公差，一开始是 1',
        'cnt = n': '`cnt` 是项数，一开始是 `n` = {n}',
        'while cnt > 1': lambda S, B, r: (f'`cnt = {S.cnt} > 1`，还没剩一个，继续' if S.cnt > 1 else '`cnt = 1`，结束'),
        8: '从左往右删：首项不变，==公差翻倍==：`d` = {B.d} × 2 = {d}',
        9: lambda S, B, r: (f'删掉一半（奇数时多留一个）：`cnt` = ({B.cnt}+1)//2 = =={S.cnt}==' ),
        15: '从右往左删同样隔一个删一个：==公差翻倍== `d` = {B.d} × 2 = {d}',
        16: '项数同样减半：`cnt` = ({B.cnt}+1)//2 = =={cnt}==',
        'if cnt == 1': lambda S, B, r: ('只剩一项 → 答案就是 `a`，直接结束' if S.cnt == 1 else f'`cnt = {S.cnt}` 还不止一项，接着从右往左删'),
        'break': '`a` 就是最终答案',
        'if cnt % 2 == 0': lambda S, B, r: (f'从右往左删：`cnt = {S.cnt}` 是偶数 → 最后一项保留、==首项会被删掉=='
                                            if S.cnt % 2 == 0 else f'`cnt = {S.cnt}` 是奇数 → 首项和末项都保留，`a` 不变'),
        'a += d': '首项被删，新首项是原来的第二项：`a` += `d` = {d} → =={a}==',
        'return a': '最终剩下的整数 `a` = =={a}==',
    },
    cards=dict(
        one_liner='剩余元素始终是等差数列：只记首项、公差、项数',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`1..n` 排成一列，交替从左、从右「隔一个删一个」，直到只剩一个',
                 '求最后剩下的数，`n` 最大 10^15',
                 '本视频：`n = 13` → `9`'],
        quote='无论何时，剩余的元素必然都是一个等差数列，而对于等差数列，只需维护其起始值a，公差d以及项数cnt就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n` 太大不能真的删，但每次剩下的仍是等差数列 `a, a+d, a+2d, …`',
              '从左删：`a` 不变，`d` 翻倍，`cnt` 变为 `(cnt+1)//2`',
              '从右删：`cnt` 偶数时首项被删，`a += d`；奇数时 `a` 不变；`d` 翻倍，`cnt` 同样减半'],
        result='13 → 7 → 4 → 2 → 1，最后剩 `9` ✓',
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '==不反转序列==：右删时只需判断首项是否被删（`cnt` 偶数）',
                 '每轮循环做「左删、右删」两次，所以中途要检查 `cnt == 1` 提前退出',
                 '对比灵神：他每次都把序列反转，公差用 `d *= -2` 带符号，从而只写一种删法'],
    ),
)
