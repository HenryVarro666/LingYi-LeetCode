CONFIG = dict(
    num=1954, title='收集足够苹果的最小花园周长', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='推公式 + 二分', tags=['难度分 1759'],
    code='''
class Solution(object):
    def minimumPerimeter(self, neededApples):
        
        l = 1
        r = neededApples

        while l < r:
            mid = (l + r) >> 1
            if 2 * mid * (mid + 1) * (2 * mid + 1) < neededApples:
                l = mid + 1
            else:
                r = mid
        
        return l * 8
''',
    call='Solution().minimumPerimeter(13)',
    expect=16,
    views=[
        dict(type='array', var=lambda S: list(range(0, S['neededApples'] + 1)), h=240, label='半边长 l 的候选范围（下标 = l 的值）',
             window=('l', 'r'),
             pointers={'l': 'blue', 'r': 'pink', 'mid': 'yellow'}, cell=64),
        dict(type='text', size=34, fn=lambda S: (f"`l = mid = {S['mid']}`：苹果数 `2l(l+1)(2l+1)` = =={2*S['mid']*(S['mid']+1)*(2*S['mid']+1)}==，需要 `{S['neededApples']}`" if 'mid' in S else f"边框上有 `12l^2` 个苹果，正方形里共 `2l(l+1)(2l+1)` 个")),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'mid', ('neededApples', 'neededApples', 'green')],
    captions={
        'l = 1': '`l` 是半边长（边长 `2l`），最小取 1',
        'r = neededApples': '`r = {r}`：半边长不会超过需求数，作为二分上界',
        'while l < r': '区间 `[{l}, {r}]`：=={"还没收缩到一点，继续二分" if l < r else "l == r，答案找到"}==',
        'mid = ': '取中点 `mid = ({l} + {r}) >> 1 = {mid}`',
        'if 2 * mid': '`2·{mid}·{mid+1}·{2*mid+1} = {2*mid*(mid+1)*(2*mid+1)}`，和 `{neededApples}` 比：=={"不够，答案在右边" if 2*mid*(mid+1)*(2*mid+1) < neededApples else "够了，mid 可能是答案，往左找更小的"}==',
        'l = mid + 1': 'mid 不够 → `l = mid + 1 = {l}`',
        'r = mid': 'mid 够了 → `r = mid = {r}`（mid 本身保留）',
        'return l * 8': '最小半边长 `l = {l}`，周长 `8l = {ret}`',
    },
    cards=dict(
        one_liner='一圈一圈数苹果，推出公式后二分半边长',
        complexity='时间 `O(log neededApples)`，空间 `O(1)`',
        problem=['坐标 `(i, j)` 处的树有 `|i| + |j|` 个苹果',
                 '买下以原点为中心的正方形，求至少 `neededApples` 个苹果的最小周长',
                 '示例：`13` → `16`'],
        quote='单个边框上的苹果数是12 * l^2，那么边长为2l的正方形里面一共就有 2 * l * (l + 1) * (2l + 1)。',
        quote_src='—— yiduobo 题解原文',
        idea=['把边长 `2l` 的正方形一圈一圈拎出来：每圈上边有 `(3l+2)·l` 个苹果',
              '四条边减去重复计数的四个角：整圈 `12l^2`',
              '平方和公式累加得总数 `2l(l+1)(2l+1)`，随 l 单调增 → 二分 l'],
        summary=['时间 `O(log neededApples)`，空间 `O(1)`',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '易错：二分的是半边长 `l`，周长是 `8l`',
                 '对比灵神：灵神用开立方一步定位，yiduobo 用二分，不依赖浮点'],
    ),
)
