CONFIG = dict(
    num=575, title='分糖果', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='set 去重 · min(k, n/2)',
    code='''
class Solution:
    def distributeCandies(self, candyType: List[int]) -> int:
        return min(len(set(candyType)), len(candyType) // 2)
''',
    call='Solution().distributeCandies([1,1,2,3,3,3])',
    expect=3,
    views=[
        dict(type='array', var='candyType', pointers={}, h=240),
        dict(type='text', fn=lambda S: (f"不同种类 `k = {len(set(S['candyType']))}`，上限 `n/2 = {len(S['candyType'])//2}`，答案 `min(k, n/2)` = =={min(len(set(S['candyType'])), len(S['candyType'])//2)}==" if 'candyType' in S else ''), h=90),
        dict(type='set', var=lambda S: set(S['candyType']) if 'candyType' in S else set(), fmt=lambda x: str(x), h=160, label='set(candyType)'),
    ],
    watch=[('k', 'len(set(candyType))', 'green'), ('n/2', 'len(candyType) // 2', 'orange')],
    captions={
        'return min': '不同的糖有 `{len(set(candyType))}` 种，至多吃 `n/2 = {len(candyType)//2}` 颗 → 取较小者 =={ret}==',
    },
    cards=dict(
        one_liner='设不同糖的种类数为 k，答案就是 min(k, n/2)',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`candyType[i]` 是第 `i` 枚糖的类型，只能吃 `n/2` 枚',
                 '求最多能吃到几种不同的糖',
                 '示例：`[1,1,2,3,3,3]` → `3`'],
        quote='一般地，设 k 为 candyType 中的不同元素个数，那么答案为 min(k, n/2)',
        quote_src='—— 灵茶山艾府题解',
        idea=['种类数 `k` 是上限：每种至少吃一颗最多得到 `k` 种',
              '吃的颗数 `n/2` 也是上限：一颗最多贡献一种',
              '两个上限都能取到，所以取较小值'],
        before=[dict(heading='先看两个示例', lines=[
            '示例 2：`[1,1,2,3]` 有 3 种糖，但至多吃 `n/2 = 2` 颗 → 答案 `2`',
            '示例 3：`[6,6,6,6]` 只有 1 种糖，吃 2 颗也只有 1 种 → 答案 `1`',
            '两个例子分别被「吃的颗数」和「糖的种类」卡住'])],
        after=[dict(heading='为什么能同时取到', lines=[
            '种类数 `k` ≥ `n/2` 时：每颗吃不同种，吃满 `n/2` 种',
            '种类数 `k` < `n/2` 时：每种至少吃一颗，再随便补够',
            '所以答案恰好是两者较小值，不用模拟'])],
        summary=['时间 `O(n)`，空间 `O(n)`（set）',
                 '一行搞定：`len(set(...))` 统计种类',
                 '易错：用整除 `//`，`n` 保证为偶数'],
    ),
)
