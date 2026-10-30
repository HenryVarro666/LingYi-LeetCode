def _ans_color(S, i, v):
    if 'i' not in S:
        return None
    if i == S['i']:
        return 'green' if v == '1' and S['_line'] >= 12 else 'blue'
    return None


CONFIG = dict(
    num=3849, title='重新排列后的最大按位异或值', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='从高位贪心 · 剩余 0/1 计数',
    tags=['灵神题单', '难度分 1556'],
    code='''
class Solution:
    def maximumXor(self, s: str, t: str) -> str:
        cnt0 = t.count('0')
        left = [cnt0, len(t) - cnt0]  # t 中剩余的 0 和 1 的个数

        ans = list(s)
        for i, ch in enumerate(ans):
            x = int(ch)
            # 如果 x 是 0，那就看还有没有剩下的 1
            # 如果 x 是 1，那就看还有没有剩下的 0
            if left[x ^ 1] > 0:
                left[x ^ 1] -= 1
                ans[i] = '1'  # x ^ (x ^ 1) = 1
            else:  # 只能让两个相同的数异或
                left[x] -= 1
                ans[i] = '0'  # x ^ x = 0
        return ''.join(ans)
''',
    call="Solution().maximumXor('0110', '1110')",
    expect='1101',
    views=[
        dict(type='string', var='s', pointers={'i': 'blue'}, h=200, label='s（固定不动）'),
        dict(type='array', var='left', h=170, label='left：t 中剩余的 [0 的个数, 1 的个数]',
             color=lambda S, i, v: ('yellow' if 'x' in S and i == (S['x'] ^ 1) and S['_line'] in (11, 12) else None)),
        dict(type='array', var='ans', h=200, label='ans：先是 s 的拷贝，逐位改成异或结果', color=_ans_color, pointers={'i': 'blue'}),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'cyan'), ('left', 'left', 'orange')],
    captions={
        'cnt0 = t.count': 't 里有 `{cnt0}` 个 `0`',
        'left = [cnt0': '`left = {left}`：t 里剩下的 0 和 1 各多少个，位置可以任意排',
        'ans = list(s)': '`ans` 先拷贝 s，后面逐位改成异或结果',
        'x = int(ch)': '处理 `s[{i}] = {x}`：高位优先，这位想要异或出 `1`',
        'if left[x ^ 1] > 0': lambda S, B, r: (f"`s[{S['i']}] = {S['x']}`，需要 t 放 `{S['x'] ^ 1}`，还剩 `{S['left'][S['x'] ^ 1]}` 个 → 有，可以得到 1"
                                               if S['left'][S['x'] ^ 1] > 0 else
                                               f"`s[{S['i']}] = {S['x']}`，需要 t 放 `{S['x'] ^ 1}`，但已经没有了 → 只能放相同的"),
        'left[x ^ 1] -= 1': '用掉一个 `{x ^ 1}`：`left = {left}`',
        "ans[i] = '1'": '`{x} ^ {x ^ 1} = 1`：这一位是 `1`，`ans = {"".join(ans)}`',
        'left[x] -= 1': '被迫用一个相同的 `{x}`：`left = {left}`',
        "ans[i] = '0'": '`{x} ^ {x} = 0`：这一位只能是 `0`，`ans = {"".join(ans)}`',
        'return': '拼成答案 `{"".join(ans)}`',
    },
    cards=dict(
        one_liner='高位优先：能异或出 1 就一定去拿',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制串 `s`、`t` 等长，`t` 可任意重排，`s` 不动',
                 '求 `s` 异或重排后 `t` 的最大值（仍是二进制串）',
                 '示例：`s="0110"`，`t="1110"` → `"1101"`'],
        quote='为了让异或结果尽量大，我们要优先满足异或结果的高位是 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['重排 t 只关心“还剩几个 0、几个 1”，所以用 `left` 计数',
              '从左到右：s 是 0 就找剩下的 1，s 是 1 就找剩下的 0，两种情况合并成 `x ^ 1`',
              '没得选时只能放相同的数，这一位是 0'],
        summary=['时间 `O(n)`，空间 `O(n)`（原地改 s 可到 `O(1)`）',
                 '`x ^ 1` 把两种情况合并：s 是 0 找 1，s 是 1 找 0',
                 '易错点：没得选时也要扣掉 `left[x]`，因为这位仍然占了 t 的一个字符',
                 '同类：从最左开始贪心，高位的 1 比后面所有位加起来都重要'],
    ),
)
