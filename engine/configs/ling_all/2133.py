CONFIG = dict(
    num=2133, title='检查是否每一行每一列都包含全部整数', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='计数数组 · 按轮数判重（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def checkValid(self, matrix: List[List[int]]) -> bool:
        cnt = [0] * 101  # cnt 记录的是当前循环轮数
        for i, row in enumerate(matrix):
            for v in row:
                if cnt[v] != i:
                    return False
                cnt[v] += 1
        for j in range(len(matrix[0])):
            for row in matrix:
                v = row[j]
                if cnt[v] != len(matrix) + j:
                    return False
                cnt[v] += 1
        return True
''',
    call='Solution().checkValid([[1,2,3],[3,1,2],[2,3,1]])',
    expect=True,
    snap_maxlen=5,
    views=[
        dict(type='grid', var='matrix', label='matrix', h=250, cell=80),
        dict(type='array', var='cnt', label='cnt[v]（只画 0..4，下标 0 不用）', h=170,
             color=lambda S, i, v: 'yellow' if 'v' in S and S['v'] == i else None),
        dict(type='text', fn=lambda S: ('`cnt[v]` 必须恰好等于当前轮数：行轮数 = `i`，列轮数 = `n + j`' if 'v' not in S else f"读到 `v = {S['v']}`，`cnt[{S['v']}] = {S['cnt'][S['v']] if S['v'] < 5 else '?'}`"), size=26),
    ],
    watch=['i', 'j', 'v'],
    captions={
        'cnt = [0]': '`cnt[v]` 记录数字 `v` 已经出现过几轮：前 `n` 轮是逐行，后 `n` 轮是逐列',
        'for i, row': '第 `{i}` 行：这一轮每个数字应该刚好第 `{i + 1}` 次出现',
        'if cnt[v] != i': lambda S, B, r: (f'`cnt[{S.v}] = {S.cnt[S.v]}`，当前是第 `{S.i}` 行 → '
                                           + ('==相等：这个数在这一行首次出现，没有重复=='
                                              if S.cnt[S.v] == S.i else '==不等：这一行里 v 重复了（或上一行缺了它）=='
                                              )),
        'cnt[v] += 1': lambda S, B, r: f'`cnt[{S.v}]` 加一，变成 `{S.cnt[S.v]}`，表示这个数又在本轮出现了一次',
        'for j in range': lambda S, B, r: ('行都检查完了，每个数的 `cnt` 都是 `n`；接着逐列，第 `0` 列' if 'j' not in B else (f'第 `{S.j}` 列：每个数应刚好第 `{S.j + 1}` 次出现' if S.j != B.get('j') else '列也检查完了')),
        'v = row[j]': '按列读：`row[{j}] = {v}`',
        'if cnt[v] != len': lambda S, B, r: (f'`cnt[{S.v}] = {S.cnt[S.v]}`，应等于 `n + j = {len(S.matrix) + S.j}` → '
                                             + ('==相等，这一列里没有重复==' if S.cnt[S.v] == len(S.matrix) + S.j else '==不等，这一列里 v 重复了==')),
        'return False': '某个数字的轮数对不上：行或列有重复，返回 `False`',
        'return True': '所有行和列都没有重复，而数值在 `1..n` 内 → `True`',
    },
    skip=['v = row[j]'],
    max_steps=90,
    cards=dict(
        one_liner='不用每行建集合：用一个 cnt，按轮数判重',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`n x n` 矩阵，==每一行和每一列==都要包含 `1` 到 `n` 的全部整数才有效',
                 '示例：`[[1,2,3],[3,1,2],[2,3,1]]` → `true`',
                 '本视频用这个示例'],
        quote='cnt 记录的是当前循环轮数',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['数值都在 `1..n`，行内没有重复就恰好是 `1..n`',
              '第 `i` 行开始前，每个数的 `cnt` 都应是 `i`；读到后加一',
              '逐列时接着数：第 `j` 列开始前应是 `n + j`；这样不用清空、不用建集合'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n^2)`，空间 `O(n)`（`cnt` 固定 101 项）',
                 '易错点：列的轮数要加上 `n`（`len(matrix) + j`），不能从 0 重新算',
                 '对比哈希集合：不用每行每列新建集合，更省空间'],
    ),
)
