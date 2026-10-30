CONFIG = dict(
    num=2813, title='子序列最大优雅度', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='先保品类，再逐个替换末尾',
    tags=['堆（优先队列）', '反悔贪心', '难度分 2640'],
    code='''
class Solution(object):
    def findMaximumElegance(self, items, k):

        vis = set()
        vis_cate = set()
        choose = []
        now = 0
        items.sort(reverse=True)
        for index, (p, c) in enumerate(items):
            if c not in vis_cate:
                vis_cate.add(c)
                choose.append(p)
                vis.add(index)
                if len(choose) == k:
                    break
        
        now = sum(choose) + len(vis_cate) ** 2

        k -= len(vis_cate)
        res = now
        for index, (p, c) in enumerate(items):
            if index not in vis:
                if k > 0:
                    now += p
                    k -= 1
                else:
                    if choose[-1] >= p:
                        break
                    now -= len(choose) * 2 - 1
                    now -= choose.pop()
                    now += p
                
                res = max(res, now)
        
        return res
''',
    call='Solution().findMaximumElegance([[2,3],[10,1],[3,2],[9,1],[8,1]], 3)',
    expect=28,
    views=[
        dict(type='text', fn=lambda S: (f"当前优雅度 `now=`==`{S['now']}`==；最优 `res=`==`{S['res']}`==" if 'res' in S else (f"品类阶段：已选 `{len(S['choose'])}` 个不同品类，总利润 `{sum(S['choose'])}`" if 'choose' in S else '')), size=26),
        dict(type='array', var="[f'{p}/{c}' for p, c in items]", label='items（利润/品类，按利润从大到小）', h=210, cell=96,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if i in S.get('vis', ()) else None)),
        dict(type='array', var='choose', label='choose：品类阶段选出的利润（末尾最小）', h=200, cell=96),
        dict(type='set', var='vis_cate', label='vis_cate：已选品类', h=130),
    ],
    watch=[('index', 'index', 'blue'), ('k', 'k', 'pink'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'items.sort': '按利润从大到小排序：每个品类遇到的第一个就是该品类最大利润 → {items}',
        9: '品类阶段：看项目 `{index}`：利润 `{p}`，品类 `{c}`',
        15: '品类阶段结束：已选的利润都是各自品类里最大的',
        4: '`vis` 记已选项目的下标，`vis_cate` 记已选品类',
        6: '`choose` 记品类阶段选出的利润，末尾是最小的',
        'if c not in vis_cate': lambda S, B, r: (f'品类 `{S.c}` 还没选过 → 选这个品类里利润最大的 `{S.p}`' if S.c not in S.vis_cate else f'品类 `{S.c}` 已有更大利润的项目 → 跳过'),
        'choose.append': '`choose` 加入利润 `{p}`：{choose}',
        'vis.add(index)': '记下已选项目下标 `{index}`',
        'if len(choose) == k': lambda S, B, r: (f'选满 `k = {S.k}` 个不同品类 → 品类阶段结束' if len(S.choose) == S.k else f'才选了 `{len(S.choose)}` 个品类，不足 `k={S.k}`，继续'),
        'now = sum': '初始优雅度：`{sum(choose)} + {len(vis_cate)}² = {now}`',
        'k -= len(vis_cate)': '还差 `k = {k}` 个项目要补（品类不足时先补满，不替换）',
        'res = now': '`res` 先记下当前优雅度 =={res}==',
        21: '第二轮，按利润从大到小看项目 `{index}`：利润 `{p}`，品类 `{c}`',
        'if index not in vis': lambda S, B, r: (f'项目 `{S.index}` 没被选过 → 考虑它' if S.index not in S.vis else f'项目 `{S.index}` 已在品类阶段选过 → 跳过'),
        'if k > 0': lambda S, B, r: (f'还差 `{S.k}` 个没选满 → 直接补上' if S.k > 0 else '已选满 k 个 → 只能替换'),
        25: '直接补上：`now` + `{p}` → =={now}==',
        'k -= 1': '空位减一：`k` → {k}',
        'if choose[-1] >= p': lambda S, B, r: (f'`choose[-1] = {S.choose[-1]} ≥ p = {S.p}`：新项目不比被替换的大，后面更小 → 结束' if S.choose[-1] >= S.p else f'`choose[-1] = {S.choose[-1]} < p = {S.p}`：替换有赚'),
        28: '之后的利润更小，替换不会更优，直接结束',
        'now -= len(choose)': '被替换的是唯一品类，品类数减一：平方项减少 `2×{len(choose)}-1` = {len(choose)*2-1} → `now` = {now}',
        'now -= choose.pop()': '再去掉被替换项目的利润 `{B.choose[-1]}`：`now` = {now}',
        31: '加上新项目利润 `{p}`：`now` = =={now}==',
        'res = max(res, now)': '`res = max({B.res}, {now}) = {res}`',
        'return res': '最大优雅度 =={res}==',
    },
    cards=dict(
        one_liner='先把品类做到极致，再用高利润项目替换末尾',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`items[i] = [利润, 品类]`，选 `k` 个项目',
                 '优雅度 = ==利润之和 + 不同品类数的平方==，求最大值',
                 '本视频：`[[2,3],[10,1],[3,2],[9,1],[8,1]]`，`k=3` → `28`'],
        quote='既然有利润和品类两个属性，那么不妨先将其中之一做到极致，然后再看有没有修正的余地。我在这里选择的优先满足品类。',
        quote_src='—— yiduobo 题解原文',
        idea=['利润排序后一趟遍历，每个品类取最大利润的一个，凑出尽量多的不同品类（最多 `k` 个）',
              '品类不足 `k` 个：先把空位用最大的剩余项目补满',
              '再遍历剩余项目：用它替换 `choose[-1]`（最小的唯一品类）',
              '替换使品类数减一，所以 `now` 要减 `len(choose)*2-1`，再减被换出的利润，加上新利润'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：替换时品类数减一，平方项变化量是 `2L-1`（`L` 为替换前的品类数）',
                 '遇到 `choose[-1] >= p` 可直接 `break`，因为后面利润更小',
                 '对比灵神：灵神先选前 k 个再用栈反悔；yiduobo 先保品类再替换',
                 '原文为 Python 2 风格，本题代码无需修改'],
    ),
)
