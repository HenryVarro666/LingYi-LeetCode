TARGET = [2, 3, 5]


def _replay(ans):
    """按 ans 里的操作模拟一遍栈"""
    st, cur = [], 0
    for op in ans or []:
        if op == 'Push':
            cur += 1
            st.append(cur)
        else:
            st.pop()
    return st


def _stream_color(S, i, v):
    x = S.get('x')
    if x is None:
        return None
    if v == x:
        return 'yellow'
    if v < x:
        return 'green' if v in S['target'] else None
    return None


def _stream_dim(S, i, v):
    x = S.get('x')
    return x is not None and v < x and v not in S['target']


def _if(S, B, ret):
    x, i, t = S.x, S.i, S.target
    if x == t[i]:
        return f'`x = {x} == target[{i}] = {t[i]}`：==是我们要的数=='
    tail = '（target 严格递增，`x` 不会超过 `target[i]`）' if x == 1 else ''
    return f'`x = {x} < target[{i}] = {t[i]}`：不是我们要的数' + tail


CONFIG = dict(
    num=1441, title='用栈操作构建数组', difficulty='Medium', category='栈',
    author='灵茶山艾府', technique='阅读理解 · 先入栈，不要就弹出',
    tags=['字节30天'],
    code='''
class Solution:
    def buildArray(self, target: List[int], n: int) -> List[str]:
        ans = []
        i = 0
        for x in range(1, target[-1] + 1):
            ans.append("Push")  # 先把 x 入栈（题目要求）
            if x == target[i]:  # x 是我们要的数
                i += 1
            else:  # x 不是我们要的数，出栈
                ans.append("Pop")
        return ans
''',
    call=f'Solution().buildArray({TARGET}, 6)',
    expect=['Push', 'Pop', 'Push', 'Push', 'Push', 'Pop', 'Push'],
    views=[
        dict(type='array', var=lambda S: list(range(1, S['target'][-1] + 1)), label='整数流 1, 2, …（只读到 target[-1]）',
             cell=84, color=_stream_color, dim=_stream_dim),
        dict(type='array', var='target', label='target（i 指向下一个想要的数）', cell=84, pointers={'i': 'pink'},
             color=lambda S, k, v: 'green' if k < S.get('i', 0) else None),
        dict(type='stack', var=lambda S: _replay(S.get('ans')), label='栈（按 ans 模拟）', h=120),
        dict(type='array', var='ans', label='ans（操作序列）', cell=112, h=140),
    ],
    watch=[('x', 'x', 'yellow'), ('i', 'i', 'pink')],
    captions={
        'ans = []': '`ans` 记录操作序列',
        'i = 0': '`i = 0`：指向 `target` 里==下一个想要的数==',
        'for x in range': lambda S, B, r: (
            f'从流中读取 `x = {S.x}`' if 'x' not in B or S.x != B.x
            else f'读完 `target[-1] = {S.target[-1]}` 就停：栈已经等于 target，==不再读后面的数=='),
        'ans.append("Push")': lambda S, B, r: (f'先把 `{S.x}` 入栈：==不管要不要，都得先 Push==（题目要求）' if S.x == 1
                                               else f'先 Push `{S.x}`'),
        'if x == target[i]': _if,
        'i += 1': '`{x}` 留在栈里，`i` → `{i}`，下一个想要的数' + "{'是 ' + str(target[i]) if i < len(target) else '没有了'}",
        'ans.append("Pop")': '不是我们要的数 → ==出栈==：`ans` 末尾加 `"Pop"`',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='依次读 1, 2, …：每个数先 Push，不在 target 里就再 Pop',
        complexity='时间 `O(mx)`，空间 `O(1)`（返回值不计；`mx` = target 最后一个数）',
        problem=['给数组 `target` 和整数 `n`，从流 `1..n` 依次读数，用 `"Push"`/`"Pop"` 使栈（底→顶）等于 `target`',
                 '读到的数必须先 Push；栈等于 `target` 后立刻停止',
                 '示例：`target = [1,3], n = 3` → `["Push","Push","Pop","Push"]`',
                 '本视频：`target = [2,3,5], n = 6`'],
        quote='先把 x 入栈。如果 `x = target[i]`，那么 ==x 是我们要的数==，把 i 加一……否则 `x < target[i]`，那么 ==x 不是我们要的数==，把 x 出栈。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`target` 的最后一个数 `mx` 读完，栈就等于 `target` → 只枚举 `x = 1..mx`',
              '指针 `i` 指向 `target` 中下一个想要的数',
              '由于 `target` 严格递增，`x ≤ target[i]` 始终成立'],
        result='`["Push","Pop","Push","Push","Push","Pop","Push"]` ✓（6 不用读）',
        summary=['时间 `O(mx)`，空间 `O(1)`（返回值不计）',
                 '易错：不要的数也必须==先 Push 再 Pop==，不能直接跳过',
                 '易错：循环到 `target[-1]` 就停，不是到 `n`',
                 '用不到 `n`：题目保证 `target[i] ≤ n`'],
    ),
)
