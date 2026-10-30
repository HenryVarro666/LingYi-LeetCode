def _txt(S):
    if 'p2' not in S:
        return ''
    if S.get('_line', 0) < 16:
        return f"最大值下标 `p1 = {S['p1']}`，最小值下标 `p2 = {S['p2']}`"
    n = len(S['nums'])
    p1, p2 = S['p1'], S['p2']
    return f"方案1 移除 0..p2：`{p2+1}`；方案2 移除 p1..n-1：`{n-p1}`；方案3 两头：`{p1+1+n-p2}`"


CONFIG = dict(
    num=2091, title='从数组中移除最大值和最小值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历 · 三种移除方案',
    tags=['灵神题单', '难度分 1384'],
    code='''
class Solution(object):
    def minimumDeletions(self, nums):

        if len(nums) == 1:
            return 1
        
        ma = mi = None
        for index, num in enumerate(nums):
            if ma is None or ma < num:
                p1 = index
                ma = num
            if mi is None or mi > num:
                p2 = index
                mi = num
        
        if p1 > p2:
            p1, p2 = p2, p1
        
        return min(p2 + 1, len(nums) - p1, p1 + 1 + len(nums) - p2)
''',
    call='Solution().minimumDeletions([0,-4,19,1,8,-2,-3,5])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=28, h=130),
        dict(type='array', var='nums', pointers={'p1': 'blue', 'p2': 'pink', 'index': 'yellow'}, h=330,
             color=lambda S, i, v: ('blue' if i == S.get('p1') else 'pink' if i == S.get('p2') else None)),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), 'ma', 'mi'],
    captions={
        'if len(nums) == 1': '先看边界：只有一个数时，它既是最大又是最小，删 1 次就够',
        'ma = mi = None': '`ma`、`mi` 记录当前最大、最小值，一开始都还没有',
        'for index, num': '看下标 `{index}`，值 `{num}`',
        'if ma is None or ma < num': '`ma = {B.ma}`，`num = {num}`：' + '{"num 更大，更新最大值" if (B.ma is None or B.ma < num) else "不更大"}',
        'p1 = index': '最大值位置 `p1 = {p1}`',
        'ma = num': '`ma` 更新为 `{ma}`',
        'if mi is None or mi > num': '`mi = {B.mi}`，`num = {num}`：' + '{"num 更小，更新最小值" if (B.mi is None or B.mi > num) else "不更小"}',
        'p2 = index': '最小值位置 `p2 = {p2}`',
        'mi = num': '`mi` 更新为 `{mi}`',
        'if p1 > p2': '`p1 = {p1}`，`p2 = {p2}`：谁先谁后无所谓，只考虑 `p1 < p2` → ' + '{"需要交换" if p1 > p2 else "不用交换"}',
        'p1, p2 = p2, p1': '交换后 `p1 = {p1} < p2 = {p2}`',
        'return min': '三种方案：`{p2+1}`、`{len(nums)-p1}`、`{p1+1+len(nums)-p2}` → ==`{ret}`==',
    },
    cards=dict(
        one_liner='先找到两个位置，再比较三种移除方案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次只能从数组前面或后面移除一个元素',
                 '求同时移除最大值和最小值的最少次数',
                 '本视频：`[0,-4,19,1,8,-2,-3,5]` → `3`'],
        quote='由于题目对数字的移除规则与数字的大小无关，因此在这里p1和p2是可以互换的，那么不妨只考虑p1 < p2的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['先处理边界：长度为 1 时答案是 1',
              '一趟遍历找出最大值、最小值的下标 `p1`、`p2`',
              '方案1 移除 `0..p2`；方案2 移除 `p1..n-1`；方案3 两头各移除',
              '三种方案取最少次数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '长度为 1 时 `p1`、`p2` 无法区分，要先单独返回 1',
                 '方案 3 是 `p1 + 1 + n - p2`，别漏了两个 `+1`',
                 '原文为 Python 2 写法，在 Python 3 下无需修改',
                 '对比灵神：灵神一次比较用 if/elif，不用 ma、mi 记录值'],
    ),
)
