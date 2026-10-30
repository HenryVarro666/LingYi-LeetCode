def _in(S, k):
    return S['_inner'].get(k)


def _bits(m):
    return '{' + ','.join(str(d) for d in range(10) if m >> d & 1) + '}'


def _txt(S):
    inn = S['_inner']
    if 'mask' not in inn:
        return '正难则反：数出 `[1, n]` 里==没有重复数字==的个数，用 `n` 减去它'
    return (f"第 {inn['i']} 位：已用数字集合 mask = =={_bits(inn['mask'])}==；"
            f"贴着 n = {inn['is_limit']}，已开始填数 = {inn['is_num']}")


CONFIG = dict(
    num=1012, title='至少有 1 位重复的数字', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='正难则反 + 数位 DP（mask 记录已选数字）',
    tags=['灵神题单', '动态规划', '难度分 2230'],
    code='''
class Solution:
    def numDupDigitsAtMostN(self, n: int) -> int:
        s = str(n)
        @cache  # 记忆化搜索
        def f(i: int, mask: int, is_limit: bool, is_num: bool) -> int:
            if i == len(s):
                return int(is_num)  # is_num 为 True 表示得到了一个合法数字
            res = 0
            if not is_num:  # 可以跳过当前数位
                res = f(i + 1, mask, False, False)
            low = 0 if is_num else 1  # 如果前面没有填数字，必须从 1 开始（因为不能有前导零）
            up = int(s[i]) if is_limit else 9  # 如果前面填的数字都和 n 的一样，那么这一位至多填 s[i]（否则就超过 n 啦）
            for d in range(low, up + 1):  # 枚举要填入的数字 d
                if (mask >> d & 1) == 0:  # d 不在 mask 中
                    res += f(i + 1, mask | (1 << d), is_limit and d == up, True)
            return res
        return n - f(0, 0, True, False)
''',
    call='Solution().numDupDigitsAtMostN(20)',
    expect=1,
    views=[
        dict(type='string', var='s', label='s = str(n)（蓝 = 当前位）', cell=80, h=150,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('i') else None),
        dict(type='text', fn=_txt, size=24, h=90),
        dict(type='calls', h=250),
    ],
    watch=[('i', lambda S: _in(S, 'i'), 'blue'),
           ('mask', lambda S: _bits(_in(S, 'mask')) if _in(S, 'mask') is not None else None, 'cyan'),
           ('low', lambda S: _in(S, 'low'), 'green'), ('up', lambda S: _in(S, 'up'), 'orange'),
           ('res', lambda S: _in(S, 'res'), 'yellow')],
    skip=['for d in range', 's = str(n)', 'res = 0', '@cache'],
    captions={
        'if i == len(s)': lambda S, B, ret: ('填完所有数位：`is_num` 为真才是一个合法数字（没有重复），返回 `1`；没填过数字返回 `0`'
                                              if S.i == len(S.s) else f'`i = {S.i} < {len(S.s)}`：还没填完，继续'),
        'res = f(i + 1, mask, False, False)': '`is_num` 为假：==可以跳过这一位==（数字位数比 n 少），后面不再受 n 约束，`mask` 不变',
        'low = 0 if is_num': '`low = {low}`：前面没填过数就必须从 1 开始（无前导零）；填过了就从 0 开始',
        'up = int(s[i])': '`up = {up}`：贴着 n 时这一位至多填 `s[{i}]`，否则可以填到 9',
        'for d in range': lambda S, B, ret: (
            f'`d` 已经枚举到上限 `up = {S.up}`，这一位结束' if S.d >= S.up and B.get('d') == S.d and B.get('mask') == S.mask else
            f'枚举要填的数字 `d`（`{S.low}` 到 `{S.up}`），轮到 `d = {S.d}`'),
        'if (mask >> d & 1) == 0': lambda S, B, ret: (
            f'枚举 `d = {S.d}`（`{S.low}` 到 `{S.up}`）：不在 mask `{_bits(S.mask)}` 里 → 可以填' if (S.mask >> S.d & 1) == 0 else
            f'枚举 `d = {S.d}`：==已经在 mask `{_bits(S.mask)}` 里==，填了就会重复，跳过'),
        'res += f(i + 1': '填 `d = {d}`：`mask` 变成 `{_bits(mask | (1 << d))}`；`is_limit` = `{is_limit and d == up}`，`is_num` = True',
        'return res': '这一位及之后的无重复数共 `{res}` 个',
        'return n - f(0, 0, True, False)': lambda S, B, ret: (
            '`f(0, 0, True, False)` 数的是 `[1, n]` 里==无重复==的数；答案 = `n` 减去它' if ret is None else
            f'无重复的数共 `{S.n - ret}` 个 → 有重复的 = `{S.n}` − `{S.n - ret}` = ==`{ret}`=='),
        'return int(is_num)': lambda S, B, ret: '填完了且 `is_num` 为真：得到一个无重复的数 → 返回 `1`' if S.is_num else '一位都没填：不是合法数字 → 返回 `0`',
    },
    max_steps=50,
    cards=dict(
        one_liner='正难则反：数「没有重复数字」的个数，n 减去它',
        complexity='时间 `O(m·D·2^D)`，空间 `O(m·2^D)`，`m = log n`，`D = 10`',
        problem=['给正整数 `n`，求 `[1, n]` 中==至少有 1 位重复==数字的整数个数',
                 '示例：`n=100` → `10`（11、22、…、99、100）',
                 '本视频：`n=20` → `1`（只有 11）'],
        quote='正难则反，转换成求无重复数字的个数。答案等于 n 减去无重复数字的个数。mask 表示前面选过的数字集合，换句话说，第 i 位要选的数字不能在 mask 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `f(i, mask, is_limit, is_num)`：`mask` 是前面选过的数字集合（位运算）',
              '`is_limit` = 是否贴着 `n`；`is_num` = 前面是否已经填了数字（不然可以跳过当前位）',
              '枚举 `d` 时只要 `d` 不在 `mask` 里就能填，填完把 `d` 加进 `mask`'],
        summary=['时间 `O(m·D·2^D)`：状态 `m·2^D`，每个状态枚举 `D` 个数字',
                 '`is_num` 为假才能跳过当前位，同时从 1 开始填，避免前导零',
                 '`is_num` 其实可以用 `mask != 0` 代替；也可以只对 `(i, mask)` 记忆化',
                 '最后别忘了 `n - f(...)`：`f` 数的是==无重复==的数'],
    ),
)
