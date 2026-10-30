CONFIG = dict(
    num=656, title='金币路径', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='反向 DP · 单调双端队列', tags=[],
    code='''
class Solution(object):
    def cheapestJump(self, coins, maxJump):

        if coins[-1] == -1:
            return []

        n = len(coins)
        f = [0]
        next = [-1]

        q = deque()
        q.append([0, n - 1])

        for index in range(n - 2, -1, -1):
            if not q:
                return []
            
            if coins[index] != -1:
                f.append(q[0][0] + coins[index])
                next.append(q[0][1])
                while q and q[-1][0] >= f[-1]:
                    q.pop()
                q.append([f[-1], index])
            else:
                f.append(-1)
                next.append(-1)
            
            while q and q[0][1] >= index + maxJump:
                q.popleft()
        
        next.reverse()
        res = [1]
        now = 0
        while now != n - 1:
            now = next[now]
            res.append(now + 1)

        return res
''',
    call='Solution().cheapestJump([1,2,4,-1,2], 2)',
    expect=[1, 3, 5],
    views=[
        dict(type='array', var='coins', pointers={'index': 'blue'}, h=230, label='coins（-1 = 不能落脚）',
             color=lambda S, i, v: 'red' if v == -1 else None),
        dict(type='array', var=lambda S: ['·'] * (len(S['coins']) - len(S['f'])) + S['f'][::-1] if 'f' in S else [], h=150, label='f：到终点的最小代价（· 未算）',
             color=lambda S, i, v: 'red' if v == -1 else None if v == '·' else 'green'),
        dict(type='queue', var='q', h=170, fmt=lambda x: f'代价{x[0]}@下标{x[1]}', label='单调双端队列 q（队头最优）'),
    ],
    watch=[('index', 'index', 'blue'), ('f', 'f'), ('q', 'q', 'cyan')],
    captions={
        'if coins[-1] == -1': '终点 `coins[-1] = {coins[-1]}`，不是 -1，可以落脚；若是 -1 则直接返回 `[]`',
        'f = [0]': '反向 DP：`f` 依次存 终点、倒数第 2、…… 位置到终点的最小代价，终点是 0',
        'next = [-1]': '`next` 记录每个位置的最优下一落脚点（用来还原路径）',
        'q.append([0': '队列放入 `[代价, 下标]`，先放终点 `[0, {n-1}]`',
        'for index in range': '从后往前算每个位置：`index = {index}`',
        'if not q': '队列里还有可用落脚点吗：{"没有，到不了终点，返回 []" if not q else "有，继续算"}',
        'if coins[index] != -1': '`coins[{index}] = {coins[index]}` → {"可落脚，用队头最优去算" if coins[index] != -1 else "是 -1，不能落脚"}',
        'f.append(q[0][0]': '队头代价 `{q[0][0]}` 就是 `index+1..index+maxJump` 里最便宜的 → `f` = 队头 + `coins[{index}]` = =={f[-1]}==，下一跳 `{q[0][1]}`',
        'while q and q[-1][0]': lambda S, B, r: (f'队尾代价 `{S.q[-1][0]}` >= 新代价 `{S.f[-1]}`：它更远又更贵，永远用不上 → 弹出' if S.q and S.q[-1][0] >= S.f[-1] else '队尾比新位置便宜，或队列已空 → 停止弹出，队列代价保持严格递增'),
        'q.append([f[-1]': '把新位置 `[{f[-1]}, {index}]` 入队（它更靠前，字典序更小）',
        'f.append(-1)': '不能落脚，`f = -1`、`next = -1`',
        'while q and q[0][1]': lambda S, B, r: (f'队头下标 `{S.q[0][1]} >= {S.index} + {S.maxJump}`：下一个位置跳不到它 → 弹出队头' if S.q and S.q[0][1] >= S.index + S.maxJump else '队头仍在 `maxJump` 范围内（或队列空）→ 保留'),
        'next.reverse()': '`next` 反转成按下标顺序，再沿着它走',
        'res = [1]': '路径从第 1 号位置出发（下标 + 1）',
        'while now != n - 1': '`now = {now}`，没到终点 `{n-1}` → 继续跳',
        'now = next[now]': '跳到最优下一落脚点 `{now}`',
        'res.append': '路径加入 `{now + 1}`：`res` = {res}',
        'return res': '最便宜且字典序最小的路径：`{res}`',
    },
    cards=dict(
        one_liner='倒着做 DP，单调队列取窗口内最便宜的落脚点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从位置 1 出发，每次最多跳 `maxJump` 格，`-1` 的格子不能落脚，经过格子要付金币',
                 '求到达位置 n 的最小花费路径，花费相同取字典序最小；到不了返回 `[]`',
                 '示例：`coins=[1,2,4,-1,2]`，`maxJump=2` → `[1,3,5]`'],
        quote='通过反向动态规划来规避掉字典序的影响……在 i + 1 到 i + maxJump 这些位置中挑选下一个落脚点时，会优先选择靠前的位置，从而使得字典序最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` = 从 `i` 出发到终点的最小代价 = 窗口内最小 `f[j]` + `coins[i]`',
              '窗口最小值用单调双端队列：新位置入队时弹出不比它好的队尾',
              '队头超出 `maxJump` 就弹出；同代价时靠前位置后入队，保证字典序最小'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '队列空了说明无路可走，要返回 `[]`；终点是 -1 同理',
                 '用队尾 `>=` 弹出：代价相同留下更靠前的，字典序才最小',
                 '输出的是 1 起始的位置，所以 `res` 里存 `now + 1`',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
