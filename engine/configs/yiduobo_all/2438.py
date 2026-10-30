def _top(S):
    if 'power' not in S or 'queries' not in S:
        return ''
    if 'x' in S and 'y' in S and 's' in S and 'res' in S:
        x, y, s = S['x'], S['y'], S['s']
        left = s[x - 1] if x > 0 else 0
        return f"区间 `[{x}, {y}]` 的幂次和 = `s[{y}]{f' − s[{x - 1}]' if x > 0 else ''}` = {s[y]}{f' − {left}' if x > 0 else ''} = =={s[y] - left}==，乘积 = `2^{s[y] - left}`"
    n = S.get('n', 0)
    return f"剩下的 n = `{bin(n)[2:] if n else '0'}`，已剥出 {len(S['power'])} 个 1 位"


def _wl(S):
    return S['x'] if 'x' in S and 'res' in S and 's' in S else None


def _wr(S):
    return S['y'] if 'y' in S and 'res' in S and 's' in S else None


CONFIG = dict(
    num=2438, title='二的幂数组中查询范围内的乘积', difficulty='Medium', category='位运算',
    author='yiduobo', technique='二进制剥位 + 对数转加法（前缀和）',
    tags=['灵神题单·位运算', '难度分 1610'],
    code='''
class Solution(object):
    def productQueries(self, n, queries):

        power = []
        now = 0
        while n:
            if n & (1 << now):
                n ^= (1 << now)
                power.append(now)
            now += 1

        s = [power[0]]
        for p in power[1:]:
            s.append(s[-1] + p)
        
        pow2 = [1]
        mod = 10 ** 9 + 7
        for index in range(500):
            pow2.append(pow2[-1] + pow2[-1])
            if pow2[-1] >= mod:
                pow2[-1] -= mod

        res = []
        for x, y in queries:
            p = s[y]
            if x > 0:
                p -= s[x - 1]
            res.append(pow2[p])
            
        
        return res
''',
    call='Solution().productQueries(45, [[0,1],[2,3],[0,3]])',
    expect=[4, 256, 1024],
    views=[
        dict(type='text', fn=_top, size=26, h=60),
        dict(type='string', var=lambda S: bin(S['n'])[2:] if S.get('n') else '0', label='n 的二进制（剥掉的 1 会消失）', cell=70, h=120),
        dict(type='array', var='power', label='power：每个 1 所在的位（框 = 当前查询的区间）', cell=90, h=150, window=(_wl, _wr)),
        dict(type='array', var='s', label='s：power 的前缀和', cell=90, h=170),
        dict(type='array', var='res', label='res：各查询答案', cell=100, h=110),
    ],
    watch=[('n', 'n'), ('now', 'now', 'blue'), ('power', 'power', 'pink'), ('s', 's', 'green')],
    captions={
        'power = []': '`power` 里存的不是 2 的幂本身，而是它的==幂次==（第几位）',
        'now = 0': '`now` 是当前检查的二进制位',
        'while n': lambda S, B, ret: (f'`n = {S.n}` 还有 1 没剥完' if S.n else '`n = 0`，所有 1 都剥完了'),
        'if n & (1 << now)': lambda S, B, ret: (f'第 `{S.now}` 位是 1 → 这一位对应一个 2 的幂' if S.n & (1 << S.now)
                                                else f'第 `{S.now}` 位是 0 → 跳过'),
        'n ^= (1 << now)': '异或把第 `{now}` 位清零：`n` 剩 `{n}`',
        'power.append': '`power` 追加幂次 `{now}` → `{power}`',
        'now += 1': '看下一位：`now` → {now}',
        's = [power[0]]': '乘法 → 加法：2 的幂相乘等于幂次相加，所以对 `power` 做前缀和，`s = {s}`',
        's.append(s[-1]': '`s` 追加 `{B.s[-1]} + {p}` = =={s[-1]}==',
        'pow2 = [1]': '`pow2[i] = 2^i % mod`，提前算好，之后 O(1) 查表',
        'mod =': '取模用 `mod = 10^9+7`',
        'p = s[y]': '区间 `[{x}, {y}]` 的幂次和先取 `s[{y}] = {p}`',
        'if x > 0': lambda S, B, ret: (f'`x = {S.x} > 0` → 要减掉前面的 `s[{S.x - 1}] = {S.s[S.x - 1]}`' if S.x > 0
                                       else '`x = 0`，区间从头开始，不用减'),
        'p -= s[x - 1]': '`p` = `s[{y}] − s[{x - 1}]` = =={p}==',
        'res.append(pow2': '答案 = `2^{p}` = =={res[-1]}==',
        'return res': '全部查询回答完毕：`{res}`',
    },
    skip=['pow2.append', 'if pow2[-1] >= mod', 'pow2[-1] -= mod', 'for index in range(500)', 'res = []'],
    cards=dict(
        one_liner='区间乘积取模不便除法，就用对数把乘法变加法',
        complexity='时间 `O(m + log n)`，空间 `O(log n)`',
        problem=['把 `n` 拆成==最少==个 2 的幂之和，升序排成 `power`',
                 '每个查询 `[l, r]`：`power[l..r]` 的乘积，对 `10^9+7` 取模',
                 '示例：`n=15` → `[1,2,4,8]`，`[0,3]` → `64`；本视频用 `n=45`'],
        quote='将乘法操作利用对数转化为加法操作。这样一来，区间乘积就转化为了区间和运算，再将其转化为前缀和就能很方便的计算了。',
        quote_src='—— yiduobo 题解原文',
        idea=['数量要最少 → 不能有重复的幂 → 就是二进制里每个 1 剥出来一项',
              '区间乘积 = 前缀乘积相除，但取模后除法要逆元，麻烦',
              '2 的幂只看幂次：乘积变成幂次的区间和，再查 `pow2` 表'],
        summary=['时间 `O(m + log n)`，`pow2` 预处理 500 项是常数',
                 '幂次和最多 `(1+29)×29/2`，不超过 500，所以 `range(500)` 够用',
                 '区间 `[x, y]`：`x = 0` 时直接用 `s[y]`，否则减去 `s[x-1]`',
                 '原文为 Python 2 写法，本题无需修改，可直接运行',
                 '对比灵神：灵神用 `n & -n` 取最低位，yiduobo 逐位扫描 `1 << now`'],
    ),
)
