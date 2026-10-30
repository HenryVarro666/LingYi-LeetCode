def _top(S):
    if 'flag1' not in S:
        return ''
    return f"第 {S['i']} 行 vs 第 0 行：`flag1`（每格都不同）= {S['flag1']}，`flag2`（每格都相同）= {S['flag2']}" if 'i' in S else ''


def _cell(S, i, j, v):
    if 'i' not in S:
        return None
    if S.get('j') is not None and i == S['i'] and j == S['j']:
        return 'yellow'
    if i == 0 and S.get('j') is not None and j == S['j']:
        return 'blue'
    if i == 0:
        return 'blue'
    if i == S['i']:
        return 'purple'
    return None


CONFIG = dict(
    num=2128, title='通过翻转行或列来去除所有的1', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='行与首行：全同或全异',
    tags=[],
    code='''
class Solution(object):
    def removeOnes(self, grid):

        m = len(grid)
        n = len(grid[0])
        for i in range(1, m):
            flag1 = flag2 = True
            for j in range(n):
                if grid[i][j] == grid[0][j]:
                    flag1 = False
                if grid[i][j] != grid[0][j]:
                    flag2 = False
            
            if not flag1 and not flag2:
                return False
        
        return True
''',
    call='Solution().removeOnes([[1,0,1],[0,1,0],[1,0,1]])',
    expect=True,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='grid', var='grid', label='grid（蓝 = 第 0 行，紫 = 当前行，黄 = 正在比较的格子）', cursors=[], color=_cell, h=330, cell=96),
        dict(type='text', fn=lambda S: '每行必须和第 0 行==完全相同==或==完全相反==，否则无解', size=26),
    ],
    watch=[('i', 'i', 'purple'), ('j', 'j', 'yellow'), ('flag1', 'flag1', 'green'), ('flag2', 'flag2', 'orange')],
    captions={
        'm = len': '`m = {m}` 行',
        'n = len': '`n = {n}` 列',
        'for i in range': lambda S, B, ret: (f'检查第 `{S.i}` 行和第 0 行的关系' if S.get('i') is not None and S.i != B.get('i') or 'i' not in B else '每一行都检查过了'),
        'flag1 = flag2 = True': '先假设：`flag1` = 这行和首行==每格都不同==，`flag2` = ==每格都相同==',
        'for j in range': lambda S, B, ret: (f'看第 `{S.j}` 列' if 'j' not in B or S.j != B.j else '这一行的所有列都比完了'),
        'if grid[i][j] == grid[0][j]': lambda S, B, ret: (f'`{S.grid[S.i][S.j]} == {S.grid[0][S.j]}` → 这格相同，所以不可能“每格都不同”，`flag1 = False`' if S.grid[S.i][S.j] == S.grid[0][S.j]
                                                         else f'`{S.grid[S.i][S.j]} != {S.grid[0][S.j]}` → 不相同，`flag1` 保持不变'),
        'if grid[i][j] != grid[0][j]': lambda S, B, ret: (f'`{S.grid[S.i][S.j]} != {S.grid[0][S.j]}` → 这格不同，所以不可能“每格都相同”，`flag2 = False`' if S.grid[S.i][S.j] != S.grid[0][S.j]
                                                         else f'`{S.grid[S.i][S.j]} == {S.grid[0][S.j]}` → 相同，`flag2` 保持不变'),
        'flag1 = False': '`flag1 = False`：这行不是首行的“反面”',
        'flag2 = False': '`flag2 = False`：这行不是首行的“复制”',
        'if not flag1 and not flag2': lambda S, B, ret: (f'`flag1 = {S.flag1}`，`flag2 = {S.flag2}`：==既不全同也不全异== → 无法消除，返回 False' if not S.flag1 and not S.flag2
                                                         else f'`flag1 = {S.flag1}`，`flag2 = {S.flag2}`：至少有一个成立 → 这行没问题'),
        'return False': '这行和首行有的格相同、有的格不同：翻列时必然顾此失彼 → `False`',
        'return True': '每一行都与首行全同或全异 → 翻转若干列后能让每行同色，再翻行即可清零 → `True`',
    },
    cards=dict(
        one_liner='每一行要么和第一行完全相同，要么完全相反',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`m x n` 的 0/1 矩阵，每次可以翻转==一整行==或==一整列==（0 变 1，1 变 0）',
                 '问能否把所有的 1 都去掉（全部变成 0）',
                 '本视频：`[[1,0,1],[0,1,0],[1,0,1]]` → `true`'],
        quote='每行需要翻转的列必须都一样，也就是各行要么完全相同，要么完全不同。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一行内的 0 和 1 只能靠翻转==列==来调整，所以先选一些列翻转，让每行变成全 0 或全 1',
              '为某一行翻了某些列后，就不能再动其他列，否则会打乱这一行',
              '因此各行翻的列必须相同：每行和第一行比较，要么每格都同，要么每格都异'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '`flag1` 为“全不同”，`flag2` 为“全相同”，两个都为 False 才失败',
                 '只比较第 0 行与其余行，不需要两两比较',
                 '原文代码已是 Python 3 写法，无需改动（题面库里缺失，题意据文章与 LeetCode 原题补写）'],
    ),
)
