NUMS = [-50, -49, -48, -50, -47]
K, X = 3, 2
LO, HI = 51, 61   # cnt[51:61] 对应值 -50..-41（负数下标 cnt[-50] 就是 cnt[51]）


def _cnt(S):
    c = S.get('cnt')
    return None if c is None else [c[LO:HI]]


def _hdr(S):
    return [str(v) for v in range(-50, -50 + (HI - LO))]


def _txt(S):
    if 'left' in S and S.get('v') is not None and S.get('_line', 0) in (11, 12, 13):
        return f'还需要数 `left = {S["left"]}` 个；扫到值 `v = {S["v"]}`，它出现 `{S["cnt"][S["v"]]}` 次'
    return '`cnt` 是计数数组：负数下标 `cnt[-50]` 其实是 `cnt[51]`，下面只画值 -50 ~ -41'


CONFIG = dict(
    num=2653, title='滑动子数组的美丽值', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长滑动窗口 + 计数数组',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针', '难度分 1786'],
    code='''
class Solution:
    def getSubarrayBeauty(self, nums: List[int], k: int, x: int) -> List[int]:
        cnt = [0] * 101
        for num in nums[:k - 1]:  # 先往窗口内添加 k-1 个数
            cnt[num] += 1

        ans = [0] * (len(nums) - k + 1)
        for i, (in_, out) in enumerate(zip(nums[k - 1:], nums)):
            cnt[in_] += 1  # 进入窗口（保证窗口有恰好 k 个数）
            left = x  # 从 x 开始倒着减，减到 <= 0 就找到了答案
            for v in range(-50, 0):  # 暴力枚举负数范围 [-50, -1]
                left -= cnt[v]
                if left <= 0:  # 找到答案
                    ans[i] = v
                    break
            cnt[out] -= 1  # 离开窗口
        return ans
''',
    call=f'Solution().getSubarrayBeauty({NUMS}, {K}, {X})',
    expect=[-49, -49, -48],
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='nums', label='nums（框 = 当前窗口，窗口长 k）', cell=84, h=190,
             window=('i', 'i + k - 1'), pointers={'i': 'blue'},
             color=lambda S, j, v: 'green' if 'i' in S and S.get('_line', 0) >= 9 and S['i'] <= j < S['i'] + S['k'] and j == S['i'] + S['k'] - 1 and S.get('_line') == 9 else None),
        dict(type='table', var=_cnt, label='cnt：窗口内每个值的出现次数（只画 -50 ~ -41）', cols=_hdr, rows=lambda S: ['次数'],
             h=190, cell=70,
             color=lambda S, r, c, v: ('yellow' if S.get('v') == c - 50 and S.get('_line', 0) in (11, 12, 13) else ('cyan' if v else None))),
        dict(type='array', var='ans', label='ans（每个窗口的美丽值）', cell=84, h=130,
             pointers={'i': 'blue'}),
    ],
    watch=[('i', 'i', 'blue'), ('in_', 'in_', 'green'), ('out', 'out', 'pink'), ('left', 'left', 'orange'), ('v', 'v', 'yellow')],
    captions={
        'cnt = [0] * 101': '值域 `[-50, 50]` 共 101 个数 → 用==计数排序==的思路，开 101 个计数器；负数下标会绕到数组末尾',
        'for num in nums[:k - 1]': lambda S, B, r: (f'先放入前 `k-1` 个数：`num = {S.num}`' if S.get('num') != B.get('num') else '前 `k-1` 个数放完了'),
        'cnt[num] += 1': '值 `{num}` 的计数 +1：`cnt[{num}] = {cnt[num]}`',
        'ans = [0] *': '一共有 `{len(nums) - k + 1}` 个窗口，答案先全填 `0`（第 x 小不是负数时美丽值就是 0）',
        'for i, (in_, out)': lambda S, B, r: (f'第 `{S.i}` 个窗口：右边进来 `{S.in_}`，之后左边的 `{S.out}` 要离开' if 'i' in S and S.get('i') != B.get('i') or 'i' not in B
                                              else '所有窗口都处理完了'),
        'cnt[in_] += 1': '`{in_}` 进入窗口 → 窗口恰好有 `k` 个数：`cnt[{in_}] = {cnt[in_]}`',
        'left = x': '找第 `x = {x}` 小：从 `left = x` 开始，==扫过的值依次减去它们的个数==',
        'for v in range(-50': lambda S, B, r: f'从小到大枚举值 `v = {S.v}`' if S.get('v') is not None else '枚举结束',
        'left -= cnt[v]': '值 `{v}` 出现 `{cnt[v]}` 次 → `left = {B.left} - {cnt[v]} = {left}`',
        'if left <= 0': lambda S, B, r: (f'`left = {S.left} ≤ 0`：小于等于 `{S.v}` 的数已经够 `x` 个 → ==`{S.v}` 就是第 x 小==' if S.left <= 0
                                         else f'`left = {S.left} > 0`：还差 `{S.left}` 个，继续往大的值找'),
        'ans[i] = v': '第 `{i}` 个窗口的美丽值 = `{v}`',
        'break': '找到了，不用再扫更大的值',
        'cnt[out] -= 1': '`{out}` 离开窗口：`cnt[{out}] = {cnt[out]}`，为下一个窗口做准备',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='值域只有 101，借计数排序：窗口里扫一遍计数就能找到第 x 小',
        complexity='时间 `O(nU)`，`U = 50`；空间 `O(U)`',
        problem=['定长 `k` 的每个子数组：第 `x` 小的数若是负数，美丽值就是它，否则为 `0`',
                 '示例：`nums = [1,-1,-3,-2,3], k = 3, x = 2` → `[-1,-2,-2]`',
                 '本视频：`[-50,-49,-48,-50,-47], k = 3, x = 2` → `[-49,-49,-48]`'],
        quote='第 x 小等价于：求==最小==的 v，满足 ≤ v 的数==至少==有 x 个。……借鉴计数排序的思想，用一个 cnt 数组维护窗口内每个数的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['窗口滑动时只增减两个计数：进入 `+1`，离开 `-1`',
              '从 `v = -50` 起往大扫，`left` 从 `x` 减去 `cnt[v]`，减到 `<= 0` 的那个 `v` 就是答案',
              '只需检查负数 `[-50, -1]`：扫完都没减到 0，美丽值保持 `0`'],
        summary=['时间 `O(nU)`，`U = 50`；空间 `O(U)`',
                 '易错：先==进入==窗口再统计，统计完才让左端离开；`cnt[-50]` 借负数下标落在 `cnt[51]`',
                 '答案数组初值就是 `0`：第 x 小不是负数时不用改',
                 '视频里的示例值都靠近 -50，所以扫描很快；一般情况最多扫 50 个值',
                 '附：有序集合写法 `SortedList`（来自 sortedcontainers）`O(n log k)`，本视频未演示'],
    ),
)
