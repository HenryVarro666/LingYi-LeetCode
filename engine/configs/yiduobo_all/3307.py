def _idx(S):
    return S.get('index') if S['_line'] >= 14 else None


def _txt(S):
    if 'half' in S and 'k' in S:
        return f"每个操作后的字符串长度 = `2 × half`，现在 `half` = `{S['half']}`；`k` = ==`{S['k']}`== {'在右半段（> half）' if S['k'] > S['half'] else '在左半段（<= half）'}"
    if 'length' in S:
        return f"模拟长度：`length` = `{S['length']}`，目标 `k` = `{S['k']}`"
    return ''


CONFIG = dict(
    num=3307, title='找出第 K 个字符 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='倍增找长度 + 从后往前消除操作',
    tags=['位运算', '贪心与思维'],
    code='''
class Solution(object):
    def kthCharacter(self, k, operations):

        length = 1
        p = 0
        while length < k:
            length += length
            p += 1
        
        p -= 1
        delta = 0
        half = length >> 1

        for index in range(p, -1, -1):
            if k > half:
                k -= half
                delta += operations[index]
            half >>= 1

        return chr(97 + delta % 26)
''',
    call='Solution().kthCharacter(10, [0, 1, 0, 1])',
    expect='b',
    views=[
        dict(type='text', fn=_txt, size=26, h=70),
        dict(type='array', var='operations', label='operations（蓝 = 正在消除的那一次）', cell=84, h=230,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'index'}),
        dict(type='text', fn=lambda S: (f"`delta` = {S['delta']}：从 `a` 往后数 {S['delta']} 个字母 → `{chr(97 + S['delta'] % 26)}`" if 'delta' in S else ''), size=26, h=70),
    ],
    watch=[('length', 'length', 'cyan'), ('p', 'p', 'purple'), ('k', 'k', 'blue'), ('half', 'half', 'orange'), ('delta', 'delta', 'green')],
    skip=['length = 1', 'p = 0', 'p += 1'],
    captions={
        'while length < k': lambda S, B, r: (f'`length = {S.length} < k = {S.k}`：还没覆盖到第 `k` 个，再操作一轮' if S.length < S.k
                                             else f'`length = {S.length} >= k = {S.k}`：第 `k` 个字符已在其中，`p = {S.p}` 次操作够了'),
        'length += length': '每轮操作长度翻倍 → `length = {length}`（只需知道长度，不用真造字符串）',
        'p -= 1': '`p` 退一格，指向最后一个有用的操作下标 `{p}`；之后的操作都影响不到第 `k` 个字符',
        'delta = 0': '`delta` 记录：一路上有多少次「变成下一个字母」',
        'half = length >> 1': '最后一次操作前字符串长 `half = {half}`，操作产出的右半段是它的副本',
        'for index': lambda S, B, r: (f'从后往前，逐个消除操作 `index = {S.index}`' if S.half > 0 else '`0` 号操作也消除完了，循环结束'),
        'if k > half': lambda S, B, r: (f'`k = {S.k} > half = {S.half}` → 第 `k` 个在右半段，是这次操作复制出来的' if S.k > S.half
                                        else f'`k = {S.k} <= half = {S.half}` → 在左半段，没受 `operations[{S.index}]` 影响'),
        'k -= half': '对应前半段的第 `k - half` 个：`k` → `{k}`',
        'delta += operations': '`operations[{index}] = {operations[index]}`：0 原样复制，1 要加一 → `delta = {delta}`',
        'half >>= 1': '换到上一次操作：`half` 减半 → `{half}`',
        'return chr': '还原到最初的 `a`，往后数 `delta = {delta}` 个 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='先倍增找出操作数，再从后往前一个个消除操作的影响',
        complexity='时间 `O(log k)`，空间 `O(1)`（`log k` 约 47）',
        problem=['`word` 初始为 `a`；操作 0：复制拼到后面；操作 1：每个字母变成下一个再拼上去',
                 '执行完全部操作后求第 `k` 个字符，`k` 最大 `10^14`',
                 '示例：`k = 10, operations = [0,1,0,1]` → `b`'],
        quote='注意到每轮操作并不会影响到原始的word，也就是说一旦生成了第k个字符，后续的operations就没有用了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`length` 从 1 倍增到 `>= k`：得到有用的操作数 `p`，后面的操作可忽略',
              '`k > half`：它是复制出来的，等价于前半段第 `k - half` 个，操作 1 记 `delta += 1`',
              '`k <= half`：不受这次操作影响。逐个消除到只剩 `a`，再加 `delta`'],
        summary=['时间 `O(log k)`，空间 `O(1)`',
                 '易错点：`while` 结束后 `p -= 1`，因为第 `p` 次操作（下标 `p-1`）才是最后一个有用的',
                 '`delta` 要对 26 取模（`z` 后面是 `a`）',
                 '对比灵神：他用递归 `pop` 操作，这里先倍增算长度再迭代；两者本质都是数 `a` 要加几次'],
    ),
)
