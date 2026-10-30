W = 3


def _bin(x, w):
    return format(x, f'0{w}b') if x is not None else '?'


def _txt(S):
    I = S['_inner']
    line = I.get('_line', S.get('_line'))
    if 'cand' in I and 'state' in I and 'g' in S and 'h' in I:
        s, c = I['state'], I['cand']
        w = W - 1
        return f'上一行缝 `{_bin(s, w)}` & 新一行缝 `{_bin(c, w)}` = `{_bin(s & c, w)}`' + ('  ==无对齐，可叠==' if s & c == 0 else '  ==有对齐，不行==')
    if 'state' in I and 'f' in S and 'candidate' not in S:
        st = I['state']
        return f'`state = {_bin(st, W)}`：第 k 位为 1 表示这一行在 k+1 处有砖缝'
    return '砖缝用二进制位表示：长度为 `b` 的砖，缝在它右端，对应位 `b-1`'


CONFIG = dict(
    num=2184, title='建造坚实的砖墙的方法数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状压 DP：行的砖缝集合 + 逐行转移',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def buildWall(self, height, width, bricks):

        move_mapping = {}
        for b in bricks:
            if b > width:
                continue
            move_mapping[1 << (b - 1)] = b

        f = [False] * (1 << width)
        f[0] = True
        for state in range(1 << width):
            lowbit = state & -state
            if lowbit in move_mapping and f[state >> move_mapping[lowbit]]:
                f[state] = True
        
        candidate = []
        for state in range(1 << (width - 1), 1 << width):
            if f[state]:
                candidate.append(state ^ (1 << (width - 1)))

        mod = 10 ** 9 + 7
        g = [0] * (1 << (width - 1))
        g[0] = 1
        for _ in range(height):
            h = g[:]
            g = [0] * (1 << (width - 1))
            for state in range(1 << (width - 1)):
                for cand in candidate:
                    if state & cand == 0:
                        g[cand] += h[state]
                        if g[cand] >= mod:
                            g[cand] -= mod
        
        res = 0
        for state in range(1 << (width - 1)):
            res += g[state]
            if res >= mod:
                res -= mod

        return res
''',
    call=f'Solution().buildWall(2, {W}, [1, 2])',
    expect=2,
    views=[
        dict(type='array', var='f', label='f[state]：这个砖缝集合能否由给定的砖铺满一行', cell=84, h=190,
             color=lambda S, i, v: ('blue' if i == S['_inner'].get('state') and 'candidate' not in S else 'green' if v else None)),
        dict(type='array', var='candidate', label='candidate：可行的一行（去掉右端边界后的砖缝集合）', cell=84, h=170),
        dict(type='array', var=lambda S: S.get('h') if 'h' in S else S.get('g'), label='h：下面一行各缝型的方案数（蓝 = 当前 state）', cell=84, h=170,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('state') and 'cand' in S['_inner'] else None),
        dict(type='array', var='g', label='g：叠上新一行后各缝型的方案数（粉 = 当前 cand）', cell=84, h=170,
             color=lambda S, i, v: 'pink' if i == S['_inner'].get('cand') else None),
        dict(type='text', size=26, h=60, fn=_txt),
    ],
    watch=[('height', 'height', 'blue'), ('width', 'width', 'blue'),
           ('state', lambda S: S['_inner'].get('state'), 'yellow'), ('cand', lambda S: S['_inner'].get('cand'), 'pink'),
           ('res', 'res', 'green')],
    skip=['if b > width', 'continue', 'for b in bricks', 'for state in range', 'for cand in candidate',
          'for _ in range(height)', 'mod = ', 'g[cand] -= mod', 'res += g[state]', 'if g[cand] >= mod',
          'if res >= mod', 'res -= mod', 'lowbit = state', 'f[state] = True', 'if f[state]:', 'f[0] = True', 'candidate = []'],
    captions={
        'move_mapping[1 << (b - 1)]': '长度 `{b}` 的砖：它的缝在第 `{b-1}` 位 → 记 `move_mapping[{1 << (b-1)}] = {b}`',
        'f = [False]': '`f[state]`：用砖把 `width` 格铺成缝位置恰为 `state` 的一行，是否可行',
        'if lowbit in move_mapping': lambda S, B, r: (
            f'`state = {S.state:03b}`，`lowbit = {S.lowbit}` 对应长 `{S.move_mapping[S.lowbit]}` 的砖，去掉它剩 `{S.state >> S.move_mapping[S.lowbit]}`，'
            + ('剩下的能铺 → ==`f[state] = True`==' if S.f[S.state >> S.move_mapping[S.lowbit]] else '剩下的铺不出 → 不可行')
            if S.lowbit in S.move_mapping else f'`state = {S.state:03b}`：`lowbit = {S.lowbit}` 没有对应长度的砖 → 不可行'),
        'candidate.append': '最右端一定是缝（整行铺满）→ 取最高位为 1 的 `state`，==去掉最右边界位==：候选 `{state ^ (1 << (width - 1))}`',
        'g = [0] * (1 << (width - 1))': '`g[s]`：已铺若干行，顶行缝型为 `s` 的方案数',
        'g[0] = 1': '地面当作“没有缝”的虚拟行：`g[0] = 1`，因此第一行可接任何候选',
        'h = g[:]': '`h` 保存下面一层的结果；`g` 重新开始，计算新的一行',
        'if state & cand == 0': lambda S, B, r: (f'下面一行缝 `{S.state:02b}`，新一行缝 `{S.cand:02b}`：`& = {S.state & S.cand:02b}` → '
                                                 + ('==没有对齐的缝==，可以叠' if S.state & S.cand == 0 else '有缝对齐，会形成竖直裂缝，不行')),
        'g[cand] += h[state]': '叠上去：`g[{cand}] += h[{state}]` → `{g[cand]}`',
        'return res': '把顶行所有缝型的方案数相加：`res = {ret}`',
    },
    max_steps=46,
    cards=dict(
        one_liner='先找出一行的所有可行缝型，再逐行叠、缝不能对齐',
        complexity='时间 `O(2^w·w + h·C²)`，空间 `O(2^w)`（C = 可行缝型数）',
        problem=['用若干种长度的砖（高 1，不可旋转，数量不限）砌一面 `height × width` 的墙',
                 '砖必须水平放，整行铺满；==相邻两行的砖缝不能在同一位置对齐==（两端除外）',
                 '求方案数，对 `10^9+7` 取模',
                 '本视频：`height=2, width=3, bricks=[1,2]` → `2`'],
        quote='可以使用状态压缩来表示当前这一行有哪些位置是砖缝，然后就可以通过状态压缩动态规划来计算当前这些砖在单一的行中可以砌成什么样。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[state]`：用 `lowbit` 找最左的砖，去掉它看剩余能否铺满',
              '最右边界必有缝，所以只取最高位为 1 的 `state`，再去掉该位做候选',
              '逐行 DP：新一行 `cand` 与下一行 `state` 按位与为 0 才能叠'],
        result='`height=2` 层叠完，总方案数 `2` ✓',
        summary=['每行方案先预处理，之后每层 DP 只和候选缝型有关',
                 '时间 `O(h·C²)`，`C` 是可行行型数；`width ≤ 10` 所以很小',
                 '易错：最右边界要算进 `f` 的 state，但不能放进相邻行的对齐比较',
                 '`g` 用滚动数组（`h = g[:]`）节省掉 `height` 这一维',
                 '原文为 Python 2 风格，代码无需修改，直接运行'],
    ),
)
