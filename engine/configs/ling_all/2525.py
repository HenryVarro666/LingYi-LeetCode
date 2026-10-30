def _txt(S):
    if 'x' not in S:
        return '题目给定：`length=1000, width=35, height=700, mass=300`'
    v = S['length'] * S['width'] * S['height']
    s = f"体积 `{S['length']}×{S['width']}×{S['height']}` = {v}"
    if 'y' not in S:
        return s + '；任一维度 ≥ 10000 或体积 ≥ 10^9 → Bulky？ ==' + ('是' if S['x'] else '否') + '=='
    return s + f"；Bulky = =={S['x']}==，Heavy = =={S['y']}=="


CONFIG = dict(
    num=2525, title='根据规则将箱子分类', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 用变量名简化逻辑',
    tags=['灵神题单', '难度分 1301'],
    code='''
class Solution:
    def categorizeBox(self, length: int, width: int, height: int, mass: int) -> str:
        x = length >= 10000 or width >= 10000 or height >= 10000 or length * width * height >= 10 ** 9
        y = mass >= 100
        if x and y: return "Both"
        if x: return "Bulky"
        if y: return "Heavy"
        return "Neither"
''',
    call='Solution().categorizeBox(1000, 35, 700, 300)',
    expect='Heavy',
    views=[
        dict(type='text', fn=_txt, size=30, h=200),
        dict(type='array', var=lambda S: [S['length'], S['width'], S['height'], S['mass']], label='length / width / height / mass', h=220),
    ],
    watch=[('x (Bulky)', 'x', 'orange'), ('y (Heavy)', 'y', 'blue')],
    captions={
        'x = length': '先判断 ==Bulky==：三个维度都 `< 10000`，体积 `{length*width*height}` `< 10^9` → `x = {x}`',
        'y = mass': '再判断 ==Heavy==：`mass = {mass} >= 100` → `y = {y}`',
        'if x and y': '`x = {x}`、`y = {y}`：两者都为真才是 Both → 不成立，往下看',
        'if x:': '`x = {x}`：只有 Bulky 为真才返回 Bulky → 不成立',
        'if y:': '`y = {y}`：到这里 x 已经为假，y 为真 → 只是 ==Heavy==',
        'return "Heavy"': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='读懂题意，按要求分类讨论，变量名帮你理清逻辑',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给长、宽、高、质量，判断箱子是 Bulky / Heavy / Both / Neither',
                 'Bulky：某个维度 `>= 10^4` 或体积 `>= 10^9`；Heavy：质量 `>= 100`',
                 '示例：`1000, 35, 700, 300` → `"Heavy"`'],
        quote='读题题，按照要求分类讨论即可。可以用变量名来简化逻辑。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先用 `x` 表示是不是 Bulky，`y` 表示是不是 Heavy',
              '再按 Both、Bulky、Heavy、Neither 的顺序依次判断',
              '前面的分支已经排除了情况，后面的判断不必再重复写条件'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：体积 `10^9` 要用整数 `10 ** 9`，Python 不会溢出，其他语言要用 64 位整数',
                 '`x` 和 `y` 的判断都是 `>=`，边界值要算进去',
                 '返回顺序：先判 Both，再判单独的 Bulky、Heavy'],
    ),
)
