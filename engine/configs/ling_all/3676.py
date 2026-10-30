def _pos(S):
    return S['nums'].index(S['x']) if 'x' in S else None


CONFIG = dict(
    num=3676, title='碗子数组的数目', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 出栈时配对',
    tags=['灵神题单·单调栈', '难度分 1848'],
    code='''
class Solution:
    def bowlSubarrays(self, nums: List[int]) -> int:
        ans = 0
        st = []
        for x in nums:
            while st and st[-1] < x:
                st.pop()
                if st:
                    ans += 1
            st.append(x)
        return ans
''',
    call='Solution().bowlSubarrays([6,2,5,3,1,4])',
    expect=3,
    views=[
        dict(type='array', var='nums', pointers={'x': 'blue'}, h=170,
             color=lambda S, i, v: 'blue' if 'x' in S and i == _pos(S) else None),
        dict(type='stack', var='st', h=260, fmt=lambda v: str(v)),
        dict(type='text', fn=lambda S: f"栈（底→顶）`{S['st']}`，当前 `x = {S['x']}`" if 'x' in S and 'st' in S else ''),
    ],
    watch=[('x', 'x', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计碗的个数',
        'st = []': '单调栈：栈里的数从底到顶 ==递减==',
        'while st and st[-1] < x': lambda S, B, r: (
            f'栈顶 `{S.st[-1]}` < `x = {S.x}`：栈顶右边第一个更大的数就是 x → 要出栈' if S.st and S.st[-1] < S.x
            else ('栈空了，没有左端点，停止出栈' if not S.st else f'栈顶 `{S.st[-1]}` > `x = {S.x}`：x 比栈顶小，停止出栈')),
        'st.pop()': '弹出栈顶 `{B.st[-1]}`：它是中间最大值，右端点是 `{x}`',
        'if st:': lambda S, B, r: (
            f'弹出后栈里还有 `{S.st[-1]}`：它和 `x = {S.x}` 做两端，夹住刚弹出的数 → ==碗=='
            if S.st else '弹出后栈空：左边没有更大的数，凑不出碗'),
        'ans += 1': '栈非空说明中间至少有一个数，长度 >= 3 → `ans` = =={ans}==',
        'st.append(x)': '`x` 入栈：栈 `{st}`',
        'return ans': '一共 `{ans}` 个碗',
    },
    max_steps=90,
    cards=dict(
        one_liner='每个数出栈时，栈里剩下的就是一个合法左端点',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组长度 >= 3，且两端较小值 ==严格大于== 中间所有数的最大值',
                 '数组元素互不相同，求碗的个数',
                 '示例：`[2,5,3,1,4]` → `2`；本视频：`[6,2,5,3,1,4]` → `3`'],
        quote='无论是左大右小（比如 [3,1,2]）还是左小右大（比如 [2,1,3]），当我们遍历到 nums[i] 时，如果出栈后栈不为空，说明栈顶和 nums[i] 是合法子数组的左右端点。',
        quote_src='—— 灵茶山艾府题解 · 写法二',
        idea=['每个右端点 r，只需看它左边==最近的大于等于它==的数',
              '左高右低、左低右高两种碗，都在单调栈里一次算完',
              '弹出一个数后栈不空，说明长度至少 3，答案加一'],
        summary=['时间 `O(n)`，每个数最多入栈出栈各一次',
                 '先出栈再判断 `if st`：栈不空同时保证了长度 >= 3',
                 '题解还给了写法一（用下标，分开统计左高右低、左低右高）和把 `nums` 当栈的 `O(1)` 空间写法',
                 '本题元素互不相同；有重复时要规定一侧找大于等于、另一侧找严格大于，避免重复统计'],
    ),
)
