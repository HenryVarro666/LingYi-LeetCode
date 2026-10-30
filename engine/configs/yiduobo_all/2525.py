def _txt(S):
    if 'bulky' not in S:
        return '题目给定：`length=200, width=50, height=800, mass=50`'
    if 'heavy' not in S:
        return f"最大维度 `{max(S['length'], S['width'], S['height'])}`，体积 `{S['length']*S['width']*S['height']}` → bulky = =={S['bulky']}=="
    return f"bulky = =={S['bulky']}==，heavy = =={S['heavy']}=="


CONFIG = dict(
    num=2525, title='根据规则将箱子分类', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='分别判断 bulky 与 heavy',
    tags=['灵神题单', '难度分 1301'],
    code='''
class Solution(object):
    def categorizeBox(self, length, width, height, mass):

        bulky = (max(length, width, height) >= 10000) or (length * width * height >= (10 ** 9))
        heavy = (mass >= 100)

        if bulky:
            if heavy:
                return "Both"
            else:
                return "Bulky"
        elif heavy:
            return "Heavy"
        else:
            return "Neither"
''',
    call='Solution().categorizeBox(200, 50, 800, 50)',
    expect='Neither',
    views=[
        dict(type='text', fn=_txt, size=30, h=200),
        dict(type='array', var=lambda S: [S['length'], S['width'], S['height'], S['mass']], label='length / width / height / mass', h=220),
    ],
    watch=[('bulky', 'bulky', 'orange'), ('heavy', 'heavy', 'blue')],
    captions={
        'bulky =': '`max = {max(length, width, height)}`，体积 `{length*width*height}`：都没到上限 → `bulky = {bulky}`',
        'heavy =': '`mass = {mass}`，没到 100 → `heavy = {heavy}`',
        'if bulky': '`bulky = {bulky}`：不是 Bulky，进入后面的判断',
        'elif heavy': '`heavy = {heavy}`：也不是 Heavy',
        'return "Neither"': '两个条件都不满足 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='先分别判断是不是 bulky、是不是 heavy，再组合出结果',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给长、宽、高、质量，判断箱子属于 Bulky、Heavy、Both 还是 Neither',
                 '本视频示例：`200, 50, 800, 50` → `"Neither"`'],
        quote='按照题目描述分别判断箱子是否为bulky和heavy，然后返回最终结果即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`bulky`：最大维度 `>= 10000`，或者体积 `>= 10^9`',
              '`heavy`：质量 `>= 100`',
              '再用嵌套的 if 把四种组合都列出来'],
        after=[dict(heading='四种结果怎么来', lines=['`bulky` 且 `heavy` → `"Both"`', '只有 `bulky` → `"Bulky"`；只有 `heavy` → `"Heavy"`', '都不是 → `"Neither"`，本例就是这一种'])],
        summary=['时间、空间都是 `O(1)`',
                 '体积 = 三个维度的乘积，边界 `>=` 别写成 `>`',
                 '原文为 Python 2 写法，代码在 Python 3 下无需修改',
                 '对比灵神：灵神把条件缩成 x、y 两个变量，用平铺的 if 返回'],
    ),
)
