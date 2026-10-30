def _iv(S):
    iv = S.get('intervals')
    if iv is None:
        return '区间还没开始收集'
    return '缺失区间 `intervals` = ' + (('  '.join(f'[{a}, {b}]' for a, b in iv)) if iv else '（空）')


def _res(S):
    r = S.get('res')
    if r is None:
        return '最终格式化后的 `res` 还没生成'
    return '输出 `res` = ' + ('  '.join(f'"{x}"' for x in r) if r else '（空）')


CONFIG = dict(
    num=163, title='缺失的区间', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='收集区间再统一格式化', tags=[],
    code='''
class Solution(object):
    def findMissingRanges(self, nums, lower, upper):

        if not nums:
            intervals = [[lower, upper]]
        else:      
            intervals = []
            if nums[0] > lower:
                intervals.append([lower, nums[0] - 1])
        
            for index in range(1, len(nums)):
                if nums[index] > nums[index - 1] + 1:
                    intervals.append([nums[index - 1] + 1, nums[index] - 1])
        
            if nums[-1] < upper:
                intervals.append([nums[-1] + 1, upper])

        res = []
        for x, y in intervals:
            if x == y:
                res.append(str(x))
            else:
                res.append(str(x) + '->' + str(y))
        
        return res
''',
    call='Solution().findMissingRanges([2,3,5,50,75], 0, 99)',
    expect=['0->1', '4', '6->49', '51->74', '76->99'],
    views=[
        dict(type='array', var='nums', label='nums（有序，范围 [lower, upper] = [0, 99]）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if i == S.get('index') or (i == S.get('index', 99) - 1) else None),
        dict(type='text', fn=_iv, size=30, h=90),
        dict(type='text', fn=_res, size=30, h=90),
        dict(type='text', size=30, h=90, fn=lambda S: f"当前：`nums[{S['index']-1}] + 1 = {S['nums'][S['index']-1]+1}`，`nums[{S['index']}] = {S['nums'][S['index']]}`" if 'index' in S and 'res' not in S else ''),
    ],
    watch=['lower', 'upper', 'index', ('x', 'x', 'orange'), ('y', 'y', 'orange')],
    captions={
        'if not nums': '`nums` 为空 → 整段 `[lower, upper]` 都缺失；不空则看边界和相邻间隙',
        'intervals = []': '先收集区间，最后再统一格式化（长度 1 的区间输出格式不同）',
        'if nums[0] > lower': '`nums[0] = {nums[0]}` 与 `lower = {lower}` 比：{"nums[0] 更大，头部有缺口" if nums[0] > lower else "头部没缺口"}',
        'intervals.append([lower': '头部缺失 `[{lower}, {nums[0] - 1}]`，加入 intervals',
        'for index in range': '从下标 1 开始，看每个数和前一个数之间有没有缺口',
        'if nums[index] > nums[index - 1] + 1': '`{nums[index]}` 与 `{nums[index-1]} + 1 = {nums[index-1]+1}` 比：{"中间有数没出现" if nums[index] > nums[index-1]+1 else "紧挨着，没有缺口"}',
        'intervals.append([nums[index - 1]': '缺口 `[{nums[index-1]+1}, {nums[index]-1}]` 加入 intervals',
        'if nums[-1] < upper': '`nums[-1] = {nums[-1]}` vs `upper = {upper}`：{"尾部有缺口" if nums[-1] < upper else "尾部没缺口"}（放最后处理才能保证顺序）',
        'intervals.append([nums[-1]': '尾部缺失 `[{nums[-1]+1}, {upper}]`，加入 intervals',
        'for x, y in intervals': '取出区间 `[{x}, {y}]`',
        'if x == y': '`{x} == {y}`？→ {"是，单个数，只写数字" if x == y else "否，写成 x->y"}',
        'res.append(str(x))': '单个缺失数：`"{x}"`',
        'res.append(str(x) +': '区间写成 `"{x}->{y}"`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='先把缺口收集成区间，再按长度统一格式化',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['有序数组 `nums`，范围 `[lower, upper]`，返回缺失数字组成的区间',
                 '长度 1 写 `"a"`，更长写 `"a->b"`',
                 '示例：`[2,3,5,50,75]`，`[0,99]` → `["0->1","4","6->49","51->74","76->99"]`'],
        quote='注意到题目中对于长度为1的区间输出的格式与其他区间不同，所以我在这里采用的是先将区间信息收集起来，然后再统一格式化输出。',
        quote_src='—— yiduobo 题解原文',
        idea=['头部：`nums[0] > lower`，缺 `[lower, nums[0]-1]`',
              '中间：相邻两数差大于 1，缺 `[前+1, 后-1]`',
              '尾部：`nums[-1] < upper`，缺 `[nums[-1]+1, upper]`，放最后保证顺序'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`nums` 为空要单独处理：整段都缺失',
                 '格式化时 `x == y` 只输出一个数',
                 '代码原文即 Python 3 可运行，未做修改'],
    ),
)
