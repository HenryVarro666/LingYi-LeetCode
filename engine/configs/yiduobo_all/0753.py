CONFIG = dict(
    num=753, title='破解保险箱', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='De Bruijn 序列 · 欧拉回路',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def crackSafe(self, n, k):

        if n == 1:
            return ''.join([str(x) for x in range(k)])

        G = {}
        if n == 2:
            node_list = range(k)
        elif n == 3:
            node_list = [x * 10 + y for x in range(k) for y in range(k)]
        else:
            node_list = [x * 100 + y * 10 + z for x in range(k) for y in range(k) for z in range(k)]
        
        for now in node_list:
            G[now] = {}
            for edge_num in range(k):
                next = (now * 10 + edge_num) % (10 ** (n - 1))
                G[now][edge_num] = next
        
        res = []
        self.dfs(0, G, k, res)
        return ''.join(str(x) for x in res) + '0' * (n - 2)

    def dfs(self, now, G, k, res):
        for edge_num in range(k):
            if edge_num in G[now]:
                next = G[now][edge_num]
                G[now].pop(edge_num)
                self.dfs(next, G, k, res)

        res.append(now % 10)
''',
    call='Solution().crackSafe(3, 2)',
    expect='0011101000',
    views=[
        dict(type='map', var='G', label='G：点（后缀 n−1 位）→ {输入的数字: 走到的点}，走过的边会被删掉', h=110,
             fmt=lambda k, v: f'{k:02d} → {v}'),
        dict(type='calls', h=300, hide=('G', 'res')),
        dict(type='array', var='res', label='res（回溯时追加每个点的最后一位，是倒序的）', cell=60, h=130),
    ],
    watch=[('now', lambda S: S['_inner'].get('now'), 'blue'), ('edge_num', lambda S: S['_inner'].get('edge_num'), 'pink'),
           ('next', lambda S: S['_inner'].get('next'), 'green')],
    skip=['if n == 1', "return ''.join([str", 'G = {}', 'if n == 2', 'node_list = range', 'elif n == 3', 'else:',
          'node_list = [x * 100', 'G[now] = {}', 'G[now][edge_num] = next', 'for edge_num in range(k):', 'for now in node_list'],
    captions={
        'node_list = [x * 10': '`n = 3`：点是 ==n−1 = 2 位的密码==，一共 `k^(n-1) = {len(node_list)}` 个：`{list(node_list)}`',
        'next = (now * 10': '建边：点 `{now:02d}` 再输入数字 `{edge_num}`，去掉最高位、补上新数字 → 点 `{next:02d}`',
        'res = []': '`res` 用来收集答案',
        'self.dfs(0, G, k, res)': '每个点入度 = 出度 = k，欧拉回路一定存在 → ==从点 0 开始 dfs 即可==',
        'if edge_num in G[now]': lambda S, B, r: (
            f'点 `{S.now:02d}` 的边 `{S.edge_num}` 还没走 → 走它' if S.edge_num in S.G[S.now]
            else f'点 `{S.now:02d}` 的边 `{S.edge_num}` 已经走过了 → 跳过'),
        'next = G[now][edge_num]': '这条边通向点 `{next:02d}`',
        'G[now].pop(edge_num)': '==每条边只能走一次==：删掉 `G[{now}][{edge_num}]`',
        'self.dfs(next': '递归：站到点 `{next:02d}` 继续走',
        'res.append(now % 10)': '`{now:02d}` 的边都走完了 → ==回溯时==把它的最后一位 `{now % 10}` 加入 `res` → `{res}`',
        "return ''.join(str(x)": lambda S, B, r: f'`res` 拼起来 `{"".join(map(str, S.res))}`，再补 `n−2 = {S.n - 2}` 个 0（起点的前缀）→ ==`{r}`==',
    },
    max_steps=90,
    cards=dict(
        one_liner='把密码当点、输入的一位当边，一笔画走遍所有边',
        complexity='时间 `O(n·k^n)`，空间 `O(k^(n-1))`',
        problem=['保险箱密码是 `n` 位、每位 `0..k-1`，输入时只看最近 `n` 位',
                 '求一个最短的字符串，使所有 `k^n` 种密码都作为子串出现',
                 '本视频：`n = 3, k = 2` → `0011101000`（长度 10）'],
        quote='我们不再将每个状态单独列为节点，而是根据其除去首位的后缀来构图。……原图中的汉密尔顿路径问题，就转化为了新图中的欧拉路径问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['直接把 `n` 位密码当点是汉密尔顿路径，NP 难',
              '改成「点 = 后 n−1 位，边 = 新输入的一位」：每条边恰好对应一个 n 位密码',
              '每个点入度 = 出度 = k → 有欧拉回路，dfs 回溯时记录每个点的末位'],
        summary=['时间 `O(n·k^n)`，空间 `O(k^(n-1))`；答案长度 `k^n + n - 1`',
                 '最后补 `n−2` 个 0：`res` 已经含起点 0 的末位，还差起点前缀的其余部分',
                 '原文只写了 `n ≤ 4` 的点集，更大的 `n` 要自己扩展 `node_list`',
                 '原文是 Python 2 风格，代码无需修改，直接运行',
                 '同类题：2097 合法重新排列数对（欧拉路径）'],
    ),
)
