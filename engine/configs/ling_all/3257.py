BOARD = [[5, 1, 2], [9, 8, 1], [4, 7, 3]]


def _inf(x):
    return '—' if x == float('-inf') else str(x)


def _fmt(t):
    return f'{_inf(t[0])}@列{t[1]}' if t[1] >= 0 else '空'


def _P(S):
    return [_fmt(t) for t in S['p']] if 'p' in S else []


def _SUF(S):
    return [('—' if s is None else ' '.join(_fmt(t) for t in s)) for s in S['suf']]


def _cell(S, r, c, v):
    if 'p' not in S:
        return None
    line = S.get('_line')
    d = S['_inner']
    m = len(S['board'])
    if 'ans' in S:  # 前缀阶段
        if line in (19, 20, 21, 22, 23) and r == S['i'] + 1:
            return 'yellow' if c == d.get('j2') else 'cyan'
        if r <= (S['i'] if 'i' in S else -1) and any(c == t[1] and v == t[0] for t in S['p']):
            return 'green'
        return None
    i = S.get('i')
    if i is not None and r >= i and any(c == t[1] and v == t[0] for t in S['p']):
        return 'blue'
    return None


def _sufx(S):
    parts = [f'suf[{k}] = ' + '，'.join(_fmt(t) for t in s) for k, s in enumerate(S['suf']) if s is not None] if 'suf' in S else []
    return '；'.join(parts) if parts else '`suf[i]`：第 i 行及以下的前三大（还没算）'


def _txt(S):
    line = S.get('_line')
    d = S['_inner']
    if 'ans' in S and line in (21, 22, 23) and 'z' in d:
        x, y, z = d['x'], d['y'], d['z']
        j1, j2, j3 = d['j1'], d['j2'], d['j3']
        ok = '三列互不相同 ✓' if len({j1, j2, j3}) == 3 else '有两个车同列 ✗'.replace('✓', '').replace('✗', '')
        return f'前缀 `{x}`@列{j1} + 中间 `{y}`@列{j2} + 后缀 `{z}`@列{j3}：{ok}'
    return '`p` = 当前这些行里，放在三个不同列上的最大、次大、第三大（值@列）'


CONFIG = dict(
    num=3257, title='放三个车的价值之和最大 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举中间 + 前后缀分解（每侧只留 3 个不同列的最大值）',
    tags=['枚举中间', '前后缀分解', '难度分 2553'],
    code='''
class Solution:
    def maximumValueSum(self, board: List[List[int]]) -> int:
        def update(row: List[int]) -> None:
            for j, x in enumerate(row):
                for k in range(3):
                    if x > p[k][0] and all(j != j2 for _, j2 in p[:k]):
                        p[k], (x, j) = (x, j), p[k]

        m = len(board)
        suf = [None] * m
        p = [(-inf, -1)] * 3  # 最大、次大、第三大
        for i in range(m - 1, 1, -1):
            update(board[i])
            suf[i] = p[:]

        ans = -inf
        p = [(-inf, -1)] * 3  # 重置，计算 pre
        for i, row in enumerate(board[:-2]):
            update(row)
            for j2, y in enumerate(board[i + 1]):  # 第二个车
                for x, j1 in p:  # 第一个车
                    for z, j3 in suf[i + 2]:  # 第三个车
                        if j1 != j2 and j1 != j3 and j2 != j3:  # 没有同列的车
                            ans = max(ans, x + y + z)  # 注：手动 if 更快
                            break
        return ans
''',
    call=f'Solution().maximumValueSum({BOARD})',
    expect=18,
    views=[
        dict(type='grid', var='board', label='board（绿/蓝 = 当前 p 里的三个格子；黄 = 枚举的中间车）', h=250, cell=64, color=_cell),
        dict(type='text', fn=_txt, size=22, h=70),
        dict(type='array', var=_P, label='p（最大 / 次大 / 第三大：值@列）', h=180, cell=118),
        dict(type='text', fn=_sufx, size=22, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j2', 'j2', 'pink'), ('ans', 'ans', 'green')],
    skip=['for j, x in enumerate(row)', 'for k in range(3)', 'for i in range(m - 1', 'for i, row in enumerate',
          'for j2, y in', 'for x, j1 in p', 'for z, j3 in suf', 'm = len', 'suf = [None]', 'if x > p[k][0]', 'break'],
    captions={
        'p[k], (x, j) = (x, j), p[k]': lambda S, B, r: (f'`{_fmt(S._inner["p"][S._inner["k"]])}` 比第 {S._inner["k"] + 1} 名更大、且列不同 → ==插到第 {S._inner["k"] + 1} 名==，原来的那个挤下去继续比（x, j 换成被挤出的）'),
        'suf[i] = p[:]': '第 `{i}` 行及以下的前三大存进 `suf[{i}]`（复制一份，`p` 之后还会变）',
        'ans = -inf': '`ans` 先设成负无穷（价值可能是负数）',
        'p = [(-inf, -1)] * 3  # 重置': '重置 `p`，接下来从上往下算前缀，边算边枚举中间的车',
        'update(row)': '前缀：把第 `{i}` 行并入 `p` → `p` 是第 0 到 {i} 行的前三大',
        'update(board[i])': '后缀：从下往上，把第 `{i}` 行并入 `p`',
        'if j1 != j2': lambda S, B, r: ('三个车 `列 {} / {} / {}`'.format(S._inner['j1'], S._inner['j2'], S._inner['j3']) +
                                          ('互不同列 → ==合法==' if len({S._inner['j1'], S._inner['j2'], S._inner['j3']}) == 3 else '有同列 → 换下一个后缀候选')),
        'ans = max(': '合法组合：`{x} + {y} + {z}` → `ans = max({B.ans}, {x + y + z})` = =={ans}==；后缀候选按从大到小，找到第一个合法的就 `break`',
        'return ans': '所有「中间车」都枚举完 → =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='枚举中间的车，两侧只需要各记三个不同列的最大值',
        complexity='时间 `O(mn)`，空间 `O(m)`',
        problem=['`m × n` 棋盘，`board[i][j]` 是格子的价值',
                 '放三个车，==两两不同行、不同列==，求价值之和最大',
                 '示例：`[[5,1,2],[9,8,1],[4,7,3]]` → `18`'],
        quote='枚举中间的车在第 i 排，那么需要知道第 0 到 i-1 排的车放在哪最合适，以及第 i+1 到 m-1 排的车放在哪最合适。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有三个元素的题，==枚举中间==：中间车在第 `i+1` 行，前后各一个车自动不同行',
              '只需保证三列不同：前缀、后缀各保留「不同列的前三大」，足以应付任何冲突',
              '`update` 把一行的值依次插入 `p`（保持三个不同列的前三大）；后缀预处理，前缀边枚举边更新'],
        summary=['时间 `O(mn)`：`update` 每个格子常数次，枚举中间 `n × 3 × 3`',
                 '空间 `O(m)`：只存每个后缀的 3 个候选',
                 '易错：`p` 里的三个值必须来自==不同列==，插入时要检查 `j != j2`',
                 '易错：三个车互相不同列，要同时判断 `j1, j2, j3` 两两不等',
                 '题解还给了 Python3 更快写法和费用流写法；同类题：3128. 直角三角形'],
    ),
)
