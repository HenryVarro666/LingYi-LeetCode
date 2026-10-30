def _col(S, i, v):
    if 'nums1' not in S:
        return None
    eq = S['nums1'][i] == S['nums2'][i]
    if 'i' in S and i == S['i']:
        return 'blue'
    return 'orange' if eq else None


def _txt(S):
    if 'swap_cnt' not in S:
        return ''
    return f"相等对数 swap_cnt = =={S['swap_cnt']}==　众数 mode = `{S['mode']}` 出现 `{S['mode_cnt']}` 次　｜　`mode_cnt*2 = {S['mode_cnt']*2}` {'≤' if S['mode_cnt']*2 <= S['swap_cnt'] else '>'} `swap_cnt = {S['swap_cnt']}`"


CONFIG = dict(
    num=2499, title='让数组不相等的最小总代价', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='分类讨论 · 众数鸽巢',
    tags=['贪心与思维', '难度分 2633'],
    code='''
class Solution:
    def minimumTotalCost(self, nums1: List[int], nums2: List[int]) -> int:
        ans = swap_cnt = mode_cnt = mode = 0
        cnt = [0] * (len(nums1) + 1)
        for i, (x, y) in enumerate(zip(nums1, nums2)):
            if x == y:
                ans += i
                swap_cnt += 1
                cnt[x] += 1
                if cnt[x] > mode_cnt:
                    mode_cnt, mode = cnt[x], x

        for i, (x, y) in enumerate(zip(nums1, nums2)):
            if mode_cnt * 2 <= swap_cnt: break
            if x != y and x != mode and y != mode:
                ans += i
                swap_cnt += 1
        return ans if mode_cnt * 2 <= swap_cnt else -1
''',
    call='Solution().minimumTotalCost([2,2,2,1,3], [1,2,2,3,3])',
    expect=10,
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='array', var='nums1', label='nums1（橙色 = 与 nums2 相同，必须被换走）', pointers={'i': 'blue'}, color=_col, h=170),
        dict(type='array', var='nums2', label='nums2', color=_col, h=150),
        dict(type='array', var='cnt', label='cnt[x]：x 作为「相同值」出现的次数', h=170,
             color=lambda S, i, v: 'yellow' if S.get('mode') == i and v > 0 else None),
    ],
    watch=[('ans', 'ans', 'green'), 'swap_cnt', 'mode', 'mode_cnt'],
    captions={
        'ans = swap_cnt': '`ans` 总代价、`swap_cnt` 要换的位置数、`mode` 及 `mode_cnt` 众数和次数，先清零',
        'cnt = [0]': '`cnt[x]` 统计值 x 在「相同位置」出现几次',
        'if x == y': '`nums1[{i}] = {x}`，`nums2[{i}] = {y}` → {"相同，这个位置必须换" if x == y else "不同，先不管"}',
        7: '这个位置必须参与交换，代价至少是下标 `{i}`：`ans` = =={ans}==',
        8: '需要换的位置数 `swap_cnt` = =={swap_cnt}==',
        'cnt[x] += 1': '值 `{x}` 又出现一次：`cnt[{x}]` = {cnt[x]}',
        'if cnt[x] > mode_cnt': '`cnt[{x}] = {cnt[x]}` 比当前众数次数 `{B.mode_cnt}` {"多" if cnt[x] > B.mode_cnt else "不多"}',
        'mode_cnt, mode = ': '众数更新：`mode = {mode}`，出现 `{mode_cnt}` 次',
        14: '`{mode_cnt}*2 = {mode_cnt*2}` {"≤" if mode_cnt*2 <= swap_cnt else ">"} `{swap_cnt}`：{"众数没超过一半，两两互换即可，停止补位" if mode_cnt*2 <= swap_cnt else "众数超过一半（鸽巢原理），众数之间换不开，还得找外援"}',
        15: '下标 `{i}`：`{x}, {y}` {"都不是众数且本来就不同 → 可以拉来当外援" if x != y and x != mode and y != mode else "不能用（相同或含众数）"}',
        16: '外援下标 `{i}` 也要换：`ans += {i}` → =={ans}==',
        17: '需要换的位置数 `swap_cnt` 变为 =={swap_cnt}==，众数占比下降',
        18: '{"众数不超过一半了" if mode_cnt*2 <= swap_cnt else "外援不够，无解"} → 返回 `{ans if mode_cnt*2 <= swap_cnt else -1}`',
    },
    cards=dict(
        one_liner='相同位置必换；众数占一半以上就从左往右找外援',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['两个数组，可交换 `nums1` 任意两个下标的值，代价是两下标之和',
                 '要让每个下标都 `nums1[i] != nums2[i]`，求最小总代价，不可能返回 `-1`',
                 '示例：`[2,2,2,1,3]` 与 `[1,2,2,3,3]` → `10`'],
        quote='如果 modeCnt 超过 swapCnt 的一半，根据鸽巢原理，无法通过重排这些数字，让数组不相等。这种情况必须不断寻找其他的满足 nums1[j]≠nums2[j] 的数对，且数对中的数都不等于 mode。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先统计所有 `nums1[i]==nums2[i]` 的位置：它们必须换，下标和就是代价下限',
              '这些值里若众数 ==出现次数 × 2 ≤ 位置数==，两两错开交换即可（奇数个时借下标 0）',
              '否则众数之间换不开，从左往右拉入「值不同且都不是 mode」的位置，直到不再超过一半'],
        summary=['时间 `O(n)`，空间 `O(n)`；可用摩尔投票降到 `O(1)`',
                 '外援必须 `x != y` 且 `x != mode` 且 `y != mode`',
                 '从左到右取外援，因为下标小代价小',
                 '补位循环开头先判断 `mode_cnt*2 <= swap_cnt` 就 break，最后若仍不满足返回 `-1`'],
    ),
)
