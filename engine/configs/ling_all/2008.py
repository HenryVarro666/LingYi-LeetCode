RIDES = [[1, 6, 1], [3, 10, 2], [10, 12, 3], [11, 12, 2]]


def _groups_txt(S):
    g = S.get('groups')
    if g is None:
        return '按下车地点 `end` 分组：记录 `(start, end - start + tip)`'
    return '  |  '.join(f'end={e}: ' + ' '.join(f'({s},{t})' for s, t in lst) for e, lst in sorted(g.items()))


def _cand(S):
    i = S.get('i')
    if i is None or 'groups' not in S:
        return '`f[i]` = 从 1 开到 i 最多赚的钱；`i` 从 2 开始'
    g = S['groups']
    if i in g and S['_line'] >= 10:
        return '载 `end = ' + str(i) + '` 的乘客：' + '，'.join(f'`f[{s}] + {t}` = =={S["f"][s] + t}==' for s, t in g[i])
    return f'`f[{i}]`：不载在 {i} 下车的乘客，就等于 `f[{i - 1}]`'


CONFIG = dict(
    num=2008, title='出租车的最大盈利', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='记忆化搜索 1:1 翻译成递推',
    tags=['灵神题单', '难度分 1872'],
    code='''
class Solution:
    def maxTaxiEarnings(self, n: int, rides: List[List[int]]) -> int:
        groups = defaultdict(list)
        for start, end, tip in rides:
            groups[end].append((start, end - start + tip))

        f = [0] * (n + 1)
        for i in range(2, n + 1):
            f[i] = f[i - 1]
            if i in groups:
                f[i] = max(f[i], max(f[s] + t for s, t in groups[i]))
        return f[n]
''',
    call=f'Solution().maxTaxiEarnings(12, {RIDES!r})',
    expect=14,
    skip=['groups[end].append', 'for start, end, tip in rides'],
    views=[
        dict(type='text', fn=_groups_txt, size=26, h=70),
        dict(type='array', var='f', label='f[i]：从 1 开到 i 最多赚多少（黄 = 正在算）', h=300, cell=62,
             pointers={'i': 'blue', 'i - 1 if _line == 9 else None': 'pink'},
             pointer_labels={'i - 1 if _line == 9 else None': 'i-1'},
             color=lambda S, k, v: 'yellow' if k == S.get('i') else None),
        dict(type='text', fn=_cand, size=28, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('f[i-1]', "f[i - 1] if _line >= 9 else '-'"), ('f[i]', "f[i] if _line >= 9 else '-'", 'green')],
    captions={
        'groups = defaultdict': '`groups[end]`：把在同一地点下车的乘客放一起，方便枚举',
        'f = [0] * (n + 1)': '`f[i]` = 从 1 开到 `i` 最多赚多少；==`f[1] = 0`==（没有人在 1 下车）',
        'for i in range': lambda S, B, r: ('所有地点都算完了' if S.i == B.get('i') else f'算 `f[{S.i}]`：从 1 开到 {S.i}'),
        'f[i] = f[i - 1]': '==不载==在 `{i}` 下车的乘客：问题变成开到 `{i - 1}`，`f[{i}] = {f[i - 1]}`',
        'if i in groups': lambda S, B, r: (f'有乘客在 `{S.i}` 下车，枚举载哪位' if S.i in S.groups else f'没人在 `{S.i}` 下车，`f[{S.i}]` 保持 {S.f[S.i]}'),
        'f[i] = max(f[i], max': lambda S, B, r: '`max(f[{0}], 最好的一单)` = `max({1}, {2})` = =={3}==：载这单 = 开到上车点 `s` 赚 `f[s]` + 这单收入 `t`'.format(S.i, B.f[S.i], max(S.f[s] + t for s, t in S.groups[S.i]), S.f[S.i]),
        'return f[n]': '答案 `f[{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='从 1 开到 i：不载 i 下车的人，或枚举载哪一位',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['一条路上 `n` 个地点，`rides[i] = [start, end, tip]`，载这位乘客盈利 `end - start + tip`',
                 '同时最多接一单，可在同一地点下客再接客；求最多盈利',
                 '示例：`n=5, rides=[[2,5,4],[1,5,1]]` → `7`'],
        quote='如果没有乘客在 i 下车，或者我们不载在 i 下车的乘客，问题变成：从 1 开到 i-1 最多可以赚多少钱。如果有乘客在 i 下车，我们可以枚举载哪位乘客。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从右往左想：只关心「从 1 开到 i」，子问题和原问题相似',
              '载乘客 `[s, i]` 后，`s` 到 `i` 不能再载人，剩下 `f[s]`',
              '去掉递归的「递」只留「归」，就是 `f` 数组自底向上枚举'],
        after=[dict(heading='另外两种写法', lines=['先写递归 `dfs(i)`，会超时；加 `@cache` 变成记忆化搜索', '再 1:1 翻译成递推 `f[i]`（本视频演示）'])],
        summary=['时间 `O(n+m)`：`groups[i]` 的总长度是 `m`',
                 '空间 `O(n+m)`',
                 '易错：可以同地点下客再接客，所以转移用 `f[s]` 而不是 `f[s-1]`',
                 '思考题：允许同时载两位乘客该怎么做？',
                 '同类：2830、1235、1751'],
    ),
)
