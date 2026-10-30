def _I(name):
    return lambda S: S['_inner'].get(name)


def _cur(S):
    d = S['_inner']
    return d.get('i'), d.get('d'), d.get('up'), d.get('is_limit')


def _txt(S):
    i, d, up, lim = _cur(S)
    if i is None:
        return '`f(i, cnt1, is_limit)`：填到第 `i` 位、已有 `cnt1` 个 1、是否贴着 `n` 的上界'
    if i == len(S['s']):
        return f"填完了：返回 `cnt1` = =={S['_inner'].get('cnt1')}=="
    cnt1 = S['_inner'].get('cnt1')
    base = f'第 {i} 位：`is_limit = {lim}`，最多填 `up = {up if up is not None else "?"}`，已有 `cnt1 = {cnt1}`'
    return base


def _cap_if(S, B, ret):
    i = S['_inner'].get('i')
    if i == len(S.s):
        return f'`i = {i} = len(s)`：==所有位都填完==，返回 `cnt1 = {S["_inner"]["cnt1"]}`——这条路径上 1 的个数'
    return f'`i = {i} < {len(S.s)}`：还没填完，继续枚举这一位'


def _cap_up(S, B, ret):
    d = S['_inner']
    if d['is_limit']:
        return f'==受约束==：前面都和 `n` 一样，这一位至多填 `s[{d["i"]}] = {d["up"]}`'
    return '==不受约束==：前面已经比 `n` 小了，这一位随便填，至多 `9`'


def _cap_res(S, B, ret):
    d = S['_inner']
    nl = d['is_limit'] and d['d'] == d['up']
    one = '，这一位填了 `1` → `cnt1` 加 1' if d['d'] == 1 else ''
    return (f'填 `d = {d["d"]}`{one}；后面 `is_limit = {nl}`'
            f'{"（仍贴着上界）" if nl else "（已经小于 n，不再受限）"} → `res = {d["res"]}`')


CONFIG = dict(
    num='LCR 162', title='数字 1 的个数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP · 记忆化搜索',
    code='''
class Solution:
    def digitOneInNumber(self, n: int) -> int:
        s = str(n)
        @cache
        def f(i: int, cnt1: int, is_limit: bool) -> int:
            if i == len(s):
                return cnt1
            res = 0
            up = int(s[i]) if is_limit else 9
            for d in range(up + 1):  # 枚举要填入的数字 d
                res += f(i + 1, cnt1 + (d == 1), is_limit and d == up)
            return res
        return f(0, 0, True)
''',
    call='Solution().digitOneInNumber(13)',
    expect=6,
    max_steps=110,
    skip=['res = 0'],
    views=[
        dict(type='string', var='s', label='s = str(n)：逐位构造，蓝框 = 正在填的位', h=170, cell=110,
             index=False,
             color=lambda S, k, v: 'blue' if k == S['_inner'].get('i') else None,
             dim=lambda S, k, v: S['_inner'].get('i') is not None and k < S['_inner'].get('i')),
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='calls', h=330),
    ],
    watch=[('i', _I('i'), 'blue'), ('cnt1', _I('cnt1'), 'orange'), ('is_limit', _I('is_limit'), 'purple'),
           ('d', _I('d'), 'yellow'), ('res', _I('res'), 'green')],
    captions={
        's = str(n)': '把 `n` 转成字符串 `s = {s!r}`，从左往右一位一位地构造不超过 `n` 的数',
        '@cache': '记忆化：同样的 `(i, cnt1, is_limit)` 只算一次',
        'if i == len(s)': _cap_if,
        'return cnt1': '递归边界：返回 `cnt1 = {cnt1}`，即这个数里有几个 `1`',
        'up = ': _cap_up,
        'for d in range': lambda S, B, ret: (f'枚举这一位填 `d = {S["_inner"]["d"]}`（范围 `0 ~ up = {S["_inner"]["up"]}`）'
                                             if S['_inner'].get('d') != B['_inner'].get('d') else '这一位的数字枚举完了'),
        'res += f(': _cap_res,
        'return res': '这一位所有填法的 1 的个数之和：`res = {res}`',
        'return f(0, 0, True)': '入口 `f(0, 0, True)`：还没填数，受 `n` 约束，开始递归',
    },
    cards=dict(
        one_liner='一位一位构造，用 `cnt1` 记 1 的个数，`is_limit` 记是否贴着 n',
        complexity='时间 `O(m^2 D)`（`m = log n`，`D = 10`），空间 `O(m^2)`',
        problem=['给定整数 `num`，数出所有 `0 ~ num` 的数里，数字 `1` ==一共出现了多少次==',
                 '示例：`num = 13` → `6`（1, 10, 11×2, 12, 13）',
                 '本视频：`num = 13`'],
        quote='`f(i, cnt1, isLimit)` 表示构造到从左往右第 i 位，已经出现了 cnt1 个 1，在这种情况下，继续构造最终会得到的 1 的个数（你可以直接从回溯的角度理解这个过程，只不过是多了个记忆化）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `n` 变成字符串，逐位填数字，填的数不能超过 `n`',
              '`is_limit` 为真：前面和 `n` 完全一样，这一位至多填 `n[i]`；否则至多填 `9`',
              '填完所有位，返回 `cnt1`；每位枚举 `d`，遇到 `1` 就让 `cnt1` 加 1',
              '同一个 `(i, cnt1, False)` 会被多条路径到达 → `@cache`'],
        result='运行结束，返回 `6`：`0~13` 中共出现 6 个数字 1',
        summary=['时间 `O(m^2 D)`：状态数 `O(m^2)`，每个状态枚举 `D = 10` 个数字',
                 '易错：`is_limit and d == up` 才继续受限，否则后面可以填到 `9`',
                 '前导零不影响本题：填 `0` 对 `cnt1` 没有贡献',
                 '原文答疑：`is_limit = True` 的状态只有一条路径，所以可以只记忆化不受限的状态'],
    ),
)
