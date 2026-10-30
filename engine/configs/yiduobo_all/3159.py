CONFIG = dict(
    num=3159, title='查询数组中元素的出现位置', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='遍历收集下标 pos',
    code='''
class Solution(object):
    def occurrencesOfElement(self, nums, queries, x):

        pos = []
        for index, v in enumerate(nums):
            if v == x:
                pos.append(index)
        
        res = []
        for q in queries:
            if q > len(pos):
                res.append(-1)
            else:
                res.append(pos[q - 1])
        
        return res
''',
    call='Solution().occurrencesOfElement([1,3,1,7,1], [1,3,2,4], 1)',
    expect=[0, 4, 2, -1],
    views=[
        dict(type='array', var='nums', label='nums（绿色 = 等于 x）', pointers={'index': 'blue'}, h=170,
             color=lambda S, i, v: 'green' if v == S['x'] else None),
        dict(type='array', var='pos', label='pos', h=140),
        dict(type='array', var='queries', label='queries', h=140),
        dict(type='array', var='res', label='res（每个询问的答案）', h=140),
    ],
    watch=['x', 'q', ('res', 'res', 'green')],
    captions={
        'pos = []': '`pos` 用来收集 x 出现的所有下标',
        'pos.append(index)': '`nums[{index}] == {x}`：把下标 `{index}` 记进 `pos` → =={pos}==',
        'res = []': '`res` 放每个询问的答案',
        'if q > len(pos)': '`q = {q}`，`len(pos) = {len(pos)}`：{"q 比 x 的个数还大 → 没有第 q 个，答案 -1" if q > len(pos) else "x 至少出现 q 次 → 答案在 pos 里"}',
        'res.append(-1)': 'x 出现次数不足 `{q}` 次 → 答案 ==-1==',
        'res.append(pos[q - 1])': '第 `{q}` 个 x 是 `pos[{q}-1]` = ==`{pos[q-1]}`==（下标从 0 数，所以减一）',
        'return res': '全部询问答完：`{res}`',
    },
    cards=dict(
        one_liner='先遍历收集 x 的下标，再对每个询问查 pos[q-1]',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['`queries[i]` 要求找 `nums` 中第 `queries[i]` 个 `x` 的下标',
                 '出现次数少于它就返回 `-1`',
                 '本视频：`nums=[1,3,1,7,1]`，`x=1` → `[0,4,2,-1]`'],
        quote='题目关心的是x在nums中的下标，那么就可以先对nums进行一趟遍历，将x出现的所有下标用一个数组pos收集起来。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：遍历 `nums`，把等于 `x` 的下标依次放进 `pos`',
              '第二趟：对每个 `q`，比较它和 `len(pos)`',
              '不够就 `-1`，够了取 `pos[q - 1]`'],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '易错点：第 `q` 个要取 `pos[q - 1]`',
                 '原文为 Python 2 风格，只删去了类型说明，逻辑未改',
                 '对比灵神：灵神用两行列表推导式，这里是两个显式循环'],
    ),
)
