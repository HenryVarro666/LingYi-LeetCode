def _I(S):
    i = S['_inner'].get('i')
    return i if i is not None and i < len(S['s']) else None


def _info(S):
    L = S['_inner']
    if 'i' in L and 'left' in L:
        i, left, lim = L['i'], L['left'], L['limit_high']
        if i == len(S['s']):
            return f'填完了：`left = {left}` → ==' + ('恰好用完，计 1' if left == 0 else '没用完/差一些，计 0') + '=='
        hi = S['s'][i] if lim else 9
        return f'第 {i} 位：还差 `left = {left}`；{"==贴着 n==" if lim else "不受限"}，最多填 `min({hi}, {left})`'
    if 'target' in S and 'cnt' in S:
        return f'`target = {S["target"]}`：1~n 中数位和恰好为它的数有 ==`{S["cnt"]}`== 个'
    return '枚举目标数位和 `target`，用 `dfs` 数出恰好等于它的数有几个'


def _stat(S):
    if 'max_cnt' not in S or 'target' not in S:
        return ''
    return f'`max_cnt = {S["max_cnt"]}`（最大组的大小），`ans = {S["ans"]}`（这样大的组有几个）'


CONFIG = dict(
    num=1399, title='统计最大组的数目', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='数位 DP（枚举目标数位和）',
    tags=['灵神题单', '数位 DP'],
    code='''
class Solution:
    def countLargestGroup(self, n: int) -> int:
        s = list(map(int, str(n)))  # 避免在 dfs 中频繁调用 int()
        m = len(s)

        @cache
        def dfs(i: int, left: int, limit_high: bool) -> int:
            if i == m:
                return 1 if left == 0 else 0
            hi = s[i] if limit_high else 9  # 当前数位至多填 hi
            res = 0
            for d in range(min(hi, left) + 1):  # 枚举当前数位填 d
                res += dfs(i + 1, left - d, limit_high and d == hi)
            return res

        max_cnt = ans = 0
        for target in range(1, m * 9 + 1):  # 枚举目标数位和
            cnt = dfs(0, target, True)
            if cnt > max_cnt:
                max_cnt = cnt
                ans = 1
            elif cnt == max_cnt:
                ans += 1
        return ans
''',
    call='Solution().countLargestGroup(13)',
    expect=4,
    views=[
        dict(type='array', var='s', label='s = n 的各位（框 = 当前要填的位）', cell=96, h=190,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'}),
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='text', fn=_stat, size=26, h=60),
        dict(type='calls', h=200),
    ],
    watch=[('target', 'target', 'blue'), ('cnt', 'cnt', 'pink'), ('max_cnt', 'max_cnt', 'yellow'), ('ans', 'ans', 'green')],
    max_steps=50,
    skip=['m = len(s)', 'res = 0', 'for d in range', 'max_cnt = ans = 0', 'if i == m', 'return res'],
    captions={
        's = list(map': '`n = {n}` 拆成各位 `s = {s}`，从高位往低位填',
        'if i == m': lambda S, B, r: ('`i == m`：所有位都填完了' if S.i == S.m else f'`i = {S.i}`：还没填完，继续枚举这一位'),
        'return 1 if left': lambda S, B, r: f'填完所有位，`left = {S.left}`：' + ('==恰好用完 target，构造出一个数，返回 1==' if S.left == 0 else '数位和对不上 target，返回 0'),
        'hi = s[i]': lambda S, B, r: (f'`limit_high` 为真：还贴着 n，这一位至多 `s[{S.i}] = {S.hi}`' if S.limit_high
                                      else '已经比 n 小了：这一位至多 `9`'),
        'res += dfs': lambda S, B, r: (f'这一位填 `{B.d}`，剩余数位和变成 `{B.left - B.d}`；'
                                       f'下一层 `limit_high = {B.limit_high and B.d == B.hi}`'),
        'return res': '这个状态的方案数 `{ret}`，==缓存复用==：不同 target 共用同一批状态',
        'for target in range': '换一个目标数位和 `target = {target}`',
        'cnt = dfs(0': '`dfs(0, {target}, True)`：从最高位出发，数 1~n 里数位和恰好为 {target} 的数',
        'if cnt > max_cnt': lambda S, B, r: (f'`{S.cnt} > {S.max_cnt}`：出现了更大的组' if S.cnt > S.max_cnt
                                              else f'`cnt = {S.cnt}`，和 `max_cnt = {S.max_cnt}` 比较'),
        'max_cnt = cnt': '更新最大组大小 `max_cnt = {cnt}`',
        'ans = 1': '最大组重新计数，`ans = 1`',
        'elif cnt == max_cnt': lambda S, B, r: (f'`cnt = {S.cnt}` 和 `max_cnt` 一样大 → 又一个最大组' if S.cnt == S.max_cnt
                                                else f'`cnt = {S.cnt}` 比 `max_cnt = {S.max_cnt}` 小，不用管'),
        'ans += 1': '并列最大组 +1：`ans = {ans}`',
        'return ans': '共有 =={ret}== 个组并列最大',
    },
    cards=dict(
        one_liner='枚举目标数位和，数位 DP 数出每组的大小',
        complexity='时间 `O(D^2 log^2 n)`，空间 `O(D log^2 n)`',
        problem=['把 `1` 到 `n` 按数位和分组，返回==最大组里有几个数==',
                 '这里的「最大」指元素最多，并列的组都要数',
                 '示例：`n = 13` → `4`（数位和 1~4 的组各有 2 个）'],
        quote='枚举目标数位和 target=1,2,…,9m，计算 [1,n] 中有多少个整数的数位和恰好等于 target。这正是方法一哈希表中的 value 值。',
        quote_src='—— 灵茶山艾府题解（方法二：数位 DP）',
        idea=['方法一暴力：逐个数算数位和，哈希表计数；`n` 到 `10^18` 就超时',
              '`dfs(i, left, limit_high)`：第 i 位起，数位和恰好还要 `left`',
              '`left` 定义成==剩余==数位和，不同 target 才能复用同一份记忆化'],
        summary=['时间 `O(D^2 log^2 n)`：状态 `O(D log^2 n)` 个 × 每个枚举 D=10 个数字',
                 '前导零不影响数位和，所以不需要 `is_num` 参数',
                 '易错：终点要判 `left == 0`（恰好），不是 `<= 0`',
                 '本题 `n <= 10^4`，直接暴力枚举（方法一）也能过；数位 DP 是进阶',
                 '同类题：2719. 统计整数数目（上下界 + 数位和区间）'],
    ),
)
