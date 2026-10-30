def _g(S):
    if 'y' in S and 'x' in S and S['_line'] is not None:
        return f"求 gcd：`x = {S['x']}`，`y = {S['y']}`" + ('，y 为 0 → ==gcd 就是 x==' if S['y'] == 0 else '')
    if 'res' in S:
        return f"目前所有种类张数的最大公约数 `res = {S['res']}`"
    return '每种牌的张数都要是 X 的倍数 → X 必须整除每个张数'


CONFIG = dict(
    num=914, title='卡牌分组', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='张数的最大公约数',
    tags=['灵神题单', '数学算法'],
    code='''
class Solution(object):
    def hasGroupsSizeX(self, deck):

        if len(deck) == 1:
            return False

        cnt_dict = {}
        for num in deck:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        if len(cnt_dict) == 1:
            return True

        cnt_list = list(cnt_dict.values())
        res = self.gcd(cnt_list[0], cnt_list[1])
        if res == 1:
            return False
        for cnt in cnt_list[2:]:
            res = self.gcd(res, cnt)
            if res == 1:
                return False
        
        return True
    
    def gcd(self, x, y):
        while y:
            x, y = y, x % y
        
        return x
''',
    call='Solution().hasGroupsSizeX([1,1,2,2,2,2,3,3])',
    expect=True,
    views=[
        dict(type='array', var='deck', h=170, label='deck'),
        dict(type='map', var='cnt_dict', h=170, fmt=lambda k, v: f'{k}: {v} 张'),
        dict(type='text', fn=_g, h=110),
    ],
    watch=['x', 'y', 'res', 'cnt_list'],
    captions={
        'len(deck) == 1': '`len(deck) = {len(deck)}`：' + '只有 1 张牌凑不出每组 ≥ 2 张 → 直接 False' + '（这里不成立，继续）',
        'cnt_dict[num] = ': '统计每种牌的张数：`{num}` 现在有 `{cnt_dict[num]}` 张',
        'len(cnt_dict) == 1': '牌有 `{len(cnt_dict)}` 种：只有一种时全放一组即可 → True；这里不止一种，继续求公约数',
        'cnt_list = ': '取出各种牌的张数：`{cnt_list}`。每个张数都必须是 X 的倍数',
        'res = self.gcd(cnt_list[0]': '先求前两个张数的最大公约数：`gcd({cnt_list[0]}, {cnt_list[1]}) = {res}`',
        'res = self.gcd(res, cnt)': '再把下一种牌的张数 `{cnt}` 并进来：`gcd({B.res}, {cnt}) = {res}`',
        'if res == 1': lambda S, B, r: ('公约数 `1`：没有 ≥ 2 的 X 能整除所有张数 → ==不行==' if S.res == 1 else f'公约数 `{S.res}` ≥ 2，还没被否决，继续检查后面的张数'),
        'while y': '`y = {y}`：y 不为 0 就继续辗转相除（为 0 则 x 就是 gcd）',
        'x, y = y, x % y': '辗转相除：`(x, y)` → `({x}, {y})`，即 `gcd(x, y) = gcd(y, x % y)`',
        'return x': 'y 已为 0，最大公约数 = `{x}`',
        'return True': '所有张数的最大公约数 `{res}` ≥ 2 → ==可以分组==',
    },
    cards=dict(
        one_liner='每种牌的张数都得是 X 的倍数 → 求张数的最大公约数',
        complexity='时间 `O(n + k·log C)`，空间 `O(k)`（k 为牌的种类数）',
        problem=['一副牌，每张写有一个整数。选一个 `X ≥ 2`，把牌分成若干组',
                 '每组恰好 `X` 张，且组内牌上的数字都相同。能做到则返回 `True`',
                 '示例：`[1,1,2,2,2,2,3,3]` → `True`（每组 2 张）'],
        quote='某种卡牌有k张，只有当k是x的倍数时才能进行分组。……问题要求的实际上就是每种卡牌数的最大公约数。',
        quote_src='—— yiduobo 题解原文',
        idea=['每种牌各自分组，所以它的张数 `k` 必须是 `X` 的倍数',
              '`X` 要同时整除所有张数 → 它是所有张数的==公约数==',
              '只要最大公约数 ≥ 2 就行（取 `X` = 它），等于 1 则无解'],
        summary=['时间 `O(n + k·log C)`，空间 `O(k)`',
                 '易错：只有 1 张牌要先返回 `False`；只有一种牌（张数 ≥ 2）直接 `True`',
                 '提前剪枝：公约数一旦变成 1，后面不用再算',
                 '原文为 Python 2 写法，`cnt_dict.values()` 在 Python 3 里不能下标取值，已改为 `list(cnt_dict.values())`'],
    ),
)
