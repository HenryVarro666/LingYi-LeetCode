def _text(S):
    if 'index' in S and 'res' in S and S['_line'] >= 14:
        return f"分割在 `{S['index']}`：`s[{S['index']}] - mi[{S['index'] + 1}]` = {S['s'][S['index']]} − ({S['mi'][S['index'] + 1]}) = =={S['s'][S['index']] - S['mi'][S['index'] + 1]}==，当前 `res = {S['res']}`"
    if 's' in S and 'mi' not in S:
        return f"`s` = 前缀和数组，已算 {len(S['s'])} 个"
    if 'mi' in S and '_line' in S and S['_line'] < 13:
        return f"`mi` 倒着收集后缀最小值，已算 {len(S['mi'])} 个（最后会 reverse）"
    return ''


CONFIG = dict(
    num=3788, title='分割的最大得分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='正反两趟建前缀和与后缀最小值数组',
    tags=['灵神题单', '动态规划', '难度分 1306'],
    code='''
class Solution(object):
    def maximumScore(self, nums):
        
        s = [nums[0]]
        for v in nums[1:]:
            s.append(s[-1] + v)
        
        mi = [nums[-1]]
        for v in nums[-2::-1]:
            mi.append(min(mi[-1], v))
        mi.reverse()
        
        res = s[0] - mi[1]
        for index in range(1, len(nums) - 1):
            res = max(res, s[index] - mi[index + 1])
        
        return res
''',
    call='Solution().maximumScore([5,3,-1,4,2,6])',
    expect=9,
    views=[
        dict(type='text', fn=_text, size=26),
        dict(type='array', var='nums', label='nums', h=190),
        dict(type='array', var='s', label='s：前缀和 s[i] = nums[0..i]', h=190, pointers={'index': 'pink'}),
        dict(type='array', var='mi', label='mi：mi[i] = nums[i..] 的最小值', h=190,
             color=lambda S, i, v: 'orange' if 'index' in S and S['_line'] >= 13 and i == S['index'] + 1 else None),
    ],
    watch=[('v', 'v', 'yellow'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    captions={
        's = [nums[0]]': '前缀和数组先放第一个数 `s = {s}`',
        's.append': '`s[-1] + v`：上一个前缀和 `{s[-2]}` 加上 `{v}` = `{s[-1]}`',
        'mi = [nums[-1]]': '后缀最小值从最后一个数开始 `mi = {mi}`，倒着往前走',
        'mi.append': '`min(mi[-1], v)`：已见最小 `{mi[-2]}` 与新数 `{v}` 取小 = `{mi[-1]}`',
        'mi.reverse': '倒着收集的，翻转后 `mi[i]` 就表示 `nums[i]` 开始的后缀最小值：`{mi}`',
        'res = s[0]': '先把 `index = 0` 的得分作初值：`s[0] - mi[1] = {s[0]} - ({mi[1]}) = {res}`',
        'res = max': '`index = {index}`：前缀 `s[{index}] = {s[index]}`，后缀从 `{index + 1}` 起最小 `mi[{index + 1}] = {mi[index + 1]}`，得分 `{s[index] - mi[index + 1]}`，`res = max({B.res}, ...) = {res}`',
        'return res': '所有分割点都比过了，最大得分 ==`{res}`==',
    },
    cards=dict(
        one_liner='先把前缀和、后缀最小值各算一张表，再枚举切点查表',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `0..n-2` 里选分割下标 `index`',
                 '得分 = `prefixSum(index) - suffixMin(index)`，后缀从 `index+1` 开始',
                 '求所有合法分割的最大得分'],
        quote='为了方便，在这里可以修改为 suffixMin(index) 表示的就是 nums[index] 开始的后缀中的最小值，在计算得分时则需要改成 prefixSum(index) - suffixMin(index + 1)。',
        quote_src='—— yiduobo 题解',
        idea=['正着扫一趟得到前缀和数组 `s`',
              '倒着扫一趟再翻转，得到 `mi[i] = nums[i:] 的最小值`',
              '枚举 `index`，得分就是 `s[index] - mi[index + 1]`，取最大'],
        summary=['时间 `O(n)`，空间 `O(n)`（两个辅助数组）',
                 '下标偏移：后缀从 `index + 1` 开始，所以查 `mi[index + 1]`',
                 '`res` 用 `index = 0` 的得分做初值，而不是 0（得分可能为负）',
                 '`nums[-2::-1]` 是从倒数第二个往前走到头'],
    ),
)
