CONFIG = dict(
    num=3745, title='三元素表达式的最大值', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='一趟遍历 · 最大/次大/最小',
    tags=['灵神题单', '从最小/最大开始贪心', '难度分 1218'],
    code='''
class Solution(object):
    def maximizeExpressionOfThree(self, nums):
        
        ma1, ma2, mi = None, None, None
        for v in nums:
            if ma1 is None or ma1 < v:
                ma1, ma2 = v, ma1
            elif ma2 is None or ma2 < v:
                ma2 = v
            
            if mi is None or mi > v:
                mi = v
        
        return ma1 + ma2 - mi
''',
    call='Solution().maximizeExpressionOfThree([3,-1,5,2,4])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 最大，青 = 次大，红 = 最小）', h=230,
             color=lambda S, i, v: ('green' if S['nums'][i] == S.get('ma1') else 'cyan' if S['nums'][i] == S.get('ma2') else 'red' if S['nums'][i] == S.get('mi') else None) if 'ma1' in S else None),
        dict(type='text', size=32, h=160,
             fn=lambda S: f"最大 ma1 = ==`{S.get('ma1')}`==，次大 ma2 = `{S.get('ma2')}`，最小 mi = `{S.get('mi')}`" if 'ma1' in S else ''),
    ],
    watch=[('v', 'v', 'blue'), ('ma1', 'ma1', 'green'), ('ma2', 'ma2', 'cyan'), ('mi', 'mi', 'red')],
    captions={
        'ma1, ma2, mi = None': '三个量都还没有：`ma1` 最大、`ma2` 次大、`mi` 最小',
        'for v in nums': lambda S, B, r: (f'扫描完毕，没有下一个数了' if S.v == B.get('v') else f'扫描下一个数 `v = {S.v}`'),
        'if ma1 is None or ma1 < v': lambda S, B, r: ('`ma1` 还是空，或者 `v` 比 `ma1` 更大 → `v` 当新的最大' if (S.ma1 is None or B.get('ma1') is None or B['ma1'] < S.v) else f'`v = {S.v}` 不比最大值 `{S.ma1}` 大，看看能不能当次大'),
        'ma1, ma2 = v, ma1': '新的最大值 `ma1 = {ma1}`，原来的最大值退为次大 `ma2 = {ma2}`',
        'elif ma2 is None': lambda S, B, r: (f'`ma2` 为空或 `ma2 = {S.ma2}` 比 `v = {S.v}` 小 → `v` 当次大' if (S.ma2 is None or S.ma2 < S.v) else f'`v = {S.v}` 不比次大 `{S.ma2}` 大 → 忽略'),
        'ma2 = v': '次大值更新：`ma2 = {ma2}`',
        'if mi is None or mi > v': lambda S, B, r: (f'`v = {S.v}` 比最小值更小（或还没有最小值）→ 更新' if (B.get('mi') is None or B['mi'] > S.v) else f'`v = {S.v}` 不小于最小值 `{S.mi}` → 不变'),
        'mi = v': '最小值更新：`mi = {mi}`',
        'return ma1': 'a + b − c = `{ma1} + {ma2} − ({mi})` = =={ret}==',
    },
    cards=dict(
        one_liner='一趟遍历同时记下最大、次大、最小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选下标互不相同的三个数 `a`、`b`、`c`，使 `a + b - c` 最大',
                 '返回最大值',
                 '本视频：`[3,-1,5,2,4]` → `10`'],
        quote='为了使得最终答案最大，就应该让a和b尽量大，让c尽量小，于是只需一趟遍历，找出nums中的最大值以及次大值作为a和b，找出最小值作为c。',
        quote_src='—— yiduobo 题解原文',
        idea=['a、b 取最大和次大，c 取最小',
              '遍历时维护 `ma1`、`ma2`、`mi`，不用排序',
              '新最大出现时，旧最大顺位成次大'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ma1, ma2 = v, ma1`：先让旧最大退位，再放新最大，顺序靠元组赋值保证',
                 '用 `None` 表示还没有值，所以每个判断都要先判 `is None`',
                 '对比灵神：灵神排序后直接取头尾；yiduobo 手动维护三个极值',
                 '原文为 Python 2 风格，无需改动即可运行'],
    ),
)
