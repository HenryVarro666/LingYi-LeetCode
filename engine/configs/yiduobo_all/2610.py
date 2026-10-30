NUMS = [1, 3, 4, 1, 2, 3, 1]


def _draw_nums(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = len(NUMS)
    cell = min(84, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    cv.text((x0 + 18, y0 + 2), 'nums（蓝框 = 正在统计的元素）', 22, T['muted'], bold=True)
    nd = S.get('num_dict')
    line = S.get('_line')
    cur = None
    if nd is not None and line in (6, 7, 8) and 'v' in S:
        cur = sum(nd.values()) - (1 if line in (7, 8) else 0)
    for i, v in enumerate(NUMS):
        X = sx + i * cell
        past = cur is not None and i < cur or (nd is not None and line is not None and line >= 10)
        hot = cur is not None and i == cur
        cv.rect((X + 4, y0 + 44, X + cell - 4, y0 + 44 + cell - 10), fill=(52, 60, 72) if past else T['panel2'],
                r=10, outline=T['blue'] if hot else T['border'], width=5 if hot else 1)
        cv.text((X + cell / 2, y0 + 44 + cell / 2 - 5), v, 32, T['dim'] if past else T['text'], anchor='mm', bold=True)


def _draw_rows(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    res = S.get('res')
    if res is None:
        cv.text((x0 + 18, y0 + 2), f"出现次数最多是 {S.get('max_freq', 0)} 次 → 至少要这么多行", 22, T['muted'], bold=True)
        return
    cv.text((x0 + 18, y0 + 2), f"res：{len(res)} 行 = max_freq；出现 k 次的数放进 0 到 k-1 行", 22, T['muted'], bold=True)
    cell = 64
    line = S.get('_line')
    for r, row in enumerate(res):
        Y = y0 + 44 + r * (cell + 10)
        cv.text((x0 + 22, Y + cell / 2), f'行 {r}', 22, T['dim'], anchor='lm', mono=True)
        for j, v in enumerate(row):
            X = x0 + 110 + j * (cell + 8)
            fresh = line == 13 and 'index' in S and r == S['index'] and j == len(row) - 1
            cv.rect((X, Y, X + cell, Y + cell), fill=T['yellow'] if fresh else T['panel2'], r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + cell / 2), v, 30, T['bg'] if fresh else T['text'], anchor='mm', bold=True)
        if not row:
            cv.rect((x0 + 110, Y, x0 + 110 + cell, Y + cell), outline=T['border'], r=10, width=2)


CONFIG = dict(
    num=2610, title='转换二维数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按最大频次定行数 · 逐数填行',
    tags=[],
    code='''
class Solution(object):
    def findMatrix(self, nums):

        num_dict = {}
        max_freq = 0
        for v in nums:
            num_dict[v] = num_dict.get(v, 0) + 1
            max_freq = max(max_freq, num_dict[v])
        
        res = [[] for _ in range(max_freq)]
        for v in num_dict:
            for index in range(num_dict[v]):
                res[index].append(v)
        
        return res
''',
    call='Solution().findMatrix([1, 3, 4, 1, 2, 3, 1])',
    expect=[[1, 3, 4, 2], [1, 3], [1]],
    views=[
        dict(type='custom', draw=_draw_nums, h=170),
        dict(type='map', var='num_dict', fmt=lambda k, v: f'{k} 出现 {v} 次', h=190, font=26),
        dict(type='custom', draw=_draw_rows, h=330),
    ],
    watch=['v', ('max_freq', 'max_freq', 'pink'), 'index'],
    max_steps=70,
    captions={
        'num_dict = {}': '`num_dict` 统计每个数出现的次数',
        'max_freq = 0': '`max_freq` 记最大出现次数：一个数出现 k 次就至少要 k 行',
        'num_dict[v] = ': '`{v}` 又出现一次：`num_dict[{v}] = {num_dict[v]}`',
        'max_freq = max': '`max_freq = max({B.max_freq}, {num_dict[v]})` = =={max_freq}==',
        'res = [[]': '行数就取 `max_freq = {max_freq}`：先造出 {max_freq} 个空行',
        'for v in num_dict': lambda S, B, r: ('所有数都放好了' if sum(row.count(S.v) for row in S.res) == S.num_dict[S.v] else f'逐个处理不同的数 `v = {S.v}`（共出现 {S.num_dict[S.v]} 次）'),
        'for index in range': lambda S, B, r: (f'`v = {S.v}` 的 {S.num_dict[S.v]} 次出现都放好了，换下一个数' if sum(row.count(S.v) for row in S.res) == S.num_dict[S.v] else f'`v = {S.v}` 出现 {S.num_dict[S.v]} 次 → 放进第 0 到 {S.num_dict[S.v] - 1} 行，现在是第 `{S.index}` 行'),
        'res[index].append(v)': '第 `{index}` 行加入 `{v}`：每个数在不同的行各出现一次，行内不会重复',
        'return res': '`{max_freq}` 行，正好是最少的行数：`{ret}`',
    },
    cards=dict(
        one_liner='出现次数最多的数决定行数，出现 k 次就写进前 k 行',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `nums` 里的元素分到二维数组，每行元素互不相同',
                 '行数尽可能少，行长度可以不同，答案不唯一',
                 '示例：`[1,3,4,1,2,3,1]` → `[[1,3,4,2],[1,3],[1]]`'],
        quote='若某个数出现了k次，那么二维数组中至少需要有k行，才能保证这个数不会在同一个行中出现两次。更进一步的，设这些数出现次数的最大值为max_freq，那么最终的二维数组就至少需要max_freq行。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍，字典统计频次，同时记最大频次 `max_freq`',
              '造 `max_freq` 个空行，这是行数的下界',
              '一个数出现 k 次，就在第 0 到 k-1 行各放一个，刚好不重复'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`range(num_dict[v])` 填的是行号 0 到 k-1，不是 1 到 k',
                 '分两遍：先统计再填行，所以行数一开始就确定',
                 '原文为 Python 2 风格，无需改动，直接运行',
                 '对比灵神：灵神边遍历边按出现次数放行，只扫一遍；这里先统计再按字典填'],
    ),
)
