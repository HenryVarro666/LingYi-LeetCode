CONFIG = dict(
    num=2449, title='使数组相似的最少操作次数', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='按（奇偶, 值）排序 + 只数增加的一边',
    tags=['灵神题单', '双序列配对', '难度分 2076'],
    code='''
class Solution(object):
    def makeSimilar(self, nums, target):

        nums.sort(key=lambda d:(d % 2, d))
        target.sort(key=lambda d:(d % 2, d))

        n = len(nums)
        res = 0
        for index in range(n):
            if nums[index] > target[index]:
                res += (nums[index] - target[index]) // 2
        
        return res
''',
    call='Solution().makeSimilar([8,12,6,3,5], [2,14,10,7,1])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（先偶后奇，各自升序）', h=200, pointers={'index': 'blue'},
             color=lambda S, i, v: 'orange' if v % 2 else None),
        dict(type='array', var='target', label='target（同样排序）', h=200,
             color=lambda S, i, v: 'orange' if v % 2 else None),
        dict(type='text', h=70, fn=lambda S: f"橙色 = 奇数组；已累计操作次数 `res = ` =={S['res']}==" if 'res' in S else '橙色 = 奇数组'),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'nums.sort': '按 `(奇偶, 值)` 排序：偶数在前、奇数在后，同奇偶按大小：`{nums}`',
        'target.sort': 'target 同样排序：`{target}`，这样同位置的数奇偶性一致',
        'n = len': '`n = {n}`',
        'res = 0': '`res` 累计操作次数',
        'for index in range': lambda S, B, r: ('每一对都比较完了' if B.get('index') == S['index'] else f"比较第 `{S['index']}` 对：`nums[{S['index']}] = {S['nums'][S['index']]}`，`target[{S['index']}] = {S['target'][S['index']]}`"),
        'if nums[index] >': lambda S, B, r: (f'`{S.nums[S.index]} > {S.target[S.index]}`：nums 这位要减小，需要减 2 若干次 → 计入' if S.nums[S.index] > S.target[S.index]
                                              else f'`{S.nums[S.index]} <= {S.target[S.index]}`：这位是被加的，加减同步，不用重复计数'),
        'res += ': '要减 `{nums[index] - target[index]}`，减 2 需要 `{(nums[index] - target[index]) // 2}` 次：`res` → =={res}==',
        'return res': '加和减同步进行，只数减的一边，最少操作 `{res}` 次',
    },
    cards=dict(
        one_liner='操作加减同步，只数 nums 比 target 大的那些位',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每次选两个下标，一个加 2、一个减 2',
                 '让 nums 与 target 每个元素频率相同，求最少操作次数',
                 '示例：`[8,12,6,3,5]` 变成 `[2,14,10,7,1]` → `3`'],
        quote='将nums和target分奇偶，从小到大进行排序，然后一趟遍历。需要注意的是，每次加2减2都是同步执行的，因此只需要计算加或者减的操作次数就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['操作不改变奇偶性，奇数只能变奇数，偶数只能变偶数',
              '取四个数画在数轴上：线段交叉会多出不必要的操作，所以大小顺序一一对应',
              '加和减次数相同，只在 `nums[i] > target[i]` 时累加 `(差) // 2`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错：只统计 nums 大于 target 的位置，别两边都加',
                 '与灵神对比：灵神取负后求 `|差|` 之和再除 4；yiduobo 用 `(奇偶, 值)` 排序，只数减的一边'],
    ),
)
