def _I(S):
    return S['_inner'].get('i')


def _digits(S, name):
    v = S.get(name)
    return v if isinstance(v, list) else []


def _fmt(S):
    inn = S['_inner']
    i = inn.get('i')
    if i is None or 'high' not in S or 'low' not in S:
        return '把 `l`、`r` 转成 `b` 进制，对齐成同样长度，再逐位填数字'
    if inn.get('pre') is None:
        return ''
    return (f"第 {i} 位：`pre = {inn['pre']}`，贴 low = {inn['limit_low']}，贴 high = {inn['limit_high']}")


CONFIG = dict(
    num=3519, title='统计逐位非递减的整数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP（上下界模板 v2.0）',
    tags=['灵神题单', '动态规划', '难度分 2246'],
    code='''
class Solution:
    def countNumbers(self, l: str, r: str, b: int) -> int:
        # 把 s 转成 b 进制，库函数写法见【Numpy】代码
        def trans(s: str) -> List[int]:
            x = int(s)
            digits = []
            while x:
                x, r = divmod(x, b)
                digits.append(r)
            digits.reverse()
            return digits

        high = trans(r)
        n = len(high)
        low = trans(l)
        low = [0] * (n - len(low)) + low

        @cache
        def dfs(i: int, pre: int, limit_low: bool, limit_high: bool) -> int:
            if i == n:
                return 1

            lo = low[i] if limit_low else 0
            hi = high[i] if limit_high else b - 1

            res = 0
            for d in range(max(lo, pre), hi + 1):
                res += dfs(i + 1, d, limit_low and d == lo, limit_high and d == hi)
            return res

        return dfs(0, 0, True, True) % 1_000_000_007
''',
    call='Solution().countNumbers("23", "28", 8)',
    expect=3,
    views=[
        dict(type='array', var='high', label='high = r 的 b 进制（蓝 = 当前位）', cell=70, h=150,
             color=lambda S, k, v: 'blue' if k == S['_inner'].get('i') else None),
        dict(type='array', var='low', label='low = l 的 b 进制（补前导 0）', cell=70, h=150,
             color=lambda S, k, v: 'blue' if k == S['_inner'].get('i') else None),
        dict(type='text', fn=_fmt, size=24, h=80),
        dict(type='calls', h=240),
    ],
    watch=[('i', _I, 'blue'), ('pre', lambda S: S['_inner'].get('pre'), 'cyan'),
           ('lo', lambda S: S['_inner'].get('lo'), 'green'), ('hi', lambda S: S['_inner'].get('hi'), 'orange'),
           ('res', lambda S: S['_inner'].get('res'), 'yellow')],
    skip=['res = 0', 'digits.append', 'digits.reverse', 'x = int(s)', 'digits = []', 'n = len(high)'],
    captions={
        'x, r = divmod': '`{x}` 对 `b = {b}` 取余得到一个数位 `{r}`，商留下继续',
        'return digits': '进制转换结束：从高位到低位是 `{digits}`',
        'high = trans(r)': '`r` 的 {b} 进制：`{high}`，长度 `n` 就是数位数',
        'low = [0] * ': '`l` 补前导 0，和 `high` 一样长：`{low}`——这样 low/high 能逐位对齐',
        'return dfs(0, 0, True, True)': '从最高位出发：`pre = 0` 让第一位不受限制；一开始同时受 low 和 high 约束，最后对 `1e9+7` 取模',
        'if i == n': lambda S, B, ret: ('每一位都填完 → 找到一个非递减的数，返回 `1`' if S.i == S.n
                                        else f'`i = {S.i} < n`：还没填完，继续枚举这一位'),
        'lo = low[i]': '`lo = {lo}`：受 low 约束时这一位不能比 `low[{i}]` 小；否则下限 0',
        'hi = high[i]': '`hi = {hi}`：受 high 约束时这一位不能比 `high[{i}]` 大；否则上限 `b-1 = {b-1}`',
        'for d in range': lambda S, B, ret: (
            f'`d` 已经枚举到上限 `hi = {S.hi}`，这一位结束' if S.d >= S.hi and B.get('d') == S.d and B.get('pre') == S.pre else
            f'`d` 的范围是 `[max(lo, pre), hi] = [{max(S.lo, S.pre)}, {S.hi}]`：==不能比上一位 pre 小==，才保证非递减；轮到 `d = {S.d}`'),
        'res += dfs': '填 `d = {d}` 后进入下一位：`pre = {d}`；low 约束 = `{limit_low and d == lo}`，high 约束 = `{limit_high and d == hi}`（只有贴着边界填才继续受约束）',
        'return res': '这一位及之后的合法方案共 `{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='转成 b 进制，逐位填数字：下限取 max(lo, pre)，保证非递减',
        complexity='时间 `O(n·b²)`，空间 `O(n·b)`',
        problem=['给 `l`、`r`（字符串）和进制 `b`，数 `[l, r]` 内 b 进制下==每一位都不小于前一位==的整数个数，结果对 `1e9+7` 取模',
                 '示例：`l="2", r="7", b=2` → `2`（二进制 11 和 111）',
                 '本视频：`l="23", r="28", b=8` → `3`（八进制 27、33、34）'],
        quote='把 $l$ 和 $r$ 转成 $b$ 进制，然后套数位 DP v2.0 模板。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, pre, limit_low, limit_high)`：填第 `i` 位及之后，前一位填的是 `pre`',
              '同时记录 low / high 两个边界约束，只有贴边填才继续受约束',
              '枚举 `d` 从 `max(lo, pre)` 开始，非递减的条件就内置在循环范围里'],
        summary=['时间 `O(n²+n·b²)`：进制转换 `O(n²)`，状态 `O(n·b)` × 转移 `O(b)`',
                 '`pre` 初始为 0：第一位的下限本来就是 0，不会被 pre 限制',
                 '`low` 要补前导 0 到和 `high` 等长，否则逐位对不齐',
                 '题解还给了方法二：组合数学 `C(m+b-pre, b-1-pre)` 的 O(n) 公式；本视频演示方法一',
                 '本题答案较小，可以只在返回前取模'],
    ),
)
