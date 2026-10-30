CONFIG = dict(
    num=3946, title='购买最多物品数目 I', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='0-1 背包 + 最便宜物品重复买',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1728'],
    code='''
class Solution:
    def maximumSaleItems(self, items: list[list[int]], budget: int) -> int:
        max_factor = max(p[0] for p in items)
        cnt_factor = [0] * (max_factor + 1)
        for factor, _ in items:
            cnt_factor[factor] += 1

        cnt_multi = [0] * (max_factor + 1)
        f = [0] * (budget + 1)
        min_price = inf
        sum_price = 0

        for factor, price in items:
            min_price = min(min_price, price)

            if cnt_multi[factor] == 0:  # 之前没有计算过
                for j in range(factor, max_factor + 1, factor):
                    cnt_multi[factor] += cnt_factor[j]
            cnt = cnt_multi[factor]

            # 视作一个体积为 price，价值为 cnt 的物品
            # 优化：已遍历的物品的体积和至多为 sum_price，大于这个值的体积和无法凑出来
            sum_price = min(sum_price + price, budget)
            for j in range(sum_price, price - 1, -1):
                v = f[j - price] + cnt
                if v > f[j]: f[j] = v  # 手写 max 更快

        return max(fi + (budget - i) // min_price for i, fi in enumerate(f))
''',
    call='Solution().maximumSaleItems([[2,3],[3,2],[6,3]], 5)',
    expect=4,
    skip=['max_factor = max', 'for factor, _ in items', 'cnt_factor[factor] += 1', 'for j in range(factor', 'cnt_multi[factor] += cnt_factor[j]'],
    views=[
        dict(type='array', var='cnt_factor', label='cnt_factor[x]：factor 恰为 x 的物品个数', h=175, cell=52,
             pointers={'factor': 'blue'}),
        dict(type='array', var='cnt_multi', label='cnt_multi[x]：factor 是 x 的倍数的物品个数（首次买 x 得到的件数）', h=175, cell=52,
             pointers={'factor': 'blue'}),
        dict(type='text', h=56, size=26, fn=lambda S: (
            (f"物品 `(factor={S['factor']}, price={S['price']})` → 体积 `{S['price']}`，价值 `cnt={S['cnt']}`；最便宜 `min_price={S['min_price']}`"
            if S.get('_line', 0) >= 19 else f"物品 `(factor={S['factor']}, price={S['price']})`；最便宜 `min_price={S['min_price']}`") if 'price' in S else '')),
        dict(type='array', var='f', label='f[j]：花费至多为 j 时，最多获得的物品数', h=190, cell=70,
             pointers={'j': 'pink'},
             color=lambda S, i, v: 'green' if S.get('_line') == 26 and i == S.get('j') else
                                   ('yellow' if S.get('j') is not None and i == S['j'] - S.get('price', 0) and S.get('_line') == 25 else None)),
    ],
    max_steps=80,
    watch=[('min_price', 'min_price', 'cyan'), ('sum_price', 'sum_price', 'orange'), ('cnt', 'cnt', 'blue'), ('j', 'j', 'pink')],
    captions={
        'cnt_multi = [0]': '`cnt_multi[x]` 记录「首次买 factor=x 的物品」能带来多少件（含自己）',
        'f = [0] * (budget': '`f[j]` 表示花费至多 `j` 时的最多物品数，初始全 0',
        'min_price = inf': '再买同一件拿不到赠品，所以多买只会买==最便宜==的；先记 `min_price`',
        'min_price = min': '`min_price = min({B.min_price}, {price}) = {min_price}`',
        'if cnt_multi[factor] == 0': '这个 `factor` 的倍数个数算过吗？`cnt_multi[{factor}] = {cnt_multi[factor]}` → ' + '{"没算过，往下枚举倍数" if cnt_multi[factor] == 0 else "算过，直接用"}',
        'cnt = cnt_multi[factor]': '数完 `factor` 的倍数：首次买它得到 `cnt = {cnt}` 件（自己 + 免费的倍数）',
        'sum_price = min': '前面物品的体积和最多 `{sum_price}`，更大的 `j` 凑不出来，`j` 从 `{sum_price}` 开始就够',
        'v = f[j - price] + cnt': '买它：`f[{j} - {price}] + {cnt}` = =={v}==',
        'if v > f[j]': lambda S, B, r: (f'`v = {S.v}` > 原来的 `f[{S.j}] = {B.f[S.j]}` → ==买更划算==，更新为 {S.v}' if S.v > B.f[S.j] else f'`v = {S.v}` ≤ 原来的 `f[{S.j}] = {B.f[S.j]}` → 不买更好，保持不变'),
        'return max': '枚举 `i` 作为背包部分花费，剩下的 `budget - i` 全买最便宜的：`f[i] + (budget - i) // {min_price}` 取最大 = =={ret}==',
    },
    cards=dict(
        one_liner='先 0-1 背包买一遍拿赠品，剩下的钱全买最便宜的',
        complexity='时间 `O(n·budget + U log U)`，空间 `O(budget + U)`',
        problem=['`items[i] = [factor, price]`，每种物品无限供应，总花费不超过 `budget`',
                 '买了物品 `i`，所有 `factor_j` 是 `factor_i` 倍数的 `j` 各免费送一份；重复买 `i` 不再送',
                 '求买到 + 送到的物品最大总数。示例：`[[2,4],[3,2],[4,1],[6,4],[12,4]]`，`X'],
        quote='重复购买物品时，无法免费获取物品，所以贪心地，==重复购买最便宜的物品==，设其价格为 minPrice。',
        quote_src='—— 灵茶山艾府题解',
        idea=['首次买物品 `i` 能得到 `cnt_i` 件（含自己），这是一个体积 `price`、价值 `cnt` 的 ==0-1 背包==',
              '再买就没有赠品了，每件只算 1，所以剩余预算全买最便宜的',
              '枚举背包花费 `i`：答案 `max(f[i] + (budget - i) // min_price)`'],
        after=[dict(heading='优化前的写法', lines=['`cnt` 用 `O(n^2)` 暴力数倍数', '优化：枚举 `x` 的倍数累加，调和级数 `O(U log U)`；背包上界用 `sum_price` 截断'])],
        summary=['时间 `O(n·budget + U log U)`，`U = max(factor)`，空间 `O(budget + U)`',
                 '易错：物品只能「首次买」有赠品，所以背包是 ==0-1 背包==，`j` 必须倒序',
                 '最后一步枚举的 `f[i]` 即使没含最便宜物品也不会算少：多买一件的 `f` 更大',
                 '同类题：416. 分割等和子集、0-1 背包模板'],
    ),
)
