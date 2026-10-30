def _color(S, i, v):
    if 'pre' not in S or 'p' not in S or S.get('res') is None:
        return None
    pre, p = S['pre'], S['p']
    if S['_line'] < _LLOOP:
        return 'green' if (v % 2 == 0 and i == pre) else None
    if i == pre:
        return 'green'
    if i < pre:
        return 'blue'
    if i < p:
        return 'yellow'
    if i == p:
        return 'orange'
    return None


def _txt(S):
    if 'res' not in S:
        return '偶数 × 任何数 = 偶数：子数组里只要有一个偶数，乘积就是偶数'
    pre, p = S['pre'], S['p']
    n = len(S['nums'])
    if pre >= n:
        return '没有偶数：任何子数组乘积都是奇数 → 答案 0'
    if S['_line'] < _LLOOP:
        return f"`pre = {pre}`（最右偶数），`p = {p}`（下一个偶数）"
    if p > n - 1 + 1 and S['_line'] == _LLOOP:
        return f"`pre = {pre}`（最右偶数），`p = {p}`（下一个偶数）"
    return f"起点 `0 ~ {pre}` 共 `{pre + 1}` 种 × 终点 `{pre} ~ {p - 1}` 共 `{p - pre}` 种 = ==`{(pre + 1) * (p - pre)}`=="


CODE = '''
class Solution(object):
    def evenProduct(self, nums):

        pre = 0
        while pre < len(nums) and nums[pre] % 2 == 1:
            pre += 1
        
        p = pre + 1
        res = 0
        while pre < len(nums):
            while p < len(nums) and nums[p] % 2 == 1:
                p += 1
            
            res += (p - pre) * (pre + 1)
            pre = p
            p += 1
        
        return res
'''
_LS = CODE.strip('\n').split('\n')
_LLOOP = [i + 1 for i, s in enumerate(_LS) if s.strip() == 'while pre < len(nums):'][0]

CONFIG = dict(
    num=2495, title='乘积为偶数的子数组数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按最右偶数计数 · 双指针找下一个偶数',
    tags=['灵神题单'],
    code=CODE,
    call='Solution().evenProduct([9,6,7,13,2])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（绿 = pre 最右偶数，蓝 = 可选起点，黄 = 可选终点，橙 = p）', cell=100, h=250,
             pointers={'pre': 'green', 'p': 'orange'}, color=_color),
        dict(type='text', h=100, size=30, fn=_txt),
    ],
    watch=[('pre', 'pre', 'green'), ('p', 'p', 'orange'), ('res', 'res', 'green')],
    captions={
        'pre = 0': '`pre`：当前考虑的偶数的下标，先从 0 开始',
        'while pre < len(nums) and nums[pre] % 2 == 1': lambda S, B, ret: (
            f'`nums[{S.pre}] = {S.nums[S.pre]}` 是奇数 → 它不可能是最右偶数，跳过' if S.pre < len(S.nums) and S.nums[S.pre] % 2 == 1
            else (f'`nums[{S.pre}] = {S.nums[S.pre]}` 是偶数：第一个偶数找到了' if S.pre < len(S.nums) else '没有偶数了')),
        'pre += 1': '`pre` → `{pre}`',
        'p = pre + 1': '`p` 从 `pre` 后一位出发，去找==下一个偶数==',
        'res = 0': '`res` 累计答案',
        'while pre < len(nums):': lambda S, B, ret: (f'`pre = {S.pre}` 是一个偶数，统计“最右偶数恰为 `pre`”的子数组' if S.pre < len(S.nums)
                                                     else f'`pre = {S.pre}` 已经越过数组末尾：所有偶数都算完了'),
        'while p < len(nums) and nums[p] % 2 == 1': lambda S, B, ret: (
            f'`nums[{S.p}] = {S.nums[S.p]}` 是奇数，终点还能继续右延' if S.p < len(S.nums) and S.nums[S.p] % 2 == 1
            else (f'`nums[{S.p}] = {S.nums[S.p]}` 是偶数：它就是下一个偶数，终点最远到 `p - 1 = {S.p - 1}`' if S.p < len(S.nums)
                  else '`p` 到头了，终点最远到数组末尾')),
        'p += 1': '`p` → `{p}`',
        'res += (p - pre) * (pre + 1)': '起点 `0 ~ pre` 共 `{pre + 1}` 种，终点 `pre ~ p-1` 共 `{p - pre}` 种 → 增加 `{(p - pre) * (pre + 1)}`，`res = {res}`',
        'pre = p': '最右偶数换成 `p`：`pre = {pre}`',
        'return res': '返回 `{res}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='有一个偶数就够了：按“最右偶数”分类计数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['求 `nums` 里==乘积为偶数==的子数组个数',
                 '示例：`nums = [9,6,7,13]` → `6`',
                 '本视频：`nums = [9,6,7,13,2]`，答案 `11`'],
        quote='对于数组中的任意子数组，只需其中存在一个偶数，该子数组的乘积就是偶数。为了避免重复计算，在这里可以对于数组中的每个偶数，统计以该偶数为最右侧偶数的子数组数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘积为偶 ⇔ 子数组里至少一个偶数',
              '每个子数组只有一个“最右偶数”，按它分类才不重不漏',
              '最右偶数在 `pre`、下一个偶数在 `p`：起点 `0 ~ pre`，终点 `pre ~ p-1`，共 `(pre+1)*(p-pre)` 个'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '没有偶数时第一个循环把 `pre` 推到 `len(nums)`，直接返回 `0`',
                 '最后一个偶数的 `p` 会走到 `len(nums)`，终点一直延伸到数组末尾',
                 '原文题目只有 vip 题，本视频题意按 LeetCode 2495 补写'],
    ),
)
