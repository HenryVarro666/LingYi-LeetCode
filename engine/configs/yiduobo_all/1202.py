_PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _col(S, i, v):
    c = S.get('color')
    if c is None or i >= len(c) or c[i] is None:
        return None
    return _PAL[c[i] % len(_PAL)]


def _lists(S):
    cl = S.get('char_list')
    if not cl:
        return '分量字符表 `char_list`：（还没有）'
    return '分量字符表：' + '　'.join(f'[{i}] {"".join(x)}' for i, x in enumerate(cl))


def _res(S):
    r = S.get('res')
    if r is None:
        return ''
    return '已填入答案：`' + ''.join(r) + '`'


CONFIG = dict(
    num=1202, title='交换字符串中的元素', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='连通分量 + 分量内排序',
    tags=['常用数据结构', '贪心与思维'],
    code='''
class Solution(object):
    def smallestStringWithSwaps(self, s, pairs):

        n = len(s)
        g = {x:set() for x in range(n)}
        for x, y in pairs:
            g[x].add(y)
            g[y].add(x)
        
        color = [None] * n
        char_list = []
        now_color = 0
        for index in range(n):
            if color[index] is None:
                char_list.append([])
                self.dfs(index, color, g, now_color, char_list, s)
                now_color += 1
        
        for index in range(now_color):
            char_list[index] = sorted(char_list[index])
        res = []
        pos_list = [0] * now_color
        for index in range(n):
            res.append(char_list[color[index]][pos_list[color[index]]])
            pos_list[color[index]] += 1

        return ''.join(res)

    def dfs(self, now, color, g, now_color, char_list, s):
        color[now] = now_color
        char_list[-1].append(s[now])
        for next in g[now]:
            if color[next] is None:
                self.dfs(next, color, g, now_color, char_list, s)
''',
    call='Solution().smallestStringWithSwaps("dcabef", [[0,3],[1,2],[3,4]])',
    expect='bacdef',
    views=[
        dict(type='string', var='s', label='s（同色 = 同一连通分量）', color=_col, h=170),
        dict(type='array', var='color', label='color：每个下标的分量编号（None = 还没染）', pointers={'index': 'yellow'}, h=190),
        dict(type='map', var='g', label='g：下标之间的边（交换关系）', fmt=lambda k, v: f'{k}: {sorted(v)}', h=120),
        dict(type='text', fn=lambda S: _lists(S), size=24, h=50),
        dict(type='text', fn=lambda S: _res(S), size=24, h=50),
        dict(type='calls', h=130, hide=('color', 'g', 'char_list', 's', 'pairs')),
    ],
    watch=[('index', 'index', 'yellow'), ('now_color', 'now_color', 'cyan'),
           ('now', lambda S: S['_inner'].get('now') if 'now' in S['_inner'] else None, 'blue')],
    captions={
        'n = len(s)': '把每个下标看成图中的点，`n = {n}`',
        'g = {x:set()': '`g` 为每个下标准备一个邻居集合',
        'g[x].add(y)': '一对 pair 就是一条无向边：`{x} — {y}`，所以两头都要加',
        'g[y].add(x)': '对称地加上 `{y} → {x}`',
        'color = [None]': '`color` 给连通分量染色：同色的下标之间可以随意交换',
        'char_list = []': '`char_list[c]` 收集颜色 c 这个分量里的所有字符',
        'now_color = 0': '第一个分量的颜色编号从 0 开始',
        'for index in range(n)': '枚举下标 `index`',
        'if color[index] is None': lambda S, B, r: (f'下标 {S.index} 还没染色 → 它是新分量的起点，从它 dfs' if S.color[S.index] is None else f'下标 {S.index} 已经染成 `{S.color[S.index]}`，属于之前的分量，跳过'),
        'char_list.append([])': '为新分量开一个空字符列表',
        'self.dfs(index': '从 `index` 出发 dfs，把整个连通分量染成 `now_color`',
        'now_color += 1': '这个分量染完了，下一个分量用颜色 `{now_color}`',
        'color[now] = now_color': '下标 `{now}` 染成 `{now_color}`',
        'char_list[-1].append': '把它的字符 `{s[now]}` 放进当前分量的列表',
        'for next in g[now]': '依次看 `{now}` 的邻居（看完了就返回上一层）',
        'if color[next] is None': lambda S, B, r: (f'邻居 {S.next} 没染 → 继续往下 dfs' if S.color[S.next] is None else f'邻居 {S.next} 已染过，不用再走'),
        'char_list[index] = sorted': '分量 `{index}` 里的字符排序：`{char_list[index]}`，字典序最小的放前面',
        'res = []': '`res` 按下标顺序依次填答案',
        'pos_list = [0]': '`pos_list[c]` 记录分量 c 已经用到了排序后的第几个字符',
        'res.append': '下标 `{index}` 属于分量 `{color[index]}`，取该分量最小的未用字符 `{res[-1]}`',
        'pos_list[color[index]] += 1': '该分量指针后移一位：`pos_list = {pos_list}`',
        'return': '拼成答案 `{ret}`',
    },
    cards=dict(
        one_liner='下标是点，pair 是边：连通分量内的字符可以随意排列',
        complexity='时间 `O(n log n + m)`，空间 `O(n + m)`',
        problem=['给字符串 `s` 和若干下标对 `pairs`，可以任意次交换 `pairs` 中的两个位置',
                 '返回能得到的字典序最小的字符串',
                 '本视频：`s = "dcabef"`，`pairs = [[0,3],[1,2],[3,4]]` → `"bacdef"`'],
        quote='如果我们将每个下标看成图中的一个点，而一组pair看成图中的一条边的话，那么我们最终可以得到一个无向图，而图中连通的部分其对应的字符值可以任意进行交换。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 pair 建无向图，用 dfs 给每个连通分量染同一种颜色',
              '同一颜色的字符放进各自的列表并排序',
              '再按下标从小到大，每个位置取它所在分量里最小的未用字符'],
        summary=['时间 `O(n log n + m)`，空间 `O(n + m)`',
                 '易错：`char_list[-1]` 依赖「刚开的列表就是当前分量」，所以必须先 append 再 dfs',
                 '填答案时每个分量要有自己的指针 `pos_list`',
                 '原文代码在 Python 3 下可直接运行，无需改动；也可用并查集代替 dfs'],
    ),
)
