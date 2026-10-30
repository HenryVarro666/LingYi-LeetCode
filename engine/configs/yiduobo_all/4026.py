def _tcolor(S, idx, v):
    L, R = S.get('left') or [], S.get('right') or []
    if 'index' in S and 'res' in S:
        i = S['index']
        if idx == R[i] if len(R) > i else False:
            return 'orange'
        if idx == L[i - 1]:
            return 'green'
        return None
    if idx in R and 'res' not in S:
        return 'orange'
    if idx in L:
        return 'green'
    return None


def _p_ptr(S):
    p = S.get('p')
    return p if isinstance(p, int) and 0 <= p < len(S['station']) and 'res' not in S else None


def _top(S):
    if 'res' in S and 'index' in S and S['index'] < len(S['skill']) and S['left'] and len(S['right']) == len(S['skill']):
        i = S['index']
        return f"分割点 p={i}：skill[:{i}] 压在最左 `left[{i-1}]={S['left'][i-1]}`，skill[{i}:] 压在最右 `right[{i}]={S['right'][i]}`"
    if 'right' in S and 'res' not in S:
        return '第二趟：反向遍历，把后缀尽量靠后压紧'
    if 'left' in S:
        return '第一趟：正向遍历，把前缀尽量靠前压紧'
    return ''


CONFIG = dict(
    num=4026, title='工位的最大间隔', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='前缀压左 + 后缀压右',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·动态规划', '难度分 1675'],
    code='''
class Solution(object):
    def maximumGap(self, skill, station):
        
        if len(skill) == 1:
            return 0
        
        left = []
        p = 0
        for s in skill:
            while station[p] != s:
                p += 1
            left.append(p)
            p += 1
        
        right = []
        p = len(station) - 1
        for s in skill[::-1]:
            while station[p] != s:
                p -= 1
            right.append(p)
            p -= 1
        right.reverse()

        res = 0
        for index in range(1, len(skill)):
            res = max(res, right[index] - left[index - 1])
        
        return res
''',
    call="Solution().maximumGap('abcb', 'abbcbdcb')",
    expect=5,
    views=[
        dict(type='text', fn=_top, size=24),
        dict(type='string', var='skill', label='skill（绿 = 已在前缀里，粉 = 当前分割点右边的第一名工人）', cell=84, h=150,
             color=lambda S, k, v: ('pink' if k == S['index'] else 'green' if k < S['index'] else None) if ('res' in S and 'index' in S) else None),
        dict(type='string', var='station', label='station（绿 = 前缀压左的位置，橙 = 后缀压右的位置）', cell=84, h=190,
             pointers={_p_ptr: 'blue'}, pointer_labels={_p_ptr: 'p'}, color=_tcolor),
        dict(type='array', var='left', label='left[i]：skill[:i+1] 最靠前匹配到 station 的下标', cell=84, min_slots=4, h=130),
        dict(type='array', var='right', label='right[i]：skill[i:] 最靠后匹配到 station 的下标', cell=84, min_slots=4, h=130),
    ],
    watch=[('p', 'p', 'blue'), ('left', 'left', 'green'), ('right', 'right', 'orange'), ('res', 'res', 'purple')],
    captions={
        'if len(skill) == 1': '只有一名工人：没有相邻的两名工人，间隔为 0。这里有 `{len(skill)}` 名，继续',
        'left = []': '`left` 记录：匹配 skill 每个前缀时，最靠前能结束在 station 的哪个位置',
        'right = []': '`right` 记录：匹配 skill 每个后缀时，最靠后能开始在 station 的哪个位置',
        'p = 0': '正向扫描 station，`p = 0`',
        'p = len(station) - 1': '反向扫描 station，从最右边开始：`p = {p}`',
        'for s in skill:': lambda S, B, r: ('前缀都压好了' if len(S.left) == len(S.skill) else f"下一个工人技能 `s = '{S.s}'`"),
        'for s in skill[::-1]': lambda S, B, r: ('后缀都压好了' if len(S.right) == len(S.skill) else
                                                 f"从最后一个工人开始：`s = '{S.s}'`" if not S.right else f"前一个工人技能 `s = '{S.s}'`"),
        'while station[p] != s': lambda S, B, r: (f"`station[{S.p}] = '{S.station[S.p]}'` ≠ `'{S.s}'` → 这个工位用不上，`p` 继续走"
                                                  if S.station[S.p] != S.s else f"`station[{S.p}] = '{S.station[S.p]}'` == `'{S.s}'` → 匹配到了"),
        'p += 1': lambda S, B, r: ('`p` 右移一格' if B.p == S.p - 1 and S.station[B.p] != S.s else f'`p` → {S.p}：下一个工人只能用它右边的工位'),
        'p -= 1': lambda S, B, r: ('`p` 左移一格' if S.station[B.p] != S.s else f'`p` → {S.p}：前一个工人只能用它左边的工位'),
        'left.append(p)': '`left` 追加 `{p}`：前缀 `skill[:{len(left)}]` 最靠前压到 `station[{p}]`',
        'right.append(p)': '`right` 追加 `{p}`：后缀最靠后压到 `station[{p}]`',
        'right.reverse()': '`right` 是反着追加的，翻转后 `right[i]` 对应 `skill[i:]` → `{right}`',
        'res = 0': '第三步：枚举分割点 `index`，`skill[index-1]` 和 `skill[index]` 是相邻的两名工人',
        'for index in range': lambda S, B, r: (f'分割点 `index = {S.index}`' if S.get('index') != B.get('index') or 'index' not in B else '分割点都试完了'),
        'res = max': '前缀压最左：`left[{index-1}] = {left[index-1]}`，后缀压最右：`right[{index}] = {right[index]}` → 间隔 `{right[index] - left[index-1]}`，`res = max({B.res}, {right[index] - left[index-1]}) = =={res}==`',
        'return res': '最大间隔 `{res}`',
    },
    cards=dict(
        one_liner='相邻两人拉开最远：前面的压最左，后面的压最右',
        complexity='时间 `O(n+m)`，空间 `O(n)`',
        problem=['把 skill 的每个字母依次分配到 station 里技能相同、下标严格递增的工位',
                 '间隔 = 相邻两名工人工位下标差的最大值，求所有方案里最大的间隔',
                 '示例：`skill = "xyz"`，`station = "xyzz"` → `2`；本视频：`"abcb"`，`"abbcbdcb"` → `5`'],
        quote='将skill[:p]尽量靠前压紧，即在station中找出最靠前的可以匹配skill[:p]的子序列；同样的，对于skill[p:]则应该尽量靠后压紧。',
        quote_src='—— yiduobo 题解原文',
        idea=['先固定分割点 `p`：让 `skill[p-1]` 和 `skill[p]` 成为间隔最大的一对',
              '前缀越靠前、后缀越靠后，这一对拉得越开：正反各扫一趟得到 `left` 和 `right`',
              '再遍历分割点，用 `right[index] - left[index - 1]` 更新答案'],
        summary=['时间 `O(n+m)`，空间 `O(n)`',
                 '一名工人时直接返回 0，否则 `res` 初值 0 也够用',
                 '`right` 反向追加，必须 `reverse()` 后下标才和 skill 对齐',
                 '题目保证有解，所以两个 while 不会越界',
                 '对比灵神：灵神把后缀数组 suf 先算好，前缀位置边扫边用，省掉 left 数组'],
    ),
)
