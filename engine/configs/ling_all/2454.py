def _lst(S, name):
    return [S['nums'][k] for k in S[name]]


CONFIG = dict(
    num=2454, title='下一个更大元素 IV', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='两个单调栈 s、t 接力',
    tags=['灵神题单', '难度分 2175'],
    code='''
class Solution:
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        ans = [-1] * len(nums)
        s = []
        t = []
        for i, x in enumerate(nums):
            while t and nums[t[-1]] < x:
                ans[t.pop()] = x  # t 栈顶的下下个更大元素是 x
            j = len(s) - 1
            while j >= 0 and nums[s[j]] < x:
                j -= 1  # s 栈顶的下一个更大元素是 x
            t += s[j + 1:]  # 把从 s 弹出的这一整段元素加到 t
            del s[j + 1:]  # 弹出一整段元素
            s.append(i)  # 当前元素（的下标）加到 s 栈顶
        return ans
''',
    call='Solution().secondGreaterElement([2,4,0,9,6])',
    expect=[9,6,6,-1,-1],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, h=200,
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='stack', var='s', label='s（还没遇到更大数的下标）', h=130, font=28,
             fmt=lambda k: f'{k}'),
        dict(type='stack', var='t', label='t（已遇到一个更大数、等第二个的下标）', h=130, font=28,
             fmt=lambda k: f'{k}'),
        dict(type='array', var='ans', label='ans', h=160,
             color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'blue'), ('s', 's', 'yellow'), ('t', 't', 'orange'), ('j', 'j', 'pink')],
    captions={
        'ans = [-1]': '`ans` 全部先填 -1：找不到就是 -1',
        's = []': '`s` 维护==还没找到下一个更大元素==的下标（递减栈）',
        't = []': '`t` 接收从 `s` 弹出的元素：它们已有一个更大的，等第二个',
        'for i, x': '遍历到 `nums[{i}] = {x}`',
        'while t and nums[t[-1]] < x': lambda S, B, ret: (
            f'`t` 栈顶对应 `{S.nums[S.t[-1]]}` < `{S.x}`：它的第二个更大元素就是 `{S.x}`'
            if S.t and S.nums[S.t[-1]] < S.x else
            ('`t` 空了，不用再结算' if not S.t else f'`t` 栈顶 `{S.nums[S.t[-1]]}` ≥ `{S.x}`：还没遇到第二个更大的 → 停')),
        'ans[t.pop()] = x': '`t` 栈顶的下下个更大元素是 `{x}` → `ans` 更新，并弹出',
        'j = len(s) - 1': '`j` 从 `s` 栈顶开始往下找第一个 ≥ x 的位置',
        'while j >= 0 and nums[s[j]] < x': lambda S, B, ret: (
            f'`s[{S.j}]` 对应 `{S.nums[S.s[S.j]]}` < `{S.x}`：它的下一个更大元素是 `{S.x}`，要弹出 → `j` 继续往下'
            if S.j >= 0 and S.nums[S.s[S.j]] < S.x else
            ('`s` 全都比 x 小' if S.j < 0 else f'`s[{S.j}]` 对应 `{S.nums[S.s[S.j]]}` ≥ `{S.x}`：保留，停在这里')),
        'j -= 1': '`j` → {j}',
        't += s[j + 1:]': lambda S, B, ret: (f'`s[{S.j+1}:]` 这一整段刚找到下一个更大数，接力放进 `t`（顺序不变，仍然递减）' if S.j + 1 < len(B.s) else '`s` 里没有比 x 小的元素，没有东西可以接力给 `t`'),
        'del s[j + 1:]': lambda S, B, ret: ('同时把这一段从 `s` 里删掉' if S.j + 1 < len(B.s) else '没有要删的'),
        's.append(i)': '当前下标 `{i}` 入 `s`，等待它的更大元素',
        'return ans': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='被 s 弹出的元素，不扔掉，放进 t 再等一个更大数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['对每个数找右边==第二个==比它大的数，没有则为 -1',
                 '示例：`[2,4,0,9,6]` → `[9,6,6,-1,-1]`',
                 '`2` 的第一个更大是 `4`，第二个更大是 `9`'],
        quote='在这个做法中，栈顶元素弹出后，就没有用了。但对于本题，我们需要的正是弹出去的元素！',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想下一个更大元素：递减栈 `s`，遇到更大的 `x` 就弹出',
              '再用递减栈 `t` 接住从 `s` 弹出的元素，`x` 比 `t` 栈顶大 → 栈顶的第二个更大数就是它',
              '每轮顺序：先结算 `t`，再从 `s` 弹到 `t`，最后 `i` 入 `s`'],
        summary=['时间 `O(n)`：每个元素至多入栈出栈各两次',
                 '易错：必须==先结算 t，再把 s 的元素移进 t==，否则同一个 x 会被当成第二个更大数',
                 '整段 `s[j+1:]` 加到 `t` 后 `t` 依然单调递减（原文答疑）',
                 '同类题：739 每日温度、1944 队列中可以看到的人数'],
    ),
)
