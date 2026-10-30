NUMS = [2, 3, 1, 4, 1, 2]


def _loop(S):
    return 'i' in S and 'x' in S and 's' in S


ST = lambda S: max(S['i'] - S['x'], 0) if _loop(S) else None      # noqa: E731
I1 = lambda S: S['i'] + 1 if _loop(S) else None                    # noqa: E731


def _nums_color(S, k, v):
    if _loop(S) and ST(S) <= k <= S['i']:
        return 'cyan'
    return None


def _s_color(S, k, v):
    if _loop(S):
        if k == S['i'] + 1:
            return 'green'
        if k == ST(S):
            return 'red'
    return None


def _formula(S):
    if 's' not in S:
        return ''
    if not _loop(S):
        if S.get('_line') == 7:
            return f"每个下标的子数组和都累加进去了：`ans` = =={S['ans']}=="
        return '`s[k]` = 前 `k` 个数的和，开头垫一个 `s[0] = 0`'
    i, x, s = S['i'], S['x'], S['s']
    st = ST(S)
    if S.get('_line') == 6:
        return (f"`s[{i + 1}] − s[{st}]` = `{s[i + 1]} − {s[st]}` = =={s[i + 1] - s[st]}=="
                f"（子数组 `nums[{st}..{i}]`）")
    return f"`i = {i}`，`x = {x}`：子数组 `nums[{st}..{i}]`，起点 `max({i} − {x}, 0)` = =={st}=="


def _for(S, B, ret):
    if 'i' in B and B.i == S.i and B.x == S.x:
        return '所有下标都处理完了，循环结束'
    st = max(S.i - S.x, 0)
    if S.i - S.x < 0:
        return f'`i = {S.i}`，`x = {S.x}`：`i − x = {S.i - S.x}` 越界 → 起点夹到 ==0=='
    return f'`i = {S.i}`，`x = {S.x}`：子数组从 `{S.i} − {S.x} = {st}` 取到 `{S.i}`'


def _add(S, B, ret):
    i, x = S.i, S.x
    st = max(i - x, 0)
    return (f'`nums[{st}..{i}]` 的和 = `s[{i + 1}] − s[{st}]` = `{S.s[i + 1]} − {S.s[st]}` = =={S.s[i + 1] - S.s[st]}==，'
            f'`ans` {B.ans} → =={S.ans}==')


CONFIG = dict(
    num=3427, title='变长子数组求和', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 · s 长度 n+1',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def subarraySum(self, nums: List[int]) -> int:
        s = list(accumulate(nums, initial=0))
        ans = 0
        for i, x in enumerate(nums):
            ans += s[i + 1] - s[max(i - x, 0)]
        return ans
''',
    call=f'Solution().subarraySum({NUMS})',
    expect=33,
    views=[
        dict(type='text', fn=_formula, h=64),
        dict(type='array', var='nums', label='nums（青 = 当前子数组）', cell=96, h=215, window=(ST, 'i'),
             pointers={ST: 'red', 'i': 'blue'}, pointer_labels={ST: 'start'}, color=_nums_color),
        dict(type='array', var='s', label='s（s[k] = 前 k 个数的和，长度 n+1）', cell=96, h=230,
             pointers={ST: 'red', I1: 'green'}, pointer_labels={ST: 'start', I1: 'i+1'}, color=_s_color),
    ],
    watch=['i', 'x', ('ans', 'ans', 'green')],
    captions={
        's = list(accumulate': '前缀和：`s[k]` 是前 `k` 个数的和，`initial=0` 让 `s[0] = 0` 垫在最前面 → `s = {s}`',
        'ans = 0': '`ans` 累加每个下标对应的子数组和',
        'for i, x in enumerate': _for,
        'ans += s[i + 1]': _add,
        'return ans': '每个下标的子数组和都加完了，返回 `{ret}`',
    },
    cards=dict(
        one_liner='子数组 [start, i] 的和，就是 s[i+1] − s[start]',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['对每个下标 `i`，子数组是 `nums[start..i]`，其中 `start = max(0, i − nums[i])`',
                 '返回==所有这些子数组的元素和之和==',
                 '示例：`[3,1,1,2]` → `13`',
                 '本视频：`[2,3,1,4,1,2]` → `33`'],
        quote='计算 nums 的前缀和，即可 O(1) 计算任意子数组的元素和。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['先算前缀和 `s`：`s[k]` 是 `nums` 前 `k` 个数之和，`s[0] = 0`',
              '每个下标的区间和 `s[i+1] − s[start]`，`O(1)` 出结果',
              '`start` 小于 0 时用 `max(i − x, 0)` 夹到 0，==有 s[0] = 0 就不必特判=='],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：区间 `[start, i]` 的和是 `s[i + 1] − s[start]`，不是 `s[i] − s[start]`',
                 '方法一暴力：每次 `sum(nums[max(i - num, 0): i + 1])`，`O(n^2)`',
                 '方法三差分：算每个 `nums[i]` 被加进答案几次，同样 `O(n)`',
                 '同类题：前缀和基础（303、2559、3152）'],
    ),
)
