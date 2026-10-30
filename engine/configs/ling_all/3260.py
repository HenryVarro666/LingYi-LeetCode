CONFIG = dict(
    num=3260, title='找出最大的 N 位 K 回文数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='记忆化 DFS · 字典序最大路径', tags=['数学算法', '难度分 2370'],
    code='''
class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        pow10 = [1] * n
        for i in range(1, n):
            pow10[i] = pow10[i - 1] * 10 % k

        ans = [''] * n
        m = (n + 1) // 2
        vis = [[False] * k for _ in range(m + 1)]
        def dfs(i: int, j: int) -> bool:
            if i == m:
                return j == 0
            vis[i][j] = True
            for d in range(9, -1, -1):  # 贪心：从大到小枚举
                if n % 2 and i == m - 1:  # 正中间
                    j2 = (j + d * pow10[i]) % k
                else:
                    j2 = (j + d * (pow10[i] + pow10[-1 - i])) % k
                if not vis[i + 1][j2] and dfs(i + 1, j2):
                    ans[i] = ans[-1 - i] = str(d)
                    return True
            return False
        dfs(0, 0)
        return ''.join(ans)
''',
    call='Solution().largestPalindrome(5, 7)',
    expect='99799',
    views=[
        dict(type='array', var='ans', h=170, label='ans（回溯成功时从内到外填入，左右镜像）',
             color=lambda S, i, v: 'green' if v != '' else None),
        dict(type='table', var='vis', h=300, rows=lambda S: [f'i={r}' for r in range(len(S['vis']))], cols=lambda S: [f'j={c}' for c in range(S['k'])],
             color=lambda S, i, j, v: 'orange' if v else None),
        dict(type='calls', h=200),
    ],
    watch=['i', 'j', 'd', 'j2', ('m', 'm', 'cyan')],
    captions={
        'pow10[i] = pow10': '`10^{i} mod {k}` = {pow10[i]}：预处理，中途取模不影响最终余数',
        'ans = [': '`ans` 存 `n={n}` 个数位，左右镜像一起填',
        'm = (n + 1)': '只需决定前 `m = {m}` 位，另一半由镜像得到',
        'vis = [[': '`vis[i][j]`：状态「填到第 i 位、余数为 j」是否已搜过；搜过且失败就不必再搜',
        'if i == m': lambda S, B, r: (f'填完 {S.m} 位：余数 `j = {S.j}` → ' + ('==为 0，整个数能被 k 整除，成功==' if S.j == 0 else '不为 0，失败，回退')) if S.i == S.m else f'`i = {S.i} < m = {S.m}`，还没填完，继续',
        'vis[i][j] = True': '标记状态 `({i}, {j})` 已访问：以后再走到这里，结果一定和这次相同',
        'for d in range': '贪心：从 9 往 0 试，先成功的路径字典序最大。`d` = {d}',
        'if n % 2 and': '`n % 2 = {n % 2}`，`i == m-1`：{"正中间只有一个位置" if n % 2 and i == m - 1 else "不是正中间，左右各填一个 d"}',
        'j2 = (j + d * pow10[i]) % k': '正中间：`j2 = ({j} + {d}×{pow10[i]}) % {k}` = =={j2}==',
        'j2 = (j + d * (pow10': '同时填第 `{i}` 位和第 `{n-1-i}` 位：`j2 = ({j} + {d}×({pow10[i]}+{pow10[-1-i]})) % {k}` = =={j2}==',
        'if not vis[i + 1][j2]': '状态 `({B.i + 1}, {B.j2})`：{"搜过了，必失败 → 跳过，换更小的 d" if B.vis[B.i + 1][B.j2] else "没搜过 → 递归进去试，成功了就保留这个 d"}',
        'ans[i] = ans[-1 - i]': '后面能成功 → 这一位就填 `{d}`，镜像位也填 `{d}`：=={ans}==',
        'return True': '成功，一路返回 True，不再尝试更小的 d',
        'return False': '`d` 全试完都不行 → 返回 False，回溯到上一位换更小的数',
        'dfs(0, 0)': '从 `(0, 0)` 出发（什么都没填，余数 0）找字典序最大路径',
        "return ''.join": '拼成答案 `{"".join(ans)}`',
    },
    cards=dict(
        one_liner='把填数位变成图上的 DFS：状态 (位, 余数)，访问过就不再访问',
        complexity='时间 `O(nkD)`，空间 `O(nk)`，`D = 10`',
        problem=['求最大的 `n` 位回文数，要求能被 `k` 整除（`1 <= k <= 9`，`n` 最大 `10^5`）',
                 '回文数只需决定前一半，另一半镜像',
                 '示例：`n = 5, k = 7` → `"99799"`'],
        quote='无论后面的数字怎么填，这两种情况其实是一样的，因为我们只关心回文数最终模 k 的值是否为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `(i, j)`：填到第 `i` 位，已填部分模 `k` 为 `j`',
              '从 `d = 9` 开始倒着试 → 第一条走通的路径就是字典序最大',
              '一个状态失败过，再来也必失败：`vis` 保证每个状态只搜一次'],
        summary=['时间 `O(nkD)`，空间 `O(nk)`',
                 '奇数长度的正中间只有一个位置：用 `d * pow10[i]`，不能算两遍',
                 '`vis` 在进入状态时就标记；成功路径会立刻返回，所以不会误伤',
                 '预处理 `pow10` 时边乘边取模，避免大整数',
                 '同类：打印方案专题；`n` 很大时 `n` 层递归在 Python 里要注意栈深'],
    ),
)
