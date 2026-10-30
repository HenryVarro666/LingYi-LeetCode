CONFIG = dict(
    num=1944, title='队列中可以看到的人数', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='从右向左 · 单调栈存下标',
    tags=['灵神题单', '难度分 2105'],
    code='''
class Solution(object):
    def canSeePersonsCount(self, heights):

        n = len(heights)
        stack = [n - 1]

        res = [0]
        for index in range(n - 2, -1, -1):
            cnt = 0
            while stack and heights[index] > heights[stack[-1]]:
                stack.pop()
                cnt += 1
            
            if stack:
                cnt += 1
            res.append(cnt)
            stack.append(index)
        
        res.reverse()
        return res
''',
    call='Solution().canSeePersonsCount([10,6,8,5,11,9])',
    expect=[3,1,2,1,1,0],
    views=[
        dict(type='array', var='heights', label='heights', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='stack', var='stack', label='stack（候选集：保存下标，栈顶在右）', h=150, font=30),
        dict(type='array', var='res', label='res（从右往左追加，最后反转）', h=170),
    ],
    watch=[('index', 'index', 'blue'), ('cnt', 'cnt', 'green'), ('stack', 'stack', 'yellow'), ('res', 'res', 'cyan')],
    captions={
        'stack = [n - 1]': '最右边的人先入候选集（存下标 `{n-1}`）',
        'res = [0]': '最右边的人看不到任何人，`res` 从 `[0]` 开始',
        'for index in range': '考虑第 `{index}` 个人，身高 `{heights[index]}`',
        'cnt = 0': '这个人的计数清零',
        'while stack and heights[index]': lambda S, B, ret: (
            f'`{S.heights[S.index]}` > `{S.heights[S.stack[-1]]}`：能看到栈顶，且栈顶以后不会被更左的人看到 → 弹出'
            if S.stack and S.heights[S.index] > S.heights[S.stack[-1]] else
            ('候选集空了' if not S.stack else f'`{S.heights[S.index]}` < `{S.heights[S.stack[-1]]}`：栈顶更高，挡住了后面的人 → 停')),
        'stack.pop()': '栈顶被 `index` 挡住，不必再保留',
        'cnt += 1': '又看到一个人，`cnt` → =={cnt}==',
        'if stack:': lambda S, B, ret: ('此时栈不空：还能再看到栈顶那个更高的人' if S.stack else '栈空：右边没有更高的人'),
        'res.append(cnt)': '记下答案 `{cnt}`',
        'stack.append(index)': '`index` 入栈，继续向前考虑',
        'res.reverse()': '`res` 是从右往左存的 → ==反转==对应原下标',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='i<j 且 h[i]<h[j]，则 i 之前的人都不可能再看到 j',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每个人能看到右边的人，条件是中间的人都比两人矮',
                 '求每个人右侧能看到的人数',
                 '示例：`[10,6,8,5,11,9]` → `[3,1,2,1,1,0]`'],
        quote='若i < j，且heights[i] < heights[j]，那么对于i之前的所有位置k，k都不可能再看到j，因为中间夹着一个i的高度大于j的高度。',
        quote_src='—— yiduobo 题解原文',
        idea=['这个结论说明被矮子盖住的 j 不必留在候选集 → ==单调栈==',
              '从右向左扫：比栈顶高就弹出，每弹一个 +1',
              '弹完栈不空，还能看到栈顶，再 +1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '栈里存的是下标，比较时要写 `heights[stack[-1]]`',
                 '`res` 是倒着追加的，返回前别忘了 `reverse()`',
                 '对比灵神：灵神直接存身高并预先填好 `ans`，这里先追加再反转'],
    ),
)
