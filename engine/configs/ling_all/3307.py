def _sub(S):
    if 'k' not in S or 'operations' not in S:
        return ''
    n = len(S['operations'])
    return f"子问题：前 `{n}` 次操作后的字符串（长 `{2 ** n}`）里的第 ==`{S['k']}`== 个字符"




CONFIG = dict(
    num=3307, title='找出第 K 个字符 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='倒着看：递归去掉最后一次操作',
    tags=['位运算', '贪心与思维'],
    code='''
class Solution:
    def kthCharacter(self, k: int, operations: List[int]) -> str:
        if not operations:
            return 'a'
        op = operations.pop()
        # 注意 pop 之后 operations 的长度减少了 1，所以下面写的是 1<<n 而不是 1<<(n-1)
        m = 1 << len(operations)
        if k <= m:  # k 在左半段
            return self.kthCharacter(k, operations)
        # k 在右半段
        ans = self.kthCharacter(k - m, operations)
        return ascii_lowercase[(ord(ans) - ord('a') + op) % 26]
''',
    setup='from string import ascii_lowercase',
    call='Solution().kthCharacter(10, [0, 1, 0, 1])',
    expect='b',
    views=[
        dict(type='text', fn=_sub, size=28, h=70),
        dict(type='array', var='operations', label='operations（每层 pop 掉最后一个）', cell=84, h=150),
        dict(type='calls', h=330),
    ],
    watch=[('k', 'k', 'blue'), ('op', 'op', 'purple'), ('m', 'm', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'if not operations': lambda S, B, r: ('没有操作了：字符串就是最初的 `a`' if not S.operations
                                              else f'还剩 `{len(S.operations)}` 次操作，继续看最后一次'),
        'return \'a\'': '递归边界：没有操作，只有最初的字母 `a`',
        'op = operations.pop()': '去掉最后一次操作，它是 `{op}`（0 复制，1 复制并加一）。前面的字符串不受它影响',
        'm = 1 <<': '去掉后还剩 `{len(operations)}` 次操作，前半段长 `m = 2^{len(operations)} = {m}`',
        'if k <= m': lambda S, B, r: (f'`k = {S.k} <= m = {S.m}` → 在左半段，没被 `op` 改动，直接去掉这次操作' if S.k <= S.m
                                      else f'`k = {S.k} > m = {S.m}` → 在右半段，是前半段对应位置的副本'),
        'return self.kthCharacter(k, operations)': '左半段：同一个 `k`，问题缩小一层',
        'ans = self.kthCharacter': '右半段：第 `{B.k}` 个字符 = 前半段第 `k - m = {B.k} - {B.m} = {B.k - B.m}` 个字符，再按 `op = {B.op}` 变换',
        'return ascii_lowercase': '子问题返回 `{ans}`，加上 `op = {op}` → ==`{ret}`==（`op = 1` 时变成下一个字母）',
    },
    cards=dict(
        one_liner='倒着想：最后一次操作只复制前半段，去掉它问题就缩小一半',
        complexity='时间 `O(n)`（`n` 为操作数，最多 `log k` 层有用），空间 `O(n)`',
        problem=['`word` 初始为 `a`；操作 0：复制拼到自己后面；操作 1：每个字母变成下一个再拼上去',
                 '执行完全部操作后，求第 `k` 个字符，`k` 最大 `10^14`，不能模拟',
                 '示例：`k = 10, operations = [0,1,0,1]` → `b`'],
        quote='如果 k > 2^(n-1)，那么第 k 个字母在 S 的右半段，问题等价于去掉 operations[n-1]，计算右半段的第 k-2^(n-1) 个字母的子问题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每次操作字符串长度翻倍，`n` 次后长 `2^n`',
              '`k` 在左半段：不受最后一次操作影响，直接去掉它',
              '`k` 在右半段：对应前半段第 `k - 2^(n-1)` 个字母，若 `op = 1` 返回的字母再加 1'],
        summary=['时间 `O(n)`，递归深度为操作数；`pop` 会改动传入的列表',
                 '易错点：`pop` 之后 `len(operations)` 已减 1，所以 `m = 1 << len(operations)`',
                 '本质是数 `a` 需要加几次：题解的迭代写法只看 `k-1` 二进制里的 1，累加对应的 `operations[i]`',
                 '`ascii_lowercase` 用 `from string import ascii_lowercase` 补上'],
    ),
)
