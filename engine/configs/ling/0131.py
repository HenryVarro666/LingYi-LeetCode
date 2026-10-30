def _seg(S):
    if 'i' not in S:
        return ''
    st, i, s = S['start'], S['i'], S['s']
    if i >= len(s):
        return '`i == n`：整个 s 都切完了'
    t = s[st:i + 1]
    return f"当前段 `s[{st}..{i}] = '{t}'`，" + ('==是回文==' if t == t[::-1] else '不是回文') + f"；下一刀可以切在 `s[{i}]` 和 `s[{i + 1}]` 之间"


CONFIG = dict(
    num=131, title='分割回文串', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='划分型回溯 · 逗号选或不选（输入的视角）',
    code='''
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        ans = []
        path = []

        # 现在 s 未被分割的部分为 [start, n-1]
        # 当前位于下标 i，讨论是否在 i 和 i+1 之间切一刀
        def dfs(i: int, start: int) -> None:
            if i == n:  # s 分割完毕
                ans.append(path.copy())  # 复制 path
                return

            # 不分割
            if i < n - 1:  # i=n-1 时必须分割（这是最后一段），i<n-1 时才可以不分割
                dfs(i + 1, start)

            # 分割，那么得到子串 [start, i]
            t = s[start: i + 1]
            if t == t[::-1]:  # 判断 t 是不是回文串
                path.append(t)
                # 现在 s 未被分割的部分为 [i+1, n-1]
                dfs(i + 1, i + 1)
                path.pop()  # 恢复现场

        dfs(0, 0)
        return ans
''',
    call="Solution().partition('aab')",
    expect=[['aa', 'b'], ['a', 'a', 'b']],
    views=[
        dict(type='string', var='s', label='s（绿 = 已切好，框 = 当前段）', cell=76, h=140,
             window=('start', 'i'), color=lambda S, i, v: 'green' if i < S['start'] else None),
        dict(type='text', fn=_seg, h=50, size=24),
        dict(type='stack', var='path', label='path', h=100),
        dict(type='calls', h=216),
        dict(type='stack', var='ans', label='ans', h=100),
    ],
    watch=[('start', 'start', 'green'), ('i', 'i', 'blue'), ('t', 't', 'yellow')],
    captions={
        'dfs(0, 0)': '`dfs(0, 0)`：未分割的部分是整个 `s`，从下标 `0` 开始讨论',
        'if i == n': lambda S, B, ret: (
            f'`i == n`：==s 分割完毕==，path 里每段都是回文' if S.i == S.n else
            f"`i = {S.i}`：讨论是否在 `s[{S.i}]` 和 `s[{S.i + 1}]` 之间切一刀" if S.i < S.n - 1 else
            f'`i = {S.i} = n-1`：走到最后一个字符'),
        'ans.append': '复制 path 加入答案：`{ans[-1]}`',
        '                return': '返回上一层',
        'if i < n - 1': lambda S, B, ret: (
            f'`i < n-1` → 可以==不分割==（这个逗号不选）' if S.i < S.n - 1 else
            f'`i = n-1`：这是最后一段，==必须分割=='),
        'dfs(i + 1, start)': '==不分割==：`dfs({i}, {start})`，当前段继续往右延伸',
        't = s[start: i + 1]': "（`dfs({i}, {start})` 中）==分割==：得到子串 `t = s[{start}: {i + 1}] = '{t}'`",
        'if t == t[::-1]': lambda S, B, ret: (
            f"`'{S.t}'` 是回文串 → 可以在这里切一刀" if S.t == S.t[::-1] else
            f"`'{S.t}'` ==不是回文串== → 不能在这里切"),
        'path.append(t)': "`'{t}'` 加入 path → `{path}`",
        'dfs(i + 1, i + 1)': '现在未分割的部分为 `[{start}, n-1]`：`dfs({i}, {start})`',
        'path.pop()': "恢复现场：弹出 `'{B.path[-1]}'`，path 回到 `{path}`",
        'return ans': '所有分割方案找完，共 `{len(ret)}` 种',
    },
    max_steps=60,
    cards=dict(
        one_liner='相邻字符之间有个逗号：每个逗号选或不选',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['把字符串 `s` 分割成若干子串，使==每个子串都是回文串==，返回所有分割方案',
                 "示例：`\"aab\"` → `[[\"a\",\"a\",\"b\"],[\"aa\",\"b\"]]`"],
        quote='假设每对相邻字符之间有个逗号，那么就看==每个逗号是选还是不选==。……注意 `s[n-1]` 一定是最后一个字符，所以在 `i=n-1` 的时候一定要分割。',
        quote_src='—— 灵茶山艾府题解「方法一：输入的视角」',
        idea=['`dfs(i, start)`：未分割的部分从 `start` 开始，现在讨论 `i` 后面切不切',
              '不切：`dfs(i + 1, start)`；切：`t = s[start..i]` 是回文才加入 path',
              '最后一段不是回文就到不了 `i == n`，所以加入答案的一定合法'],
        result='找到 `[aa, b]` 和 `[a, a, b]` 两种方案 ✓',
        summary=['递归次数是满二叉树 `O(2^n)`，每次判回文 `O(n)` → `O(n·2^n)`',
                 '`i = n-1` 必须分割，否则最后一段没人处理',
                 '方法二「答案的视角」：`for j in range(i, n)` 枚举子串结束位置'],
    ),
)
