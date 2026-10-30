NUMS = [3, 1, 2, 1, 2, 2, 3]


def _show(S):
    st = S.get('st')
    if st is None:
        return '栈 `st` 从空开始：栈里存「还没确定要操作的数」，底小顶大'
    x = S.get('x')
    if x is None:
        return f'遍历结束，栈 `{st}` 严格递增，每个非零数各要一次操作'
    return f'当前 `x = {x}`，栈 `{st}`，已操作 `{S["ans"]}` 次'


CONFIG = dict(
    num=3542, title='将所有元素变为 0 的最少操作次数', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 弹出时记一次操作',
    tags=['灵神题单·单调栈', '难度分 1890'],
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        ans = 0
        st = []
        for x in nums:
            while st and x < st[-1]:
                st.pop()
                ans += 1
            # 如果 x 与栈顶相同，那么 x 与栈顶可以在同一次操作中都变成 0，x 无需入栈
            if not st or x != st[-1]:
                st.append(x)
        return ans + len(st) - (st[0] == 0)  # 0 不需要操作
''',
    call=f'Solution().minOperations({NUMS!r})',
    expect=5,
    views=[
        dict(type='text', fn=_show, size=30, h=70),
        dict(type='array', var='nums', label='nums（当前 x 取值相同的格子标黄）', h=190,
             color=lambda S, i, v: 'yellow' if S.get('x') == v else None),
        dict(type='stack', var='st', label='st（底小顶大，没有重复值）', fmt=lambda x: str(x), h=180),
    ],
    watch=[('x', 'x', 'blue'), ('st', 'st', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 只在「必须操作」时才加一',
        'st = []': '栈保存还没被「夹住」的数，保持底小顶大',
        'while st and x < st[-1]': lambda S, B, r: ('栈空，不用弹' if not S.st else f'`x = {S.x}` 比栈顶 `{S.st[-1]}` 小？' + ('是：栈顶右边出现了更小的数' if S.x < S.st[-1] else '否：不弹')),
        'st.pop()': '栈顶 `{B.st[-1]}`：右边是 `x = {x}`（更小），左边是栈中前一个数（也更小）→ ==被夹住，必须操作一次==，弹出',
        'ans += 1': '`ans` = {ans}：某次操作会把它变成 0（不是说先操作它）',
        'if not st or x != st[-1]': lambda S, B, r: ('栈空，`x` 直接入栈' if not S.st else
                                                   f'`x = {S.x}` 与栈顶 `{S.st[-1]}` 相同 → 同一次操作一起消掉，无需入栈' if S.x == S.st[-1]
                                                   else f'`x = {S.x}` 比栈顶 `{S.st[-1]}` 大 → 入栈'),
        'st.append(x)': '`x = {x}` 入栈，栈 `{st}`',
        'return ans': '栈 `{st}` 严格递增，里面每个非零数各一次：`{ans}` + `{len(st)}` - `{1 if st[0] == 0 else 0}` = =={ret}==',
    },
    cards=dict(
        one_liner='只在「必须操作」时加一：被更小的数夹住就是必须',
        complexity='时间 `O(n)`，空间 `O(n)`（原地写法 `O(1)`）',
        problem=['每次选一个子数组，把其中==最小的非负数==全变成 0，求把整个数组变 0 的最少次数',
                 '示例 3：`[1,2,1,2,1,2]` → `4`',
                 '本视频：`[3,1,2,1,2,2,3]` → `5`'],
        quote='从左往右遍历数组，只在「必须要操作」的时候，才把答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['左右两侧都有更小的数，这个数就==必须单独操作==',
              '单调栈：来了更小的 `x`，栈顶左（栈内前一个）右（x）都更小 → 弹出并计一次',
              '`x` 等于栈顶：同一次操作一起消，不用入栈，栈里没有重复'],
        summary=['时间 `O(n)`，每个元素至多入栈、出栈一次',
                 '结束时栈严格递增：非零数各一次，所以答案要加 `len(st)`；栈底是 0 要减 1',
                 '相等时不入栈，是为了让栈里没有重复值',
                 '还有分治（每次找最小值切段）和原地写法，把 nums 当栈即可做到 `O(1)` 空间'],
    ),
)
