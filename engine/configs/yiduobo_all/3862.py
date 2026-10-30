def _txt(S):
    L = S['_line']
    if L <= 6:
        return '先算前缀和 `s`：`s[i]` = `nums[0..i-1]` 之和'
    if L <= 15:
        return '再倒着算后缀积 `m`：太大就压成 `总和 + 1`（反正永远不会相等）'
    if 'index' in S:
        i = S['index']
        return f'`left = s[{i}] = {S["s"][i]}`，`right = m[{i+1}] = {S["m"][i+1]}`'
    return ''


def _color(S, i, v):
    return None


CONFIG = dict(
    num=3862, title='找出最小平衡下标', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='前缀和数组 + 后缀积数组',
    tags=['滑动窗口与双指针', '动态规划', '难度分 1697'],
    code='''
class Solution(object):
    def smallestBalancedIndex(self, nums):
        
        s = [0]
        for v in nums:
            s.append(s[-1] + v)
        
        m = [1]
        for v in nums[::-1]:
            if m[-1] == s[-1] + 1:
                m.append(m[-1])
            else:
                m.append(m[-1] * v)
                if m[-1] > s[-1]:
                    m[-1] = s[-1] + 1
        m.reverse()
        
        for index in range(len(nums)):
            left = s[index]
            right = m[index + 1]
            if left == right:
                return index
        
        return -1
''',
    call='Solution().smallestBalancedIndex([2,8,2,2,5])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', h=130, label='nums',
             color=lambda S, i, v: 'blue' if S['_line'] >= 18 and S.get('index') == i else None),
        dict(type='array', var='s', h=130, label='s（前缀和，s[i] = 左侧之和）',
             color=lambda S, i, v: 'green' if S['_line'] >= 18 and S.get('index') == i else None),
        dict(type='array', var='m', h=130, label='m（后缀积，m[i] = nums[i..] 之积）',
             color=lambda S, i, v: 'orange' if S['_line'] >= 18 and S.get('index') is not None and S['index'] + 1 == i else None),
    ],
    watch=[('v', 'v', 'cyan'), ('index', 'index', 'blue'), ('left', 'left', 'green'), ('right', 'right', 'orange')],
    captions={
        's = [0]': '`s[0] = 0`：空前缀之和为 0',
        'for v in nums:': lambda S, B, r: ('`nums` 扫完，前缀和 `s` 建好了' if len(S.s) == len(S.nums) + 1 else f'取 `v = {S.v}`'),
        'for v in nums[::-1]': lambda S, B, r: ('`nums` 倒着扫完了，后缀积 `m` 建好（顺序还是反的）' if len(S.m) == len(S.nums) + 1 else f'从右往左取 `v = {S.v}`'),
        's.append': '`s` 追加 `{s[-2]} + {v}` = =={s[-1]}==',
        'm = [1]': '`m[0] = 1`：空后缀之积为 1（此时 `m` 是倒着建的）',
        'if m[-1] == s[-1] + 1': lambda S, B, r: (f'`m[-1] = {S.m[-1]}` 已经是 `总和 + 1 = {S.s[-1] + 1}`：不用再乘' if S.m[-1] == S.s[-1] + 1
                                                  else f'`m[-1] = {S.m[-1]}` 还没到上限 `{S.s[-1] + 1}`，继续乘'),
        'm.append(m[-1])': '已超上限，继续沿用 `{m[-1]}`',
        'm.append(m[-1] * v)': '后缀积 `{m[-2]} × {v}` = {m[-1]}',
        'if m[-1] > s[-1]': lambda S, B, r: (f'`{S.m[-1]} > 总和 {S.s[-1]}`：不可能等于任何前缀和，压成 `{S.s[-1] + 1}`' if S.m[-1] > S.s[-1]
                                             else f'`{S.m[-1]} <= 总和 {S.s[-1]}`：保持原值'),
        'm[-1] = s[-1] + 1': '后缀积太大了 → 记成 `总和 + 1` = =={m[-1]}==，防止数字爆炸',
        'm.reverse()': '翻转：现在 `m[i]` 是 `nums[i..n-1]` 的积，`m[i+1]` 就是右侧之积：`{m}`',
        'for index in range': '枚举 `index = {index}`',
        'left = s[index]': '左侧之和 `s[{index}]` = =={left}==',
        'right = m[index + 1]': '右侧之积 `m[{index+1}]` = =={right}==',
        'if left == right': '`left = {left}` 与 `right = {right}` → {"相等！" if left == right else "不等"}',
        'return index': '`index = {index}` 是最小的平衡下标',
    },
    cards=dict(
        one_liner='先算好前缀和、后缀积两个数组，再扫一遍对照',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['下标 `index` 左侧元素之和 == 右侧元素之积，称为平衡下标',
                 '左侧没有元素和为 `0`，右侧没有元素积为 `1`',
                 '求最小的平衡下标，不存在返回 `-1`',
                 '示例：`[2,8,2,2,5]` → `2`'],
        quote='若目前的后缀积已经大于整个数组之和，那么就将当前后缀积以及接下来的其他后缀积都视为数组之和加1。',
        quote_src='—— yiduobo 题解原文',
        idea=['左侧之和 = 前缀和，右侧之积 = 后缀积：先正反各扫一趟存成数组 `s`、`m`',
              '后缀积会爆炸：一旦超过总和，之后都当作 `总和 + 1`',
              '最后一趟遍历：`s[index] == m[index + 1]` 就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`m` 是倒着建的，用之前要 `m.reverse()`，右侧积取 `m[index + 1]`',
                 '压成 `总和 + 1` 后永远不会等于任何前缀和，结果不受影响',
                 '原文已是 Python 3 可运行写法，代码未改动',
                 '对比灵神：灵神用相向双指针 `O(1)` 空间；这里用两个数组更直观'],
    ),
)
