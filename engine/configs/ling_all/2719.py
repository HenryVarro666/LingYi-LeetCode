def _I(S):
    return S['_inner'].get('i')


def _txt(S):
    I = S['_inner']
    if 'i' not in I or 's' not in I:
        return '数位 DP：数位和 `s` 不能超过 `max_sum`，填完时要 `≥ min_sum`'
    return (f"`dfs({I['i']}, {I['s']}, {I.get('limit_low')}, {I.get('limit_high')})`：数位和已是 =={I['s']}==")


CONFIG = dict(
    num=2719, title='统计整数数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP v2.0（上下界一次搜完）',
    tags=['灵神题单·动态规划'],
    code='''
class Solution:
    def count(self, num1: str, num2: str, min_sum: int, max_sum: int) -> int:
        high = list(map(int, num2))  # 避免在 dfs 中频繁调用 int()
        n = len(high)
        low = list(map(int, num1.zfill(n)))  # 补前导零（本题前导零不影响答案，可以补前导零，简化代码逻辑）

        @cache
        def dfs(i: int, s: int, limit_low: bool, limit_high: bool) -> int:
            if s > max_sum:  # 非法
                return 0
            if i == n:
                return 1 if s >= min_sum else 0

            lo = low[i] if limit_low else 0
            hi = high[i] if limit_high else 9

            res = 0
            for d in range(lo, hi + 1):  # 枚举当前数位填 d
                res += dfs(i + 1, s + d, limit_low and d == lo, limit_high and d == hi)
            return res

        return dfs(0, 0, True, True) % 1_000_000_007
''',
    call='Solution().count("1", "12", 1, 5)',
    expect=8,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='low', label='low（num1 补前导零）', cell=64, h=130, pointers={_I: 'blue'}, pointer_labels={_I: 'i'}),
        dict(type='array', var='high', label='high（num2）', cell=64, h=130, pointers={_I: 'pink'}, pointer_labels={_I: 'i'}),
        dict(type='calls', h=300),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('s', lambda S: S['_inner'].get('s'), 'yellow'),
           ('lo', lambda S: S['_inner'].get('lo'), 'cyan'), ('hi', lambda S: S['_inner'].get('hi'), 'orange'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    skip=['res = 0'],
    max_steps=50,
    captions={
        'low = ': '`low = {low}`：给 `num1` 补前导零，和 `num2` 一样长，逐位对齐',
        'if s > max_sum': lambda S, B, r: (f'`s = {S.s} > max_sum = {S.max_sum}`：数位和只增不减 → 非法，直接返回 ==0=='
                                           if S.s > S.max_sum else f'`s = {S.s} ≤ max_sum = {S.max_sum}`：还合法，继续'),
        'if i == n': lambda S, B, r: (f'`i = {S.i} < n = {S.n}`：还没填完' if S.i < S.n else '`i == n`：整个数填完了'),
        'return 1 if s >= min_sum': '填完得到一个数，数位和 `s = {s}`：`≥ min_sum = {min_sum}` 才算好整数 → 返回 ==1 或 0=='.replace('==1 或 0==', '=={ret}=='),
        'lo = ': '下界：`limit_low` 为真时这一位不能小于 `num1` 对应位，否则从 0 起：`lo = {lo}`',
        'hi = ': '上界：`limit_high` 为真时这一位不能大于 `num2` 对应位，否则到 9：`hi = {hi}`；`d` 从 `{lo}` 到 `{hi}`',
        'res += dfs': '填 `d = {B.d}`：数位和变 `{B.s + B.d}`；只有 `d` 恰好贴着边界，对应的限制才继续传下去',
        'return res': '这个状态下的好整数有 `{res}` 个',
        'return dfs(0, 0, True, True)': '从最高位出发，==两个限制都开着==；结果最后对 `10^9 + 7` 取余',
    },
    cards=dict(
        result='返回 `8`：1~5、10、11、12 的数位和都在 1..5',
        one_liner='上下界各用一个 limit 标记，一次记忆化搜索数完区间',
        complexity='时间 `O(n·m·D)`，空间 `O(n·m)`',
        problem=['给两个数字字符串 `num1`、`num2`，数位和范围 `[min_sum, max_sum]`',
                 '数 `num1 ≤ x ≤ num2` 中数位和落在范围内的整数个数，对 `10^9+7` 取余',
                 '示例：`"1"~"12"`，和在 `1..8` → `11`；本视频取和在 `1..5` → `8`'],
        quote='仿照 isLimit，再添加一个参数 limitLow，表示是否受到下界 num1 的约束。',
        quote_src='—— 灵茶山艾府题解（v2.0）',
        idea=['`dfs(i, s, limit_low, limit_high)`：填到第 `i` 位、数位和为 `s` 时的好整数个数',
              '`s > max_sum` 直接剪枝，因为数位和不会变小；填完时判断 `s ≥ min_sum`',
              '前导零不改变数位和，所以不用 `is_num` 参数，`num1` 补零对齐即可'],
        summary=['状态 `O(n·m)`，每个状态枚举 `D = 10` 个数字',
                 '易错：`num1` 要补前导零；`limit` 只在 `d` 贴边界时才往下传',
                 '`s > max_sum` 要放在 `i == n` 之前，非法就别继续了',
                 'v1.0 写法是 `calc(num2) − calc(num1) + is_num1_good`，要搜两次；v2.0 一次搞定'],
    ),
)
