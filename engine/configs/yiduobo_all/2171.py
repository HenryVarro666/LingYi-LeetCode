CONFIG = dict(
    num=2171, title='拿出最少数目的魔法豆', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='枚举剩余豆数 · 排序后求 k',
    tags=['灵神题单', '难度分 1748'],
    code='''
class Solution(object):
    def minimumRemoval(self, beans):

        res = None
        s = sum(beans)
        res = s
        n = len(beans)
        for index, b in enumerate(sorted(beans)):
            res = min(res, s - (n - index) * b)
        
        return res
''',
    call='Solution().minimumRemoval([4,1,6,5,2,9])',
    expect=11,
    views=[
        dict(type='array', var=lambda S: sorted(S['beans']), pointers={'index': 'blue'}, h=260, label='sorted(beans)',
             window=('index', 'n - 1'),
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
        dict(type='text', fn=lambda S: (f"枚举 `cnt = {S['b']}`：后面 `n − index = {S['n'] - S['index']}` 个袋子各留 {S['b']} → 剩 {S['b'] * (S['n'] - S['index'])}，拿走 `{S['s']} − {S['b'] * (S['n'] - S['index'])}` = =={S['s'] - S['b'] * (S['n'] - S['index'])}=="
                                         if 'b' in S and 'index' in S else ''), h=100),
    ],
    watch=[('s', 's', 'yellow'), ('n', 'n', 'blue'), ('index', 'index', 'blue'), ('b', 'b', 'pink'), ('res', 'res', 'green')],
    captions={
        's = sum': '`s` = 豆子总数 = =={s}==',
        'res = s': '先假设全拿走：`res = {s}`',
        'n = len': '`n = {n}` 个袋子',
        'res = None': '`res` 先占位，下一行会改成 `s`',
        'for index': lambda S, B, r: ('所有 `cnt` 都枚举完了' if 'index' in B and B['index'] == S.index
                                      else f'枚举最终每个袋子剩 `cnt = {S.b}`（排序后的第 `{S.index}` 个）'),
        'res = min': lambda S, B, r: (f"豆数 ≥ {S.b} 的袋子有 `n − index = {S.n - S.index}` 个，各留 {S.b} 颗；"
                                      f"拿走 `{S.s} − {S.n - S.index}×{S.b}` = {S.s - (S.n - S.index) * S.b}；`res` 取小 → =={S.res}=="),
        'return res': '最少拿走 `{res}` 颗',
    },
    cards=dict(
        one_liner='枚举每个袋子最终剩几颗，排序后后缀长度就是袋子数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['拿出若干豆子，使剩下的非空袋子豆数全部相等，求最少拿出多少',
                 '示例：`[4,1,6,5]` → `4`',
                 '本视频：`[4,1,6,5,2,9]` → `11`'],
        quote='设有k个袋子中的豆子数大于等于cnt，那么最终剩下的豆子数就是cnt * k，而拿走的豆子数目就是sum(beans) - cnt * k。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举最终每袋剩 `cnt`：小于 `cnt` 的拿光，其余只留 `cnt`',
              '排序后第 `index` 个数作为 `cnt`，后面共 `n − index` 个袋子',
              '拿走的 = `sum − cnt × (n − index)`，所有枚举取最小'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（`sorted` 生成新列表）',
                 '`k = n − index`：从 index 到 n−1 共 n−index 个',
                 '`res` 初值设为 `s`（全拿走），别设成 0',
                 '对比灵神：灵神把「保留」看成矩形面积求最大；本解直接算拿走多少求最小'],
    ),
)
