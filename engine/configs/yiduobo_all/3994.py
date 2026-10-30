def _cls(S, v):
    return 0 if v < S['a'] else (1 if v <= S['b'] else 2)


def _info(S):
    if 'p' not in S:
        return '三个区间里元素的相对顺序不变：只算每个元素要==向左挪多少格=='
    if 'now' not in S:
        return f"第一趟：`p = {S['p']}` 是最左区间下一个要填的位置，`res = {S['res']}`"
    return f"第二趟：`now = {S['now']}` 是当前元素的真实下标，`p = {S['p']}` 是中间区间下一个要填的位置，`res = {S['res']}`"


CONFIG = dict(
    num=3994, title='划分数组的最少相邻交换次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='两趟遍历 · 统计向左移动距离',
    tags=['灵神题单·常用数据结构', '难度分 1705'],
    code='''
class Solution(object):
    def minAdjacentSwaps(self, nums, a, b):
        
        p = 0
        res = 0
        mod = 10 ** 9 + 7
        for index, v in enumerate(nums):
            if v < a:
                res += index - p
                if res >= mod:
                    res -= mod
                p += 1
        
        now = p
        for v in nums:
            if v < a:
                continue
            
            if v <= b:
                res += now - p
                if res >= mod:
                    res -= mod
                p += 1
            
            now += 1
        
        return res
''',
    call='Solution().minAdjacentSwaps([5, 1, 9, 3, 7, 2, 8], 4, 8)',
    expect=8,
    views=[
        dict(type='text', fn=_info),
        dict(type='array', var='nums', label='nums（蓝 = 小于 a，黄 = 在 [a, b]，粉 = 大于 b）', h=200,
             pointers={'index': 'cyan'},
             color=lambda S, i, v: ('blue', 'yellow', 'pink')[_cls(S, v)]),
    ],
    watch=['p', 'now', ('res', 'res', 'green')],
    captions={
        'p = 0': '`p`：最左区间下一个元素应该填的位置',
        'if v < a': '`v = {v}` 属于最左区间吗？`{v} < {a}` → ==' + '{"是" if v < a else "否"}' + '==',
        'res += index - p': '它要从下标 `{index}` 挪到 `{p}`，向左跨过 `{index - p}` 个别区间的元素 → `res` = =={res}==',
        'p += 1': lambda S, B, r: (f'中间区间又定好一个位置：`p` → {S.p}' if 'now' in S else f'最左区间又定好一个位置：`p` → {S.p}'),
        'now = p': '最左区间处理完了；`now` = `{now}`：此后中间元素的真实下标从这里开始',
        'continue': '第二趟：属于最左区间的第一趟已经处理过 → 跳过',
        'if v <= b': '`v = {v}` 在 `[{a}, {b}]` 内吗？→ ==' + '{"是，属于中间区间" if v <= b else "否，属于最右区间"}' + '==',
        'res += now - p': '中间元素现在位于 `now = {now}`，应在 `p = {p}`：向左挪 `{now - p}` 格 → `res` = =={res}==',
        'now += 1': '`now` → {now}：下一个元素的真实下标',
        'return res': '一共需要 `{res}` 次相邻交换',
    },
    cards=dict(
        one_liner='同区间元素不交换，只统计每个元素要向左挪几格',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把数组分成三段：小于 a、在 [a, b]、大于 b，每段可以为空',
                 '每次只能交换相邻元素，求最少交换次数（模 `10^9+7`）',
                 '本视频：`[5,1,9,3,7,2,8], a=4, b=8` → `8`'],
        quote='属于同一个区间中的元素间是不应该进行交换的。这也就意味着同一区间内的元素间的相对顺序将保留原数组中的相对顺序。',
        quote_src='—— yiduobo 题解原文',
        idea=['最终的好数组可以直接确定：每个区间内保持原顺序',
              '为避免重复，只统计「右边的元素向左挪」的距离：原下标 − 目标下标',
              '第一趟处理最左区间；第二趟处理中间区间，最右区间自动就位'],
        summary=['时间 `O(n)`，空间 `O(1)`，不用真的构造好数组',
                 '第二趟里原下标要用 `now`（已跳过最左区间的位置修正），不能直接用 index',
                 '每次累加后判断 `res >= mod` 再减，防止数值过大',
                 '对比灵神：灵神把三类视作 0/1/2 直接数逆序对，yiduobo 数的是向左的移动距离'],
    ),
)
