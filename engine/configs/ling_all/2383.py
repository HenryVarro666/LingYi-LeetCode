def _idx(S):
    if 'x' not in S or 'y' not in S:
        return None
    for i, (a, b) in enumerate(zip(S['energy'], S['experience'])):
        if (a, b) == (S['x'], S['y']):
            return i
    return None


def _top(S):
    if 'eng' not in S:
        return ''
    return f"当前 精力 `eng = {S['eng']}`，经验 `exp = {S['exp']}`；已补训练共 =={S.get('ans', 0)}== 小时"


CONFIG = dict(
    num=2383, title='赢得比赛需要的最少训练时长', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='模拟 · 不够就补到刚好超过',
    tags=[],
    code='''
class Solution:
    def minNumberOfHours(self, eng: int, exp: int, energy: List[int], experience: List[int]) -> int:
        ans = 0
        for x, y in zip(energy, experience):
            if eng <= x:
                ans += x + 1 - eng
                eng = x + 1  # 补到刚好超过
            eng -= x
            if exp <= y:
                ans += y + 1 - exp
                exp = y + 1  # 补到刚好超过
            exp += y
        return ans
''',
    call='Solution().minNumberOfHours(5, 3, [1, 4, 3, 2], [2, 6, 3, 1])',
    expect=8,
    views=[
        dict(type='text', fn=_top, size=28, h=60),
        dict(type='array', var='energy', label='energy（对手精力，打赢要扣掉）', cell=96, h=180,
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='array', var='experience', label='experience（对手经验，打赢要加上）', cell=96, h=180,
             color=lambda S, i, v: 'pink' if i == _idx(S) else None),
        dict(type='text', size=26, h=80,
             fn=lambda S: (f"这一位对手：精力 `{S['x']}`、经验 `{S['y']}`；要求 `eng > {S['x']}` 且 `exp > {S['y']}`" if 'x' in S else '')),
    ],
    watch=[('eng', 'eng', 'blue'), ('exp', 'exp', 'pink'), ('ans', 'ans', 'green'), 'x', 'y'],
    captions={
        'ans = 0': '`ans` 记录总共要补的训练小时数',
        'for x, y in zip': lambda S, B, ret: ('所有对手都遍历完了' if 'x' in B and S.x == B.x and S.y == B.y
                                              else f"对上下一个对手：精力 `{S.x}`，经验 `{S.y}`"),
        'if eng <= x': lambda S, B, ret: (f'`eng = {S.eng} <= {S.x}`：精力不严格超过对手 → ==不够，要补=='
                                          if S.eng <= S.x else f'`eng = {S.eng} > {S.x}`：精力够了，不用补'),
        'ans += x + 1 - eng': '补到刚好超过需要 `{x} + 1 - {B.eng}` = {x + 1 - B.eng} 小时 → `ans = {ans}`',
        'eng = x + 1': '精力补到 `{x} + 1 = {eng}`：==刚好超过，一点都不多补==',
        'eng -= x': '打赢后精力减少 `{x}` → `eng = {eng}`',
        'if exp <= y': lambda S, B, ret: (f'`exp = {S.exp} <= {S.y}`：经验不严格超过对手 → ==不够，要补=='
                                          if S.exp <= S.y else f'`exp = {S.exp} > {S.y}`：经验够了，不用补'),
        'ans += y + 1 - exp': '补到刚好超过需要 `{y} + 1 - {B.exp}` = {y + 1 - B.exp} 小时 → `ans = {ans}`',
        'exp = y + 1': '经验补到 `{y} + 1 = {exp}`：刚好超过',
        'exp += y': '打赢后经验增加 `{y}` → `exp = {exp}`',
        'return ans': '所有对手都能打赢，需要训练的总小时数是 ==`{ans}`==',
    },
    cards=dict(
        one_liner='不够就当场补到刚好超过，补的量加起来就是答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['有初始精力 `eng`、经验 `exp`，依次对上 n 个对手',
                 '必须精力和经验都==严格超过==对手才能赢；赢后精力减、经验加',
                 '开赛前可训练：每小时让精力或经验 +1，求最少小时数',
                 '示例：`5, 3, [1,4,3,2], [2,6,3,1]` → `8`'],
        quote='遍历 energy 和 experience，如果不如对手，那么增加自己的精力和经验，补到刚好超过对手即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['精力和经验互不影响，各补各的',
              '比赛中途缺多少补多少，==补到刚好超过==，最省',
              '题目要求赛前训练？等价：把途中补的量加起来，赛前一次补完'],
        result='总共补了 8 小时：精力补 6，经验补 2 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：是 ==严格超过==，所以条件是 `<=`，补到 `x + 1`',
                 '精力补完后要先 `eng = x + 1` 再 `eng -= x`，顺序不能反',
                 '赛中补等价于赛前补：因为每次补的都是“刚好够”的最小量'],
    ),
)
