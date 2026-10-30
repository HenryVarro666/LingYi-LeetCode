CONFIG = dict(
    num=2281, title='巫师的总力量和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='单调栈求边界 + 前缀和的前缀和（贡献法）',
    tags=['单调栈', '难度分 2621'],
    code='''
class Solution:
    def totalStrength(self, strength: List[int]) -> int:
        n = len(strength)
        # left[i] 为左侧严格小于 strength[i] 的最近元素位置（不存在时为 -1）
        left = [-1] * n
        # right[i] 为右侧小于等于 strength[i] 的最近元素位置（不存在时为 n）
        right = [n] * n
        st = []
        for i, v in enumerate(strength):
            while st and strength[st[-1]] >= v:
                right[st.pop()] = i
            if st:
                left[i] = st[-1]
            st.append(i)

        ss = list(accumulate(accumulate(strength, initial=0), initial=0))  # 前缀和的前缀和

        ans = 0
        for i, v in enumerate(strength):
            l, r = left[i] + 1, right[i] - 1  # [l, r]  左闭右闭
            tot = (i - l + 1) * (ss[r + 2] - ss[i + 1]) - (r - i + 1) * (ss[i + 1] - ss[l])
            ans += v * tot  # 累加贡献
        return ans % 1_000_000_007
''',
    call='Solution().totalStrength([5,4,6,2,3])',
    expect=402,
    views=[
        dict(type='text', h=44, fn=lambda S: (
            f"以 `strength[{S['i']}]={S['v']}` 为最小值：区间 `[{S['l']}, {S['r']}]`，所有含它的子数组和之和 = ==`{S['tot']}`==，贡献 `{S['v']}×{S['tot']}`"
            if S.get('_line', 0) in (21, 22) else
            (f"以 `strength[{S['i']}]={S['v']}` 为最小值：它管辖区间 `[{S['l']}, {S['r']}]`" if S.get('_line') == 20 else None) or
            ('第一遍：单调栈找每个元素的左右边界' if 'ss' not in S else '第二遍：用前缀和的前缀和算每个元素的贡献'))),
        dict(type='array', var='strength', label='strength', h=120, pointers={'i': 'blue'},
             window=(lambda S: S['l'] if S['_line'] > 19 else None, lambda S: S['r'] if S['_line'] > 19 else None),
             color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='stack', var='st', h=110, fmt=lambda i: str(i)),
        dict(type='array', var='left', label='left', h=100),
        dict(type='array', var='right', label='right', h=100),
        dict(type='array', var='ss', label='ss', h=100),
    ],
    watch=['i', 'v', 'l', 'r', ('tot', 'tot', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'while st and': lambda S, B, ret: (
            f"栈顶 `strength[{S['st'][-1]}]` = {S['strength'][S['st'][-1]]}，`>= {S['v']}` ==成立==：它右边第一个不大于它的就是下标 `{S['i']}`，要弹出"
            if S['st'] and S['strength'][S['st'][-1]] >= S['v'] else
            ('栈空了，不用再弹' if not S['st'] else f"栈顶 `strength[{S['st'][-1]}]` = {S['strength'][S['st'][-1]]} 严格小于 `{S['v']}` → 停止弹栈")),
        'right[st.pop()] = i': '栈顶不比 `{v}` 小 → ==它的右边界就是 `{i}`==，弹出',
        'left[i] = st[-1]': '栈里剩下的栈顶严格小于 `{v}` → `left[{i}] = {left[i]}`',
        'st.append(i)': '下标 `{i}` 入栈，栈保持单调递增',
        'ss = list': '`ss` = 前缀和的前缀和：之后能 O(1) 求出「一堆子数组和之和」',
        'l, r = left': '`strength[{i}]` 是最小值的范围：`[{l}, {r}]`（边界外一个是更小的数）',
        'tot = (': '左端点 `{i-l+1}` 种、右端点 `{r-i+1}` 种，子数组和之和 = ==`{tot}`==',
        'ans += v * tot': '贡献 = 最小值 `{v}` × 和之和 `{tot}`，累加：`ans = {ans}`',
        'return ans': '最后对 `10^9+7` 取模：`{ans} % 1000000007`',
    },
    cards=dict(
        one_liner='枚举每个巫师当「最弱者」，算他管辖范围内的和之和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组的总力量 = ==最小值 × 元素和==，求所有子数组总力量之和（模 `10^9+7`）',
                 '示例：`[1,3,1,2]` → `44`；`[5,4,6]` → `213`',
                 '本视频用 `[5,4,6,2,3]` 演示'],
        quote='左侧==严格小于==当前元素的最近元素位置 L-1，以及右侧==小于等于==当前元素的最近元素位置 R+1。',
        quote_src='—— 灵茶山艾府题解 提示 1-5',
        idea=['枚举每个 `strength[i]` 当最小值，单调栈求它能管到的 `[L, R]`',
              '一边严格小于、一边小于等于，重复元素不会重复统计',
              '子数组和 = `s[r+1]-s[l]`；再做一次前缀和 `ss`，就能一步算出所有 (l, r) 的和之和'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：左边「严格小于」、右边「小于等于」，只能一边带等号',
                 '`ss` 比 `s` 再多一层前缀，下标带 `+2`；答案最后统一取模，Python 不会溢出',
                 '同类：907 子数组的最小值之和（去掉和的那一层）'],
    ),
)
