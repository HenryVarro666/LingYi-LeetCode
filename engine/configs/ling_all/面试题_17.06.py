def _cap_loop(S, B, ret):
    i = S.i
    up = int(S.s[i]) if S.is_limit else 9
    return (f'第 {i} 位：`is_limit` = {S.is_limit}，上限 `up` = {up}' +
            ('（贴着 n，不能超过 `s[%d]`）' % i if S.is_limit else '（已经比 n 小，随便填到 9）'))


def _cap_f(S, B, ret):
    d, i = S.d, B.i
    up = int(S.s[i]) if B.is_limit else 9
    lim = B.is_limit and d == up
    return (f'第 {i} 位填 `{d}`：{"==是 2，cnt2 + 1==" if d == 2 else "不是 2，cnt2 不变"}；'
            f'`is_limit` 传 `{lim}`' + ('（填满上限，下一位继续受限）' if lim else '（下一位自由）') + '，进入下一层')


def _fmt(S):
    s = S['s']
    if '_inner' not in S or 'i' not in S['_inner']:
        return f'把 n 转成字符串 `s = "{s}"`，按位填数字'
    i = S['_inner']['i']
    return f'正在填第 `{i}` 位（共 {len(s)} 位）' if i < len(s) else '填完所有位：返回路径上 `2` 的个数 `cnt2`'


CONFIG = dict(
    num='面试题 17.06', title='2出现的次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP（记忆化搜索）',
    tags=['灵神题单·动态规划'],
    code='''
class Solution:
    def numberOf2sInRange(self, n: int) -> int:
        s = str(n)
        @cache
        def f(i: int, cnt2: int, is_limit: bool) -> int:
            if i == len(s):
                return cnt2
            res = 0
            up = int(s[i]) if is_limit else 9
            for d in range(up + 1):  # 枚举要填入的数字 d
                res += f(i + 1, cnt2 + (d == 2), is_limit and d == up)
            return res
        return f(0, 0, True)
''',
    call='Solution().numberOf2sInRange(22)',
    expect=6,
    skip=['res = 0'],
    views=[
        dict(type='string', var='s', label='s = str(n)', h=170, cell=110,
             pointers={'i': 'blue'}, color=lambda S, k, v: None),
        dict(type='text', h=60, size=26, fn=_fmt),
        dict(type='calls', h=330),
    ],
    watch=[('i', 'i', 'blue'), ('cnt2', 'cnt2', 'orange'), ('is_limit', 'is_limit', 'purple'), ('d', 'd', 'yellow'), ('res', 'res', 'green')],
    captions={
        's = str(n)': '把 `n` 转成字符串，方便按位枚举：`s = "{s}"`',
        'if i == len(s)': lambda S, B, r: (f'`i = {S.i} == len(s)`：所有位都填完了 → 返回这个数里 `2` 的个数 `cnt2 = {S.cnt2}`'
                                           if S.i == len(S.s) else f'`i = {S.i} < len(s)`：还有位没填，继续'),
        'return cnt2': '这个数里有 `{cnt2}` 个 2，返回 `{cnt2}`',
        'up = int(s[i])': _cap_loop,
        'for d in range(up + 1)': lambda S, B, r: (f"枚举这一位填 `d = {S['_inner']['d']}`（`0..{S.up}`）" if 'd' in S['_inner'] and B['_inner'].get('d') != S['_inner']['d'] or ('d' in S['_inner'] and B['_inner'].get('i') != S['_inner']['i'])
                                                  else '这一位 0..up 都试完了，把总和 `res` 返回'),
        'res += f(': _cap_f,
        'return res': '这个状态下所有数字里 `2` 的个数之和是 `{res}`，返回给上一层',
        'return f(0, 0, True)': '从第 0 位开始，一开始受 `n` 约束（`is_limit = True`）：调用 `f(0, 0, True)`',
    },
    cards=dict(
        one_liner='每个数位填 0..9，把路径上 2 的个数加起来',
        complexity='时间 `O(m²·D)`（m = 位数，D = 10），空间 `O(m²)`',
        problem=['求 `0..n` 的所有整数里，数字 `2` 一共出现了多少次（`22` 算两次）',
                 '示例：`n = 25` → `9`；本视频 `n = 22` → `6`（2、12、20、21、22 里共 6 个 2）',
                 '`n` 最大 `10^9`，不能逐个数'],
        quote='定义 f(i, cnt2, isLimit) 表示在前 i 位有 cnt2 个 2 的前提下，我们能构造出的数中的 2 的个数总和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数位 DP：把 `n` 转成字符串，从高位到低位逐位填数字',
              '`is_limit` 表示前面是否一直贴着 `n`：贴着就最多填 `s[i]`，否则可以填到 9',
              '填完所有位返回 `cnt2`，每一层把各选择的结果相加',
              '前导零不影响 2 的个数，所以可以省略 `is_num` 参数'],
        summary=['时间 `O(m²D)`：状态 `(i, cnt2)` 约 `m²` 个，每个枚举 `D = 10` 个数字',
                 '`@cache` 同时缓存了 `is_limit` 的两种状态，Python 写法不必特意只缓存不受限状态',
                 '前导零填 0 不会产生 2，所以不需要 `is_num`',
                 '终点返回 `cnt2`，而不是 1：求的是 2 的个数总和，不是数字个数',
                 '同模板：233 数字 1 的个数、2376 统计特殊整数等'],
    ),
)
