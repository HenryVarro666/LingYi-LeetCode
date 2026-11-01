def _even(v):
    return sum(map(int, str(v))) % 2 == 0


CONFIG = dict(
    num=2180, title='统计各位数字之和为偶数的整数个数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='枚举 + 异或记录奇偶（Go 原文转写）', tags=[],
    code='''
class Solution:
    def countEven(self, n: int) -> int:
        ans = 0
        for i in range(1, n + 1):
            s = 0
            x = i
            while x > 0:
                s ^= x % 10 & 1  # 用异或代替加法
                x //= 10
            ans += s ^ 1  # 偶数就 +1
        return ans
''',
    call='Solution().countEven(11)',
    expect=5,
    views=[
        dict(type='text', size=30, h=110, fn=lambda S: (
            f"枚举 `i = {S['i']}`，当前剩下 `x = {S['x']}`，各位和奇偶 `s = {S['s']}`（{'奇' if S['s'] else '偶'}）" if 'i' in S and 'x' in S else '')),
        dict(type='array', var=lambda S: [i for i in range(1, S['n'] + 1)] if 'n' in S else [], label='1 … n（已判定为偶的标绿）', h=190,
             pointers={'i': 'blue'}, cell=70,
             color=lambda S, k, v: 'blue' if v == S.get('i') else ('green' if v < S.get('i', 0) and _even(v) else None)),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink'), ('s', 's', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 计数：各位数字之和为偶数的个数',
        'for i in range': '枚举 `i = {i}`',
        's = 0': '`s` 只记 `{i}` 各位和的奇偶：0 偶，1 奇；`x = {i}` 逐位拆',
        'while x > 0': lambda S, B, r: (f'`x = {S.x}` > 0：还有数位没拆' if S.x > 0 else f'`x = 0`：拆完了'),
        's ^= x % 10': '最低位 `{x % 10}`：{"奇数" if x % 10 & 1 else "偶数"} → 异或 `{x % 10 & 1}`，奇偶状态 `s` {B.s} → =={s}==（目前奇数位有{"奇" if s else "偶"}数个）',
        'x //= 10': '去掉最低位：`x` → {x}',
        'ans += s ^ 1': lambda S, B, r: (f'`s = {S.s}` 偶 → `s ^ 1 = 1`，计入：`ans` → =={S.ans}==' if S.s == 0 else f'`s = {S.s}` 奇 → `s ^ 1 = 0`，不计：`ans` 仍是 {S.ans}'),
        'return ans': '全部枚举完，共 `{ret}` 个',
    },
    skip=['x = i'],
    max_steps=120,
    cards=dict(
        one_liner='数位和的奇偶，只看奇数位有几个，用异或记就行',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['统计 `1` 到 `num` 中，各位数字之和为偶数的数的个数',
                 '示例：`num = 30` → `14`；`num = 4` → `2`',
                 '本视频用 `n = 11`：2、4、6、8、11，共 5 个'],
        quote='用异或代替加法；偶数就 +1。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['逐位拆数字：`x % 10` 取最低位，`x //= 10` 去掉它',
              '只关心和的奇偶，加法换成异或：`s ^= 最低位 & 1`',
              '`s` 为 0 说明和是偶数，`ans += s ^ 1`'],
        summary=['时间 `O(n log n)`（每个数拆 `log n` 位），空间 `O(1)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python（`x /= 10` → `x //= 10`）',
                 '易错点：运算优先级 `x % 10 & 1` 是先取模再按位与',
                 '本题其实有 `O(1)` 的数学做法，数据范围小，枚举即可'],
    ),
)
