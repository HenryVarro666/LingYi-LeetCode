def _txt(S):
    if 'w' not in S:
        return '`f[i][j]`：两个袋子能否恰好装 i 与 j'
    return f'当前物品重量 `w = {S["w"]}`：不放，放进袋 1（i），或放进袋 2（j）'


CONFIG = dict(
    num=3647, title='两个袋子中的最大重量', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='二维容量背包 · 可行性',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def maxWeight(self, weights, w1, w2):
        
        f = [[False] * (w2 + 1) for _ in range(w1 + 1)]
        f[0][0] = True
        for w in weights:
            for i in range(w1, -1, -1):
                for j in range(w2, -1, -1):
                    if i >= w and f[i - w][j]:
                        f[i][j] = True
                    if j >= w and f[i][j - w]:
                        f[i][j] = True
        
        res = 0
        for i in range(w1 + 1):
            for j in range(w2 + 1):
                if f[i][j]:
                    res = max(res, i + j)
        return res
''',
    call='Solution().maxWeight([1,2,2], 2, 2)',
    expect=4,
    max_steps=58,
    skip=['for i in range(w1, -1', 'for j in range(w2, -1', 'for i in range(w1 + 1)', 'for j in range(w2 + 1)'],
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='table', var='f', label='f[i][j]（行 i = 袋 1 重量，列 j = 袋 2 重量；绿 = 可达）', h=330, cell=70,
             rows=lambda S: [str(i) for i in range(len(S['f']))],
             cols=lambda S: [str(j) for j in range(len(S['f'][0]))],
             cursors=[('i', 'j', 'yellow', '(i,j)')], values=False,
             color=lambda S, i, j, v: 'green' if v else None),
    ],
    watch=[('w', 'w', 'pink'), ('i', 'i', 'blue'), ('j', 'j', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f = [[False]': '`f[i][j]`：袋 1 恰好装 `i`、袋 2 恰好装 `j` 是否可能',
        'f[0][0] = True': '什么都不装：`(0, 0)` ==可达==',
        'for w in weights': '放入下一件物品，重量 `{w}`',
        'if i >= w and f[i - w][j]': lambda S, B, r: (
            f'放进袋 1：`f[{S.i} − {S.w}][{S.j}]` 可达 → `f[{S.i}][{S.j}]` 也可达' if (S.i >= S.w and B.f[S.i - S.w][S.j])
            else '放进袋 1 要求 `i ≥ w` 且 `f[i−w][j]` 可达 → 不满足'),
        'f[i][j] = True': '`f[{i}][{j}] = True`：装得出 `({i}, {j})`',
        'if j >= w and f[i][j - w]': lambda S, B, r: (
            f'放进袋 2：`f[{S.i}][{S.j} − {S.w}]` 可达 → `f[{S.i}][{S.j}]` 也可达' if (S.j >= S.w and B.f[S.i][S.j - S.w])
            else '放进袋 2 要求 `j ≥ w` 且 `f[i][j−w]` 可达 → 不满足'),
        'if f[i][j]:': lambda S, B, r: ('`f[i][j]` 可达，用 `i + j` 试着更新答案' if S.f[S.i][S.j] else '`f[i][j]` 不可达，跳过'),
        'res = max': '可达的 `({i}, {j})`：总重 `{i + j}` → `res = {res}`',
        'return res': '所有可达 `(i, j)` 中 `i + j` 最大 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='两个袋子：用二维容量记录「恰好装多少」',
        complexity='时间 `O(n·w1·w2)`，空间 `O(w1·w2)`',
        problem=['给整数数组 `weights` 和两个袋子的容量 `w1`、`w2`',
                 '每件物品至多放进一个袋子，不能超容，求两袋总重最大是多少',
                 '本视频：`[1,2,2], w1=2, w2=2` → `4`'],
        quote='虽然有两个袋子，但是依然是背包问题。令f[k][i][j]表示前k个物品，其中第一个袋子放了重量i的物品，第二个袋子放了重量j的物品，是否可能达成。',
        quote_src='—— yiduobo 题解原文',
        idea=['每件物品三种选择：不要 / 放袋 1 / 放袋 2',
              '`f[i][j]` 为真，当且仅当 `f[i−w][j]` 或 `f[i][j−w]` 为真（上一轮）',
              '倒序遍历，省掉物品这一维；最后在可达格里取 `i + j` 最大'],
        summary=['时间 `O(n·w1·w2)`，空间 `O(w1·w2)`',
                 '`i`、`j` 都要倒序，保证每件物品只用一次',
                 '`f` 存可行性（布尔），答案在最后遍历可达格取最大 `i + j`',
                 '原文为 Python 2 风格，代码未改'],
    ),
)
