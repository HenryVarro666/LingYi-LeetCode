def _pos(S):
    return S['i'] if 'i' in S else None


def _fmt(p):
    return ('∞' if p[0] == float('inf') else str(p[0])) + '×' + str(p[1])


CONFIG = dict(
    num=3113, title='边界元素是最大值的子数组数目', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 记录元素和出现次数',
    tags=['灵神题单·单调栈', '难度分 2046'],
    code='''
class Solution:
    def numberOfSubarrays(self, nums: List[int]) -> int:
        ans = len(nums)
        st = [[inf, 0]]  # 无穷大哨兵
        for x in nums:
            while x > st[-1][0]:
                st.pop()
            if x == st[-1][0]:
                ans += st[-1][1]
                st[-1][1] += 1
            else:
                st.append([x, 1])
        return ans
''',
    call='Solution().numberOfSubarrays([3,1,3,2,3])',
    expect=8,
    views=[
        dict(type='array', var='nums', h=170),
        dict(type='stack', var='st', h=240, fmt=_fmt),
        dict(type='text', fn=lambda S: f"栈里每项是 `值×出现次数`，从底到顶严格递减；当前 `x = {S['x']}`" if 'x' in S else '栈里每项是 `值×出现次数`，底部 ∞ 是哨兵'),
    ],
    watch=[('x', 'x', 'blue'), ('ans', 'ans', 'green'), ('栈顶', lambda S: S['st'][-1] if S.get('st') else '', 'purple')],
    captions={
        'ans = len(nums)': '每个元素自己就是一个子数组：`ans = {ans}`',
        'st = [[inf, 0]]': '栈里存 `[值, 出现次数]`；底部放 ∞ 哨兵，永远不会被弹出',
        'while x > st[-1][0]': lambda S, B, r: (
            f'`x = {S.x}` > 栈顶 `{S.st[-1][0]}`：栈顶这个数再也凑不出左右端点相等的子数组 → 无用，弹出'
            if S.x > S.st[-1][0] else f'`x = {S.x}` <= 栈顶 `{S.st[-1][0]}`：不再弹出'),
        'st.pop()': '弹出栈顶：左边这些更小的数不可能再和以后的数配对了',
        'if x == st[-1][0]': lambda S, B, r: (
            f'`x = {S.x}` 等于栈顶 `{S.st[-1][0]}`：和左边 `{S.st[-1][1]}` 个相同的数各配一对' if S.x == S.st[-1][0]
            else f'`x = {S.x}` 小于栈顶 `{S.st[-1][0]}`：x 是新的值，左边没有可配对的相同数'),
        'ans += st[-1][1]': '`ans += {B.st[-1][1]}`（左边相同数的个数）→ =={ans}==',
        'st[-1][1] += 1': '栈顶计数加一：现在栈里有 `{st[-1][1]}` 个 `{x}`',
        'st.append([x, 1])': '`x = {x}` 第一次入栈，出现次数记为 1',
        'return ans': '一共 `{ans}` 个满足条件的子数组',
    },
    max_steps=90,
    cards=dict(
        one_liner='首尾都是最大值 = 首尾相等，且中间没有更大的数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数一数有多少子数组，第一个和最后一个元素都是该子数组的最大值',
                 '单个元素也算一个子数组',
                 '示例：`[1,4,3,3,2]` → `6`；本视频：`[3,1,3,2,3]` → `8`'],
        quote='例如 nums=[4,3,1,2,1]，在从左到右遍历的过程中，由于 2 的出现，左边的 1 永远不可能与右边的 1 组成一个题目要求的子数组。所以当遍历到 2 时，左边的 1 就是无用数据了，可以清除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['维护底大顶小的单调栈，栈里记录 ==值和出现次数==',
              '新来的 x 比栈顶大：栈顶无用，弹掉',
              'x 等于栈顶：和左边 cnt 个 x 各组成一对，答案加 cnt',
              '栈底放 ∞ 哨兵，省掉判空'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '某个值出栈后又出现，次数要==重置为 1==，所以弹出就是真的丢掉',
                 '答案初值是 `n`：长度为 1 的子数组全都合法',
                 '栈里只保留严格递减的值，相等的值合并成一项并计数'],
    ),
)
