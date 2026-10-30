L5 = 'abcde'


def _sub(S):
    d = S.get('dis')
    if not d:
        return None
    return [[None if v == -1 else v for v in r[:5]] for r in d[:5]]


def _color(S, i, j, v):
    k = S.get('k')
    if k is None or k >= 5 or S.get('_line') != 20:
        return None
    if (i == S.get('i') and j == k) or (i == k and j == S.get('j')):
        return 'blue'
    return None


def _info(S):
    if 'res' in S and 'index' in S:
        return f'逐位累加：`res` = =={S["res"]}=='
    return '规则（边）：`a→b` 2，`b→c` 5，`c→b` 5，`c→e` 1，`e→b` 2，`d→e` 20'


CONFIG = dict(
    num=2976, title='转换字符串的最小成本 I', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='Floyd 预处理 + 一趟累加',
    tags=['灵神题单·图论算法', '难度分 1882'],
    code='''
class Solution(object):
    def minimumCost(self, source, target, original, changed, cost):

        max_dis = 10 ** 6
        dis = [[-1] * 26 for _ in range(26)]
        for index in range(26):
            dis[index][index] = 0

        m = len(original)
        for index in range(m):
            x = ord(original[index]) - 97
            y = ord(changed[index]) - 97
            if dis[x][y] == -1 or dis[x][y] > cost[index]:
                dis[x][y] = cost[index]
        
        for k in range(26):
            for i in range(26):
                for j in range(26):
                    if dis[i][k] != -1 and dis[k][j] != -1 and (dis[i][j] == -1 or dis[i][j] > dis[i][k] + dis[k][j]):
                        dis[i][j] = dis[i][k] + dis[k][j]
        
        res = 0
        n = len(source)
        for index in range(n):
            x = ord(source[index]) - 97
            y = ord(target[index]) - 97
            if dis[x][y] != -1:
                res += dis[x][y]
            else:
                return -1
        
        return res
''',
    call="Solution().minimumCost('abcd', 'acbe', ['a','b','c','c','e','d'], ['b','c','b','e','b','e'], [2,5,5,1,2,20])",
    expect=28,
    skip=['max_dis', 'for index in range(26)', 'dis[index][index] = 0', 'm = len(original)', 'for index in range(m)',
          'x = ord(', 'y = ord(', 'if dis[x][y] == -1 or', 'for k in range(26)', 'for i in range(26)', 'for j in range(26)',
          'n = len(source)', 'for index in range(n)', 'if dis[i][k] != -1 and', 'if dis[x][y] != -1', 'res = 0'],
    max_steps=60, max_events=80000,
    views=[
        dict(type='string', var='source', label='source', h=140, cell=60,
             color=lambda S, k, v: 'blue' if 'res' in S and k == S.get('index') else None),
        dict(type='string', var='target', label='target', h=140, cell=60,
             color=lambda S, k, v: 'pink' if 'res' in S and k == S.get('index') else None),
        dict(type='text', fn=_info, size=24, h=80),
        dict(type='table', var=_sub, label='dis（只画 a–e，· = −1 = 不可达；行 = 起点，列 = 终点）', h=380, cell=62,
             rows=list(L5), cols=list(L5), color=_color,
             cursors=[(lambda S: S.get('i') if S.get('_line') == 20 else None, lambda S: S.get('j'), 'yellow')]),
    ],
    watch=[('res', 'res', 'green')],
    captions={
        'dis = [[-1]': '`dis` 全是 `-1`：用 `-1` 表示「暂时没有路」；对角线随后置 0',
        'dis[x][y] = cost[index]': lambda S, B, r: f'规则 `{chr(97 + S.x)}→{chr(97 + S.y)}` 成本 `{S.dis[S.x][S.y]}`：没有记录或更便宜才写入（重复规则只留最小）',
        'dis[i][j] = dis[i][k]': lambda S, B, r: (f'`k = {chr(97 + S.k)}` 中转：`{chr(97 + S.i)}→{chr(97 + S.k)}` + `{chr(97 + S.k)}→{chr(97 + S.j)}` = '
                                                   f'`{S.dis[S.i][S.k]} + {S.dis[S.k][S.j]}` ==更短（或原本不可达）== → `dis[{chr(97 + S.i)}][{chr(97 + S.j)}]` = =={S.dis[S.i][S.j]}=='),
        'res += dis[x][y]': lambda S, B, r: (f'第 {S.index} 位 `{S.source[S.index]}→{S.target[S.index]}` 的成本 `{S.dis[S.x][S.y]}` 累加 → `res` = =={S.res}=='),
        'return -1': '这一位查到 `-1`：变不过去 → 整体无解，直接返回 `-1`',
        'return res': '每位都能变，总成本 =={res}==',
    },
    cards=dict(
        one_liner='字符当节点、转换代价当边：Floyd 预处理，再一趟累加',
        complexity='时间 `O(n+m+26^3)`，空间 `O(26^2)`',
        problem=['`original[i]` 能以 `cost[i]` 的成本变成 `changed[i]`，可以连续变',
                 '把 `source` 变成 `target` 的最小总成本，不可能则返回 `-1`',
                 '本视频：`abcd → acbe` 返回 `28`'],
        quote='将字符视为图中的节点，转换的代价视为图中的边，那么交换两个字符的最小代价就是图中对应节点的最短路径长度，于是使用floyd算法提前预处理出交换任意两个字符的代价。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dis[x][y]` = 字符 x 变到字符 y 的最小代价，`-1` 表示不可达',
              '三重循环 `k, i, j`：只有 `i→k`、`k→j` 都可达，且更短才更新',
              '预处理后一趟遍历，每位查表累加；遇到 `-1` 立刻返回 `-1`',
              '视频里只保留了「发生更新」的那几步，其余判断折叠了'],
        summary=['时间 `O(n+m+26^3)`，空间 `O(26^2)`',
                 '用 `-1` 当「不可达」：比较前必须先判 `!= -1`，不能直接比大小',
                 '同一对字符有多条规则：只保留更小的',
                 '原文已是 Python 3 可运行的写法，未做改动',
                 '对比灵神：灵神用 `inf` 且 `dis[i][k] == inf` 就跳过；这里每次判 `-1`'],
    ),
)
