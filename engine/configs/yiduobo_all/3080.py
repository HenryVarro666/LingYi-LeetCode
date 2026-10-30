CONFIG = dict(
    num=3080, title='执行操作标记数组中的元素', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='下标排序 + 集合 marked + 指针 p',
    tags=[],
    code='''
class Solution(object):
    def unmarkedSumArray(self, nums, queries):

        s = sum(nums)
        n = len(nums)
        sorted_index = sorted(range(n), key=lambda d:(nums[d], d))
        marked = set()

        p = 0
        res = []

        for index, k in queries:
            if index not in marked:
                marked.add(index)
                s -= nums[index]
            
            while k > 0 and p < n:
                if sorted_index[p] in marked:
                    p += 1
                    continue
                
                marked.add(sorted_index[p])
                s -= nums[sorted_index[p]]
                p += 1
                k -= 1

            res.append(s)

        return res
''',
    call='Solution().unmarkedSumArray([1,2,2,1,2,3,1], [[1,2],[3,3],[4,2]])',
    expect=[8, 3, 0],
    views=[
        dict(type='array', var='nums', h=190, label='nums（绿色 = 已标记）',
             color=lambda S, i, v: 'green' if 'marked' in S and i in S['marked'] else None),
        dict(type='array', var='sorted_index', h=190, label='sorted_index（按 (值, 下标) 排序）', pointers={'p': 'blue'},
             dim=lambda S, i, v: 'p' in S and i < S['p']),
        dict(type='set', var='marked', h=130, fmt=lambda x: str(x)),
        dict(type='array', var='res', h=110, label='res'),
    ],
    watch=[('s', 's', 'pink'), ('p', 'p', 'blue'), 'k', ('res', 'res', 'green')],
    captions={
        's = sum': '`s` 记录未被标记的数值之和，初始 `{s}`',
        'sorted_index = sorted': '下标按 ==(数值, 下标)== 双关键字排序，同值自然下标小的在前：`{sorted_index}`',
        'marked = set': '集合 `marked` 记录已标记的下标，避免重复标记',
        'p = 0': '`p`：`sorted_index` 中下一个待检查的位置，只往后走',
        'if index not in': '`index = {index}` {"==已经标记过==，忽略" if index in marked else "还没标记 → 要标记它"}',
        'marked.add(index)': '标记下标 `{index}`',
        's -= nums[index]': '从 `s` 减去 `nums[{index}]`，`s = {s}`',
        'while k > 0': '`k = {k}`，`p = {p}` → {"继续找" if (k > 0 and p < n) else "k 用完或到末尾，本轮结束"}',
        'if sorted_index[p]': '看下标 `{sorted_index[p]}`：{"已标记 → 跳过" if sorted_index[p] in marked else "==未标记== → 它就是当前最小的未标记元素"}',
        19: '已标记 → 跳过，`p` 后移到 {p}',
        20: '`continue`：回到 `while` 重新判断',
        24: '`p += 1`：`p` 后移到 {p}，这个位置用过了',
        'marked.add(sorted_index[p])': '标记下标 `{sorted_index[p]}`（值 `{nums[sorted_index[p]]}`）',
        's -= nums[sorted_index[p]]': '`s` 减去这个值，`s = {s}`',
        'k -= 1': '又标记了一个，还需标记 `k = {k}` 个',
        'res.append': '本轮操作后未标记之和 `s = {s}`，加入答案',
    },
    cards=dict(
        one_liner='按 (数值, 下标) 排好顺序，p 往后走，集合去重',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每轮 `(index, k)`：标记 `index`，再标记 `k` 个最小的未标记数（同值取下标小的）',
                 '输出每轮后的未标记之和',
                 '示例：`[1,2,2,1,2,3,1]` → `[8,3,0]`'],
        quote='先将数组下标按照数值为第一关键字，下标值自身为第二关键字从小到大进行排序，得到数组 sorted_index，那么 k 对应的标记操作就会按照 sorted_index 中的顺序进行。',
        quote_src='—— yiduobo 题解',
        idea=['排好的 `sorted_index` 就是「标记顺序」，`p` 表示走到哪了',
              '标记 `k` 个最小值不能重复标记，所以用集合 `marked` 判断',
              '每标记一个就从 `s` 里减掉它，每轮结束把 `s` 记入答案'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '==两步都要查 marked==：`index` 可能已被标记；排序序列里的下标也可能被 `index` 提前标记',
                 '已标记的位置要 `p += 1` 再 `continue`，否则死循环',
                 '同类题：排序后用指针只扫一遍的「懒标记」写法']),
)
