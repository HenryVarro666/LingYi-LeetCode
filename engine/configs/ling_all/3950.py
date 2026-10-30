CONFIG = dict(
    num=3950, title='恰好一对连续置位', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='n & (n>>1) 只剩一个 1',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def consecutiveSetBits(self, n: int) -> bool:
        m = n & (n >> 1)  # 所有相邻比特位的 &
        return m > 0 and m & (m - 1) == 0  # m 是否恰好有一个 1
''',
    call='Solution().consecutiveSetBits(50)',
    expect=True,
    views=[
        dict(type='string', var="format(n, '07b')", label='n = 50', h=150, index=False,
             color=lambda S, i, v: None),
        dict(type='string', var="format(n >> 1, '07b')", label='n >> 1（错开一位，对应相邻两位）', h=150, index=False),
        dict(type='string', var=lambda S: format(S['m'], '07b') if 'm' in S else '-------',
             label='m = n & (n >> 1)（1 = 一对相邻的 11）', h=150, index=False,
             color=lambda S, i, v: 'green' if v == '1' and 'm' in S else None),
        dict(type='text', fn=lambda S: (f"m - 1 = `{format(S['m'] - 1, '07b')}`　m & (m-1) = `{format(S['m'] & (S['m'] - 1), '07b')}`"
                                        if S.get('_line', 0) >= 5 and 'm' in S and S['m'] > 0 else ''), size=34, h=90),
    ],
    watch=['n', 'm'],
    captions={
        'm = n &': lambda S, B, r: (f"`n & (n >> 1)` 一次把所有相邻比特做 `&`：相邻的 `11` 变成 1，其余变 0。"
                                    f"`{format(S.n, '07b')}` & `{format(S.n >> 1, '07b')}` = `{format(S.m, '07b')}`"),
        'return m > 0': lambda S, B, r: (f"`m = {S.m}` 有 {bin(S.m).count('1')} 个 1。恰好一对 `11` ⇔ m 恰好一个 1，"
                                         f"用 `m & (m-1)` 去掉最低位 1 后为 `{S.m & (S.m - 1)}`（为 0 即只有一个）→ =={r}=="),
    },
    cards=dict(
        one_liner='n 和 n>>1 按位与：每个 1 就是一对相邻置位',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['二进制里恰好有一对相邻的 `1`（置位）才返回 `true`', '示例：`6 = 110` → `true`；`5 = 101` → `false`',
                 '本视频：`50 = 110010` → `true`'],
        quote='计算 n & (n >> 1) 等价于计算 n 的所有相邻比特位的 &。所有相邻的 11 变成 1，其余变成 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`n` 与 `n >> 1` 错开一位，同一位对应相邻两位', '相邻 `11` ⇒ 结果位为 1，所以数 1 的个数就是数 `11` 的对数',
              '恰好一个 1 ⇒ `m > 0 and m & (m - 1) == 0`（2 的幂判定）'],
        after=[dict(heading='方法一：逐位遍历', lines=['`while n > 1`：若 `n & 3 == 3`（最低两位是 11）`cnt += 1`', '每次 `n >>= 1`，最后判断 `cnt == 1`，时间 `O(log n)`'])],
        summary=['方法二时间、空间均为 `O(1)`',
                 '易错：必须 `m > 0`，否则 `m = 0`（没有 11）也满足 `m & (m-1) == 0`',
                 '`111` 会产生两对 `11`（`m` 有两个 1），所以不算「恰好一对」',
                 '思考题：恰好一个 `111` → `n & (n>>1) & (n>>2)` 只剩一个 1，同样判 2 的幂'],
    ),
)
