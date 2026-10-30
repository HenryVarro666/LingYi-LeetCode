def _x(S):
    pl = S.get('pos_list')
    return S['nums'][pl[0]] if pl else None


def _nums_color(S, i, v):
    pl = S.get('pos_list')
    if not pl or v != _x(S):
        return None
    l, r = S.get('left'), S.get('right')
    if l is not None and r is not None and l < len(pl) and r > l and pl[l] <= i <= pl[min(r, len(pl)) - 1]:
        return 'green'
    return 'yellow'


def _txt(S):
    pl = S.get('pos_list')
    if not pl:
        return '先统计每种数字出现的下标，再对每种数字滑一次窗口'
    if S.get('_line') != 19 or S['right'] >= len(pl) or S['left'] >= len(pl):
        return '要删的数量 = 区间长度 − 区间内这个数字的个数'
    l, r = S['left'], S['right']
    span = pl[r] - pl[l] + 1
    cnt = r - l + 1
    return f"检查加入 `pos_list[{r}]`：区间长 `{span}` − 个数 `{cnt}` = 要删 =={span - cnt}== （k = {S['k']}）"


CONFIG = dict(
    num=2831, title='找出最长等值子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='位置列表 + 变长窗口',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1976'],
    code='''
class Solution(object):
    def longestEqualSubarray(self, nums, k):

        pos_dict = {}
        for index, v in enumerate(nums):
            if v not in pos_dict:
                pos_dict[v] = []
            pos_dict[v].append(index)
        
        res = 0
        for v in pos_dict:
            pos_list = pos_dict[v]
            left = 0
            right = 0
            while left < len(pos_list):
                if right < left:
                    right = left
                
                while right < len(pos_list) and pos_list[right] - pos_list[left] + 1 - (right - left + 1) <= k:
                    right += 1
                
                res = max(res, right - left)
                left += 1
        
        return res
''',
    call='Solution().longestEqualSubarray([1,3,2,3,1,3], 1)',
    expect=2,
    views=[
        dict(type='array', var='nums', h=150, label='nums（黄 = 当前数字，绿 = 窗口内保留的）', color=_nums_color),
        dict(type='map', var='pos_dict', h=150, label='pos_dict：数字 → 出现的位置', fmt=lambda k, v: f'{k}: {v}', font=30),
        dict(type='array', var='pos_list', h=240, label='pos_list（当前数字的位置）',
             pointers={'left': 'blue', 'right': 'pink'}),
        dict(type='text', h=100, size=28, fn=_txt),
    ],
    skip=['if v not in pos_dict', 'pos_dict[v] = []'],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('res', 'res', 'green')],
    captions={
        'pos_dict = {}': '哈希表 `pos_dict`：每种数字 → 位置列表',
        'pos_dict[v].append': '数字 `{v}` 出现在下标 `{index}` → `pos_dict[{v}] = {pos_dict[v]}`',
        'pos_list = pos_dict[v]': '只保留数字 `{v}`，位置 `{pos_list}`：其余数字都是要删的',
        'left = 0': '这一组的窗口从第 0 个位置开始',
        'right = 0': '`right` 表示窗口右边界（开区间）',
        'while left < len(pos_list)': '枚举左边界 `left`，为它找最大的 `right`',
        'if right < left': lambda S, B, r: ('`right < left`：窗口为空，`right` 要补到 `left`' if S.right < S.left else '`right >= left`，不用补'),
        'while right < len(pos_list) and': lambda S, B, r: (
            '`right` 已到末尾，不能再扩' if S.right >= len(S.pos_list) else
            f'区间长 `{S.pos_list[S.right] - S.pos_list[S.left] + 1}` − 个数 `{S.right - S.left + 1}` = 要删 `{S.pos_list[S.right] - S.pos_list[S.left] + 1 - (S.right - S.left + 1)}`，'
            + ('`<= k`：==还能扩== ' if S.pos_list[S.right] - S.pos_list[S.left] + 1 - (S.right - S.left + 1) <= S.k else '`> k`：不能再扩')),
        'right += 1': '把这个位置纳入窗口，`right` → {right}',
        'res = max': '窗口里有 `{right - left}` 个相同数字 → `res = max({B.res}, {right - left}) = {res}`',
        'left += 1': '`left` 右移：`right` 只增不减，所以总共 O(n)',
        'return res': '最长等值子数组 =={res}==',
    },
    cards=dict(
        one_liner='先找每个数字的位置，再算「留下它能留多长」',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['删除最多 `k` 个元素后，最长的等值子数组有多长',
                 '示例：`[1,3,2,3,1,3]`，`k=3` → `3`'],
        quote='首先使用一个哈希pos_dict统计每种数字出现的位置列表，接下来遍历每种数组v……再使用变长滑动窗口找出其中每个左边界left对应的最大右边界right',
        quote_src='—— yiduobo 题解原文',
        idea=['只留下数字 `v` 时：区间长 − 区间内 `v` 的个数 = ==要删的数量==',
              '要求这个数量 `<= k`；`left` 后移，`right` 也不会回退',
              '对每个 `left` 用 `right - left` 更新答案'],
        summary=['时间 `O(n)`（`right` 均摊不回退），空间 `O(n)`',
                 '`right` 是开区间右端，窗口长度 = `right - left`',
                 '`if right < left` 别漏：窗口为空时 `right` 要跟上',
                 '对比灵神：灵神把位置减去序号，直接用 `p - pos[left]`；这里保留原位置，显式减个数'],
    ),
)
