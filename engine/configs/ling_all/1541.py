S0 = '))())('


def _info(S):
    if 'i' not in S:
        return '一个 `(` 必须配两个连续的 `))`'
    i, n = S['i'], len(S['s'])
    if i >= n:
        return f'遍历结束：未配对左括号 `left = {S["left"]}`，还要补 `{S["left"] * 2}` 个 `)`'
    return f'未配对左括号 `left = {S["left"]}`，已插入 `ans = {S["ans"]}`，正在看 `s[{i}] = {S["s"][i]}`'


def _win(S, i, v):
    if 'i' not in S:
        return None
    k = S['i']
    if i == k:
        return 'blue'
    return None


CONFIG = dict(
    num=1541, title='平衡括号字符串的最少插入次数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='未配对左括号计数 · 一次吃两个右括号',
    tags=['栈', '合法括号字符串', '难度分 1759'],
    code='''
class Solution:
    def minInsertions(self, s: str) -> int:
        n = len(s)
        left = 0  # 未配对的左括号个数
        ans = i = 0

        while i < n:
            if s[i] == '(':
                left += 1  # 未配对的左括号
                i += 1
                continue

            if left > 0:
                left -= 1  # 左右括号配对
            else:
                ans += 1  # 右括号太多了，补一个左括号

            # 必须有两个连续的右括号，也就是 s[i+1] 必须也是右括号
            if i < n - 1 and s[i + 1] == ')':
                i += 2
            else:
                ans += 1  # 补一个右括号
                i += 1

        # 左括号太多了，补上缺失的右括号
        return ans + left * 2
''',
    call=f'Solution().minInsertions({S0!r})',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=90),
        dict(type='string', var='s', label='s（蓝 = 当前位置 i）', pointers={'i': 'blue'}, cell=90, h=240,
             color=_win, dim=lambda S, k, v: 'i' in S and k < S['i']),
        dict(type='text', fn=lambda S: ('补上的括号数 `ans` 是 =={}=='.format(S['ans']) if 'ans' in S else ''), size=26, h=80),
    ],
    skip=['continue'],
    watch=[('i', 'i', 'blue'), ('left', 'left', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'left = 0': '`left`：目前==还没配对==的左括号个数',
        'ans = i = 0': '`ans` 记录插入次数，`i` 是当前位置',
        'while i < n': lambda S, B, ret: (f'`i = {S.i} < {S.n}`，继续' if S.i < S.n else f'`i = {S.i} ≥ {S.n}`：字符串走完'),
        "if s[i] == '('": lambda S, B, ret: (f"`s[{S.i}] = '('` 是左括号 → 先记下来，等后面两个 `)`" if S.s[S.i] == '(' else f"`s[{S.i}] = ')'` 是右括号 → 要找一个左括号来配"),
        'left += 1': '未配对左括号 +1，`left = {left}`',
        'if left > 0': lambda S, B, ret: (f'`left = {S.left} > 0` → 有左括号可配' if S.left > 0 else '`left = 0` → 没有左括号可配，只能==补一个 `(`=='),
        'left -= 1': '左右括号配对：`left` → {left}',
        'ans += 1  # 右括号太多': '右括号太多了：开头补一个 `(`，`ans = {ans}`',
        'if i < n - 1 and s[i + 1]': lambda S, B, ret: (f"`s[{S.i + 1}] = ')'` → 两个右括号连续，一起吃掉" if S.i < S.n - 1 and S.s[S.i + 1] == ')' else '后面不是 `)`（或已到末尾）→ 只有一个 `)`，要==补一个 `)`=='),
        'i += 2': '连续两个 `)` 都用掉了：`i` 跳 2 → {i}',
        'ans += 1  # 补一个右括号': '补一个 `)`：`ans = {ans}`',
        'return ans': lambda S, B, ret: f'走完后还有 `{S.left}` 个未配对左括号，每个补 2 个 `)` → `{S.ans} + {S.left} × 2` = =={ret}==',
    },
    cards=dict(
        one_liner='维护未配对左括号个数，右括号一次吃两个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一个 `(` 必须对应两个连续的 `))`，可在任意位置插入括号',
                 '求让 `s` 平衡的最少插入次数',
                 '示例：`"))())("` → `3`（补 `(`、再补 `))`）'],
        quote='用一个变量 left 维护当前尚未配对的左括号的个数。……如果 s[i+1] 是右括号，那么跳过 s[i+1]；如果不是，必须补一个右括号。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左括号：`left += 1`，等待配对',
              '右括号：有 `left` 就配对；没有就补一个 `(`',
              '再看下一个字符：是 `)` 就一次吃两个，否则补一个 `)`；结尾剩下的 `left` 每个补 `))`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：右括号必须==连续==两个，所以要检查 `s[i+1]`，别越界（`i < n - 1`）',
                 '易错：补的 `(` 可插在开头，补的 `)` 插在中间或末尾，互不影响',
                 '模板：合法括号字符串都用「未配对左括号计数」'],
    ),
)
