CONFIG = dict(
    num=1362, title='最接近的因数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='从 sqrt 向下找第一个因数',
    tags=['灵神题单', '数学算法'],
    setup='from math import sqrt',
    code='''
class Solution(object):
    def closestDivisors(self, num):

        x = int(sqrt(num + 1) + 0.5)
        while (num + 1) % x != 0:
            x -= 1
        
        res = [x, (num + 1) // x]
        min_diff = abs(x - (num + 1) // x)

        x = int(sqrt(num + 2) + 0.5)
        while (num + 2) % x != 0:
            x -= 1

        if abs(x - (num + 2) // x) < min_diff:
            res = [x, (num + 2) // x]
        
        return res
''',
    call='Solution().closestDivisors(123)',
    expect=[5, 25],
    views=[
        dict(type='text', fn=lambda S: (lambda t: f"目标 `{t}`：试 `x = {S['x']}`，`{t} % {S['x']} = {t % S['x']}`" + ('，==整除==，配对 ' + f"`{t // S['x']}`" if t % S['x'] == 0 else '，不整除，x 再减小') if 'x' in S and S['x'] > 0 else '')(S['num'] + (2 if S['_line'] >= 12 else 1)) if 'x' in S and 'num' in S else '', size=26),
        dict(type='array', var='res', h=160, label='res：目前最接近的一对'),
    ],
    watch=['num', ('x', 'x', 'blue'), ('min_diff', 'min_diff', 'green')],
    captions={
        'x = int(sqrt(num + 1)': '`num + 1 = {num + 1}`：从 `sqrt` 附近 `x = {x}` 开始往下找（越靠近 sqrt，两个因数越接近）',
        'while (num + 1)': lambda S, B, r: (f'`{S.num+1} % {S.x} = {(S.num+1) % S.x}` ≠ 0：{S.x} 不是因数' if (S.num+1) % S.x else f'`{S.num+1} % {S.x} == 0`：找到了，第一个整除的就最接近'),
        'x -= 1': '不是因数，`x` 往下一步 → {x}',
        'res = [x, (num + 1)': '`num + 1` 的最接近因数对：`{res}`',
        'min_diff =': '差值 `min_diff = {min_diff}`',
        'x = int(sqrt(num + 2)': '再看 `num + 2 = {num + 2}`，同样从 sqrt 附近 `x = {x}` 开始',
        'while (num + 2)': lambda S, B, r: (f'`{S.num+2} % {S.x} = {(S.num+2) % S.x}` ≠ 0：{S.x} 不是因数' if (S.num+2) % S.x else f'`{S.num+2} % {S.x} == 0`：找到了'),
        'if abs(x - (num + 2)': lambda S, B, r: (f'`num + 2` 的差 `{abs(S.x - (S.num+2)//S.x)}` < 之前的 `{S.min_diff}` → 换成它' if abs(S.x - (S.num+2)//S.x) < S.min_diff else f'`num + 2` 的差 `{abs(S.x - (S.num+2)//S.x)}` >= 之前的 `{S.min_diff}` → 保留原来的'),
        'res = [x, (num + 2)': '更新答案：`{res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='两个因数乘积固定时，越靠近 sqrt 差越小',
        complexity='时间 `O(sqrt(num))`，空间 `O(1)`',
        problem=['给整数 `num`，在 `num + 1` 和 `num + 2` 里找两个整数，乘积等于其中之一，且两数差的绝对值最小',
                 '示例：`num = 8` → `[3, 3]`（`9 = 3 × 3`）',
                 '本视频：`num = 123` → `[5, 25]`'],
        quote='为了使得x和num / x尽量接近，那么自然应该从sqrt(num)开始向下尝试，寻找第一个满足num % x = 0的x，那么此时的x和num / x就是最接近的因数。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘积固定，两数越接近，说明 x 越接近 sqrt',
              '从 sqrt 向下找到的第一个因数，就是最接近的一对',
              '`num + 1` 和 `num + 2` 各做一次，取差更小的'],
        summary=['时间 `O(sqrt(num))`，空间 `O(1)`',
                 '`sqrt` 带 `+ 0.5` 四舍五入，防止浮点误差使 `x` 偏小；`x` 从上往下减',
                 '差值相等时保留 `num + 1` 的结果（用严格 `<`）',
                 '原文为 Python 2 写法，`/` 整除已改为 `//`；`sqrt` 来自 `math`'],
    ),
)
