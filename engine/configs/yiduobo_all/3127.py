G = [["B", "W", "B"], ["B", "W", "W"], ["B", "W", "B"]]


def _col(S, i, j, v):
    I, J = S.get('i'), S.get('j')
    if I is None or J is None:
        return None
    if I <= i <= I + 1 and J <= j <= J + 1:
        if 'x' in S and 'y' in S and (i, j) == (I + S['x'], J + S['y']):
            return 'yellow'
        return 'cyan' if v == 'B' else 'orange'
    return None


def _cnt(S):
    if 'w' not in S:
        return ''
    return f"窗口 `({S['i']},{S['j']})`：白色 w = =={S['w']}==，黑色 b = =={S['b']}=="


CONFIG = dict(
    num=3127, title='构造相同颜色的正方形', difficulty='Easy', category='网格图',
    author='yiduobo', technique='枚举 2×2 · 黑白计数', tags=[],
    code='''
class Solution(object):
    def canMakeSquare(self, grid):

        for i in range(2):
            for j in range(2):
                w = b = 0
                for x in range(2):
                    for y in range(2):
                        if grid[i + x][j + y] == 'W':
                            w += 1
                        else:
                            b += 1
                
                if w >= 3 or b >= 3:
                    return True
        
        return False
''',
    call=f'Solution().canMakeSquare({G})',
    expect=True,
    views=[
        dict(type='grid', var='grid', h=380, cell=110, color=_col),
        dict(type='text', fn=_cnt, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('w', 'w', 'orange'), ('b', 'b', 'cyan')],
    captions={
        'for i in range(2)': lambda S, B, r: f'窗口左上角的行 `i = {S.i}`',
        'for j in range(2)': lambda S, B, r: f'窗口左上角的列 `j = {S.j}`：看 `({S.i},{S.j})` 开头的 2×2',
        'w = b = 0': '新窗口：白、黑计数清零',
        'for x in range(2)': lambda S, B, r: ('窗口内两行都看完了' if S.x == B.get('x') else f'窗口内第 {S.x} 行'),
        'for y in range(2)': lambda S, B, r: ('这一行两列都看完了' if S.y == B.get('y') else f'窗口内第 {S.y} 列'),
        "== 'W'": lambda S, B, r: f"格子 `({S.i + S.x},{S.j + S.y})` 是 `{S.grid[S.i + S.x][S.j + S.y]}`：" + ('白色 → w 加一' if S.grid[S.i + S.x][S.j + S.y] == 'W' else '黑色 → b 加一'),
        'w += 1': '`w` → {w}',
        'b += 1': '`b` → {b}',
        'if w >= 3': lambda S, B, r: f"w = {S.w}，b = {S.b}：" + ('有一种颜色 ≥ 3 个 → 改掉另一个（或本来全同色）就行，返回 True' if S.w >= 3 or S.b >= 3 else '都不到 3（2:2）→ 这个窗口没戏，换下一个'),
        'return True': '找到可行的窗口，返回 ==True==',
        'return False': '四个窗口都是 2:2，返回 ==False==',
    },
    cards=dict(
        one_liner='窗口里某种颜色有 3 个，就改掉剩下那一个',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['3×3 的黑白矩阵，至多改一个格子颜色', '能否让某个 2×2 正方形颜色完全相同',
                 '示例：`[[B,W,B],[B,W,W],[B,W,B]]` → `true`'],
        quote='如果存在有三个格子同色的2*2正方形，只需修改不同色的那一个格子同样可以得到纯色正方形。',
        quote_src='—— yiduobo 题解原文',
        idea=['本来就纯色：答案显然是 true', '三同色一异色：改掉异色那个，也是 true',
              '所以遍历 4 个窗口，数白、黑个数，任一 ≥ 3 就返回 true'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '窗口左上角只能是 `i, j ∈ {0, 1}`，共 4 个',
                 '2:2 才是唯一不行的情况',
                 '对比灵神：灵神把窗口检查写成函数，用哈希表计数并判断 `!= 2`；这里用 w、b 两个变量'],
    ),
)
