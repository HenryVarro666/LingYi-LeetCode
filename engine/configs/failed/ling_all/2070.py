def _items_color(S, i, v):
    j = S.get('j')
    if j is not None and i < j:
        return 'green'
    return None


def _txt(S):
    if 'q' not in S:
        return '先把 `items` 按价格排序；再把询问的==下标==按询问值排序'
    return (f'询问 `q = {S["q"]}`：价格 ≤ {S["q"]} 的物品已纳入前 `{S["j"]}` 个，'
            f'它们的最大美丽值 `max_beauty = {S["max_beauty"]}`')


CONFIG = dict(
    num=2070, title='每一个查询的最大美丽值', difficulty='Medium', category='二分算法',
    author='灵茶山艾府', technique='离线算法 · 排序 + 双指针',
    tags=['题单·常用数据结构', '难度分 1724'],
    code='''
class Solution:
    def maximumBeauty(self, items: List[List[int]], queries: List[int]) -> List[int]:
        items.sort(key=lambda item: item[0])
        idx = sorted(range(len(queries)), key=lambda i: queries[i])

        ans = [0] * len(queries)
        max_beauty = j = 0
        for i in idx:
            q = queries[i]
            # 增量地遍历满足 queries[i-1] < price <= queries[i] 的物品
            while j < len(items) and items[j][0] <= q:
                max_beauty = max(max_beauty, items[j][1])
                j += 1
            ans[i] = max_beauty
        return ans
''',
    call='Solution().maximumBeauty([[1,2],[3,2],[2,4],[5,6],[3,5]], [3,1,5,2])',
    expect=[5, 2, 6, 4],
    views=[
        dict(type='array', var='items', label='items（按价格排序，绿 = 已纳入的物品 [价格, 美丽值]）', pointers={'j': 'blue'},
             color=_items_color, cell=110, h=200),
        dict(type='array', var='queries', label='queries（原顺序）', pointers={'i': 'pink'}, cell=90, h=190),
        dict(type='array', var='idx', label='idx（按询问值从小到大排的下标）', cell=90, h=130),
        dict(type='array', var='ans', label='ans（按原顺序回答）', cell=90, h=140,
             color=lambda S, i, v: 'green' if i == S.get('i') and S.get('_line', 0) >= 14 else None),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('i', 'i', 'pink'), ('q', 'q', 'orange'), ('j', 'j', 'blue'), ('max_beauty', 'max_beauty', 'green')],
    captions={
        'items.sort': '物品按价格从小到大排序：`{items}`',
        'idx = sorted': '不直接动 `queries`，只排==下标==：`idx = {idx}`，这样答案还能按原顺序放回去',
        'ans = [0]': '`ans` 先全填 0，长度和 `queries` 一样',
        'max_beauty = j = 0': '`j` 是物品指针，`max_beauty` 是目前已纳入物品的最大美丽值',
        'for i in idx': lambda S, B, r: (f'按询问值从小到大处理：下标 `i = {S.i}`' if 'i' not in B or S.i != B.i
                                         else '所有询问都处理完了'),
        'q = queries[i]': '当前询问 `q = {q}`',
        'while j < len(items)': lambda S, B, r: (
            f'`items[{S.j}]` 价格 {S['items'][S.j][0]} ≤ {S.q}：属于==新增==的物品 → 纳入' if S.j < len(S['items']) and S['items'][S.j][0] <= S.q
            else (f'物品都纳入了' if S.j >= len(S['items'])
                  else f'`items[{S.j}]` 价格 {S['items'][S.j][0]} > {S.q}：再往后只会更贵 → 停')),
        'max_beauty = max': '`max_beauty = max({B.max_beauty}, {items[j][1]})` = =={max_beauty}==，只增不减',
        'j += 1': '`j` 右移，下一个物品 → `{j}`（`j` 只往前走，整个过程总共 n 步）',
        'ans[i] = max_beauty': '询问 {q} 的答案：价格 ≤ {q} 的物品中最大美丽值 = =={max_beauty}==，写到 `ans[{i}]`',
        'return ans': '按原顺序返回 `{ans}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='询问从小到大排好，物品指针只增不减',
        complexity='时间 `O(n log n + m log m)`，空间 `O(m)`',
        problem=['每个物品 `[价格, 美丽值]`，每次询问 `q`：价格 `≤ q` 的物品中最大美丽值，没有则为 `0`',
                 '示例：`items=[[1,2],[3,2],[2,4],[5,6],[3,5]]`，`queries=[1..6]` → `[2,4,5,5,6,6]`',
                 '本视频：`queries = [3,1,5,2]` → `[5,2,6,4]`'],
        quote='离线算法：把 queries 排序，通过改变回答询问的顺序，使问题更容易处理。',
        quote_src='—— 灵茶山艾府题解',
        idea=['询问变大时，满足条件的物品只会==变多==，上一次的答案可以接着用',
              '只需增量遍历 `queries[i-1] < price <= queries[i]` 的物品，再和上次的最大值取 `max`',
              '排序下标数组 `idx` 而不是 `queries` 本身，答案才能放回原位置'],
        summary=['时间 `O(n log n + m log m)`，瓶颈在排序；空间 `O(m)`',
                 '易错：`ans[i]` 用原下标 `i` 写入，不是排序后的位置',
                 '灵神还给了在线写法：按价格排序后求 beauty 前缀最大值，每个询问二分 `bisect_right`；',
                 '再进一步删掉“价格高但美丽值不更高”的无用物品，思路类似单调栈',
                 '同类题见灵神数据结构题单「专题：离线算法」'],
    ),
)
