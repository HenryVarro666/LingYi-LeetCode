Q0 = [[0, 0, 4], [0, 1, 2], [1, 0, 1], [0, 0, 3], [1, 2, 1]]


def _mat(S):
    n = S['n']
    return [[0] * n for _ in range(n)]


def _cell(S, i, j, v):
    if 'vis_r' not in S:
        return None
    r = i in S['vis_r']
    c = j in S['vis_c']
    if r and c:
        return 'purple'
    if r:
        return 'blue'
    if c:
        return 'pink'
    return None


def _fn(S):
    if 'res' not in S:
        return '倒推：某格最终的值是最后一次覆盖它的那个操作'
    return f"已覆盖行 `{sorted(S['vis_r'])}`，列 `{sorted(S['vis_c'])}`，累计 res = =={S['res']}=="


CONFIG = dict(
    num=2718, title='查询后矩阵的和', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='倒推 · 按行列统计',
    tags=['灵神题单·贪心与思维', '难度分 1769'],
    code='''
class Solution(object):
    def matrixSumQueries(self, n, queries):

        vis_r = set()
        vis_c = set()
        res = 0
        for t, index, v in queries[::-1]:
            if t == 0:
                if index in vis_r:
                    continue
                vis_r.add(index)
                res += (n - len(vis_c)) * v
            else:
                if index in vis_c:
                    continue
                vis_c.add(index)
                res += (n - len(vis_r)) * v
        
        return res
''',
    call=f'Solution().matrixSumQueries(3, {Q0})',
    expect=13,
    views=[
        dict(type='table', var=_mat, label='3×3 矩阵（蓝 = 行已覆盖，粉 = 列已覆盖，紫 = 交叉）', h=300, cell=80,
             values=False, color=_cell),
        dict(type='text', fn=_fn, size=24, h=60),
        dict(type='set', var='vis_r', label='vis_r：已覆盖的行', h=130),
        dict(type='set', var='vis_c', label='vis_c：已覆盖的列', h=130),
    ],
    watch=['t', 'index', 'v', ('res', 'res', 'green')],
    captions={
        'vis_r = set()': '`vis_r`：倒推时已经出现过的行覆盖',
        'vis_c = set()': '`vis_c`：已经出现过的列覆盖',
        'for t, index, v': '倒推取一个操作：`t={t}`（0 行 / 1 列），`index={index}`，`v={v}`',
        'if t == 0': lambda S, B, r: '`t = 0` → 这是一次==行==覆盖' if S.t == 0 else '`t = 1` → 这是一次==列==覆盖',
        'if index in vis_r': lambda S, B, r: f'第 `{S.index}` 行之后已经覆盖过 → 这次的值全被盖住，==跳过==' if S.index in S.vis_r else f'第 `{S.index}` 行后面没再覆盖 → 本次有效',
        'if index in vis_c': lambda S, B, r: f'第 `{S.index}` 列之后已经覆盖过 → 这次的值全被盖住，==跳过==' if S.index in S.vis_c else f'第 `{S.index}` 列后面没再覆盖 → 本次有效',
        'continue': '直接看下一个更早的操作',
        'vis_r.add': '记下：第 `{index}` 行已被覆盖',
        'vis_c.add': '记下：第 `{index}` 列已被覆盖',
        'res += (n - len(vis_c))': '后面有 `{len(vis_c)}` 列覆盖过，这行只剩 `{n} - {len(vis_c)}` = {n - len(vis_c)} 格有效，贡献 `{n - len(vis_c)} × {v}` → res = =={res}==',
        'res += (n - len(vis_r))': '后面有 `{len(vis_r)}` 行覆盖过，这列只剩 `{n} - {len(vis_r)}` = {n - len(vis_r)} 格有效，贡献 `{n - len(vis_r)} × {v}` → res = =={res}==',
        'return res': '矩阵和 = =={ret}==',
    },
    cards=dict(
        one_liner='覆盖题倒推：后来的盖住先来的，扣掉被盖的格子',
        complexity='时间 `O(q)`，空间 `O(q)`',
        problem=['`n×n` 全 0 矩阵，查询 `[t, index, v]`：`t=0` 整行改成 `v`，`t=1` 整列改成 `v`',
                 '执行完所有查询后返回矩阵元素之和',
                 '示例：`n=3`，`[[0,0,4],[0,1,2],[1,0,1],[0,2,3],[1,2,1]]` → `17`',
                 '本视频：`[[0,0,4],[0,1,2],[1,0,1],[0,0,3],[1,2,1]]` → `13`（第 0 行覆盖了两次）'],
        quote='某个位置最终的结果必然是最后一次覆盖的结果，可以考虑倒推求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模大，不能真的模拟覆盖；某格的值只看最后一次覆盖',
              '倒推时，一次行覆盖之后若又出现 `k` 次不同的列覆盖，本行就有 `k` 格不算',
              '所以行用 `vis_c` 的大小扣，列用 `vis_r` 的大小扣'],
        summary=['时间 `O(q)`，空间 `O(q)`',
                 '易错：已经覆盖过的行/列要 `continue`，不能重复计入',
                 '行与列的扣减对象是==对方==的集合',
                 '对比灵神：灵神把两个集合放进数组 `vis[type]`，yiduobo 分成 `vis_r`、`vis_c` 两段写',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
