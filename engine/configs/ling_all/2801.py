def _pos(S):
    i = S['_inner'].get('i')
    s = S.get('s')
    return i if isinstance(i, int) and s is not None and i < len(s) else None


def _info(S):
    I = S['_inner']
    if 'pre' not in I:
        return '统计 `calc(n)`：不超过 n 的步进数字，相邻数位差恰好为 1'
    pre = I['pre'] if I['is_num'] else '—'
    return (f"第 `{I['i']}` 位 · 上一位 `{pre}`\n"
            f"贴上界 `{I['is_limit']}` · 已填数 `{I['is_num']}`")


CONFIG = dict(
    num=2801, title='统计范围内的步进数字数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP · 记忆化搜索（pre + is_limit + is_num）',
    tags=['灵神题单', '数位 DP', '难度分 2367'],
    code='''
class Solution:
    def countSteppingNumbers(self, low: str, high: str) -> int:
        MOD = 10 ** 9 + 7
        def calc(s: str) -> int:
            @cache  # 记忆化搜索
            def f(i: int, pre: int, is_limit: bool, is_num: bool) -> int:
                if i == len(s):
                    return int(is_num)  # is_num 为 True 表示得到了一个合法数字
                res = 0
                if not is_num:  # 可以跳过当前数位
                    res = f(i + 1, pre, False, False)
                low = 0 if is_num else 1  # 如果前面没有填数字，必须从 1 开始（因为不能有前导零）
                up = int(s[i]) if is_limit else 9  # 如果前面填的数字都和 s 的一样，那么这一位至多填 s[i]（否则就超过 s 啦）
                for d in range(low, up + 1):  # 枚举要填入的数字 d
                    if not is_num or abs(d - pre) == 1:  # 第一位数字随便填，其余必须相差 1
                        res += f(i + 1, d, is_limit and d == up, True)
                return res % MOD
            return f(0, 0, True, False)
        return (calc(high) - calc(str(int(low) - 1))) % MOD
''',
    call='Solution().countSteppingNumbers("1", "11")',
    expect=10,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='string', var='s', label='当前上界 s（蓝箭头 = 正在填第 i 位）', pointers={_pos: 'blue'},
             pointer_labels={_pos: 'i'}, cell=80, h=200),
        dict(type='calls', hide=('is_limit',), h=330),
    ],
    watch=[('i', "_inner.get('i')", 'blue'), ('pre', "_inner.get('pre')", 'pink'),
           ('low', "_inner.get('low')", 'cyan'), ('up', "_inner.get('up')", 'cyan'),
           ('d', "_inner.get('d')", 'orange'), ('res', "_inner.get('res')", 'green')],
    skip=[3, 7, 9, 14],
    max_steps=42,
    captions={
        'return (calc(high)': '答案 = `calc(high) - calc(low-1)`：不超过 high 的 减去 不超过 low-1 的（Python 大整数可以直接减一）',
        'return f(0': '入口：从最高位开始，受 `s` 约束，还没填数字；`pre` 填什么都行',
        'return int(is_num)': lambda S, B, r: ('`is_num = True`：填了数字，而且每一步都满足差 1 → ==得到一个步进数字，返回 1==' if S.is_num
                                                else '`is_num = False`：从头到尾一个数字都没填 → 不是数字，返回 0'),
        'if not is_num:': lambda S, B, r: ('前面还没填数字 → ==这一位可以跳过==（构造位数更少的数）' if not S.is_num
                                         else '前面已经填了数字，这一位必须填'),
        'res = f(i + 1, pre, False': '跳过这一位：后面位数更少，一定比 `s` 小 → `is_limit` 变 False，`is_num` 仍为 False',
        'low = 0 if': '`is_num = {is_num}` → 这一位从 `low = {low}` 开始填（还没填过就不能是前导零）',
        'up = int': '`is_limit = {is_limit}` → 这一位至多填 `up = {up}`（贴上界时不能超过 `s[i]`）',
        'for d in range': '枚举这一位填 `d`，范围 `[{low}, {up}]`',
        'if not is_num or abs': lambda S, B, r: (f'枚举 `d = {S.d}`（范围 `[{S.low}, {S.up}]`）：第一个数字随便填 → 可以' if not S.is_num
                                                 else (f'枚举 `d = {S.d}`（范围 `[{S.low}, {S.up}]`）：`|d - pre| = |{S.d} - {S.pre}| = {abs(S.d - S.pre)}`' + (' = 1 → ==可以填==' if abs(S.d - S.pre) == 1 else ' ≠ 1 → ==不能填=='))),
        'res += f': '填 `d = {d}`：上一位变成 `d`；只有 `d == up` 才继续贴上界；`is_num` 变 True',
        'return res % MOD': '这一层合法数字个数 `res = {res}`，返回上一层',
    },
    cards=dict(
        one_liner='逐位填数字，要求相邻数位差恰好为 1；区间用前缀相减',
        complexity='时间 `O(nD²)`，空间 `O(nD)`',
        problem=['相邻数位差的绝对值都恰好是 1 的数叫步进数字，不能有前导 0',
                 '求 `[low, high]` 内步进数字的个数（`low`、`high` 是很大的字符串），结果模 `10^9+7`',
                 '示例：`low="1", high="11"` → `10`（1~9 和 10）'],
        quote='`pre` 表示上一个数位的值。`isLimit` 表示当前是否受到了 n 的约束。`isNum` 表示 i 前面的数位是否填了数字。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`calc(n)` = 不超过 `n` 的步进数字个数，答案 `calc(high) - calc(low-1)`',
              '`f(i, pre, is_limit, is_num)`：`is_num` 为假时可以跳过这一位，不会有前导零',
              '第一位随便填，之后每位必须满足 `abs(d - pre) == 1`'],
        summary=['时间 `O(nD²)`，`n` 是 `high` 的长度，`D = 10`',
                 '`@cache` 的状态数 `O(nD)`，每个状态枚举 `D` 个数字',
                 '易错点：`is_num` 为假时 `pre` 没有意义，要先判断 `not is_num`',
                 '`low - 1` 在 Python 里直接 `str(int(low) - 1)`；其他语言可以用 `valid(low)` 补回来'],
    ),
)
