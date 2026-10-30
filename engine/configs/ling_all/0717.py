CONFIG = dict(
    num=717, title='1 比特与 2 比特字符', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='从左到右解码',
    tags=[],
    code='''
class Solution:
    def isOneBitCharacter(self, bits: List[int]) -> bool:
        n = len(bits)
        i = 0
        while i < n - 1:  # 循环直到剩下至多一个数字
            i += bits[i] + 1  # 如果 bits[i] == 1 则跳过下一位
        return i == n - 1  # 注意题目保证 bits[n-1] == 0，无需判断
''',
    call='Solution().isOneBitCharacter([1,1,0,1,0,0])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: ('' if 'i' not in S else f"剩余未解码：从下标 `{S['i']}` 开始，共 `{len(S['bits']) - S['i']}` 位")),
        dict(type='array', var='bits', pointers={'i': 'blue'}, h=300,
             color=lambda S, i, v: 'pink' if 'i' in S and i == len(S['bits']) - 1 else None,
             dim=lambda S, i, v: 'i' in S and i < S['i']),
    ],
    watch=[('n', 'n', 'purple'), ('i', 'i', 'blue')],
    captions={
        'while i < n - 1': lambda S, B, r: (f"`i = {S.i} < n - 1 = {S.n - 1}`：还剩至少两位 → 继续解码" if S.i < S.n - 1
                                              else f"`i = {S.i} >= n - 1 = {S.n - 1}`：剩下至多一个数字 → 停止"),
        'i += bits[i]': lambda S, B, r: (f"`bits[{B.i}] = {S.bits[B.i]}`：" + ("是 0，一比特字符，==跳过 1 位==" if S.bits[B.i] == 0 else "是 1，两比特字符，==连下一位一起跳过 2 位==") + f"，`i` → {S.i}"),
        'return i == n - 1': lambda S, B, r: (f"`i = {S.i}`，`n - 1 = {S.n - 1}`：恰好停在最后一位 → 最后一个字符是一比特，返回 ==True==" if S.i == S.n - 1
                                              else f"`i = {S.i}` 越过了最后一位：最后的 0 被两比特字符吃掉 → 返回 ==False=="),
    },
    cards=dict(
        one_liner='第一位能唯一确定字符类型：0 是一比特，1 是两比特',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一比特字符是 `0`，两比特字符是 `10` 或 `11`',
                 '`bits` 以 `0` 结尾，问最后一个字符是不是一比特字符',
                 '示例：`[1,1,1,0]` → `False`；`[1,0,0]` → `True`'],
        quote='两种字符替换后的第一个数字一定是不同的，一个是 0，另一个是 1。换句话说，我们可以通过 bits[0] 确定字符串的第一个字符。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 `a -> 0`，`b -> 10` 想成编码：看第一位就知道是 a 还是 b',
              '`bits[i] = 0` 去掉 1 位，`bits[i] = 1` 去掉 2 位，用 `i += bits[i] + 1` 一句搞定',
              '剩下 1 位：必是最后的 0 → True；刚好用完：最后一个是 `b` → False'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环条件是 `i < n - 1`，不是 `i < n`：停在 `n-1` 说明最后的 0 独立成字符',
                 '题目保证 `bits[n-1] = 0`，所以不用再判断最后一位'],
    ),
)
