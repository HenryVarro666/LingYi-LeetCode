CONFIG = dict(
    num=1331, title='数组序号转换', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='排序去重 + 哈希表',
    tags=['灵神题单', '常用数据结构'],
    code='''
class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        # 去重排序
        sorted_arr = sorted(set(arr))

        # 构建哈希表
        rank = {x: i for i, x in enumerate(sorted_arr, 1)}

        for i, x in enumerate(arr):
            arr[i] = rank[x]

        return arr
''',
    call='Solution().arrayRankTransform([37,12,28,9,100,56,80,5,12])',
    expect=[5, 3, 4, 2, 8, 6, 7, 1, 3],
    views=[
        dict(type='array', var='arr', label='arr（原地改成序号）', pointers={'i': 'blue'}, h=210,
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] else None),
        dict(type='array', var='sorted_arr', label='sorted_arr（去重后升序）', h=170),
        dict(type='map', var='rank', label='rank（值 → 序号）', fmt=lambda k, v: f'{k}: {v}', h=230, font=28),
    ],
    watch=['i', 'x', 'sorted_arr'],
    captions={
        'sorted_arr = sorted': '`set` 去重、`sorted` 升序：`{sorted_arr}`，下标 + 1 就是序号',
        'rank = {': '值 → 序号：`enumerate(sorted_arr, 1)` 从 1 开始编号，得到 `{rank}`',
        'for i, x in enumerate(arr)': '按原顺序逐个查表：`x = {x}`',
        'arr[i] = rank[x]': '`rank[{x}] = {rank[x]}`，原地把 `arr[{i}]` 换成序号 =={rank[x]}==',
        'return arr': '相同的数字查到同一个序号，所以相等元素序号相同：`{arr}`',
    },
    cards=dict(
        one_liner='排序去重后，下标就是序号，用哈希表一查即得',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把数组每个元素换成它排序后的序号，序号从 1 开始',
                 '越大序号越大，==相等的元素序号相同==，且序号要尽可能小',
                 '示例：`[37,12,28,9,100,56,80,5,12]` → `[5,3,4,2,8,6,7,1,3]`'],
        quote='复制一份，排序去重后，得到 sortedArr = [10,20,30]。然后创建一个哈希表，把 10,20,30 分别映射到 1,2,3。最后，查询 20,20,10,30 在哈希表中对应的 value，即为答案。',
        quote_src='—— 灵茶山艾府题解 · 方法二',
        idea=['去重后每个值只出现一次，它在有序数组里的位置 + 1 就是==最小的序号==',
              '把「值 → 序号」存进哈希表，查询只要 `O(1)`',
              '遍历原数组，用 `rank[x]` 原地覆盖'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(n)`',
                 '必须先去重：不去重的话相等元素会占多个序号',
                 '序号从 1 开始：`enumerate(sorted_arr, 1)`',
                 '灵神另给了方法一：对 `sorted_arr` 用 `bisect_left` 二分查下标 + 1，不用哈希表'],
    ),
)
