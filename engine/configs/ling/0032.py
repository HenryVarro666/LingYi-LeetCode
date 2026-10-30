def _match(s, i):
    """index of the '(' matched with the ')' at i (nearest unmatched '(' on the left), or None"""
    depth = 0
    for j in range(i - 1, -1, -1):
        if s[j] == ')':
            depth += 1
        elif depth == 0:
            return j
        else:
            depth -= 1
    return None


def _on(S):
    """just popped the partner of s[i] -> segment st[-1]+1 .. i is fully matched"""
    if 'i' not in S or S['s'][S['i']] != ')':
        return False
    m = _match(S['s'], S['i'])
    return m is not None and m not in S['st']


def _text(S):
    if _on(S):
        i, top = S['i'], S['st'][-1]
        return f"已配对区间 `[{top + 1}, {i}]`：长度 = `i − 栈顶` = {i} − ({top}) = =={i - top}=="
    return '栈里存==未配对==括号的下标；栈底 = 最近一个「无法配对」的位置'


CONFIG = dict(
    num=32, title='最长有效括号', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='栈（存未配对下标，一次遍历）',
    code='''
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        st = [-1]  # 未配对括号的下标，其中栈底元素表示永远无法配对的括号下标
        ans = 0

        for i, ch in enumerate(s):
            if ch == '(':
                st.append(i)  # 保存左括号的下标
            elif len(st) > 1:
                st.pop()  # 右括号与栈顶的左括号配对
                ans = max(ans, i - st[-1])  # 从 st[-1]+1 到 i 都已配对，长为 i - st[-1]
            else:  # s[i] 是永远无法配对的右括号
                st[0] = i  # 替换栈底

        return ans
''',
    call='Solution().longestValidParentheses(")()(())")',
    expect=6,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='string', var='s', label='s', cell=100, h=230,
             pointers={'i': 'yellow', 'st[-1]': 'blue'}, pointer_labels={'st[-1]': '栈顶'},
             window=(lambda S: S['st'][-1] + 1 if _on(S) else None, lambda S: S['i'] if _on(S) else None),
             window_color='green',
             color=lambda S, k, v: 'yellow' if k == S.get('i') else None),
        dict(type='stack', var='st', label='st（存下标）', h=130),
    ],
    watch=[('i', 'i', 'yellow'), ('ch', 'ch', 'yellow'), ('栈顶', 'st[-1]', 'blue'), ('ans', 'ans', 'green')],
    skip=['for i, ch in enumerate'],
    captions={
        'st = [-1]': '栈里存==未配对==括号的下标；先放 `-1` 当栈底，充当「左边界」',
        'ans = 0': '`ans = 0`：目前最长有效长度',
        "if ch == '('": lambda S, B, ret: (f'`s[{S.i}] = "("`：左括号，下标入栈，等右括号来配对' if S.ch == '('
                                           else f'`s[{S.i}] = ")"`：右括号，看看有没有左括号能和它配对'),
        'st.append(i)': '保存左括号的下标：`st = {st}`',
        'elif len(st) > 1': lambda S, B, ret: (f'栈里除了栈底还有左括号 `{S.st[-1]}` → ==能配对==' if len(S.st) > 1
                                               else '栈里只剩栈底 → ==没有左括号可以配对=='),
        'st.pop()': '`s[{i}]` 与左括号 `{B.st[-1]}` 配对，弹出；新栈顶 `{st[-1]}` 是左边最近的未配对位置',
        'ans = max': lambda S, B, ret: (f'从 `{S.st[-1] + 1}` 到 `{S.i}` 都已配对，长 `{S.i} - ({S.st[-1]})` = {S.i - S.st[-1]}，`ans` = =={S.ans}=='
                                        + ('；==左边相邻的有效段自动连上了==' if S.st[-1] + 1 < _match(S.s, S.i) else '')),
        'st[0] = i': '`s[{i}]` 是永远无法配对的右括号 → ==替换栈底== `st[0] = {i}`，它成为新的左边界',
        'return ans': '遍历结束，返回 =={ret}==',
    },
    cards=dict(
        one_liner='栈里存未配对的下标，i − 栈顶 就是以 i 结尾的有效长度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['只含 `(` 和 `)` 的字符串，求==最长有效（格式正确且连续）括号子串==的长度',
                 '示例：`")()())"` → `4`（`"()()"`）',
                 '演示：`")()(())"` → `6`（`"()(())"`）'],
        before=[dict(heading='什么是有效括号？', lines=[
            '==消消乐==：不断消除相邻的 `()`，最后变成空串，就是有效括号',
            '无效：左括号缺右括号（`(()`），或右括号缺左括号（`())`）',
            '配对标记：`)` 找左侧最近的未配对 `(`，标记这对，答案 = ==最长连续标记==',
        ])],
        quote='既然栈中保存的是未配对的下标，那么==从栈顶加一的位置到 i，就是已配对的连续括号==，长度为 i 减去栈顶，更新答案的最大值。',
        quote_src='—— 灵茶山艾府题解（优化：一次遍历）',
        idea=['永远无法配对的 `)` 也放进栈（替换栈底）→ 保证「栈顶 + 1」是左端点',
              '一开始放 `-1` → 「左端点是 0」的情况也兼容了，不用特判空栈',
              '`len(st) > 1` 才有左括号可配：栈底只当边界，不参与配对'],
        after=[dict(heading='O(1) 空间：只数左右括号', lines=[
            '左右个数相等 → 长度 `right × 2`；右括号太多 → 两个计数器清零',
            '`left > right` 时无法判断：是 `((())` 还是 `()(()`？',
            '把 s ==旋转 180°== 再遍历一遍，多出来的左括号就移到了后面',
        ])],
        summary=['时间 `O(n)`，空间 `O(n)`；计数法可做到 `O(1)`',
                 '易错：栈底先放 `-1`，否则 `"()"` 这种从 0 开始的算不对',
                 '易错：无法配对的 `)` 要==替换栈底==，不是直接忽略',
                 '配对标记写法：标记完求 `is_valid` 中最长连续 True（同 485 题）'],
    ),
)
