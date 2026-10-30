CONFIG = dict(
    num=1122, title='数组的相对排序', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='映射下标作第一关键字排序',
    code='''
class Solution(object):
    def relativeSortArray(self, arr1, arr2):

        p = {}
        l = len(arr2)
        for index, num in enumerate(arr2):
            p[num] = index
        
        arr1 = sorted(arr1, key=lambda d:(p.get(d, l), d))
        return arr1
''',
    call='Solution().relativeSortArray([2,3,1,3,2,4,6,7,9,2,19], [2,1,4,3,9,6])',
    expect=[2,2,2,1,4,3,3,9,6,7,19],
    views=[
        dict(type='array', var='arr2', h=170, label='arr2（给定的顺序）',
             pointers={'index': 'blue'}),
        dict(type='map', var='p', h=230, fmt=lambda k, v: f'{k} → {v}'),
        dict(type='array', var='arr1', h=190, label='arr1'),
    ],
    watch=['l', 'index', 'num'],
    captions={
        'p = {}': '`p` 记录 arr2 中每个数的位置，作为排序的第一关键字',
        'l = len': '`l = len(arr2) = {l}`：不在 arr2 中的数统一映射到 `l`，排在最后',
        'p[num] = index': '`p[{num}] = {index}`：{num} 排在第 {index} 位',
        'arr1 = sorted': '按 `(p.get(d, {l}), d)` 排序：先看映射值，再看数值本身；不在 arr2 的数映射值都是 {l}，于是按大小升序排在末尾',
        'return': '返回排序结果 `{arr1}`',
    },
    cards=dict(
        one_liner='先给 arr2 里的数编号，一次 sort：编号第一，数值第二',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`arr2` 的元素互不相同，且都在 `arr1` 中',
                 '把 `arr1` 按 `arr2` 的顺序排；不在 `arr2` 的元素按升序放在末尾',
                 '示例：`[2,3,1,3,2,4,6,7,9,2,19]`，`[2,1,4,3,9,6]` → `[2,2,2,1,4,3,3,9,6,7,19]`'],
        quote='先建立起arr2中每个数字对当前下标的映射……不在arr2中的数字，我们可以统一将其映射到l上。',
        quote_src='—— yiduobo 题解原文',
        idea=['arr2 里的数映射到 `0 ~ l-1`，其余统一映射到 `l`',
              '排序键 `(映射值, 数值)`：映射值决定先后',
              '映射值相同的（重复数、或不在 arr2 的数）再按数值排'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`p.get(d, l)`：没出现过的数默认 `l`，比所有下标都大',
                 '值域小时也可以用计数排序做到线性',
                 '原文无需改动，Python 3 可直接运行'],
    ),
)
