def _text(S):
    ln = S.get('_line')
    if 'ma' in S and 'index' in S and 'suffix' in S and ln in (11, 12, 13, 16, 17, 18):
        i = S['index']
        if i < len(S['suffix']):
            return f"下标 `{i}`：不稳定值 = 前缀最大 `{S['ma']}` − 后缀最小 `{S['suffix'][i]}` = =={S['ma'] - S['suffix'][i]}== （k = {S['k']}）"
    if 'suffix' in S and len(S['suffix']) < len(S['nums']):
        return '先从后往前预处理：`suffix` 依次记录后缀最小值（此时是倒着存的）'
    return '前缀最大值边遍历边算，后缀最小值用预处理好的 `suffix`'


def _suf_mark(S, i, v):
    if 'index' in S and 'ma' in S and len(S['suffix']) == len(S['nums']) and i == S['index'] and S.get('_line', 0) >= 11:
        return 'pink'
    return None


CONFIG = dict(
    num=3903, title='最小稳定下标 I', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='后缀最小值预处理 + 前缀最大值', tags=[],
    code='''
class Solution(object):
    def firstStableIndex(self, nums, k):
        
        n = len(nums)
        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(min(suffix[-1], nums[index]))
        
        suffix.reverse()
        ma = nums[0]
        v = ma - suffix[0]
        if v <= k:
            return 0
        for index in range(1, n):
            ma = max(ma, nums[index])
            v = ma - suffix[index]
            if v <= k:
                return index
        return -1
''',
    call='Solution().firstStableIndex([5, 0, 1, 4, 6], 3)',
    expect=3,
    views=[
        dict(type='text', fn=_text, size=28, h=80),
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue'}, cell=100, h=230,
             color=lambda S, i, v: 'cyan' if 'ma' in S and 'index' in S and S.get('_line', 0) >= 11 and v == S['ma'] and i <= S['index'] else None),
        dict(type='array', var='suffix', label='suffix[i] = min(nums[i..n-1])（建表时倒着存，reverse 后与下标对齐）', cell=100,
             color=_suf_mark, h=230),
    ],
    watch=[('index', 'index', 'blue'), ('ma', 'ma', 'cyan'), ('v', 'v', 'yellow'), ('k', 'k', 'green')],
    skip=['n = len(nums)'],
    captions={
        'suffix = [nums[-1]]': '从最后一个元素开始：`suffix` 先放 `nums[-1] = {nums[-1]}`',
        'for index in range(n - 2': lambda S, B, r: ('下标已经倒着走完，`suffix` 建好了' if 'index' in B and B.index == S.index else f'倒着往前，当前下标 `{S.index}`' if S.index != S.n - 1 else '倒着遍历下标 `n-2 ... 0`'),
        'suffix.append': '`min({B.suffix[-1]}, nums[{index}]={nums[index]})` = {suffix[-1]}：把 `nums[{index}..]` 的最小值追加进 `suffix`',
        'suffix.reverse()': '`suffix` 是从后往前存的，反转后 `suffix[i]` 正好是 `nums[i..n-1]` 的最小值 = {suffix}',
        'ma = nums[0]': '前缀最大值 `ma` 从 `nums[0] = {ma}` 开始',
        'v = ma - suffix[0]': '下标 0：不稳定值 `{ma} − {suffix[0]}` = =={v}==',
        'if v <= k': lambda S, B, r: f'`v = {S.v}` {"≤" if S.v <= S.k else ">"} `k = {S.k}`' + ('，==稳定下标，就是最小的==' if S.v <= S.k else '，不稳定，继续往后'),
        'for index in range(1, n)': lambda S, B, r: f'枚举下一个下标 `index = {S.index}`，`ma` 只需要随着往后扫描更新',
        'ma = max(ma, nums[index])': '前缀最大值：`max({B.ma}, nums[{index}]={nums[index]})` = =={ma}==',
        'v = ma - suffix[index]': '下标 `{index}`：`{ma} − {suffix[index]}` = =={v}==',
        'return index': '这是第一个稳定下标：返回 =={ret}==，从前往后扫所以一定最小',
        'return 0': '下标 0 就稳定，返回 0',
        'return -1': '所有下标都不稳定，返回 `-1`',
    },
    cards=dict(
        one_liner='从前往后找第一个稳定下标：前缀最大边走边算，后缀最小先预处理',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['不稳定值：`max(nums[0..i]) − min(nums[i..n-1])`',
                 '不稳定值 `<= k` 的下标叫稳定下标',
                 '返回最小的稳定下标，没有则返回 `-1`',
                 '示例：`[5,0,1,4], k = 3` → `3`；本视频用 `[5,0,1,4,6]`'],
        quote='对于前缀最大值，可以随着index的遍历进行计算，而对于后缀最小值，则可以进行预处理，从后往前遍历一遍，计算出每个后缀中的最小值。',
        quote_src='—— yiduobo 题解原文',
        idea=['要最小的下标 → ==从前往后==枚举，遇到第一个满足的就返回',
              '后缀最小值要从后往前算：先预处理出 `suffix` 数组',
              '前缀最大值 `ma` 随遍历一路 `max` 更新，用 `ma - suffix[index]` 判断'],
        summary=['时间 `O(n)`，空间 `O(n)`（`suffix` 数组）',
                 '`suffix` 是倒着 append 的，==必须 reverse== 后才和下标对齐',
                 '下标 0 要单独判断（前缀最大就是 `nums[0]`），循环从 1 开始',
                 '同系列 3904 数据范围 `10^5`，这个 `O(n)` 解法同样适用',
                 '原文为 Python 2 风格（class Solution(object)），无需修改'],
    ),
)
