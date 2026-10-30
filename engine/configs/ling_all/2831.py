def _x(S):
    pos = S.get('pos')
    if pos:
        return S['nums'][pos[0]]
    return None


def _win(S):
    pos = S.get('pos')
    if not pos or 'right' not in S or 'left' not in S or S['right'] >= len(pos) or S['left'] >= len(pos):
        return None
    return S['left']


def _nums_color(S, i, v):
    pos = S.get('pos')
    if not pos or v != _x(S):
        return None
    if 'right' in S and 'left' in S and S['left'] < len(pos) and S['right'] < len(pos):
        if pos[S['left']] + S['left'] <= i <= pos[S['right']] + S['right']:
            return 'green'
    return 'yellow'


def _txt(S):
    pos = S.get('pos')
    if not pos or 'p' not in S or 'left' not in S:
        return '把相同元素的下标分组；`pos` 里存 `下标 − 组内序号`'
    return f"要删的数 = `p − pos[left]` = `{S['p']} − {pos[S['left']]}` = =={S['p'] - pos[S['left']]}==（k = {S['k']}）"


CONFIG = dict(
    num=2831, title='找出最长等值子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组 + 滑动窗口（pos[i]-i）',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1976'],
    code='''
class Solution:
    def longestEqualSubarray(self, nums: List[int], k: int) -> int:
        pos_lists = defaultdict(list)
        for i, x in enumerate(nums):
            pos_lists[x].append(i - len(pos_lists[x]))

        ans = 0
        for pos in pos_lists.values():
            if len(pos) <= ans:
                continue  # 无法让 ans 变得更大
            left = 0
            for right, p in enumerate(pos):
                while p - pos[left] > k:  # 要删除的数太多了
                    left += 1
                ans = max(ans, right - left + 1)
        return ans
''',
    call='Solution().longestEqualSubarray([1,3,2,3,1,3], 1)',
    expect=2,
    views=[
        dict(type='array', var='nums', h=150, label='nums（黄 = 当前这组的数，绿 = 窗口覆盖范围）', color=_nums_color),
        dict(type='map', var='pos_lists', h=150, label='pos_lists：值 → 下标 − 组内序号', fmt=lambda k, v: f'{k}: {v}', font=30),
        dict(type='array', var='pos', h=240, label='pos（当前这组）', pointers={'left': 'blue', 'right': 'pink'},
             window=(_win, 'right')),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'p', ('ans', 'ans', 'green')],
    captions={
        'pos_lists = defaultdict': '哈希表：每种数字 → 它出现的下标列表',
        'pos_lists[x].append': '`x = {x}` 的第 {len(pos_lists[x])} 个出现在下标 `{i}`，存 `i − 组内序号 = {pos_lists[x][-1]}`：这样两端相减就直接是要删的个数',
        'if len(pos) <= ans': lambda S, B, r: (f'这组只有 `{len(S.pos)}` 个，`<= ans = {S.ans}`：==再怎么也不会更长== → 跳过' if len(S.pos) <= S.ans
                                              else f'这组有 `{len(S.pos)}` 个，`> ans = {S.ans}`，还有希望，开窗口'),
        'continue': '无法让 `ans` 变大，换下一组',
        'left = 0': '换一组数字，窗口从头开始：`left = 0`',
        'for right, p in enumerate(pos)': '右端点 `right` 右移，`p = pos[right] = {p}`',
        'while p - pos[left] > k': lambda S, B, r: (f'要删 `{S.p} − {S.pos[S.left]} = {S.p - S.pos[S.left]}` 个，`> k = {S.k}` → ==删太多了==，收缩左端' if S.p - S.pos[S.left] > S.k
                                                   else f'要删 `{S.p} − {S.pos[S.left]} = {S.p - S.pos[S.left]}` 个，`<= k = {S.k}` → 窗口合法'),
        'left += 1': '`left` 右移到 {left}，窗口里相同的数变少，要删的数也变少',
        'ans = max': '窗口里有 `{right - left + 1}` 个相同数且能凑成连续 → `ans = max({B.ans}, {right - left + 1}) = {ans}`',
        'return ans': '最长等值子数组长度 =={ans}==',
    },
    cards=dict(
        one_liner='相同数字分组，每组做一次「要删的数 ≤ k」的滑动窗口',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['删除最多 `k` 个元素后，能得到的最长等值子数组（元素全相等）有多长',
                 '示例：`nums=[1,3,2,3,1,3], k=3` → `3`（删下标 2、4，得 `[1,3,3,3]`）','本视频取 `k=1`，答案 `2`，能看到窗口收缩'],
        quote='把相同元素分组，相同元素的下标记录到哈希表中……`pos` 实际保存的是 `pos[i]-i`，需要删除的元素个数简化为 `pos[right] - pos[left]`。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一组里下标为 `pos[left]..pos[right]`，中间不是这个数的都要删',
              '先减去组内序号：==要删的个数 = pos[right] − pos[left]==',
              '个数 `> k` 就移动 `left`；每个 `right` 用窗口长度更新答案'],
        summary=['`left` 总移动次数不超过 n，时间 `O(n)`；空间 `O(n)`',
                 '易错：`pos` 存的是 `i - len(pos_lists[x])`，不是原下标',
                 '`len(pos) <= ans` 时可以直接跳过这一组',
                 '思考题：把「删除」改成「修改」就是 424 题（替换后的最长重复字符）'],
    ),
)
