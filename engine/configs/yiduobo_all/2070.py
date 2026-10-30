def _txt(S):
    if 'q' not in S:
        return '物品按价格排序，询问也按大小排序（带上原下标）'
    rng = '还没有物品' if S['p'] == 0 else f'`sorted_items[0..{S["p"] - 1}]`'
    return f'询问阈值 `{S["q"]}`：已满足的物品 {rng}，最大美丽值 `now = {S["now"]}`'


CONFIG = dict(
    num=2070, title='每一个查询的最大美丽值', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='离线 · 排序后单调指针',
    tags=['题单·常用数据结构', '难度分 1724'],
    code='''
class Solution(object):
    def maximumBeauty(self, items, queries):

        sorted_items = sorted(items, key=lambda d:d[0])
        sorted_queries = sorted([[q, index] for index, q in enumerate(queries)])
        res = [0] * len(sorted_queries)
        p = 0
        now = 0
        for q, index in sorted_queries:
            while p < len(sorted_items) and sorted_items[p][0] <= q:
                now = max(now, sorted_items[p][1])
                p += 1
            
            res[index] = now
        
        return res
''',
    call='Solution().maximumBeauty([[1,2],[3,2],[2,4],[5,6],[3,5]], [3,1,5,2])',
    expect=[5, 2, 6, 4],
    views=[
        dict(type='array', var='sorted_items', label='sorted_items（按价格；绿 = 已满足过的物品 [价格, 美丽值]）',
             pointers={'p': 'blue'}, cell=110, h=200,
             color=lambda S, i, v: 'green' if i < S.get('p', 0) else None),
        dict(type='array', var='sorted_queries', label='sorted_queries（[询问值, 原下标]，从小到大）',
             cell=110, h=170,
             color=lambda S, i, v: 'orange' if v[1] == S.get('index') and 'q' in S else None),
        dict(type='array', var='res', label='res（按原下标放答案）', cell=90, h=165,
             color=lambda S, i, v: 'green' if i == S.get('index') and S.get('_line', 0) >= 14 else None),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('q', 'q', 'orange'), ('index', 'index', 'pink'), ('p', 'p', 'blue'), ('now', 'now', 'green')],
    captions={
        'sorted_items = sorted': '物品按价格从小到大排序：`{sorted_items}`',
        'sorted_queries = sorted': '询问连同原下标一起排序：`{sorted_queries}`，阈值只会越来越大',
        'res = [0]': '`res` 按原下标存答案，先全是 0',
        'p = 0': '`p`：已经满足条件的物品个数（下一个待检查的物品）',
        'now = 0': '`now`：满足当前询问的物品里的最大美丽值',
        'for q, index in sorted_queries': lambda S, B, r: (
            f'取阈值 `q = {S.q}`（原下标 `{S.index}`）' if 'q' not in B or S.q != B.q or S.index != B.index
            else '所有询问处理完了'),
        'while p < len': lambda S, B, r: (
            f'`sorted_items[{S.p}]` 价格 {S.sorted_items[S.p][0]} ≤ {S.q}：新满足的物品 → 纳入' if S.p < len(S.sorted_items) and S.sorted_items[S.p][0] <= S.q
            else ('物品都用完了' if S.p >= len(S.sorted_items)
                  else f'`sorted_items[{S.p}]` 价格 {S.sorted_items[S.p][0]} > {S.q}：阈值递增，后面也不满足 → 停')),
        'now = max': '`now = max({B.now}, {sorted_items[p][1]})` = =={now}==，用上一个询问的结果接着更新',
        'p += 1': '`p` 后移 → `{p}`，均摊 `O(1)`，不会回退',
        'res[index] = now': '阈值 {q} 的答案 =={now}==，放到 `res[{index}]`',
        'return res': '`res = {res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='区间最值？排序之后就是单调指针',
        complexity='时间 `O(n log n + m log m)`，空间 `O(m)`',
        problem=['物品 `[价格, 美丽值]`，每次询问 `q`：价格 `≤ q` 的物品里最大美丽值，没有则为 `0`',
                 '示例：`items=[[1,2],[3,2],[2,4],[5,6],[3,5]]`，`queries=[1,2,3,4,5,6]` → `[2,4,5,5,6,6]`',
                 '本视频：`queries = [3,1,5,2]` → `[5,2,6,4]`'],
        quote='题目乍一看是一个典型的区间最值问题，但是如果采用离线做法的话，就可以排序后利用单调性来解决了。',
        quote_src='—— yiduobo 题解原文',
        idea=['物品按价格排序，询问也排序，并带上原下标好把答案放回去',
              '用 `p` 记录能满足当前询问的物品个数：阈值变大，`p` 只增不减',
              '上一个询问的结果 `now` 接着用，只拿新纳入的物品去更新'],
        summary=['时间 `O(n log n + m log m)`，空间 `O(m)`',
                 '易错：`sorted_queries` 要带原下标，`res[index]` 才能对上',
                 '没有物品满足时 `now` 还是 0，正好是题目要求的答案',
                 '原文为 Python 2 风格，本题代码无需改动，直接可运行',
                 '对比灵神：同样离线双指针，灵神排的是下标数组，另给了二分写法'],
    ),
)
