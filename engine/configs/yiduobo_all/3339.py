CONFIG = dict(
    num=3339, title='查找K偶数数组的数量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='计数 DP · 末位奇偶分类',
    tags=[],
    code='''
class Solution(object):
    def countOfArrays(self, n, m, k):
        
        f = [0] * (k + 1)
        g = [0] * (k + 1)

        even = m // 2
        odd = m - even

        f[0] = even
        g[0] = odd

        mod = 10 ** 9 + 7
        for index in range(1, n):
            for pair in range(k, 0, -1):
                f[pair], g[pair] = (f[pair - 1] + g[pair]) * even % mod, (f[pair] + g[pair]) * odd % mod
            f[0], g[0] = g[0] * even % mod, (f[0] + g[0]) * odd % mod
        
        return (f[k] + g[k]) % mod
''',
    call='Solution().countOfArrays(4, 3, 2)',
    expect=4,
    views=[
        dict(type='array', var='f', pointers={'pair': 'blue'}, label='f[pair]：末位是偶数、恰有 pair 对相邻偶数的数组数', h=200),
        dict(type='array', var='g', pointers={'pair': 'blue'}, label='g[pair]：末位是奇数、恰有 pair 对相邻偶数的数组数', h=200),
        dict(type='text', fn=lambda S: f"1..m 中偶数 ==`{S['even']}`== 个，奇数 ==`{S['odd']}`== 个" if 'odd' in S else '', h=60),
    ],
    watch=['index', 'pair', ('even', 'even', 'cyan'), ('odd', 'odd', 'orange')],
    captions={
        'f = [0]': '`f[p]`：长度为 `length`、末位偶数、恰有 `p` 对相邻偶数的数组数',
        'g = [0]': '`g[p]`：同样条件，但末位是奇数',
        'even = m': '`1..{m}` 中偶数 `{even}` 个，奇数 `{odd}` 个（先算偶数，奇数 = m − 偶数）',
        'odd = m': '奇数个数 `odd = {odd}`',
        'f[0] = even': '长度 1、0 对：末位偶数有 `{even}` 种 → `f[0] = {f[0]}`',
        'g[0] = odd': '长度 1、0 对：末位奇数有 `{odd}` 种 → `g[0] = {g[0]}`',
        'mod =': '答案很大，所有乘加都对 `10^9+7` 取模',
        'for index': lambda S, B, r: (f'把长度扩到 `{S.index + 1}`' if S.index != B.get('index') else 'n 轮都扩完了，长度到达 `n`'),
        'for pair': lambda S, B, r: (f'倒着枚举 `pair = {S.pair}`：新值要用旧的 `pair - 1`，倒序才不会被覆盖' if S.pair != B.get('pair') else '`pair` 从 k 到 1 都更新完，再单独处理 `pair = 0`'),
        'f[pair], g[pair] =': '`f[{pair}]`：末位填偶数，`f[{pair-1}]` 填偶数新增一对 + `g[{pair}]` 填偶数不增对，再 × `{even}` = =={f[pair]}==；`g[{pair}]`：末位填奇数，`f`+`g` 再 × `{odd}` = =={g[pair]}==',
        'f[0], g[0] =': '`pair = 0`：偶数结尾只能接在奇数结尾后（否则成对）：`f[0] = g[0] × {even}` = =={f[0]}==；`g[0]` = (`f[0]`+`g[0]`) × `{odd}` = =={g[0]}==',
        'return': '末位奇偶都算：`f[{k}] + g[{k}]` = =={ret}==',
    },
    cards=dict(
        one_liner='式子只在两数都是偶数时为偶：数「相邻偶数对」恰好 k 对的数组',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['给定 `n, m, k`：数组长 `n`，元素取值 `1..m`',
                 '下标 `i` 满足 `arr[i]*arr[i+1] - arr[i] - arr[i+1]` 为偶数，恰有 `k` 个，就叫 k 偶数数组',
                 '求这样的数组个数，对 `10^9+7` 取模；本视频：`n=4, m=3, k=2`'],
        quote='当且仅当arr[i]和arr[i + 1]都是偶数时，式子的结果才是偶数。',
        quote_src='—— yiduobo 题解原文',
        idea=['式子等价于「两个相邻数都是偶数」→ 问题变成数相邻偶数对',
              '`f` 记末位偶数、`g` 记末位奇数，下标是已有的偶数对数',
              '偶数结尾可由 `f[pair-1]`（新增一对）或 `g[pair]` 转来，奇数结尾不增对'],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '易错点：`pair` 要倒序枚举，且 `f[0]` 单独处理（没有 `pair-1`）',
                 '`f[pair], g[pair]` 同时赋值，右边都用旧值',
                 '原文本身已兼容 Python 3（`//` 整除），未作改动'],
    ),
)
