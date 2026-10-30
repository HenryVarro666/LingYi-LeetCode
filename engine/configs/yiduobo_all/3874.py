def _in2(S):
    return 'res' in S and 'nxt' in S or ('pre' in S and 'peak' in S and S.get('_line', 0) >= 11)


def _cur(S):
    if 'res' not in S or 'peak' not in S or not S['peak']:
        return None
    i = S.get('index')
    if i is None or i >= len(S['peak']):
        return None
    return S['peak'][i]


def _lo(S):
    c = _cur(S)
    if c is None or 'pre' not in S or S.get('_line', 0) < 23:
        return None
    return S['pre'] + 1 if S['pre'] >= 0 else 0


def _hi(S):
    c = _cur(S)
    if c is None or 'nxt' not in S or S.get('_line', 0) < 23:
        return None
    return S['nxt'] - 1


def _color(S, i, v):
    p = S.get('peak') or []
    c = _cur(S)
    if 'res' not in S and i == S.get('index') and 'index' in S:
        return 'yellow'
    if c is not None and i == c:
        return 'blue'
    if i in p:
        return 'green'
    return None


def _txt(S):
    if 'res' not in S:
        return '先扫一遍，找出所有峰（比左右邻居都大）'
    if S.get('_line', 0) >= 25 and 'right' in S:
        return f"峰 `{_cur(S)}`：左边界 `{S['left']}` 种 × 右边界 `{S['right']}` 种 = =={S['left'] * S['right']}=="
    return f"峰下标 `peak = {S['peak']}`，逐个算以它为唯一峰的子数组"


CONFIG = dict(
    num=3874, title='只有一个峰的合法子数组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='找出所有峰 · 乘法原理',
    tags=[],
    code='''
class Solution(object):
    def validSubarrays(self, nums, k):
        
        peak = []
        for index in range(1, len(nums) - 1):
            if nums[index] > nums[index - 1] and nums[index] > nums[index + 1]:
                peak.append(index)

        res = 0
        for index in range(len(peak)):
            if index == 0:
                pre = -1
            else:
                pre = peak[index - 1]
            
            left = min(peak[index] - pre, k + 1)
        
            if index == len(peak) - 1:
                nxt = len(nums)
            else:
                nxt = peak[index + 1]
            
            right = min(nxt - peak[index], k + 1)

            res += left * right
        
        return res
''',
    call='Solution().validSubarrays([1,3,2,4,1,5,2,0], 2)',
    expect=14,
    views=[
        dict(type='text', h=90, size=30, fn=_txt),
        dict(type='array', var='nums', label='nums（绿 = 峰，黄 = 正在判断，蓝 = 当前峰，框 = 子数组可延伸的范围）', cell=96, h=240,
             window=(_lo, _hi), color=_color),
        dict(type='array', var='peak', label='peak（所有峰的下标）', cell=96, h=170,
             color=lambda S, i, v: 'blue' if 'nxt' in S and i == S.get('index') else None),
    ],
    watch=['index', 'pre', 'nxt', ('left', 'left', 'cyan'), ('right', 'right', 'orange'), ('res', 'res', 'green')],
    captions={
        'peak = []': '`peak` 用来存所有峰的下标',
        'for index in range(1, len(nums) - 1)': '峰不可能在两端，只看 `1 .. n-2`',
        'if nums[index] > nums[index - 1]': lambda S, B, r: (
            f"`nums[{S.index}] = {S.nums[S.index]}` 比左 `{S.nums[S.index-1]}`、右 `{S.nums[S.index+1]}` "
            + ('都大 → ==是峰==' if S.nums[S.index] > S.nums[S.index-1] and S.nums[S.index] > S.nums[S.index+1] else '不是都大 → 不是峰')),
        'peak.append(index)': '记下峰 `{index}`，现在 `peak = {peak}`',
        'res = 0': '`res` 累计答案：每个峰各算一次，子数组恰含一个峰所以不会重复',
        'for index in range(len(peak))': '依次处理每个峰 `peak[{index}] = {peak[index]}`',
        'pre = -1': '第一个峰左边没有别的峰，当作 `pre = -1`，左边最多延伸到下标 0',
        'pre = peak[index - 1]': '前一个峰在 `{pre}`：子数组不能碰到它，左端最多延伸到 `{pre + 1}`',
        'left = min': '左端选法 = `min(峰 − pre, k+1)` = `min({peak[index] - pre}, {k + 1})` = =={left}==：既不越过前一个峰，也不超过 k 的距离',
        'nxt = len(nums)': '最后一个峰右边没有别的峰，当作 `nxt = n = {nxt}`',
        'nxt = peak[index + 1]': '后一个峰在 `{nxt}`：右端最多延伸到 `{nxt - 1}`',
        'right = min': '右端选法 = `min(nxt − 峰, k+1)` = `min({nxt - peak[index]}, {k + 1})` = =={right}==',
        'res += left * right': '左端 `{left}` 种 × 右端 `{right}` 种 = `{left * right}`，`res` = =={res}==',
        'return res': '所有峰都算完，一共 `{res}` 个合法子数组',
    },
    cards=dict(
        one_liner='先找出所有峰，再按峰计数：左端选法 × 右端选法',
        complexity='时间 `O(n)`，空间 `O(n)`（峰数组）',
        problem=['峰：`nums[i]` 比左右邻居都大（`1 <= i <= n-2`）',
                 '子数组 `[l, r]` 合法：==恰好含一个峰==，且峰到两端距离都 `<= k`',
                 '本视频：`nums = [1,3,2,4,1,5,2,0]`，`k = 2` → `14`'],
        quote='包含peak[index]的合法子数组左边界left_bound最多延伸到peak[index - 1] + 1，同时还需要满足peak[index] - left_bound <= k。',
        quote_src='—— yiduobo 题解原文',
        idea=['峰的判断很简单，先扫一遍把峰下标存进 `peak`',
              '含峰 `p` 的子数组，左端不能碰前一个峰，也不能离 `p` 超过 `k`：`min(p − pre, k + 1)` 种',
              '右端同理 `min(nxt − p, k + 1)` 种，两边相乘，各峰相加'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '第一个峰前一个峰设为 `-1`，最后一个峰后一个峰设为 `n`，免去特判边界',
                 '易错点：`k` 是距离上限，所以可选个数是 `k + 1`（包含峰自己）',
                 '子数组恰含一个峰，所以按峰分类互不重复'],
    ),
)
