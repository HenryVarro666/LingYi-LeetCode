CONFIG = dict(
    num=1337, title='矩阵中战斗力最弱的K行', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='统计 1 的个数 · 排序',
    code='''
class Solution(object):
    def kWeakestRows(self, mat, k):

        cnt_list = []
        for index, line in enumerate(mat):
            cnt_list.append([sum(line), index])
        
        return [x[1] for x in sorted(cnt_list, key=lambda d:(d[0], d[1]))[:k]]
''',
    call='Solution().kWeakestRows([[1,1,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,1,0,0,0]], 2)',
    expect=[2, 0],
    views=[
        dict(type='grid', var='mat', h=300, cursors=[('index', 0, 'yellow', '')],
             color=lambda S, i, j, v: 'green' if 'index' in S and i == S['index'] and v == 1 else None),
        dict(type='text', size=30, fn=lambda S: ('(1 的个数, 行号)：' + '  '.join(f"`({a}, {b})`" for a, b in S['cnt_list'])) if 'cnt_list' in S else ''),
    ],
    watch=['index', 'k', ('cnt_list', 'cnt_list', 'green')],
    captions={
        'cnt_list = []': '`cnt_list` 用来存每一行的 `[战斗力, 行号]`',
        'for index, line': '取第 `{index}` 行：`{line}`',
        'cnt_list.append': '这一行有 `{sum(line)}` 个 1（士兵），记下 ==[{sum(line)}, {index}]==',
        'return [x[1]': lambda S, B, r: f'按 `(1 的个数, 行号)` 从小到大排序：战斗力相同时行号小的更弱；取前 `{S.k}` 个的行号 → =={r}==',
    },
    cards=dict(
        one_liner='数每行 1 的个数，连同行号一起排序',
        complexity='时间 `O(m·n + m log m)`，空间 `O(m)`',
        problem=['矩阵每行由若干 1（士兵）后接若干 0（平民）组成',
                 '1 越少战斗力越弱；一样多时行号小的更弱',
                 '返回最弱的 `k` 行的行号：本视频 `k = 2` → `[2, 0]`'],
        quote='统计每一行中1的数目，从小到大排序后输出行号即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['每行记成 `[sum(line), index]`',
              '排序键 `(d[0], d[1])`：先比 1 的个数，再比行号',
              '排完取前 `k` 个，只留行号'],
        summary=['时间 `O(m·n + m log m)`，空间 `O(m)`',
                 '行号放进排序键，才能处理战斗力相同的情况',
                 '原文已是 Python 3 可运行的写法，仅删去了 `class` 下的无关内容，代码未改动'],
    ),
)
