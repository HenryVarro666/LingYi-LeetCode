BOX = [["#", ".", "*", "."], ["#", "#", "*", "."]]


def _c(S, i, j, v):
    return {'#': 'orange', '*': 'red'}.get(v)


CONFIG = dict(
    num=1861, title='旋转盒子', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='倒序遍历 + 双指针 k',
    tags=['难度分 1537'],
    code='''
class Solution:
    def rotateTheBox(self, boxGrid: list[list[str]]) -> list[list[str]]:
        m, n = len(boxGrid), len(boxGrid[0])
        ans = [['.'] * m for _ in range(n)]

        for i, row in enumerate(boxGrid):
            k = n - 1
            for j in range(n - 1, -1, -1):
                if row[j] == '*':  # 障碍物
                    ans[j][-1 - i] = '*'
                    k = j - 1  # 障碍物左边最近的石头，在旋转后掉落到 j-1
                elif row[j] == '#':  # 石头
                    ans[k][-1 - i] = '#'  # 旋转后，石头掉落到 k
                    k -= 1

        return ans
''',
    call=f'Solution().rotateTheBox({BOX!r})',
    expect=[["#", "."], ["#", "#"], ["*", "*"], [".", "."]],
    views=[
        dict(type='grid', var='boxGrid', label='boxGrid（# 石头，* 障碍物）：当前行 i 倒着扫', h=220, cell=70, color=_c,
             cursors=[('i', 'j', 'yellow')]),
        dict(type='grid', var='ans', label='ans（青框 = k 落点，红框 = 障碍物位置）', h=360, cell=70, color=_c,
             cursors=[("j if row[j] == '*' else None", 'm - 1 - i', 'red'), ('k', 'm - 1 - i', 'cyan')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'yellow'), ('k', 'k', 'cyan')],
    captions={
        'm, n = len': '`boxGrid` 是 `{m}×{n}`，旋转后变成 `{n}×{m}`',
        'ans = [': '先把答案全填成空位 `.`，之后只需要放石头和障碍物',
        'for i, row': lambda S, B, r: (f'每一行互相独立，处理第 `{S.i}` 行：旋转后它在倒数第 `{S.i}` 列（`-1 - {S.i}`）'
                                       if 'i' in S and ('i' not in B or S.i != B.i) else '所有行处理完毕'),
        'k = n - 1': '`k` = 石头旋转后会掉落到的位置（对应原行的列下标），先设成最右 `{k}`',
        'for j in range': lambda S, B, r: ('这一行扫完了' if 'j' in B and B.j == S.j
                                           else f'倒着扫：`j = {S.j}`，当前格 `{S.boxGrid[S.i][S.j]!r}`'),
        "if row[j] == '*'": lambda S, B, r: (f'`row[{S.j}] = {S.row[S.j]!r}`：是障碍物' if S.row[S.j] == '*'
                                             else f'`row[{S.j}] = {S.row[S.j]!r}`：不是障碍物'),
        "ans[j][-1 - i] = '*'": '障碍物不会动：放在 `ans[{j}][-1-{i}]`',
        'k = j - 1': '障碍物左边最近的石头，掉下来会停在 `j-1`：`k` → =={k}==',
        "elif row[j] == '#'": lambda S, B, r: (f'`row[{S.j}] = {S.row[S.j]!r}`：是石头，会掉落到 `k = {S.k}`' if S.row[S.j] == '#'
                                               else f'`row[{S.j}]` 是空位，什么也不用做'),
        "ans[k][-1 - i] = '#'": '石头掉落到 `ans[{k}][-1-{i}]`（不是它原来的列 {j}）',
        'k -= 1': '这个落点被占了，左边下一块石头只能落到 `k = {k}`',
        'return ans': '旋转后的盒子：`{ans}`',
    },
    cards=dict(
        one_liner='倒着扫每一行，用 k 记住石头的落点',
        complexity='时间 `O(mn)`，空间 `O(1)`（不含返回值）',
        problem=['`m×n` 的盒子里有石头 `#`、障碍物 `*`、空位 `.`',
                 '顺时针旋转 90 度，石头在重力下垂直掉落，直到碰到障碍物、石头或底部',
                 '返回旋转后的 `n×m` 矩阵；示例：`[["#",".","*","."],["#","#","*","."]]`'],
        quote='如果 row[j] 是石头，那么它掉落到 row[k]。然后把 k 减一，表示左边下一块石头掉落后的位置。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['每一行互相独立；格子 `(i, j)` 旋转后位于 `(j, m-1-i)`',
              '倒着遍历，遇到障碍物：它自己不动，左边石头最远落到 `j-1`',
              '遇到石头：落到 `k`，然后 `k -= 1` 给下一块留位置'],
        after=[dict(heading='方法一：正序遍历', lines=['统计两个障碍物之间的石头数 `cnt`',
                                                  '遇到障碍物（或行尾）时，从这里往前连续填 `cnt` 个石头'])],
        summary=['时间 `O(mn)`，空间 `O(1)`（不含返回值）',
                 '旋转后的坐标：`(i, j) → (j, m-1-i)`，用 `ans[j][-1 - i]`',
                 '障碍物左边不是石头也没关系，`k` 会继续被更新',
                 '另一种写法（方法一）：正序遍历 + 计数器，思路是数石头个数再往前填',
                 '同类：分组循环 / 相向双指针'],
    ),
)
