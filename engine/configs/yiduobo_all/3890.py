def _txt(S):
    if 'a' not in S or 'b' not in S or 'v' not in S:
        if 'good' in S:
            return f"`cnt` 里出现次数 `> 1` 的和：`good = {S['good']}`"
        return '枚举 `a <= b`，把每个立方和 `a³ + b³` 记进哈希表 `cnt`'
    if 'good' in S:
        return f"`cnt` 里出现次数 `> 1` 的和：`good = {S['good']}`"
    a, b, v = S['a'], S['b'], S['v']
    c = S.get('cnt', {}).get(v, 0)
    return f"`{a}³ + {b}³ = {a ** 3} + {b ** 3} = ` =={v}== （已出现 `{c}` 次）"


CONFIG = dict(
    num=3890, title='可由多种立方和构造的整数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='暴力枚举 a、b · 哈希表计数',
    tags=[],
    code='''
class Solution(object):
    def findGoodIntegers(self, n):
        
        cnt = {}
        a = 1
        while a ** 3 * 2 <= n:
            b = a + 1
            v = a ** 3 + b ** 3
            while v <= n:
                cnt[v] = cnt.get(v, 0) + 1
                b += 1
                v = a ** 3 + b ** 3
            a += 1
        
        good = []
        for v in cnt:
            if cnt[v] > 1:
                good.append(v)
        
        good.sort()
        res = []
        for v in good:
            if v <= n:
                res.append(v)
        return res
''',
    call='Solution().findGoodIntegers(1729)',
    expect=[1729],
    views=[
        dict(type='text', h=100, size=28, fn=_txt),
        dict(type='map', var='cnt', label='cnt（和 → 出现次数；黄 = 刚更新）', fmt=lambda k, v: f'{k}: {v}', h=330, font=26),
        dict(type='array', var='good', label='good（出现 >= 2 次的和）', cell=130, h=170),
    ],
    watch=['a', 'b', ('v', 'v', 'yellow'), 'res'],
    skip=['b += 1', 'a += 1', 'for v in cnt:', 'v = a ** 3 + b ** 3', 'b = a + 1', 'while v <= n', 'if cnt[v] > 1', 'while a ** 3 * 2', 'a = 1', 'for v in good', 'if v <= n', 'good = []', 'res = []', 'good.sort()'],
    max_steps=110,
    captions={
        'while a ** 3 * 2 <= n': lambda S, B, r: (f'`a = {S.a}`：最小的和是 `2a³ = {2 * S.a ** 3}`，`<= n` → 继续' if 2 * S.a ** 3 <= S.n
                                                  else f'`2a³ = {2 * S.a ** 3} > n`：再往后连 `a=b` 都超了 → ==停止枚举 a=='),
        'v = a ** 3 + b ** 3': '`v = {a}³ + {b}³ = {v}`',
        'while v <= n': lambda S, B, r: (f'`v = {S.v} <= {S.n}` → 记一次' if S.v <= S.n else f'`v = {S.v} > {S.n}`：`b` 再大只会更大 → ==换下一个 a=='),
        'cnt = {}': '`cnt` 记每个立方和出现几次；`a` 到 `2a³ > n` 止，`b` 到和 `> n` 止',
        'cnt[v] =': '`{a}³ + {b}³ = {v}` → `cnt[{v}]` = `{B.cnt.get(v, 0)} + 1` = =={cnt[v]}=={"（出现第 2 次，是好整数！）" if cnt[v] > 1 else ""}',
        'b += 1': '`b` → {b}',
        'a += 1': '`a` → {a}',
        'good = []': '枚举完毕，再从 `cnt` 里挑次数大于 1 的',
        'for v in cnt': '检查 `cnt` 中的 `{v}`',
        'if cnt[v] > 1': lambda S, B, r: f'`cnt[{S.v}] = {S.cnt[S.v]}` ' + ('`> 1` → ==好整数==' if S.cnt[S.v] > 1 else '不超过 1 → 只有一种写法'),
        'good.append(v)': '`cnt[{v}] = {cnt[v]} > 1`：有两种以上写法 → `good` 加入 `{v}`',
        'good.sort()': '`good` 排序：{good}',
        'res = []': '`res` 放 `<= n` 的好整数',
        'if v <= n': '`{v} <= {n}` → 加入答案',
        'res.append(v)': '`res` = {res}',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='暴力枚举所有 a³+b³，哈希表里出现两次以上的就是好整数',
        complexity='时间 `O(n^(2/3))`，空间 `O(n^(2/3))`',
        problem=['好整数 `x`：至少有两组不同的正整数 `(a, b)`，`a <= b`，`x = a³ + b³`',
                 '返回 `<= n` 的所有好整数，升序',
                 '本视频用小一点的 `n = 1729` → `[1729]`（`1³+12³ = 9³+10³`）'],
        quote='由于n不超过10^9，而好整数是立方和的形式，那么就意味着a和b都不可能超过1000，因此在这里可以直接暴力枚举所有可能的(a, b)，然后利用哈希表记录所有立方和出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`a, b` 都不会超过 `1000`，枚举量 `~10^6`，直接暴力',
              '外层 `a` 到 `2a³ > n` 为止；内层 `b` 往上加，直到 `a³+b³ > n`',
              '哈希表统计次数，取次数 `> 1` 的，排序后筛 `<= n`'],
        summary=['时间约 `O(n^(2/3))`，空间同阶（每次查询都重新枚举）',
                 '`b` 从 `a + 1` 起，所以 `a = b` 的 `2a³` 没计入；它不可能等于另一组立方和，不影响结果',
                 '对比灵神：灵神把 `10^9` 内的好整数预处理一次，再二分；yiduobo 每次按 `n` 现算',
                 '最后一步 `if v <= n` 是多余的保险，`cnt` 里的和本来就 `<= n`'],
    ),
)
