CONFIG = dict(
    num=3947, title='购买最多物品数目 II', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='买一送一候选 · 价格排序',
    tags=['灵神题单', '难度分 2215'],
    code='''
class Solution(object):
    def maximumSaleItems(self, items, budget):
        
        freq = {}
        mi_p = None
        ma_f = 0
        for f, p in items:
            freq[f] = freq.get(f, 0) + 1
            if mi_p is None or mi_p > p:
                mi_p = p
            ma_f = max(ma_f, f)
        
        cnt = {}
        for f in range(1, ma_f + 1):
            cnt[f] = 0
            for x in range(f, ma_f + 1, f):
                cnt[f] += freq.get(x, 0)

        candidates = []
        for f, p in items:
            if p < mi_p * 2 and cnt[f] > 1:
                candidates.append((p, cnt[f] - 1))

        candidates.sort()
        res = 0
        for p, c in candidates:
            if budget >= p * c:
                budget -= p * c
                res += c * 2
            else:
                res += budget // p * 2
                budget %= p
        
        return res + budget // mi_p
''',
    call='Solution().maximumSaleItems([[1,6],[2,4],[3,5]], 19)',
    expect=5,
    views=[
        dict(type='map', var='freq', fmt=lambda k, v: f'{k}: {v}', h=130),
        dict(type='map', var='cnt', fmt=lambda k, v: f'{k}: {v}', h=130),
        dict(type='array', var='candidates', label='candidates = (价格, 买一送一次数)', cell=120, h=160),
        dict(type='text', fn=lambda S: (f"最便宜 `mi_p = {S['mi_p']}`；价格 `< {S['mi_p']*2}` 才值得买一送一" if S.get('mi_p') is not None else ''), size=28, h=70),
    ],
    watch=[('mi_p', 'mi_p', 'cyan'), 'budget', ('res', 'res', 'green')],
    captions={
        'freq[f] = freq.get': '`factor = {f}` 的物品有 `{freq[f]}` 个',
        'mi_p = p': '更便宜的价格出现了：`mi_p = {mi_p}`',
        'ma_f = max': '最大的 factor：`ma_f = {ma_f}`',
        'cnt[f] = 0': '统计 factor 是 `{f}` 的倍数的物品总数 `cnt[{f}]`',
        'cnt[f] += freq.get': '倍数 `x = {x}` 有 `{freq.get(x, 0)}` 个 → `cnt[{f}]` = =={cnt[f]}=='.replace('{x}', '{x}'),
        'if p < mi_p * 2': lambda S, B, r: (f'`p = {S.p} < 2×{S.mi_p}` 且 `cnt[{S.f}] = {S.cnt[S.f]} > 1` → 有买一送一的价值' if S.p < S.mi_p * 2 and S.cnt[S.f] > 1
                                            else f'`p = {S.p}`，`cnt[{S.f}] = {S.cnt[S.f]}`：不满足（太贵或没有可送的）→ 不要'),
        'candidates.append': '加入候选：价格 `{p}`，买一送一 `{cnt[f] - 1}` 次（倍数里去掉自己）',
        'candidates.sort()': '按价格从小到大排：==先买最便宜的买一送一==',
        'for p, c in candidates': '候选 `价格 {p}`，最多 `{c}` 次买一送一',
        'if budget >= p * c': lambda S, B, r: (f'`budget = {S.budget} >= {S.p}×{S.c}` → 名额买得完' if S.budget >= S.p * S.c
                                                else f'`budget = {S.budget} < {S.p}×{S.c}` → 只能买 `{S.budget} // {S.p}` 次'),
        'budget -= p * c': '花掉 `{p}×{c}`，`budget` → =={budget}==',
        'res += c * 2': '每次买一送一得 2 个：`res` → =={res}==',
        'res += budget // p * 2': '买不满：`res` += `({B.budget} // {p})×2` → =={res}==',
        'budget %= p': '余下的钱 `budget` → {budget}',
        'return res': '剩余的钱全买最便宜的：`{res} + {budget} // {mi_p}` = =={ret}==',
    },
    cards=dict(
        one_liner='买一送一只买便宜的，剩下的钱全买最便宜的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每种物品无限买，总花费不超过 `budget`',
                 '买物品 `i` 最多送一个 `factor` 是 `factor_i` 倍数的其他物品',
                 '示例：`items=[[1,6],[2,4],[3,5]], budget=19` → `5`'],
        quote='对于买一送一的部分，其花费必须小于mi_p * 2才有购买的价值，否则的话购买两份最便宜的mi_p显然是更优的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt[f]` = factor 是 `f` 的倍数的物品数；某物品前 `cnt[f]-1` 次购买享受买一送一',
              '超出名额的购买，都应该买最便宜的 `mi_p`',
              '候选 `(价格, 次数)` 按价格排序，依次买；钱不够就有多少买多少'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`cnt[f] > 1` 才有名额：要减去物品自己',
                 '钱不足时：`budget // p * 2` 再 `budget %= p`',
                 '原文本身可直接在 Python 3 运行，没有改动',
                 '对比灵神：灵神把同价格名额合并；yiduobo 直接排序候选列表'],
    ),
)
