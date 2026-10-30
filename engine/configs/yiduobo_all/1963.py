def _color(S, i, v):
    if 'l' not in S or 'r' not in S:
        return None
    if i == S['l'] and i != S['r']:
        return 'blue'
    if i == S['r']:
        return 'pink'
    if i > S['r']:
        return 'orange' if v == '[' else None
    return None


def _txt(S):
    if 'cnt' not in S:
        return ''
    return f"`cnt = {S['cnt']}`：左边多出来、还没配对的 `[` 个数；已交换 `res = {S.get('res', 0)}` 次"


CONFIG = dict(
    num=1963, title='使字符串平衡的最小交换次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='扫描 + 右指针找最靠右的左括号',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1689'],
    code='''
class Solution(object):
    def minSwaps(self, s):

        r = len(s) - 1
        while s[r] != '[':
            r -= 1

        cnt = 0
        l = 0
        res = 0
        while l < r:
            if s[l] == '[':
                cnt += 1
            elif cnt > 0:
                cnt -= 1
            else:
                res += 1
                cnt += 1
                r -= 1
                while r > l and s[r] != '[':
                    r -= 1
        
            l += 1

        return res
''',
    call='Solution().minSwaps("]]][[][[")',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='string', var='s', label='s（蓝 = l 扫描位置，粉 = r 最右边的左括号）', cell=80,
             pointers={'l': 'blue', 'r': 'pink'}, color=_color, h=220),
        dict(type='text', fn=lambda S: ('这一步：`cnt == 0` 却遇到 `]` → 与 ==r 处的 `[`== 交换（只记次数）' if S.get('_line') in (17, 18, 19, 20) else '平衡 = 任意前缀里 `[` 不比 `]` 少'), size=26),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('cnt', 'cnt', 'yellow'), ('res', 'res', 'green')],
    captions={
        'r = len(s) - 1': '`r` 先指向末尾，准备找最靠右的 `[`',
        'while s[r] != ': lambda S, B, r_: (f"`s[{S.r}] = '{S.s[S.r]}'` 不是 `[` → `r` 继续左移" if S.s[S.r] != '[' else f"`s[{S.r}] = '['`：`r` 就是最右边的左括号"),
        6: '`r` → {r}，继续往左找 `[`',
        21: '`r` → {r}，继续往左找',
        'cnt = 0': '`cnt`：当前多出来的未配对左括号',
        'l = 0': '`l` 从左向右扫描',
        'res = 0': '`res` 记录交换次数',
        'while l < r': lambda S, B, r_: (f"`l = {S.l} < r = {S.r}`，继续扫描" if S.l < S.r else f"`l = {S.l}` 追上 `r = {S.r}`：后面都是换过去的 `[`，不会再出问题，结束"),
        "if s[l] == '['": lambda S, B, r_: (f"`s[{S.l}]` 是左括号 → `cnt` + 1" if S.s[S.l] == '[' else f"`s[{S.l}]` 是右括号，看有没有左括号可配"),
        'cnt += 1': lambda S, B, r_: (f"`cnt` → {S.cnt}" if S.s[S.l] == '[' else f"换来了一个 `[`：`cnt` → {S.cnt}"),
        'elif cnt > 0': lambda S, B, r_: (f"`cnt = {S.cnt} > 0`，这个 `]` 有左括号可配" if S.cnt > 0 else f"`cnt = 0`：右括号比左括号多，出现不匹配，要交换"),
        'cnt -= 1': '右括号配掉一个左括号：`cnt` → {cnt}',
        'res += 1': '与最靠右的 `[`（下标 `{r}`）交换，次数 `res` → =={res}==',
        19: lambda S, B, r_: f"那个 `[` 用掉了，`r` 左移到 {S.r}",
        'while r > l and': lambda S, B, r_: (f"`r = {S.r} > l`，`s[{S.r}] = '{S.s[S.r]}'` 不是 `[` → 继续左移找新的最右 `[`" if S.r > S.l and S.s[S.r] != '[' else f"`r = {S.r}` 是新的最靠右的 `[`，或已到 `l`"),
        'l += 1': '`l` → {l}',
        'return res': '最少交换 `{res}` 次',
    },
    max_steps=90,
    cards=dict(
        one_liner='右括号多了就和最靠右的左括号换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 由相同数量的 `[` 和 `]` 组成，可任意交换两个位置的括号',
                 '返回使 `s` 成为平衡字符串的最少交换次数',
                 '示例：`][][` → `1`；本视频：`]]][[][[` → `2`'],
        quote='最具性价比的交换自然是让当前多出来的右括号与位置在最后面的左括号进行交换。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左到右扫描，某一时刻右括号多于左括号就不匹配',
              '用指针 `r` 标出最靠右的 `[`，交换后左移找新的',
              '扫描位置 `l` 追上 `r` 时，右边已全是换过去的 `[`，可以结束'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '交换只是计数：`cnt += 1` 相当于把 `]` 当成了换来的 `[`',
                 '易错：`r` 左移时要判断 `r > l`，避免越过扫描位置',
                 '原文代码在 Python 3 下可直接运行，未做修改',
                 '对比灵神：灵神最后不用 `r`，直接 `c // 2` 求答案'],
    ),
)
