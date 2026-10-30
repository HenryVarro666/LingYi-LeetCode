CONFIG = dict(
    num=1944, title='队列中可以看到的人数', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='从右往左 · 单调栈',
    tags=['灵神题单', '难度分 2105'],
    code='''
class Solution:
    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        ans = [0] * n
        st = []
        for i in range(n - 1, -1, -1):
            while st and st[-1] < heights[i]:
                st.pop()
                ans[i] += 1
            if st:  # 还可以再看到一个人
                ans[i] += 1
            st.append(heights[i])
        return ans
''',
    call='Solution().canSeePersonsCount([10,6,8,5,11,9])',
    expect=[3,1,2,1,1,0],
    views=[
        dict(type='array', var='heights', label='heights（从右往左遍历）', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='stack', var='st', label='st（没被挡住的人的身高，栈顶在右）', h=150, font=30),
        dict(type='array', var='ans', label='ans（每个人能看到的人数）', h=170,
             color=lambda S, i, v: 'green' if 'i' in S and i == S['i'] else None),
    ],
    watch=[('i', 'i', 'blue'), ('heights[i]', 'heights[i]', 'blue'), ('st', 'st', 'yellow'), ('ans[i]', 'ans[i]', 'green')],
    captions={
        'ans = [0] * n': '`ans` 先全填 0，最右边的人右边没人，答案就是 0',
        'st = []': '栈 `st` 里只放==没被挡住==的人的身高',
        'for i in range': '从右往左看第 `{i}` 个人，身高 `{heights[i]}`',
        'while st and st[-1] < heights[i]': lambda S, B, ret: (
            f'栈顶 `{S.st[-1]}` < `{S.heights[S.i]}`：他能看到栈顶，且栈顶被他挡住 → 继续弹'
            if S.st and S.st[-1] < S.heights[S.i] else
            ('栈空了，没人可弹' if not S.st else f'栈顶 `{S.st[-1]}` > `{S.heights[S.i]}`：更高的人挡在前面 → 停止弹出')),
        'st.pop()': '弹出被挡住的人：`i` 左边的人再也看不到他了',
        'ans[i] += 1': lambda S, B, ret: (f'`ans[{S.i}]` 加一 → =={S.ans[S.i]}=='),
        'if st:': lambda S, B, ret: ('栈不空：栈顶比自己高，还能再看到这一个人（但看不到更远的）' if S.st
                                   else '栈空：右边已经没有更高的人了'),
        'st.append(heights[i])': '自己入栈：对更左边的人来说，==他是新的挡板==',
        'return ans': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='从右往左，用栈只留下没被挡住的人',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`heights` 互不相同，第 `i` 人能看到右边第 `j` 人，当且仅当中间的人都比两人矮',
                 '求每个人能看到右边多少人',
                 '示例：`[10,6,8,5,11,9]` → `[3,1,2,1,1,0]`'],
        quote='如果发现一个 h[k] 比右边的数 h[j] 大，那么 h[k] 就把 h[j]「挡住」，k 左边的人再也不会看到 j 了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['被挡住的人永远不会再被遍历：==及时去掉无用数据==',
              '弹出的每个人都能被 `i` 看到，所以弹一个加一',
              '弹完后栈顶比自己高，也能看到，再加一'],
        summary=['时间 `O(n)`：每个人至多入栈出栈各一次',
                 '易错：弹完后栈不空，要额外 `+1`（看到那个更高的人）',
                 '题目保证身高互不相同，所以不用处理相等',
                 '同类题：739 每日温度、2454 下一个更大元素 IV'],
    ),
)
