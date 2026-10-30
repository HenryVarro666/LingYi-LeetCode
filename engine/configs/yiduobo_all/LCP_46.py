CONFIG = dict(
    num='LCP 46', title='志愿者调配', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='倒推线性表达式 · 设未知数 v',
    tags=[],
    code='''
class Solution(object):
    def volunteerDeployment(self, finalCnt, totalNum, edges, plans):

        num_list = [[1, 0]]
        for num in finalCnt:
            num_list.append([0, num])
        
        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        for op, x in plans[::-1]:
            if op == 1:
                num_list[x][0] *= 2
                num_list[x][1] *= 2
            elif op == 2:
                for y in g.get(x, set()):
                    num_list[y][0] -= num_list[x][0]
                    num_list[y][1] -= num_list[x][1]
            else:
                for y in g.get(x, set()):
                    num_list[y][0] += num_list[x][0]
                    num_list[y][1] += num_list[x][1]

        tot_a = tot_b = 0
        for index in range(len(num_list)):
            tot_a += num_list[index][0]
            tot_b += num_list[index][1]
        
        v = (totalNum - tot_b) // tot_a
        res = [num_list[index][0] * v + num_list[index][1] for index in range(len(num_list))]
        return res
''',
    call='Solution().volunteerDeployment([1, 16], 21, [[0, 1], [1, 2]], [[2, 1], [1, 0], [3, 0]])',
    expect=[5, 7, 9],
    views=[
        dict(type='table', var='num_list', h=230, cell=64, label='num_list[i] = [a, b]：该馆当前人数 = a·v + b',
             rows=lambda S: [f'馆{i}' for i in range(len(S['num_list']))], cols=['a', 'b'],
             color=lambda S, i, j, v: ('pink' if i == S['x'] else 'cyan' if i == S.get('y') else None) if 'op' in S else None),
        dict(type='map', var='g', h=170, fmt=lambda k, v: f'{k}: {sorted(v)}', label='g：相邻馆（无向边）'),
        dict(type='text', size=30, fn=lambda S: (
            f"人数总和：`{S['tot_a']}·v + {S['tot_b']}` = `{S['totalNum']}`" if 'tot_a' in S and 'v' not in S else
            (f"`v` = ==`{S['v']}`==，每个馆人数 = `a·v + b`" if 'v' in S else ''))),
    ],
    watch=[('op', 'op', 'blue'), ('x', 'x', 'pink'), ('tot_a', 'tot_a', 'cyan'), ('tot_b', 'tot_b', 'yellow'), ('v', 'v', 'green')],
    captions={
        'num_list = [[1, 0]]': '馆 0 在最后一轮的人数是未知数 `v` → 表示成 `1·v + 0` = `[1, 0]`',
        'num_list.append': '其余馆最后一轮人数已知：`[0, {num}]`，即 `0·v + {num}`',
        'g[x].add(y)': '记录无向边 `{x}`—`{y}`，之后要找相邻的馆',
        'for op, x in plans[::-1]': lambda S, B, r: f"==倒着==处理操作，现在是 `op = {S.op}`、`x = {S.x}`：{'人数减半，逆操作是翻倍' if S.op == 1 else '邻馆各加 x 的人数，逆操作是各减去' if S.op == 2 else '邻馆各减 x 的人数，逆操作是各加回'}",
        'g = {}': '`g` 存每个馆相邻的馆（无向图）',
        'num_list[x][0] *= 2': '操作 1 是「`x` 的人数减半」，倒推回去就是 ×2：`num_list[{x}]` = `{num_list[x]}`',
        'num_list[x][1] *= 2': '常数项也 ×2：`num_list[{x}]` = `{num_list[x]}`',
        'elif op == 2': '操作 `{op}`（馆 `{x}`）：正向是邻居各 +x 的人数，倒推是各自减去',
        'num_list[y][0] -= num_list[x][0]': '邻居 `{y}` 减去馆 `{x}` 的表达式：a 系数 → `{num_list[y][0]}`',
        'num_list[y][1] -= num_list[x][1]': '邻居 `{y}` 的常数项 → `{num_list[y][1]}`，`num_list[{y}]` = `{num_list[y]}`',
        'num_list[y][0] += num_list[x][0]': '操作 3（正向邻居各 −x 的人数）倒推要加回：邻居 `{y}` 的 a → `{num_list[y][0]}`',
        'num_list[y][1] += num_list[x][1]': '邻居 `{y}` 的常数项 → `{num_list[y][1]}`，`num_list[{y}]` = `{num_list[y]}`',
        'tot_a = tot_b = 0': '开始把 n 个线性式相加',
        'tot_a += ': '累加系数：`tot_a` = {tot_a}',
        'tot_b += ': '累加常数：`tot_b` = {tot_b}',
        'v = (totalNum': '总人数不变：`{tot_a}·v + {tot_b} = {totalNum}` → ==v = {v}==',
        'res = [': '把 `v` 代回每个表达式，得到最初每个馆的人数 `{res}`',
        'return res': '最初人数为 ==`{ret}`==',
    },
    skip=['if op == 1', 'elif op == 2', 'g[y].add(x)', 'if x not in g', 'if y not in g', 'g[x] = set()', 'g[y] = set()', 'for x, y in edges'],
    cards=dict(
        one_liner='只设一个未知数 v，倒着把每个馆都表示成 a·v+b',
        complexity='时间 `O(n + m·deg)`，空间 `O(n)`',
        problem=['`n` 个场馆最初志愿者人数未知，总和为 `totalNum`',
                 '`plans` 里每轮：1 = 馆 x 人数减半；2 = 邻馆各加 x 的人数；3 = 邻馆各减 x 的人数',
                 '已知最后一轮后馆 1…n−1 的人数 `finalCnt`，求最初每个馆人数',
                 '本视频：`finalCnt=[1,16], totalNum=21` → `[5,7,9]`'],
        quote='不妨只设一个未知数v表示第0个数最后一轮的值，然后从后往前倒推。由于是线性变换，那么往回推到最上面那一轮时将会得到n个关于v的线性表达式。',
        quote_src='—— yiduobo 题解原文',
        idea=['n 很大，不能解 n 元方程；馆 0 最后的人数设成 `v`，其他馆已知',
              '每个馆存一个 `[a, b]` 表示 `a·v + b`，倒着做逆操作：减半变翻倍，加变减，减变加',
              '最初总人数也是 `totalNum`：`Σa·v + Σb = totalNum`，解出 v 再代回'],
        summary=['时间 `O(n + 操作数 × 度数)`，空间 `O(n)`',
                 '要从后往前遍历 `plans[::-1]`，并且用「逆操作」',
                 '原文为 Python 2 写法，`v = (totalNum - tot_b) / tot_a` 已改为整数除法 `//`',
                 '题目保证结果是整数，所以整除不会丢信息'],
    ),
)
