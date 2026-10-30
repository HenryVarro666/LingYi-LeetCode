_I = lambda S: S['_inner'].get('i')


def _state(S):
    I = S['_inner']
    if 'diff' not in I:
        return '数位 DP：构造 `low` 到 `high` 之间的数，==左半数位和 − 右半数位和 = diff=='
    i = I['i']
    lo = '受 low 约束' if I['limit_low'] else 'low 不再约束'
    hi = '受 high 约束' if I['limit_high'] else 'high 不再约束'
    st = '还没填数字' if I['start'] < 0 else f"首个非零位 start={I['start']}"
    return f"`dfs(i={i})`：{st}，`diff = {I['diff']}`，{lo}，{hi}"


def _cap_zero(S, B, ret):
    I = S['_inner']
    if I['lo']:
        return f"前面没填数字，剩余 `{I['n'] if 'n' in I else S['n'] - I['i']}` 位是奇数，当前位不能填；但 `lo = {I['lo']} > 0` 必须填 → 不合法，返回 0"
    return f"前面没填数字，剩余 `{S['n'] - I['i']}` 位是奇数 → 当前位==留空==（长度必须为偶数），直接递归下一位"


CONFIG = dict(
    num=2843, title='统计对称整数的数目', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='上下界数位 DP',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution:
    def countSymmetricIntegers(self, low: int, high: int) -> int:
        high = list(map(int, str(high)))  # 避免在 dfs 中频繁调用 int()
        n = len(high)
        low = list(map(int, str(low).zfill(n)))  # 补前导零，和 high 对齐

        @cache
        def dfs(i: int, start: int, diff: int, limit_low: bool, limit_high: bool) -> int:
            if diff < 0:
                return 0
            if i == n:
                return 1 if diff == 0 else 0

            lo = low[i] if limit_low else 0
            hi = high[i] if limit_high else 9

            # 如果前面没有填数字，且剩余数位个数是奇数，那么当前数位不能填数字
            if start < 0 and (n - i) % 2:
                # 如果必须填数字（lo > 0），不合法，返回 0
                return 0 if lo else dfs(i + 1, start, diff, True, False)

            res = 0
            is_left = start < 0 or i < (start + n) // 2
            for d in range(lo, hi + 1):
                res += dfs(i + 1,
                           i if start < 0 and d else start,  # 记录第一个填数字的位置
                           diff + (d if is_left else -d),  # 左半 + 右半 -
                           limit_low and d == lo,
                           limit_high and d == hi)
            return res

        return dfs(0, -1, 0, True, True)
''',
    call='Solution().countSymmetricIntegers(1200, 1230)',
    expect=4,
    skip=['is_left =', 'for d in range', 'high = list', 'low = list', 'limit_low and d == lo,', 'limit_high and d == hi)', 'diff + (d if', 'i if start < 0', 'lo = low', 'hi = high', 'res = 0'],
    views=[
        dict(type='array', var=lambda S: S.get('high') if isinstance(S.get('high'), list) else None, label='high 的数位（蓝箭头 = 当前填第 i 位）', cell=70, h=150,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'},
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('i') else None),
        dict(type='array', var=lambda S: S.get('low') if isinstance(S.get('low'), list) else None, label='low 的数位（补前导零对齐）', cell=70, h=150,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'},
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('i') else None),
        dict(type='text', fn=_state, size=24, h=70),
        dict(type='calls', h=230),
    ],
    watch=[('i', lambda S: S['_inner'].get('i', '-'), 'blue'),
           ('diff', lambda S: S['_inner'].get('diff', '-'), 'yellow'),
           ('lo', lambda S: S['_inner'].get('lo', '-'), 'cyan'),
           ('hi', lambda S: S['_inner'].get('hi', '-'), 'pink'),
           ('res', lambda S: S['_inner'].get('res', '-'), 'green')],
    captions={
        'str(high)': '`high` 拆成数位，只拆一次，==避免在 dfs 里反复调用 int()==',
        'n = len(high)': '`n = {n}`：最多 {n} 位，所以只会出现 {n} 位的对称整数',
        'str(low).zfill': '`low` 补前导零到 {n} 位，和 `high` 逐位对齐：`{low}`',
        'if diff < 0': lambda S, B, r: (f"右半和已超过左半和：`diff = {S['_inner']['diff']} < 0` → 不可能再回到 0，==剪枝返回 0=="
                                        if S['_inner']['diff'] < 0 else f"`diff = {S['_inner']['diff']} ≥ 0`，还有希望，继续"),
        'if i == n': lambda S, B, r: (f"填完了 {S.n} 位：`diff = {S['_inner']['diff']}`，" +
                                      ('==等于 0== → 左右数位和相等，找到 1 个对称整数' if S['_inner']['diff'] == 0 else '不等于 0 → 不是对称整数，返回 0'))
                                     if S['_inner']['i'] == S.n else f"`i = {S['_inner']['i']}` 还没填完 {S.n} 位，继续",
        'if start < 0 and': lambda S, B, r: (f"这一位的取值范围 `[lo, hi] = [{S['_inner']['lo']}, {S['_inner']['hi']}]`（受 low/high 约束时收窄）。" +
                                            ('前面还没填数字且剩余位数是奇数 → ==这一位只能留空==（对称整数长度必须为偶数）'
                                             if (S['_inner']['start'] < 0 and (S.n - S['_inner']['i']) % 2)
                                             else '可以填数字')),
        'return 0 if lo': _cap_zero,
        'res = 0': '`res` 累加当前位填 `{lo}`…`{hi}` 各个数字后的方案数',
        'res += dfs': '当前位填 `d = {d}`：交给下一层构造后面的数位，累计 `res = {res}`',
        'return res': '这一层所有 `d` 试完，方案数 ==`{ret}`==',
        'return dfs(0': '从最高位开始：还没填数字、`diff = 0`、同时受 low 和 high 约束',
    },
    max_steps=54,
    cards=dict(
        one_liner='逐位构造，记录左半与右半数位和的差，差为 0 就是对称整数',
        complexity='数位 DP 时间 `O(D²n³)`；枚举法 `O((high-low)log high)`',
        problem=['一个 `2n` 位的整数，前 `n` 位数字之和 = 后 `n` 位数字之和，就是==对称整数==',
                 '数出 `[low, high]` 里有多少个对称整数',
                 '本视频示例：`low=1200, high=1230` → `4`（1203、1212、1221、1230）'],
        quote='如果 high = 10^18，方法一就超时了，怎么办？……`start` 表示从左往右第一个非零数字的下标。用于判断现在处于对称整数的左半还是右半。',
        quote_src='—— 灵茶山艾府题解（方法二：上下界数位 DP）',
        idea=['`high` 很大时不能逐个枚举，改成==一位一位填==，用记忆化搜索数方案',
              '`diff` = 左半和 − 右半和：左半加、右半减，最后 `diff == 0` 才算数',
              '`limit_low` / `limit_high` 保证填出的数落在 `[low, high]` 内；前面没填数字且剩余位数为奇数时，这一位留空'],
        summary=['数位 DP 时间 `O(D²n³)`（D=10），空间 `O(Dn³)`',
                 '易错点：`start` 记录首个非零位，决定半场边界 `(start + n) // 2`',
                 '`diff < 0` 要先判断，右半和超过左半和就剪枝',
                 '灵神的方法一：本题数据只到 10^4，直接枚举，把 ASCII 值左半和与右半和比较即可'],
    ),
)
