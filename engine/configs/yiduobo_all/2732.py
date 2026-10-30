GRID = [[1, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [0, 0, 0, 1]]


def _b(x):
    return format(x, '04b')


def _txt(S):
    if 's2' in S and 's1' in S:
        a, b = S['s1'], S['s2']
        return f'`{_b(a)} & {_b(b)} = {_b(a & b)}`' + ('  ==为 0，找到一对==' if a & b == 0 else '  不为 0')
    if 'line' in S and 'state' in S:
        return f'第 {S.get("index", "-")} 行 → `state = {_b(S["state"])}`（从左到右每读一列 ×2 再加）'
    return '一行 → 一个状态（二进制数）；`state_dict[状态] = 行号`'


CONFIG = dict(
    num=2732, title='找到矩阵中的好子集', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='证明只需两行 + 枚举状态对',
    tags=['灵神题单', '难度分 2240'],
    code='''
class Solution(object):
    def goodSubsetofBinaryMatrix(self, grid):

        state_dict = {}
        for index, line in enumerate(grid):
            state = 0
            for v in line:
                state = state * 2 + v
            
            if state == 0:
                return [index]
            
            state_dict[state] = index
        
        for s1 in state_dict:
            for s2 in state_dict:
                if s1 & s2 == 0:
                    return sorted([state_dict[s1], state_dict[s2]])
        
        return []
''',
    call=f'Solution().goodSubsetofBinaryMatrix({GRID})',
    expect=[0, 3],
    skip=['for v in line'],
    views=[
        dict(type='grid', var='grid', label='grid（每行读成一个二进制数）', h=230, cell=70,
             color=lambda S, r, c, v: ('yellow' if 'state' in S and 's1' not in S and r == S.get('index') else None)),
        dict(type='map', var='state_dict', label='state_dict：状态 → 行号', fmt=lambda k, v: f'{format(k, "04b")}（{k}） → 第 {v} 行',
             h=270, font=30),
        dict(type='text', fn=_txt, size=30, h=90),
    ],
    watch=[('index', 'index', 'blue'), ('state', 'state'), ('s1', 's1', 'orange'), ('s2', 's2', 'pink')],
    captions={
        'state_dict = {}': '`state_dict` 记录：每种状态 → 出现的行号',
        'for index, line in enumerate': lambda S, B, r: (f'读第 `{S.index}` 行 `{S.line}`' if 'line' in S and S.get('index') != B.get('index') or 'index' not in B else '所有行都读完了'),
        'state = 0': '`state` 清零',
        'state = state * 2 + v': '读到 `{v}`：`state = state × 2 + {v}` = `{state}`',
        'if state == 0': lambda S, B, r: ('这一行全 0，任选它一行就是好子集' if S.state == 0
                                           else f'`state = {S.state} ≠ 0`，不是全 0'),
        'state_dict[state] = index': '状态 `{state}` 记在第 `{index}` 行（相同状态只留一个）',
        'for s1 in state_dict': '==前面证明了：有解必有两行的解==，所以枚举两个状态 `s1`、`s2`',
        'for s2 in state_dict': '`s2 = {s2}`',
        'if s1 & s2 == 0': lambda S, B, r: (f'`{S.s1} & {S.s2} = {S.s1 & S.s2}` → ==两行没有同列的 1==，是好子集' if S.s1 & S.s2 == 0
                                             else f'`{S.s1} & {S.s2} = {S.s1 & S.s2} ≠ 0`：有同一列都是 1，不行'),
        'return sorted': '两行是 `{state_dict[s1]}`、`{state_dict[s2]}`，要升序 → `{ret}`',
        'return []': '任意两种状态都相交 → 无解，返回 `[]`',
    },
    max_steps=90,
    cards=dict(
        one_liner='先证明：有解就一定有两行的解',
        complexity='时间 `O(mn + 4^n)`，空间 `O(2^n)`',
        problem=['二进制矩阵，选若干行，==每列的和 ≤ 行数的一半==，返回行下标（升序）',
                 '没有好子集就返回空数组，多个解返回任意一个',
                 '本视频：`[[1,1,1,0],[0,1,1,1],[1,0,1,1],[0,0,0,1]]` → `[0,3]`'],
        quote='如果有解，那么必然存在一个仅由两行组合的解。由于每一行最多只有2^n种可能的状态，那么只需枚举两种合法的状态组合',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数行的解去掉一行仍是解 → 必有偶数行的解',
              '每行 ≤ 5 个数，若所有行都至少 3 个 1，总数会超过上限 → 必有一行 1 的个数 ≤ 2',
              '按 0/1/2 个 1 分类，都能配出两行的解 → 只枚举状态对 `s1 & s2 == 0`'],
        summary=['时间 `O(mn + 4^n)`，空间 `O(2^n)`',
                 '全 0 行单独返回；相同状态只记一次行号',
                 '易错：返回前 `sorted`，行下标要升序',
                 '原文代码在 Python 3 下可直接运行，没有改动',
                 '对比灵神：灵神用位运算 `<<`，yiduobo 用 `×2 + v`；灵神最后用 SOS DP 优化'],
    ),
)
