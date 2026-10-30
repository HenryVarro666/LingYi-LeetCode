def _pos(S):
    i = S['_inner'].get('i')
    s = S.get('s')
    return i if isinstance(i, int) and s is not None and i < len(s) else None


def _info(S):
    I = S['_inner']
    if 'val' not in I:
        return '构造数字：记录「模 k 的余数 val」和「奇偶数位差 diff」'
    return (f"第 `{I['i']}` 位 · 余数 `val={I['val']}` · 奇偶差 `diff={I['diff']}`\n"
            f"贴上界 `{I['is_limit']}` · 已填数 `{I['is_num']}`")


CONFIG = dict(
    num=2827, title='范围中美丽整数的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP · 余数 + 奇偶数位差',
    tags=['灵神题单', '数位 DP', '难度分 2324'],
    code='''
class Solution:
    def numberOfBeautifulIntegers(self, low: int, high: int, k: int) -> int:
        def calc(high: int) -> int:
            s = str(high)
            @cache  # 记忆化搜索
            def dfs(i: int, val: int, diff: int, is_limit: bool, is_num: bool) -> int:
                if i == len(s):
                    return int(is_num and val == 0 and diff == 0)  # 找到了一个合法数字
                res = 0
                if not is_num:  # 可以跳过当前数位
                    res = dfs(i + 1, val, diff, False, False)
                d0 = 0 if is_num else 1  # 如果前面没有填数字，必须从 1 开始（因为不能有前导零）
                up = int(s[i]) if is_limit else 9  # 如果前面填的数字都和 high 的一样，那么这一位至多填 s[i]（否则就超过 high 啦）
                for d in range(d0, up + 1):  # 枚举要填入的数字 d
                    res += dfs(i + 1, (val * 10 + d) % k, diff + d % 2 * 2 - 1, is_limit and d == up, True)
                return res
            return dfs(0, 0, 0, True, False)
        return calc(high) - calc(low - 1)
''',
    call='Solution().numberOfBeautifulIntegers(10, 20, 3)',
    expect=2,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='string', var='s', label='当前上界 s（蓝箭头 = 正在填第 i 位）', pointers={_pos: 'blue'},
             pointer_labels={_pos: 'i'}, cell=80, h=200),
        dict(type='calls', hide=('is_limit',), h=330),
    ],
    watch=[('i', "_inner.get('i')", 'blue'), ('val', "_inner.get('val')", 'orange'),
           ('diff', "_inner.get('diff')", 'pink'), ('up', "_inner.get('up')", 'cyan'),
           ('res', "_inner.get('res')", 'green')],
    skip=[4, 5, 7, 9],
    max_steps=42,
    captions={
        'return calc(high)': '答案 = 不超过 `high` 的美丽数 − 不超过 `low-1` 的美丽数（前缀和思想）',
        's = str(high)': '把上界转成字符串 `s = {s!r}`，逐位去填',
        'if i == len(s)': lambda S, B, r: ('数位全部填完了' if S['_inner']['i'] == len(S.s) else '还有数位要填，继续'),
        'return int(is_num': lambda S, B, r: (
            f"数位填完：`val={S.val}`，`diff={S.diff}`，`is_num={S.is_num}` → "
            + ('填了数、被 `k` 整除、奇偶数位一样多 → ==美丽整数，返回 1==' if r else
               ('没有填任何数 → 不算，返回 0' if not S.is_num else
                (f'`val={S.val}` 不能被 `k` 整除 → 返回 0' if S.val != 0 else f'`diff={S.diff}` ≠ 0，奇偶数位个数不等 → 返回 0')))),
        'if not is_num': lambda S, B, r: ('前面还没填数 → ==当前位可以跳过==（相当于构造更短的数）' if not S.is_num
                                         else '前面已经填了数，当前位必须填'),
        'res = dfs(i + 1, val, diff, False': '跳过这一位：后面不再受上界约束，`val`、`diff` 保持不变，`is_num` 仍为 False',
        'd0 = 0': '`is_num = {is_num}` → ' + '下界 `d0 = {d0}`：没填过数时不能有前导零，只能从 1 起',
        'up = int': '`is_limit = {is_limit}` → 这一位至多填 `up = {up}`（贴上界时不能超过 `s[i]`）',
        'for d in range': '枚举这一位填 `d`，范围 `[{d0}, {up}]`',
        'res += dfs': '填 `d = {d}`：`val` → `(val*10+d) % k`，奇数 `diff+1`、偶数 `diff-1`；只有 `d == up` 才继续贴上界',
        'return res': '这一层合法方案数 `res = {res}`，返回上一层',
        'return dfs(0': '入口：从最高位开始，余数 0、差 0，受上界约束，还没填数',
    },
    cards=dict(
        one_liner='数位 DP：逐位填数，记住「模 k 余数」和「奇偶位数差」',
        complexity='时间 `O(n²kD)`，空间 `O(n²k)`',
        problem=['一个数「奇数位与偶数位个数相同」且「能被 `k` 整除」就是美丽的',
                 '求 `[low, high]` 内美丽整数的个数',
                 '示例：`low=10, high=20, k=3` → `2`（12 和 18）'],
        quote='`diff` 表示奇数数位的数目与偶数数位的数目的差。注意我们无需对奇数数位的数目和偶数数位的数目分别各用一个参数表示，那样效率更低。',
        quote_src='—— 灵茶山艾府题解',
        idea=['区间拆成两个前缀：`calc(high) - calc(low-1)`',
              '`dfs(i, val, diff, is_limit, is_num)`：`val` 是已填部分模 `k`，填 `d` 后变 `(val*10+d) % k`',
              '`diff` 填奇数 +1、偶数 −1；终点要求 `val == 0` 且 `diff == 0`'],
        summary=['时间 `O(n²kD)`，`n` 是 `high` 的位数，`D = 10`',
                 '`is_num` 区分「还没填数」：不能把前导零当成偶数位',
                 '易错点：`low - 1` 可能为 0，`calc(0)` 是 0 个美丽数，没问题',
                 '非 Python 语言 `diff` 会出现负数，可以把入口设为 `n`，终点判断 `diff == n`'],
    ),
)
