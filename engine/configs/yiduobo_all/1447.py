CONFIG = dict(
    num=1447, title='最简分数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举分子分母 + gcd 判断互质',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def simplifiedFractions(self, n):

        res = []
        for i in range(2, n + 1):
            for j in range(1, i):
                x = i
                y = j
                while y:
                    x, y = y, x % y

                if x == 1:
                   res.append(str(j) + '/' + str(i))
        
        return res
''',
    call='Solution().simplifiedFractions(4)',
    expect=['1/2', '1/3', '2/3', '1/4', '3/4'],
    views=[
        dict(type='text', fn=lambda S: (f"分数 `{S['j']}/{S['i']}`：求 `gcd({S['j']}, {S['i']})`，当前 `x = {S['x']}`，`y = {S['y']}`" if 'x' in S and 'j' in S else (f"分母 `i = {S['i']}`" if 'i' in S else '')), size=32, h=100),
        dict(type='stack', var='res', label='res（已找到的最简分数）', fmt=lambda x: str(x), h=130),
    ],
    watch=['i', 'j', ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        'res = []': '`res` 收集所有最简分数',
        'for i in range': '枚举分母 `i = {i}`（分母至少 2，分子才能 < 分母）',
        'for j in range': '枚举分子 `j = {j}`，分数 `{j}/{i}` 必须小于 1',
        'x = i': '`x = {i}`',
        'y = j': '`y = {j}`：对 `({x}, {y})` 做辗转相除',
        'while y': lambda S, B, r: (f'`y = {S.y}` ≠ 0，继续' if S.y else f'`y = 0`：`gcd({S.j}, {S.i}) = {S.x}`'),
        'x, y = y, x % y': '`x, y = {x}, {y}`',
        'if x == 1': lambda S, B, r: (f'gcd = 1：`{S.j}/{S.i}` 已是最简分数' if S.x == 1 else f'gcd = {S.x} > 1：`{S.j}/{S.i}` 还能约分，它的最简形式已在前面出现，跳过'),
        'res.append': '加入答案：`{res[-1]}`',
        'return res': '共 `{len(res)}` 个最简分数',
    },
    cards=dict(
        one_liner='n 最大才 100，直接枚举分子分母，gcd 等于 1 就是最简分数',
        complexity='时间 `O(n^2 log n)`，空间 `O(1)`（不含答案）',
        problem=['给定 `n`，返回所有分母 ≤ n、介于 0 和 1 之间（不含）的 ==最简分数==',
                 '最简分数：分子分母的最大公约数为 1',
                 '示例：`n = 4` → `["1/2","1/3","1/4","2/3","3/4"]`（顺序任意）'],
        quote='由于这里的n最大只有100，那么可以直接枚举分母和分子，然后对于每一组分母和分子，计算其最大公约数并进行约分即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['分母 `i` 从 2 到 n，分子 `j` 从 1 到 i-1（保证小于 1）',
              '对每一对求 `gcd(j, i)`，辗转相除',
              'gcd 为 1 就是最简，加入答案；否则它是某个更小分数的倍数，会重复'],
        summary=['时间 `O(n^2 log n)`，空间 `O(1)`（不含答案）',
                 '分子从 1 开始、到 i-1 结束，不含 0 和 1',
                 '答案顺序任意，本题按分母从小到大产生',
                 '本题代码无 Python 2 专有写法，原样使用'],
    ),
)
