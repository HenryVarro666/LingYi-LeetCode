CONFIG = dict(
    num=2363, title='合并相似的物品', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='Counter 相加 + 排序',
    tags=[],
    code='''
class Solution:
    def mergeSimilarItems(self, items1: List[List[int]], items2: List[List[int]]) -> List[List[int]]:
        return sorted((Counter(dict(items1)) + Counter(dict(items2))).items())
''',
    call='Solution().mergeSimilarItems([[1,1],[4,5],[3,8]], [[3,1],[1,5]])',
    expect=[[1, 6], [3, 9], [4, 5]],
    views=[
        dict(type='array', var='items1', label='items1 = [value, weight]', cell=120, h=150, font=30),
        dict(type='array', var='items2', label='items2 = [value, weight]', cell=120, h=150, font=30),
        dict(type='text', h=60, size=30, fn=lambda S: '`Counter(dict(items1))` = `{1: 1, 4: 5, 3: 8}`' if 'items1' in S else ''),
        dict(type='text', h=60, size=30, fn=lambda S: '`Counter(dict(items2))` = `{3: 1, 1: 5}`' if 'items1' in S else ''),
        dict(type='text', h=60, size=30, fn=lambda S: '相加：同一个 value 的 weight 加起来 → `{1: 6, 4: 5, 3: 9}`，再按 value 排序' if 'items1' in S else ''),
    ],
    result_fn=lambda r: [list(x) for x in r],
    watch=[],
    captions={
        'return sorted': '`dict(items1)` 把每个 `[value, weight]` 当键值对；两个 `Counter` 相加会把相同 value 的 weight ==求和==；`.items()` 后 `sorted` 按 value 升序 → `[[1, 6], [3, 9], [4, 5]]`',
    },
    cards=dict(
        after=[dict(heading='Counter 相加做了什么', lines=['`dict(items1)`：把 `[value, weight]` 当键值对，得到 `{1: 1, 4: 5, 3: 8}`','`Counter(...) + Counter(...)`：相同的键，值相加','`.items()` 得到 `(value, weight)` 二元组，`sorted` 默认按第一项（value）升序','题解还给了其它写法，这里选最简洁的一行写法'])],
        one_liner='每个 [value, weight] 直接当键值对，Counter 相加就是合并',
        complexity='时间 `O((n+m) log(n+m))`，空间 `O(n+m)`',
        problem=['两个物品集合，每项 `[value, weight]`，同一集合里 value 唯一',
                 '合并后相同 value 的重量求和，按 value 升序返回',
                 '示例：`[[1,1],[4,5],[3,8]]` 与 `[[3,1],[1,5]]` → `[[1,6],[3,9],[4,5]]`'],
        quote='一行写法，由于每个元素都是一个长为 2 的列表，所以可以直接作为键值对传入 dict，然后通过 Counter 把值加起来。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长为 2 的列表可以直接传给 `dict`，得到 value → weight',
              '`Counter` 相加：键相同的值相加，键不同的各自保留',
              '最后 `sorted(...items())` 按 value 升序'],
        summary=['时间 `O((n+m) log(n+m))`，瓶颈在排序，空间 `O(n+m)`',
                 '易错点：`Counter` 相加会丢掉非正数的计数，本题 weight 都 ≥ 1 所以没问题',
                 '题解还提到其它写法（如手写哈希表），一行写法最短'],
    ),
)
