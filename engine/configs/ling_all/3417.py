G = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

CONFIG = dict(
    num=3417, title='跳过交替单元格的之字形遍历', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='取反标记 + 奇数行反转',
    code='''
class Solution:
    def zigzagTraversal(self, grid: List[List[int]]) -> List[int]:
        ans = []
        ok = True
        for i, row in enumerate(grid):
            if i % 2:
                row.reverse()
            for x in row:
                if ok:
                    ans.append(x)
                ok = not ok
        return ans
''',
    call=f'Solution().zigzagTraversal({G})',
    expect=[1, 3, 5, 7, 9],
    views=[
        dict(type='grid', var='grid', label='grid（奇数行已被反转；蓝框 = 当前行）', cell=84, h=300,
             color=lambda S, i, j, v: 'blue' if 'i' in S and i == S['i'] else None),
        dict(type='array', var='row', label='row（当前行遍历顺序）', cell=84, h=180,
             pointers={'row.index(x)': 'pink'}, pointer_labels={'row.index(x)': 'x'},
             color=lambda S, k, v: ('green' if S.get('ok') and 'x' in S and v == S['x'] else None)),
        dict(type='array', var='ans', label='ans', cell=70, h=170, color=lambda S, k, v: 'green'),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'pink'), ('ok', 'ok', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ok = True': '`ok` 表示当前数字能不能选，第一个数要选，所以初始 ==True==',
        'for i, row': lambda S, B, r: (f'看第 `{S.i}` 行：`{S.row}`' if S.get('i') != B.get('i') or 'i' not in B else '所有行都遍历完了'),
        'if i % 2': lambda S, B, r: (f'`i = {S.i}` 是奇数行 → 要倒着走，先反转' if S.i % 2 else f'`i = {S.i}` 是偶数行，从左往右，不用反转'),
        'row.reverse()': '奇数行反转后，从左往右读就是之字形的从右往左：`{row}`',
        'for x in row': lambda S, B, r: (f'遍历当前行的数 `x = {S.x}`' if S.get('x') != B.get('x') or 'x' not in B else '这一行遍历完了'),
        'if ok': lambda S, B, r: (f'`ok = True` → 这个数 `{S.x}` 要选' if S.ok else f'`ok = False` → 这个数 `{S.x}` 要跳过'),
        'ans.append': '选中 `{x}`，加入答案：`ans = {ans}`',
        'ok = not ok': '每遍历一个数就取反：选一个、跳一个、选一个……`ok = {ok}`（==换行也不重置==）',
        'return ans': '遍历完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='用 ok 取反：选一个跳一个，奇数行反转后照常遍历',
        complexity='时间 `O(mn)`，空间 `O(1)`（返回值不计）',
        problem=['按之字形遍历 `grid`：偶数行向右、奇数行向左',
                 '遍历中==隔一个取一个==，跳过每个交替的单元格',
                 '示例：`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,3,5,7,9]`'],
        quote='用一个变量 ok 表示当前数字能否加入答案。初始值为 true，每遍历一个数就取反，这样我们可以选一个数，跳过一个数，选一个数，跳过一个数，……',
        quote_src='—— 灵茶山艾府题解',
        idea=['`ok` 不随换行重置，所以整条之字形路径上严格交替',
              '下标为奇数的行先 `row.reverse()`，之后每行都是从左往右读',
              '本视频 3x3 的第 1 行：`6` 跳过、`5` 选、`4` 跳过'],
        summary=['时间 `O(mn)`，空间 `O(1)`',
                 '易错：`ok` 要在整个遍历里连续取反，不能每行重置',
                 '写法二：前 2k 行共 2kn 个数是偶数，偶数行都从第一个开始选；奇数行从下标 `n-1-n%2` 开始倒着隔一个取，切片 `row[end::-2]` 一行搞定',
                 '另有 Python 一行写法：`chain` 展开后 `[::2]`'],
    ),
)
