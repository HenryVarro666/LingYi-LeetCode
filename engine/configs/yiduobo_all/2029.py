CONFIG = dict(
    num=2029, title='石子游戏 IX', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='模 3 分类 · ma/mi 分情况',
    tags=['博弈论', '贪心与思维', '难度分 2277'],
    code='''
class Solution(object):
    def stoneGameIX(self, stones):

        zero = one = two = 0
        for stone in stones:
            if stone % 3 == 0:
                zero += 1
            elif stone % 3 == 1:
                one += 1
            else:
                two += 1

        ma, mi = one, two
        if ma < mi:
            ma, mi = mi, ma
        
        if mi == 0:
            return ma > 2 and zero % 2 == 1
        
        if zero % 2 == 0:
            return True

        return ma - mi > 2
''',
    call='Solution().stoneGameIX([5,1,2,4,3])',
    expect=False,
    views=[
        dict(type='array', var='stones', label='stones（绿 = 余 0，蓝 = 余 1，粉 = 余 2）', h=210, cell=100,
             color=lambda S, i, v: {0: 'green', 1: 'blue', 2: 'pink'}[v % 3]),
        dict(type='text', h=70, size=32,
             fn=lambda S: f"zero（余 0）=={S.get('zero', 0)}==　one（余 1）=={S.get('one', 0)}==　two（余 2）=={S.get('two', 0)}=="),
        dict(type='text', h=70, size=32,
             fn=lambda S: f"ma（较多）=={S['ma']}==　mi（较少）=={S['mi']}==　ma−mi = =={S['ma'] - S['mi']}==" if 'ma' in S else ''),
    ],
    watch=[('zero', 'zero', 'green'), ('one', 'one', 'blue'), ('two', 'two', 'pink'), 'ma', 'mi'],
    captions={
        'zero = one': '按模 3 分成三类，分别计数：`zero`、`one`、`two`',
        'if stone % 3 == 0': '`{stone} % 3 = {stone % 3}`：{"余 0，归 zero" if stone % 3 == 0 else "余数不是 0，继续判断"}',
        'zero += 1': '余 0 的石子：`zero` → =={zero}==，它不改变余数，可以在中途插入，相当于互换先后手',
        'elif stone % 3 == 1': '`{stone} % 3 = {stone % 3}`：{"余 1，归 one" if stone % 3 == 1 else "余 2，归 two"}',
        'one += 1': '`one` → =={one}==',
        'two += 1': '`two` → =={two}==',
        'ma, mi = one, two': '余 1 和余 2 地位等价，只关心个数：先令 `ma = {ma}`，`mi = {mi}`',
        'if ma < mi': '`ma < mi`？`{ma} < {mi}` → {"成立，交换使 ma 为较多的一类" if ma < mi else "不成立，ma 已是较多的一类"}',
        'ma, mi = mi, ma': '交换：`ma = {ma}`，`mi = {mi}`',
        'if mi == 0': '`mi == 0`？`{mi} == 0` → {"成立：Alice 只能取一次 ma，之后只剩 zero 可插" if mi == 0 else "不成立：1、2 都有，Alice 有两种开局"}',
        'return ma > 2': 'ma ≤ 2 时能全部取完 → Alice 输；ma > 2 时看 zero 的奇偶 → =={ret}==',
        'if zero % 2 == 0': '`zero = {zero}` 是{"偶数" if zero % 2 == 0 else "奇数"}：{"Alice 先取 mi 那类，序列长度为奇数，Alice 必胜" if zero % 2 == 0 else "两种开局都被 zero 打乱，要看 ma 比 mi 多多少"}',
        'return True': 'zero 为偶数 → Alice 必胜 → ==返回 True==',
        'return ma - mi': '`ma − mi = {ma - mi}`：只有 `> 2` 时 Alice 才赢 → =={ret}==',
    },
    cards=dict(
        one_liner='模 3 分类：0 当作换手，1 和 2 等价，只看 ma 和 mi',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['Alice 先手轮流取石子；取完后已取之和被 3 整除的人输，全取完 Bob 赢',
                 '双方最优，Alice 赢返回 `true`',
                 '示例：`[5,1,2,4,3]` → `false`'],
        quote='余0这一类不能一来就出，但是可以在中途任意时候出，相当于转换了先手和后手。对于余1和余2这两类，余1和余2可以认为是完全等价的，那么在这里就只需要关心这两种石子的堆数。',
        quote_src='—— yiduobo 题解原文',
        idea=['记 `zero` 为余 0 的个数，余 1/2 中较多的叫 `ma`，较少的叫 `mi`',
              '`mi == 0`：Alice 只能取一次 ma，只有 `ma > 2` 且 `zero` 为奇数才赢',
              '`mi > 0`：取 mi 开局序列长度为奇数 → `zero` 偶数就赢；`zero` 奇数则取 ma 开局，需 `ma − mi > 2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文代码在 Python 3 下无需改动',
                 '先看 `mi == 0`，再看 `zero` 的奇偶，最后才比较 `ma − mi`，顺序不能乱',
                 '对比灵神：灵神把三个分支合并成两条判断，结果与这里一致'],
    ),
)
