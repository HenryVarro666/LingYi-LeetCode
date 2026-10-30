CONFIG = dict(
    num=3946, title='购买最多物品数目 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='01 背包 + 最便宜物品正序补买',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1728'],
    code='''
class Solution(object):
    def maximumSaleItems(self, items, budget):
        
        f = [0] * (budget + 1)
        mi_p = None
        for i in range(len(items)):
            cnt = 1
            for j in range(len(items)):
                if i != j and items[j][0] % items[i][0] == 0:
                    cnt += 1

            for v in range(budget, items[i][1] - 1, -1):
                f[v] = max(f[v - items[i][1]] + cnt, f[v])

            if mi_p is None or mi_p > items[i][1]:
                mi_p = items[i][1]

        for v in range(mi_p, budget + 1):
            f[v] = max(f[v - mi_p] + 1, f[v])
        
        return f[-1]
''',
    call='Solution().maximumSaleItems([[6,2],[2,6],[3,4]], 9)',
    expect=4,
    skip=['for j in range(len(items))'],
    views=[
        dict(type='table', var='items', label='items[i] = [factor, price] 即列 f、p（蓝 = 当前物品 i，黄 = 它的倍数）', h=190, cell=130,
             cols=['f', 'p'], rows=lambda S: [f'i={k}' for k in range(len(S['items']))],
             color=lambda S, r, c, v: ('blue' if r == S.get('i') else ('yellow' if S.get('i') is not None and S.get('j') is not None and r == S['j'] and S['_line'] == 9 else None))),
        dict(type='text', h=56, size=26, fn=lambda S: (
            f"物品 `{S['i']}`：买一件拿到 `cnt = {S['cnt']}` 件，花 `{S['items'][S['i']][1]}`" if S.get('i') is not None and S.get('_line', 0) >= 12 and S.get('_line', 0) < 20
            else (f"物品 `{S['i']}`：数它的倍数，当前 `cnt = {S['cnt']}`" if S.get('i') is not None and S.get('cnt') is not None else ''))),
        dict(type='array', var='f', label='f[v]：花费不超过 v 时能得到的最多物品数', h=210, cell=70,
             pointers={'v': 'pink'},
             color=lambda S, i, x: 'green' if S.get('_line') == 13 and i == S.get('v') else None),
    ],
    max_steps=68,
    watch=[('i', 'i', 'blue'), ('cnt', 'cnt', 'yellow'), ('mi_p', 'mi_p', 'cyan'), ('v', 'v', 'pink')],
    captions={
        'f[v] = max(f[v - mi_p]': lambda S, B, r: f'再买一件最便宜的：`f[{S.v} - {S.mi_p}] + 1` = {B.f[S.v - S.mi_p] + 1}，对比原来 `f[{S.v}]` = {B.f[S.v]} → =={S.f[S.v]}==',
        'f = [0] * (budget': '`f[v]` = 花费不超过 `v` 时最多能得到多少件，初始全 0',
        'mi_p = None': '`mi_p` 记最便宜的价格，后面补买它',
        'for i in range(len(items))': '第 `{i}` 个物品：先数买它能免费带来几件',
        'cnt = 1': '买下的这件自己算 1 件，`cnt = 1`',
        'if i != j': lambda S, B, r: (f'物品 `{S.j}` 的 factor `{S['items'][S.j][0]}` 能被 `{S['items'][S.i][0]}` 整除 → ==免费送一件==，`cnt = {S.cnt}`' if B.cnt != S.cnt else ('就是自己，不送' if S.i == S.j else f'`{S[chr(105)+chr(116)+chr(101)+chr(109)+chr(115)][S.j][0]}` 不能被 `{S[chr(105)+chr(116)+chr(101)+chr(109)+chr(115)][S.i][0]}` 整除，不送')),
        'f[v] = max(': lambda S, B, r: f'买它：`f[{S.v} - {S['items'][S.i][1]}] + {S.cnt}` = {B.f[S.v - S['items'][S.i][1]] + S.cnt}，不买：`f[{S.v}]` = {B.f[S.v]} → 取大 = =={S.f[S.v]}==（v 倒序，保证每个物品只买一次）',
        'mi_p is None': '更新最便宜价格：`mi_p = {mi_p}`',
        'for v in range(mi_p': lambda S, B, r: ('01 背包做完。重复买没有赠品，每件只算 1 → 只补买最便宜的，这次 ==v 正序==（允许重复）' if S.v == S.mi_p else ('补买阶段结束' if S.v == B.v else f'==v 正序==走到 `{S.v}`（正序 = 允许重复买最便宜的）')),
        'return f[-1]': '`f[budget]` 就是预算内最多的物品数 = =={ret}==',
    },
    cards=dict(
        one_liner='先 01 背包带赠品，再正序补买最便宜的',
        complexity='时间 `O(n^2 + n·budget)`，空间 `O(budget)`',
        problem=['`items[i] = [factor, price]`，每种物品无限供应，总花费不超过 `budget`',
                 '买了 `i`，所有 `factor` 被 `factor_i` 整除的物品各送一份；重复买 `i` 不再送',
                 '求最多拿到多少件。示例：`[[6,2],[2,6],[3,4]]`，`budget = 9` → `4`'],
        quote='多次购买同一个物品并不能多次获取赠品，因此冲着赠品去的购物对每种物品只会执行最多一次。……是一个非常经典的01背包问题',
        quote_src='—— yiduobo 题解',
        idea=['买一次物品 `i`：花 `price`，得 `cnt`（自己 + 倍数物品）件 → 01 背包，`v` 倒序',
              '没有赠品的购物只选最便宜的，可买多次 → 在背包基础上 `v` ==正序== 再扫一遍',
              '两遍扫完，`f[-1]` 就是答案'],
        summary=['时间 `O(n^2 + n·budget)`：数倍数 `O(n^2)`，背包 `O(n·budget)`；空间 `O(budget)`',
                 '易错：赠品背包 ==倒序==（只买一次），补买最便宜 ==正序==（可买多次）',
                 '`cnt` 初值是 1（自己），倍数要排除 `i == j`',
                 '本题代码已是 Python 3 写法，无需改动'],
    ),
)
