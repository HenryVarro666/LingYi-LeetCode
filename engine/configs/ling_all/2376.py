def _I(S):
    return S['_inner']


def _ptr(S):
    i = _I(S).get('i')
    return i if i is not None and 0 <= i < len(S['s']) else None


def _digits(m):
    return '{' + ','.join(str(d) for d in range(10) if m >> d & 1) + '}'


CONFIG = dict(
    num=2376, title='统计特殊整数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP（mask + is_limit + is_num）',
    tags=['灵神题单', '数位 DP', '难度分 2120'],
    code='''
class Solution:
    def countSpecialNumbers(self, n: int) -> int:
        s = str(n)
        @cache  # 缓存装饰器，避免重复计算 dfs 的结果（记忆化）
        def dfs(i: int, mask: int, is_limit: bool, is_num: bool) -> int:
            if i == len(s):
                return 1 if is_num else 0  # is_num 为 True 表示得到了一个合法数字
            res = 0
            if not is_num:  # 可以跳过当前数位
                res = dfs(i + 1, mask, False, False)
            # 如果前面没有填数字，则必须从 1 开始（因为不能有前导零）
            low = 0 if is_num else 1
            # 如果前面填的数字都和 n 的一样，那么这一位至多填 s[i]（否则就超过 n 啦）
            up = int(s[i]) if is_limit else 9
            for d in range(low, up + 1):  # 枚举要填入的数字 d
                if mask >> d & 1 == 0:  # d 不在 mask 中，说明之前没有填过 d
                    res += dfs(i + 1, mask | (1 << d), is_limit and d == up, True)
            return res
        return dfs(0, 0, True, False)
''',
    call='Solution().countSpecialNumbers(12)',
    expect=11,
    views=[
        dict(type='string', var='s', label='s = str(n)（蓝箭头 = 正在填的数位 i）', cell=64, h=160,
             pointers={_ptr: 'blue'}, pointer_labels={_ptr: 'i'}),
        dict(type='text', h=56, fn=lambda S: (
            f"已用数字 `mask` = ==`{_digits(_I(S)['mask'])}`==，`is_limit = {_I(S)['is_limit']}`，`is_num = {_I(S)['is_num']}`"
            if 'mask' in _I(S) else '')),
        dict(type='calls', h=330, hide=()),
    ],
    skip=['if i == len(s)', 'res = 0', 'low = 0', 'for d in range'],
    watch=[('i', "_inner['i']", 'blue'), ('mask', "_inner.get('mask')", 'pink'),
           ('d', "_inner.get('d')", 'yellow'), ('res', "_inner.get('res')", 'green')],
    captions={
        'if i == len(s)': lambda S, B, r: (f'`i == {len(S.s)}`：所有数位处理完了' if S.i == len(S.s) else f'`i = {S.i} < {len(S.s)}`，还有数位要处理'),
        'return 1 if is_num': '{"填完了且填过数字：构造出一个特殊整数 → 返回 1" if is_num else "一位都没填（空数）→ 返回 0"}',
        'if not is_num': lambda S, B, r: ('没填过数字 → ==可以跳过这一位==，构造更短的数' if not S.is_num
                                         else '前面已经填了数字，这一位必须填'),
        'res = dfs(i + 1, mask, False, False)': '跳过：位数更少必小于 n → `is_limit = False`',
        'low = 0': '`low = {low}`：' + '{"前面填过数字，可以从 0 开始" if is_num else "还没填数字，首位不能是 0（没有前导零）"}',
        'up = int': lambda S, B, r: (f'`is_limit = True`：前面都和 n 一样，这一位至多填 `s[{S.i}] = {S.up}`' if S.is_limit
                                     else '`is_limit = False`：前面已经比 n 小，这一位至多填 `9`'),
        'if mask >> d': lambda S, B, r: (f'枚举 `d = {S.d}`（范围 {S.low}~{S.up}）：不在 `{_digits(S.mask)}` 中 → ==没用过，可以填=='
                                         if S.mask >> S.d & 1 == 0 else f'枚举 `d = {S.d}`（范围 {S.low}~{S.up}）：已在 `{_digits(S.mask)}` 中 → ==重复数字，不能填=='),
        'res += dfs': lambda S, B, r: f'填 `{S.d}`：`mask` → `{_digits(S.mask | (1 << S.d))}`，进入下一位',
        'return res': '这一层得到 `res = {res}` 个，返回上一层',
        'return dfs(0, 0, True, False)': '入口：从 `s[0]` 开始，`mask` 空集，受 n 约束，还没填数字',
    },
    cards=dict(
        one_liner='逐位填数字，用 mask 记录用过的数字，不许重复',
        complexity='时间 `O(m·D·2^D)`，空间 `O(m·2^D)`（`m = log n`，`D = 10`）',
        problem=['如果一个正整数每一位数字都互不相同，称它为特殊整数',
                 '求 `[1, n]` 中特殊整数的个数',
                 '示例：`n = 20` → `19`（只有 `11` 不是）',
                 '本视频：`n = 12` → `11`'],
        quote='`mask` 表示前面选过的数字集合，换句话说，第 `i` 位要选的数字不能在 `mask` 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, mask, is_limit, is_num)`：构造第 `i` 位及之后数位的合法方案数',
              '`is_limit`：前面和 n 一样时，这一位至多填 `s[i]`；`is_num`：前面是否填过数字，用来处理前导零',
              '用位运算当集合：`mask >> d & 1` 判断，`mask | (1 << d)` 加入'],
        summary=['时间 `O(m·D·2^D)`：状态 `O(m·2^D)`，每个状态枚举 `D` 个数字',
                 '易错点：不填数字时 `low = 1`、`is_limit` 变 False；终点要看 `is_num`',
                 '`is_num` 在本题可由 `mask != 0` 代替，保留它是为了方便掌握模板',
                 '可以只记忆化 `(i, mask)`：只有 `is_limit = False` 且 `is_num = True` 的状态会重复出现'],
    ),
)
