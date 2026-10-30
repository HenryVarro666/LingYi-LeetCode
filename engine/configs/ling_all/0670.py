def _txt(S):
    if 'max_idx' not in S:
        return ''
    s = S['s']
    p, q = S['p'], S['q']
    if p == -1:
        return f"`max_idx = {S['max_idx']}`（右侧最大 =={s[S['max_idx']]}==）　还没找到要交换的位置"
    return f"`max_idx = {S['max_idx']}`（右侧最大 =={s[S['max_idx']]}==）　待交换：`s[{p}] = {s[p]}` ↔ `s[{q}] = {s[q]}`"


CONFIG = dict(
    num=670, title='最大交换', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='字符串贪心 · 倒序维护最大值',
    tags=['灵神题单', '字符串贪心'],
    code='''
class Solution:
    def maximumSwap(self, num: int) -> int:
        s = str(num)
        max_idx = len(s) - 1
        p = q = -1
        for i in range(len(s) - 2, -1, -1):
            if s[i] > s[max_idx]:  # s[i] 是目前最大数字
                max_idx = i
            elif s[i] < s[max_idx]:  # s[i] 右边有比它大的
                p, q = i, max_idx  # 更新 p 和 q
        if p == -1:  # 这意味着 s 是降序的
            return num
        s = list(s)
        s[p], s[q] = s[q], s[p]  # 交换 s[p] 和 s[q]
        return int(''.join(s))
''',
    call='Solution().maximumSwap(9952767)',
    expect=9972765,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='s', label='s（蓝 = 右侧最大 max_idx，粉 = 当前 i，橙 = 待交换 p）', cell=90, h=230,
             pointers={'i': 'pink', 'max_idx': 'blue', 'p': 'orange', 'q': 'green'},
             color=lambda S, k, v: ('orange' if k == S.get('p') else 'green' if k == S.get('q') else None) if S.get('p', -1) >= 0 else None),
    ],
    watch=['i', ('max_idx', 'max_idx', 'blue'), ('p', 'p', 'orange'), ('q', 'q', 'green')],
    captions={
        's = str': '`num` 转成字符串 `s = "{s}"`',
        'max_idx = len': '`max_idx` 记录==当前右侧最大数字==的下标，先指向最后一位 `{max_idx}`',
        'p = q = -1': '`p`、`q` 是要交换的两个下标，`-1` 表示还没找到',
        'for i in range': lambda S, B, r: ('扫描结束' if B.get('i') == S.get('i') else f'从右往左看 `i = {S.i}`，`s[i] = {S.s[S.i]}`'),
        'if s[i] > s[max_idx]': lambda S, B, r: (f"`{S.s[S.i]}` > `{S.s[S.max_idx]}`：比右边都大，成为新的最大数字" if S.s[S.i] > S.s[S.max_idx]
                                                  else f"`{S.s[S.i]}` ≤ `{S.s[S.max_idx]}`：不比当前最大数字大"),
        'max_idx = i': '`max_idx` → {max_idx}：只有==严格更大==才更新，相同数字保留靠右的那个',
        'elif s[i] < s[max_idx]': lambda S, B, r: (f"`{S.s[S.i]}` < `{S.s[S.max_idx]}`：右边有比它大的 → 值得交换" if S.s[S.i] < S.s[S.max_idx]
                                                   else f"`{S.s[S.i]}` == `{S.s[S.max_idx]}`：相同数字，交换没收益，也不更新"),
        'p, q = i, max_idx': '记下 `p = {p}`，`q = {q}`；继续往左，==越靠左的 p 越好==，会覆盖旧值',
        'if p == -1': lambda S, B, r: ('`p == -1`：没有可换的 → s 是降序，已经最大' if S.p == -1
                                       else f'`p = {S.p}`，有可交换的一对'),
        'return num': 's 本身降序，直接返回 `num`',
        's = list': '字符串不能改，转成列表',
        's[p], s[q] = ': '交换 `s[{p}]` 和 `s[{q}]`：大数字换到更靠前的位置 → `{"".join(s)}`',
        "return int": '拼回数字 =={ret}==',
    },
    cards=dict(
        one_liner='倒着扫，换最左边「右边有更大数」的那位',
        complexity='时间 `O(log num)`，空间 `O(log num)`',
        problem=['最多交换一次数字中任意两位，求能得到的最大值',
                 '示例：`2736` → `7236`；`9973` → `9973`（不用换）',
                 '本视频：`9952767` → `9972765`'],
        quote='和最后一个 7 交换是最优的。倒序遍历 s，同时维护最大数的下标 maxIdx。它只在遇到更大的数字才更新，遇到相同数字不会更新。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数字右边没有更大的，无需交换；有更大的就必须换，换成右边==最大的那个==',
              '最大数字有多个，换==最后一个==，这样小数字被换到更低位',
              '倒着扫：每发现右边有更大数就覆盖 `p, q`，最终留下==最靠左==的一对'],
        summary=['时间 `O(log num)`，空间 `O(log num)`',
                 '`s[i] > s[max_idx]` 才更新 `max_idx`，相等不更新，才能取到最后一个最大数',
                 '`p` 只会越来越靠左，所以不用 break',
                 '`p == -1` 表示本来就是降序，不用交换',
                 '思考题：限制距离 `k`、或允许交换两次，贪心要再细化'],
    ),
)
