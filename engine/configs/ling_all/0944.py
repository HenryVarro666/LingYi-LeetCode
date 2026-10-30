def _grid(S):
    return [list(s) for s in S['strs']]


def _colidx(S):
    if 'col' not in S:
        return None
    strs = S['strs']
    cols = list(zip(*strs))
    for k, c in enumerate(cols):
        if c == S['col']:
            return k
    return None


def _cell(S, i, j, v):
    k = _colidx(S)
    if k is None:
        return None
    if j == k:
        if 'x' in S and 'y' in S and S['_line'] in (6, 7):
            return 'red' if S['x'] > S['y'] and S['col'][i] in (S['x'], S['y']) else 'blue'
        return 'blue'
    return None


def _txt(S):
    if 'ans' not in S:
        return ''
    if 'col' not in S:
        return '按列检查：从上到下看有没有“上面比下面大”'
    return f"当前列 `{''.join(S['col'])}`，已删列数 ==ans== = {S['ans']}"


CONFIG = dict(
    num=944, title='删列造序', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='zip(*strs) 转置 + pairwise',
    code='''
class Solution:
    def minDeletionSize(self, strs: List[str]) -> int:
        ans = 0
        for col in zip(*strs):
            if any(x > y for x, y in pairwise(col)):
                ans += 1
        return ans
''',
    call='Solution().minDeletionSize(["cba","daf","ghi"])',
    expect=1,
    views=[
        dict(type='text', fn=_txt),
        dict(type='grid', var=_grid, color=_cell, h=330, cell=90, label=''),
    ],
    watch=['col', 'x', 'y', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 记录==不是递增的列数==',
        'for col in zip': lambda S, B, r: (f"`zip(*strs)` 把网格转置，`col` 就是一整列：`{''.join(S.col)}`"
                                           if B.get('col') != S.col else '列都取完了，循环结束'),
        'if any': lambda S, B, r: (f"列 `{''.join(S.col)}` 中存在上面比下面大的相邻对 → ==这列要删=="
                                   if any(x > y for x, y in pairwise(S.col)) else f"列 `{''.join(S.col)}` 从上到下一路不减 → 保留"),
        'ans += 1': '这一列不是非严格递增：`ans` → {ans}',
        'return ans': '所有列检查完，要删 `{ans}` 列',
    },
    cards=dict(
        one_liner='转置之后逐列检查，有“上大下小”就删',
        complexity='时间 `O(nm)`，空间 `O(1)`',
        problem=['`n` 个等长字符串排成网格，删掉不是按字典序非严格递增的列',
                 '返回要删除的列数',
                 '示例：`["cba","daf","ghi"]` → `1`（只有列 1 `b,a,h` 不递增）'],
        quote='对于每一列，从上到下遍历，如果发现上面的字母比下面的大，那么这一列不是递增的，答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`zip(*strs)` 一次拿到每一列，不用写双层下标',
              '`pairwise(col)` 给出相邻两个字母 `x, y`，只要 `x > y` 就说明这列要删',
              '`any` 找到第一个反例就停'],
        summary=['时间 `O(nm)`，额外空间 `O(1)`（不计 zip 产生的列）',
                 '“非严格递增”：相等不算违规，判断用 `x > y`，不是 `>=`',
                 '写法二：`list(col) != sorted(col)`，同样判断这一列是否有序'],
    ),
)
