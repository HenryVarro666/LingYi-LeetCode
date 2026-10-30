def _sim(s, k):
    """逐字符模拟同一算法，返回每个 i 的 (压入后, 消除后) 栈快照"""
    st, out = [], []
    for b in s:
        if st and st[-1][0] == b:
            st[-1][1] += 1
        else:
            st.append([b, 1])
        a = [list(x) for x in st]
        if b == ')' and len(st) > 1 and st[-1][1] == k and st[-2][1] >= k:
            st.pop()
            st[-1][1] -= k
            if st[-1][1] == 0:
                st.pop()
        out.append((a, [list(x) for x in st]))
    return out


def _idx(S):
    """当前正在处理 s 的第几个字符（不在循环里返回 -1）"""
    if 'b' not in S or 'st' not in S:
        return -1
    s, k, b = S['s'], S['k'], S['b']
    st = [list(x) for x in S['st']]
    sim = _sim(s, k)
    prev = [[]] + [c for _, c in sim]
    for i, ch in enumerate(s):
        if ch != b:
            continue
        if st in (prev[i], sim[i][0], sim[i][1]):
            return i
    return -1


def _top(S):
    st = S.get('st')
    if st is None:
        return ''
    cur = ''.join(b * c for b, c in st)
    return f"栈里压缩的内容还原：`{cur or '（空）'}`"


CONFIG = dict(
    num=3703, title='移除K-平衡子字符串', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 + 连续字符计数（压缩）',
    tags=['栈', '邻项消除', '难度分 1802'],
    code='''
class Solution:
    def removeSubstring(self, s: str, k: int) -> str:
        st = []  # 栈中保存 [字符, 连续出现次数]
        for b in s:
            if st and st[-1][0] == b:
                st[-1][1] += 1  # 连续相同括号个数 +1
            else:
                st.append([b, 1])  # 新的括号

            # 栈顶的 k 个右括号与栈顶下面的 k 个左括号抵消
            if b == ')' and len(st) > 1 and st[-1][1] == k and st[-2][1] >= k:
                st.pop()
                st[-1][1] -= k
                if st[-1][1] == 0:
                    st.pop()

        return ''.join(b * cnt for b, cnt in st)
''',
    call='Solution().removeSubstring("((()))(()", 2)',
    expect='()(()',
    views=[
        dict(type='string', var='s', label='s（蓝 = 正在处理的括号）', cell=84, h=150,
             dim=lambda S, i, v: _idx(S) > i,
             color=lambda S, i, v: 'blue' if _idx(S) == i else None),
        dict(type='stack', var='st', label='st（[括号, 连续个数]，栈顶在右）', fmt=lambda x: f'{x[0]} × {x[1]}', h=130, font=30),
        dict(type='text', fn=_top, size=28, h=70),
    ],
    watch=[('k', 'k', 'yellow'), ('b', 'b', 'blue'), ('st', 'st', 'green')],
    captions={
        'st = []': '栈里不存单个括号，而是存 `[括号, 连续个数]`：把连续相同的括号==压缩==',
        'if st and st[-1][0] == b': lambda S, B, r: (
            f'栈顶括号 `{S.st[-1][0]}` 与 `{S.b}` 相同 → 接在后面' if len(S.st) and S.st[-1][0] == S.b else '栈空或栈顶括号不同 → 开新的一段'),
        'st[-1][1] += 1': '连续个数 +1：栈顶变成 `{st[-1][0]} × {st[-1][1]}`',
        'st.append([b, 1])': '新的一段入栈：`{b} × 1`',
        "if b == ')' and": lambda S, B, r: (
            f"栈顶 `) × {S.st[-1][1]}`，个数 == k = `{S.k}`；下面 `( × {S.st[-2][1]}` ≥ k → ==凑出一个 k-平衡子串，消除=="
            if S.b == ')' and len(S.st) > 1 and S.st[-1][1] == S.k and S.st[-2][1] >= S.k
            else ('是左括号，不会产生新的消除' if S.b != ')' else
                  (f"栈顶 `) × {S.st[-1][1]}`，个数还不到 k = `{S.k}`，继续等" if len(S.st) > 1 and S.st[-1][1] < S.k else
                   '栈顶右括号凑不齐 k 个，或下面的左括号不够 k 个，不能消除'))),
        'st.pop()': '弹出栈顶的 k 个右括号',
        'st[-1][1] -= k': '新栈顶的左括号个数减 k：`{st[-1][0]} × {st[-1][1]}`',
        'if st[-1][1] == 0': lambda S, B, r: ('左括号被用光了 → 这一段也弹出' if S.st[-1][1] == 0 else '左括号还有剩余 → 保留'),
        "return ''.join": '栈里剩下的各段拼回字符串：`{ret}`',
    },
    cards=dict(
        one_liner='栈里存「括号 + 连续个数」，凑齐 k 对就整段抵消',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s` 只含 `(` 和 `)`；`k` 个 `(` 后跟 `k` 个 `)` 叫 k-平衡',
                 '重复删除所有 k-平衡子串，返回最终字符串',
                 '示例：`"((()))()()()"`，`k = 3` → `"()()()"`；本视频：`"((()))(()"`，`k = 2` → `"()(()"`'],
        quote='栈中不能只存字符，而是存字符连续出现的次数（相当于压缩了连续出现的字符）。……栈中保存二元组 (b, cnt)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['这是邻项消除：一边遍历一边入栈，能消就消',
              '栈顶是 `) × k`，且下面的 `(` 至少 `k` 个 → 抵消 `k` 对',
              '下面的 `(` 减去 `k`，减到 0 就整段弹出'],
        summary=['时间 `O(n)`，空间 `O(n)`：每个字符最多入栈、出栈一次',
                 '易错：只在 `b == ")"` 且栈顶个数 `== k` 时检查，不是 `>= k`',
                 '易错：下面左括号个数 `>= k` 即可，不必恰好等于 `k`；剩下的左括号继续留在栈里',
                 '一般性：先做 3561、1209，再来本题'],
    ),
)
