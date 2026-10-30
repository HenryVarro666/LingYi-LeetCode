def _col(S, i, v):
    if 'nums1' not in S:
        return None
    if 'index' in S and i == S['index']:
        return 'blue'
    return 'orange' if S['nums1'][i] == S['nums2'][i] else None


def _txt(S):
    if 'swap_cnt' not in S:
        return ''
    return f"下限 swap_cost = =={S['swap_cost']}==　｜　`max_cnt*2 = {S['max_cnt']*2}` {'≤' if S['max_cnt']*2 <= S['swap_cnt'] else '>'} `swap_cnt = {S['swap_cnt']}`　（check_num = {S['check_num']}）"


CONFIG = dict(
    num=2499, title='让数组不相等的最小总代价', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='下标和下限 · 次数不过半',
    tags=['贪心与思维', '难度分 2633'],
    code='''
class Solution(object):
    def minimumTotalCost(self, nums1, nums2):

        cnt = {}
        max_cnt = 0
        check_num = None

        swap_cnt = 0
        swap_cost = 0

        for index, (x, y) in enumerate(zip(nums1, nums2)):
            if x == y:
                cnt[x] = cnt.get(x, 0) + 1
                if cnt[x] > max_cnt:
                    max_cnt = cnt[x]
                    check_num = x
                
                swap_cnt += 1
                swap_cost += index
        
        if max_cnt * 2 <= swap_cnt:
            return swap_cost
        
        for index, (x, y) in enumerate(zip(nums1, nums2)):
            if x != y and x != check_num and y != check_num:
                swap_cost += index
                swap_cnt += 1
                if max_cnt * 2 <= swap_cnt:
                    return swap_cost
        
        return -1
''',
    call='Solution().minimumTotalCost([2,2,2,1,3], [1,2,2,3,3])',
    expect=10,
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='array', var='nums1', label='nums1（橙色 = 与 nums2 相同，必须换）', pointers={'index': 'blue'}, color=_col, h=170),
        dict(type='array', var='nums2', label='nums2', color=_col, h=150),
        dict(type='map', var='cnt', label='cnt：相同位置上各数字的出现次数', h=150),
    ],
    watch=[('swap_cost', 'swap_cost', 'green'), 'swap_cnt', 'check_num', 'max_cnt'],
    captions={
        'cnt = {}': '`cnt` 记录「相同位置」上每个数字出现几次',
        'max_cnt = 0': '`max_cnt`：出现最多的那个数字的次数',
        'check_num = None': '`check_num`：这个出现最多的数字',
        'swap_cnt = 0': '`swap_cnt`：需要换的位置个数',
        'swap_cost = 0': '`swap_cost`：已确定的代价，先记为 0',
        11: '{"相同位置都检查完了" if B.get("index") == index else "看下标 `" + str(index) + "`：`x = " + str(x) + "`，`y = " + str(y) + "`"}',
        12: '`{x}` {"==" if x == y else "!="} `{y}` → {"必须交换的位置" if x == y else "不用动"}',
        13: '数字 `{x}` 的次数记为 `{cnt[x]}`',
        14: '`cnt[{x}] = {cnt[x]}` {">" if cnt[x] > B.max_cnt else "不超过"} `max_cnt = {B.max_cnt}` → {"它成为出现最多的数" if cnt[x] > B.max_cnt else "不更新"}',
        15: '最多的次数更新：`max_cnt = {max_cnt}`',
        16: '出现最多的数：`check_num = {check_num}`',
        18: '又多一个要换的位置：`swap_cnt` = =={swap_cnt}==',
        19: '这个位置必须交换，下标和就是答案下限：`swap_cost` = =={swap_cost}==',
        21: '`max_cnt*2 = {max_cnt*2}` {"≤" if max_cnt*2 <= swap_cnt else ">"} `swap_cnt = {swap_cnt}` → {"次数不过半，可直接返回下限" if max_cnt*2 <= swap_cnt else "过半了，众数之间换不开，要补外援"}',
        22: '次数不过半，下限可达：返回 `swap_cost = {swap_cost}`',
        24: '补位：看下标 `{index}`：`x = {x}`，`y = {y}`',
        25: '`x != y` 且都不是 `check_num = {check_num}` → {"这个位置可以拉来当外援" if x != y and x != check_num and y != check_num else "不能用"}',
        26: '外援下标 `{index}` 也加入：`swap_cost` = =={swap_cost}==',
        27: '`swap_cnt` = =={swap_cnt}==，众数占比下降',
        28: '`max_cnt*2 = {max_cnt*2}` {"≤" if max_cnt*2 <= swap_cnt else ">"} `swap_cnt = {swap_cnt}` → {"不过半了，返回" if max_cnt*2 <= swap_cnt else "还不够，继续找外援"}',
        29: '`swap_cost` 就是答案：`{swap_cost}`',
        30: '外援用完仍过半 → `-1`',
    },
    cards=dict(
        one_liner='相同位置的下标和是下限，次数不过半才能达到',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['两个数组，可交换 `nums1` 任意两下标的值，代价是下标之和',
                 '要让所有 `nums1[i] != nums2[i]`，求最小总代价，不可能则 `-1`',
                 '示例：`[2,2,2,1,3]` 与 `[1,2,2,3,3]` → `10`'],
        quote='对于这些位置是必须进行交换的，也就是说本题答案的下限就是这些下标之和。接下来的问题是在什么情况下可以达到这个下限。',
        quote_src='—— yiduobo 题解原文',
        idea=['把每个相同位置的数字出现次数看成一堆数：每次换掉两个不同的数 = 两个次数各减 1',
              '这和第 1753 题移除石子一样：==最大堆不超过总数一半==就能全消掉',
              '超过一半就从没被牵扯的下标里，补「不等且都不是 check_num」的位置，直到不过半或用完'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`max_cnt * 2 <= swap_cnt` 是能否达到下限的判据',
                 '补位时要求 `x`、`y` 都不等于 `check_num`',
                 '原文为 Python 2 风格，只删去了类型说明，逻辑未改',
                 '对比灵神：灵神在补位循环开头判断并 break，yiduobo 在补位后立即 return'],
    ),
)
