def _txt(S):
    if 'x' not in S:
        return '哈希表 `last_index`：key = ==reverse(nums[i])==，value = 最近的下标 i'
    j, x = S['j'], S['x']
    if x in S['last_index'] and S['last_index'][x] < j:
        return f"`nums[{j}] = {x}` 在表中：左边 `reverse(nums[{S['last_index'][x]}]) = {x}` → 距离 =={j - S['last_index'][x]}=="
    return f"`nums[{j}] = {x}`：左边没有数反转后等于它"


CONFIG = dict(
    num=3761, title='镜像对之间最小绝对距离', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 哈希表',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1669'],
    code='''
class Solution:
    def minMirrorPairDistance(self, nums: List[int]) -> int:
        last_index = {}
        ans = inf

        for j, x in enumerate(nums):
            if x in last_index:
                ans = min(ans, j - last_index[x])
            rev = int(str(x)[::-1])
            last_index[rev] = j

        return ans if ans < inf else -1
''',
    call='Solution().minMirrorPairDistance([45,120,33,54,21,12])',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（j = 当前枚举的右端点）', pointers={'j': 'blue'}, h=210,
             dim=lambda S, i, v: 'j' in S and i > S['j']),
        dict(type='map', var='last_index', label='last_index：reverse(nums[i]) → 最近下标 i',
             fmt=lambda k, v: f'{k} → {v}', h=170, font=34),
        dict(type='text', fn=_txt, h=90, size=30),
    ],
    watch=[('j', 'j', 'blue'), 'x', ('rev', 'rev', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'last_index = {}': '`last_index` 记录 j ==左边== 每个 `reverse(nums[i])` 的最大下标',
        'ans = inf': '`ans` 初始为 `inf`，表示还没找到镜像对',
        'for j, x in': lambda S, B, r: (f'枚举右端点 `j = {S.j}`，`x = {S.x}`' if 'j' not in B or S.j != B.j else '遍历结束'),
        'if x in last_index': lambda S, B, r: (f'左边有 `reverse(nums[i]) = {S.x}` → 找到镜像对 `({S.last_index[S.x]}, {S.j})`' if S.x in S.last_index
                                               else f'表里没有 `{S.x}`：左边没有数反转后等于 `{S.x}`'),
        'ans = min': '下标越靠右距离越小，所以只存最大下标：`ans = min({B.ans}, {j} − {last_index[x]}) = {ans}`',
        'rev = int': lambda S, B, r: (f'`reverse({S.x}) = {S.rev}`：`int` ==自动去掉前导零==' if str(S.x).endswith('0')
                                      else f'`reverse({S.x}) = {S.rev}`'),
        'last_index[rev] = j': lambda S, B, r: (f'`{S.rev}` 已在表中：==覆盖==为更靠右的下标 `{S.j}`，以后距离更小' if S.rev in B.last_index
                                                else f'把 `{S.rev} → {S.j}` 放进表，供==右边==的数查询'),
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='枚举右端点 j，哈希表存左边的 reverse 值',
        complexity='时间 `O(n log U)`，空间 `O(n)`',
        problem=['镜像对 `(i, j)`：`i < j` 且 `reverse(nums[i]) == nums[j]`（==有方向==）',
                 '求镜像对下标的最小距离，不存在返回 `-1`',
                 '示例：`[12,21,45,33,54]` → `1`；本视频：`[45,120,33,54,21,12]` → `1`'],
        quote='枚举 j，同时用哈希表维护 j 左边的 reverse(nums[i]) 的==最大下标==，哈希表的 key 是 reverse(nums[i])，value 是下标 i。',
        quote_src='—— 灵茶山艾府题解',
        idea=['查表用 `nums[j]`，存表用 `reverse(nums[j])`：==不对称==，别写反',
              '同一个 key 只保留最靠右的下标，距离才最小',
              '先查询再更新，保证 `i < j`'],
        summary=['时间 `O(n log U)`，空间 `O(n)`',
                 '易错：题目是 `reverse(nums[i]) == nums[j]`，不是反过来',
                 '`int(str(x)[::-1])` 自动忽略前导零：`120 → 21`',
                 '另一种写法：用 `divmod` 逐位反转，不用字符串'],
    ),
)
