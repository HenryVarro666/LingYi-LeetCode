CONFIG = dict(
    num=1298, title='你能从盒子里获得的最大糖果数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='BFS · 哈希表暂存打不开的盒子',
    tags=['灵神题单·图论算法', '难度分 1825'],
    code='''
class Solution(object):
    def maxCandies(self, status, candies, keys, containedBoxes, initialBoxes):

        n = len(status)
        q = []
        box_set = set()
        for box in initialBoxes:
            if status[box]:
                q.append(box)
            else:
                box_set.add(box)
        
        l = 0
        r = len(q)
        res = 0
        while l < r:
            now = q[l]
            res += candies[now]
            l += 1
            for key in keys[now]:
                if key in box_set:
                    q.append(key)
                    box_set.remove(key)
                    r += 1
                else:
                    status[key] = 1
            for box in containedBoxes[now]:
                if status[box]:
                    q.append(box)
                    r += 1
                else:
                    box_set.add(box)

        return res
''',
    call='Solution().maxCandies([1,0,1,0], [7,5,4,100], [[],[],[1],[]], [[1,2],[3],[],[]], [0])',
    expect=16,
    views=[
        dict(type='array', var='status', label='status（1=能打开，拿到钥匙会被改成 1）', cell=100, h=170,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var='q', label='q（BFS 队列；蓝=正在处理，其后=待处理）', cell=100, h=170,
             pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='set', var='box_set', label='box_set（拿到了但暂时打不开的盒子）', fmt=lambda x: str(x), h=130),
        dict(type='text', fn=lambda S: f"已拿糖果 res = ==​{S.get('res', 0)}==", size=28, h=70),
    ],
    watch=[('now', 'now', 'blue'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        'n = len(status)': '`status[i]` 为 1 表示盒子 `i` 能打开',
        'q = []': 'BFS 队列 `q`：放「现在就能打开」的盒子',
        'box_set = set()': '哈希表 `box_set`：放「拿到了但还打不开」的盒子',
        'for box in initialBoxes': '看初始盒子 `{box}`',
        'res = 0': '`res` 累计糖果数',
        'q.append(box)': '盒子 `{box}` 入队：`q = {q}`',
        'box_set.add(box)': '`box_set` 加入 `{box}`：{box_set}',
        'l = 0': '队头 `l = 0`',
        'r = len(q)': '队尾 `r = {r}`：`q[l:r]` 就是待处理的盒子',
        'while l < r': lambda S, B, r: ('队列不空，取下一个盒子' if S.l < S.r else '队列空了，没有能再打开的盒子 → 结束'),
        'now = q[l]': '取出队头盒子 `{now}`',
        'res += candies[now]': '1、收集糖果：`res += {candies[now]}` → =={res}==',
        'l += 1': '队头后移：`l` → {l}',
        'for key in keys[now]': '2、看盒子 `{now}` 里的钥匙：`{keys[now]}`',
        'if key in box_set': lambda S, B, r: (f'钥匙 `{S.key}` 对应的盒子已经在哈希表里 → ==现在能开了==' if S.key in S.box_set
                                              else f'盒子 `{S.key}` 还没拿到 → 只能先记下：把 `status[{S.key}]` 设成 1'),
        'q.append(key)': '盒子 `{key}` 入队：`q = {q}`',
        'box_set.remove(key)': '从哈希表移除 `{key}`',
        'r += 1': '队尾后移：`r` → {r}',
        'status[key] = 1': '`status[{key}] = 1`：有钥匙了，盒子一出现就能开',
        'for box in containedBoxes[now]': '3、看盒子 `{now}` 里的子盒子：`{containedBoxes[now]}`',
        'if status[box]': lambda S, B, r: ((f'初始盒子 `{S.box}` 是开着的 → 直接入队' if S.status[S.box] else f'初始盒子 `{S.box}` 关着 → 先放进哈希表，等钥匙')
                                           if S._line == 8 else
                                           (f'子盒子 `{S.box}` 的 `status` 为 1 → 之前就有钥匙，==能开==' if S.status[S.box]
                                            else f'子盒子 `{S.box}` 的 `status` 为 0 → 暂时打不开，放进哈希表')),
        'return res': '最多拿到 `{res}` 颗糖',
    },
    cards=dict(
        one_liner='能打开的进队列，打不开的先放哈希表，等钥匙来',
        complexity='时间 `O(n+L)`，空间 `O(n)`',
        problem=['盒子里有糖果、钥匙、小盒子；盒子要开着或有钥匙才能打开',
                 '给出初始拥有的盒子，求最多能拿到多少糖果',
                 '示例：初始盒子 `[0]` → `7 + 4 + 5 = 16`'],
        quote='对于初始拥有的盒子，我们将可以打开的盒子加入到bfs的队列中，并使用哈希表保存剩下暂时无法打开的盒子。',
        quote_src='—— yiduobo 题解原文',
        idea=['每处理一个盒子分三步：收糖果 → 看钥匙 → 看子盒子',
              '钥匙对应的盒子在哈希表里：现在能开了，入队并从表里删掉',
              '钥匙对应的盒子不在表里：改 `status` 为 1，盒子之后出现就能直接开',
              '子盒子 `status` 为 1 就入队，否则放进哈希表'],
        summary=['时间 `O(n+L)`，空间 `O(n)`',
                 '队列用「列表 + l/r 下标」实现，不用 `pop(0)`',
                 '易错：钥匙和盒子谁先到都要处理，所以才要「哈希表 + 改 status」两头配合',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神用 DFS + `has_key/has_box`；yiduobo 用 BFS + 哈希表'],
    ),
)
