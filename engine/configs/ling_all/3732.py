CONFIG = dict(
    num=3732, title='一次替换后的三元素最大乘积', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='取绝对值前二大',
    tags=['贪心与思维', '乘积贪心', '难度分 1529'],
    code='''
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        mx = mx2 = 0
        for x in nums:
            x = abs(x)
            if x > mx:
                mx2 = mx  # 原来的最大变成次大
                mx = x  # x 是新的最大
            elif x > mx2:
                mx2 = x  # 最大不变，x 是新的次大
        return mx * mx2 * 10 ** 5
''',
    call='Solution().maxProduct([-5, 7, 0, 3, -9, 2])',
    expect=6300000,
    views=[
        dict(type='text', fn=lambda S: f"绝对值前二大：==最大 {S['mx']}==，==次大 {S['mx2']}==；第三个数替换成 `±10^5`，凑成正积" if 'mx' in S else '替换的那个数可以取到 ±10^5，所以只需挑出另外两个数', h=90),
        dict(type='array', var='nums', h=260, label='nums（绿 = 当前绝对值最大，青 = 次大）',
             color=lambda S, i, v: ('green' if 'mx' in S and abs(v) == S['mx'] and S['mx'] > 0 else
                                    'cyan' if 'mx2' in S and abs(v) == S['mx2'] and S['mx2'] > 0 else None)),
    ],
    watch=[('x', 'x', 'yellow'), ('mx', 'mx', 'green'), ('mx2', 'mx2', 'cyan')],
    captions={
        'mx = mx2 = 0': '绝对值最大、次大都从 `0` 开始',
        'for x in nums': '取下一个数',
        'x = abs(x)': '只看绝对值：`|x| = {x}`（符号靠第三个数 ±10^5 来凑）',
        'elif x > mx2': '`x > mx2`（{x} > {mx2}）→ {"成立" if x > mx2 else "不成立"}：不是最大，但比次大大才是新的次大',
        'if x > mx': '`x > mx`（{x} > {mx}）→ {"成立" if x > mx else "不成立"}：比最大还大才是新的最大',
        'mx2 = mx': '`mx2 = {mx2}`：原来的最大退为次大',
        'mx = x': '`mx = {mx}`：x 是新的最大',
        'mx2 = x': '`mx2 = {mx2}`：最大不变，x 是新的次大',
        'return': lambda S, B, ret: f'`{S.mx} × {S.mx2} × 10^5` = =={ret}==',
    },
    cards=dict(
        one_liner='挑绝对值最大的两个数，第三个数替换成 ±10^5 凑正',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` 中恰好一个元素替换成 `[-10^5, 10^5]` 内任意整数',
                 '然后选三个不同下标的数，求最大乘积',
                 '示例：`[-5,7,0]` → `3500000`；本视频：`[-5,7,0,3,-9,2]` → `6300000`'],
        quote='计算绝对值前二大元素。如果这两个元素取绝对值之前的乘积是负数，那么把第三个数变成 -10^5。否则，把第三个数变成 10^5。',
        quote_src='—— 灵茶山艾府题解',
        idea=['替换值范围最大就是 `10^5`，不会比任何原数小，所以最优一定用上它',
              '另外两个数乘积为负就替换成 `-10^5`，否则 `10^5`，乘积都是正的',
              '因此只要让这两个数的==绝对值乘积最大==，即取绝对值前二大'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先 `abs` 再比较；符号由替换的第三个数处理，不用管',
                 '`mx` 和 `mx2` 初始为 0：数组长度至少 3，答案正确',
                 '先把 `mx` 传给 `mx2`，再更新 `mx`，顺序不能反'],
    ),
)
