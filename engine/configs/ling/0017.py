MAPPING = "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"


def _keys(S):
    i = S['i']
    if i < S['n']:
        d = S['digits'][i]
        return f"按键 `{d}` → `MAPPING[{d}] = '{MAPPING[int(d)]}'`" + (f"，当前 `c = '{S['c']}'`" if 'c' in S else '')
    return '`i == n`：每一位都填好了，拼成答案'


def _for(S, B, ret):
    d = S.digits[S.i]
    letters = MAPPING[int(d)]
    if 'c' in S and S.c != B.get('c'):
        return f"第 `{S.i}` 位是按键 `{d}`，在 `'{letters}'` 里枚举：这次选 `'{S.c}'`"
    return f"按键 `{d}` 的 `'{letters}'` 都试完了 → `dfs({S.i})` 结束，返回上一层"


CONFIG = dict(
    num=17, title='电话号码的字母组合', difficulty='Medium', category='回溯',
    author='灵茶山艾府', technique='回溯三问 · path 定长直接覆盖',
    code='''
MAPPING = "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        n = len(digits)
        if n == 0:
            return []

        ans = []
        path = [''] * n  # 注意 path 长度一开始就是 n，不是空列表

        def dfs(i: int) -> None:
            if i == n:
                ans.append(''.join(path))
                return
            for c in MAPPING[int(digits[i])]:
                path[i] = c  # 直接覆盖
                dfs(i + 1)

        dfs(0)
        return ans
''',
    call="Solution().letterCombinations('23')",
    expect=['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf'],
    views=[
        dict(type='string', var='digits', label='digits（蓝 = 第 i 位）', cell=64, h=130,
             color=lambda S, i, v: 'blue' if i == S['i'] else None),
        dict(type='text', fn=lambda S: _keys(S) if 'i' in S else '', h=50, size=26),
        dict(type='array', var='path', label='path（暗 = 旧值，等着被覆盖）', cell=64, h=150, pointers={'i': 'blue'},
             dim=lambda S, i, v: i > S['i'] or (i == S['i'] and S['path'][i] != S.get('c'))),
        dict(type='calls', h=180),
        dict(type='stack', var='ans', label='ans', h=100),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'pink'), 'path'],
    skip=['                return'],
    captions={
        'n = len(digits)': '`n = len(digits) = {n}`：答案里每个字符串都恰好 `{n}` 个字母',
        'if n == 0': '`n == 0` 时没有组合，直接返回 `[]`；这里 `n = {n}`，继续',
        'if i == n': lambda S, B, ret: (
            f'`i == n`（{S.i} == {S.n}）→ path 的每一位都填好了'
            if S.i == S.n else
            f'`i = {S.i} < n`：给 `path[{S.i}]` 选一个字母，后面的交给 `dfs({S.i + 1})`'),
        "ans.append(''.join(path))": "把 path 拼成字符串 `'{ans[-1]}'` 加入答案，然后回到上一层",
        'for c in MAPPING': _for,
        'path[i] = c': lambda S, B, ret: (
            f"直接覆盖：`path[{S.i}] = '{S.c}'`" + ('，所以==不需要恢复现场==' if len(S.ans) < 2 else '')),
        "path = [''] * n": "注意 path 长度一开始就是 n，不是空列表：`path = {path}`",
        'dfs(i + 1)': '递归 `dfs({i})`：处理下标 `≥ {i}` 的剩余部分',
        'dfs(0)': '`dfs(0)`：枚举下标 `≥ 0` 的所有字母组合',
        'return ans': '全部组合生成完毕，共 `{len(ret)}` 个',
    },
    max_steps=60,
    cards=dict(
        one_liner='每一位枚举一个字母，剩下的交给 dfs(i + 1)',
        complexity='时间 `O(n·4^n)`，空间 `O(n)`（不计返回值）',
        problem=['给一个只含数字 `2-9` 的字符串，返回它在电话按键上能表示的所有字母组合',
                 '`2→abc  3→def  4→ghi  5→jkl  6→mno  7→pqrs  8→tuv  9→wxyz`',
                 "示例：`\"23\"` → `[\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]`"],
        quote='`dfs(i)` 处理的是==从下标 i 到末尾的所有字母组合==。它不仅仅在枚举 `i`，还包含了 `dfs(i+1), dfs(i+2), …, dfs(n)` 这之后的所有递归调用。',
        quote_src='—— 灵茶山艾府题解「答疑」',
        idea=['当前操作：枚举 `path[i]` 填哪个字母',
              '子问题：构造下标 `≥ i` 的部分；下一个子问题：`dfs(i + 1)`',
              '`path` 长度固定为 `n`，==直接覆盖==，无需恢复现场'],
        result='9 个组合全部生成 ✓（中间分支已快进）',
        summary=['满四叉树最多 `O(4^n)` 个节点，每个答案拼接 `O(n)` → `O(n·4^n)`',
                 '易错：`path` 一开始就要是长度 `n`，不是空列表',
                 '易错：`digits` 为空要返回 `[]`，不是 `[""]`',
                 '同样的「回溯三问」可以直接套到子集、全排列'],
    ),
)
