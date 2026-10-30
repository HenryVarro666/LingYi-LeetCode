CONFIG = dict(
    num=2005, title='斐波那契树的移除子树游戏', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='SG 函数 · 克朗定理',
    tags=['灵神题单·数学算法', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def findGameWinner(self, n):
        sg = []
        sg.append(0)
        sg.append(1)
        for index in range(2, n):
            sg.append((sg[index - 1] ^ sg[index - 2]) + 1)
        
        if n == 1:
            return False

        res = sg[n - 1] ^ sg[n - 2]
        return res > 0
''',
    call='Solution().findGameWinner(6)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"`sg[{S['index']}] = (sg[{S['index']-1}] ^ sg[{S['index']-2}]) + 1 = ({S['sg'][S['index']-1]} ^ {S['sg'][S['index']-2]}) + 1 = {S['sg'][S['index']]}`"
                                         if 'index' in S and len(S['sg']) > S['index'] else 'sg[i] 表示 order(i+1) 这棵树的 SG 值')),
        dict(type='array', var='sg', pointers={'index': 'blue'}, h=300,
             color=lambda S, i, v: 'green' if i == len(S['sg']) - 1 and 'index' in S else None),
        dict(type='text', fn=lambda S: (f"`res = sg[{len(S['sg'])-1}] ^ sg[{len(S['sg'])-2}] = {S['sg'][-1]} ^ {S['sg'][-2]}` = =={S['res']}==") if 'res' in S else ''),
    ],
    watch=['n', 'index', ('res', 'res', 'green')],
    captions={
        'sg = []': '`sg[i]` 存「第 i+1 号斐波那契树」的 SG 值；每个子树可看成一条链',
        'sg.append(0)': '`sg[0] = 0`：对应只有根节点的树 order(1)，根不能拿，没有可走的步',
        'sg.append(1)': '`sg[1] = 1`：对应 order(2)，只能拿一个叶子，SG 值 1',
        'for index': lambda S, B, r: (f'递推到 `index = {S.index}`：这棵树由左右两棵小树挂在根上' if len(S.sg) < S.n else '`sg` 已经算到 `sg[n-1]`，循环结束'),
        'sg.append((sg': '克朗定理：左右子树的链长异或，再 +1 把根的那条边接上：`sg[{index}] = ({sg[index-1]} ^ {sg[index-2]}) + 1 = {sg[index]}`',
        'if n == 1': lambda S, B, r: ('`n == 1`：只有根，先手只能拿根 → 输' if S.n == 1 else f'`n = {S.n}`，不是 1，继续'),
        'res = sg': '先手面对根的左右两棵子树：谁拿走最后的非根节点，对方就只能拿根。答案看 `sg[{n-1}] ^ sg[{n-2}] = {res}`',
        'return res': lambda S, B, r: (f'`res = {S.res} > 0` → 异或值非零，先手（Alice）必胜 → ==True==' if S.res > 0 else f'`res = 0` → 先手必败 → ==False=='),
    },
    cards=dict(
        one_liner='树上 SG 函数：左右子树的 SG 值异或，非零先手必胜',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['斐波那契树 `order(n)`：根是 `n`，左子树 `order(n-2)`，右子树 `order(n-1)`',
                 'Alice 先手，每次选一个节点，删除它及整棵子树；==被迫删根的人输==',
                 '返回 Alice 是否必胜；本视频：`n = 6` → `True`'],
        quote='对于树上sg函数相关的问题，通常需要用到克朗定理，具体来说就是对于一棵树而言，其各个树链可以合并成为一条单链，而这条单链的长度则是各个支链上的边数的异或和。',
        quote_src='—— yiduobo 题解原文',
        idea=['拿到根的人输 → 转化成：左右两棵子树里，谁拿走最后的节点',
              '克朗定理：各支链长度异或 = 合并后单链长度；长为 k 的链 SG = k',
              '递推 `sg(i) = sg(i-1) ^ sg(i-2) + 1`，答案看 `sg(n-1) ^ sg(n-2)` 是否非零'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '==n == 1 要单独判==：只有根，先手必败；否则 `sg[n-2]` 越界',
                 '`+ 1` 是把根与子树连接的那条边算进去，不能漏',
                 '同类题：SG 函数 / Nim 游戏，状态异或非零先手必胜'],
    ),
)
