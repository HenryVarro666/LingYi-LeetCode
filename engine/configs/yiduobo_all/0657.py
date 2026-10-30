CONFIG = dict(
    num=657, title='机器人能否返回原点', difficulty='Easy', category='模拟',
    author='yiduobo', technique='遍历累计 U、L 坐标',
    code='''
class Solution(object):
    def judgeCircle(self, moves):

        U = L = 0
        for move in moves:
            if move == 'U':
                U += 1
            elif move == 'D':
                U -= 1
            elif move == 'L':
                L += 1
            else:
                L -= 1
        
        if U == 0 and L == 0:
            return True

        return False
''',
    call='Solution().judgeCircle("ULDRR")',
    expect=False,
    views=[
        dict(type='string', var='moves', label='moves（走法序列）', h=170),
        dict(type='text', size=34, fn=lambda S: (
            f"当前这步 `move = {S['move']}`" if 'move' in S else '')),
        dict(type='text', size=34, fn=lambda S: (
            f"纵向 `U` = =={S['U']}==，横向 `L` = =={S['L']}==" if 'U' in S and 'L' in S else '')),
    ],
    watch=[('move', 'move', 'yellow'), ('U', 'U', 'green'), ('L', 'L', 'blue')],
    captions={
        'U = L = 0': '`U` 记上下、`L` 记左右，都从 0 开始：==D 当作 −1 个 U，R 当作 −1 个 L==',
        "move == 'U'": lambda S, B, r: f"这步是 `{S.move}`" + ('，是 U → 上移，`U` 加 1' if S.move == 'U' else '，不是 U → 看下一个分支'),
        "move == 'D'": lambda S, B, r: f"这步是 `{S.move}`" + ('，是 D → 相当于 −1 个 U' if S.move == 'D' else '，不是 D → 继续判断'),
        "move == 'L'": lambda S, B, r: f"这步是 `{S.move}`" + ('，是 L → 左移，`L` 加 1' if S.move == 'L' else '，不是 L → 只剩 R'),
        'U += 1': '`U` → {U}',
        'U -= 1': 'D 抵消一个 U：`U` → {U}',
        'L += 1': '`L` → {L}',
        'L -= 1': '只剩 R，抵消一个 L：`L` → {L}',
        'if U == 0': lambda S, B, r: (f"走完了：`U = {S.U}`，`L = {S.L}`，" +
                                      ('都是 0 → 回到原点' if S.U == 0 and S.L == 0 else '至少一个不是 0 → 没回到原点')),
        'return True': '回到原点，返回 True',
        'return False': '没回到原点，返回 False',
    },
    cards=dict(
        one_liner='D 当成 −1 个 U，R 当成 −1 个 L，最后看两个数是否都为 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['机器人从原点出发，按 `moves` 里的 `U/D/L/R` 各走一步',
                 '走完后位于原点返回 `True`，否则 `False`',
                 '本视频：`"ULDRR"` → 最后停在原点右边一格，返回 `False`'],
        quote='1个D可以认为是-1个U，而1个R则可以认为是-1个L，于是我们最后只需要遍历整个行动序列，统计其中U和L的数目，若二者都为0，说明走回了原点。',
        quote_src='—— yiduobo 题解原文',
        idea=['`U` 统计纵向：U 加 1，D 减 1',
              '`L` 统计横向：L 加 1，R 减 1（最后的 else 就是 R）',
              '遍历一遍后两个数都是 0 才算回到原点'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：只统计步数相等不够，要让 D 抵消 U、R 抵消 L',
                 '本题的 else 分支默认是 R，输入只含 UDLR 才成立',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
