def _col(S, k, v):
    if v == 'L':
        return 'pink'
    if v == 'R':
        return 'blue'
    return None


def _seg(S):
    if 'start_pos' not in S or 'index' not in S:
        return ''
    flag = '有' if S['right_flag'] else '没有'
    return f"当前区间从 `start_pos = {S['start_pos']}` 开始，目前==" + flag + "==待结算的右倒骨牌（`right_flag = " + str(S['right_flag']) + "`）"


CONFIG = dict(
    num=838, title='推多米诺', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按 L / R 切段 · right_flag 标记',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·贪心与思维', '难度分 1638'],
    code='''
class Solution(object):
    def pushDominoes(self, dominoes):
        start_pos = 0
        right_flag = False
        res = ''
        for index, char in enumerate(dominoes):
            if char == 'R':
                if right_flag:
                    res += 'R' * (index - start_pos)
                else:
                    res += '.' * (index - start_pos)
                start_pos = index
                right_flag = True
            elif char == 'L':
                if right_flag:
                    delta = index - start_pos
                    res += 'R' * ((delta + 1) // 2)
                    if delta % 2 == 0:
                        res += '.'
                    res += 'L' * ((delta + 1) // 2)
                    right_flag = False
                else:
                    res += 'L' * (index - start_pos + 1)
                start_pos = index + 1
        if right_flag:
            res += 'R' * (len(dominoes) - start_pos)
        else:
            res += '.' * (len(dominoes) - start_pos)
        return res
''',
    call='Solution().pushDominoes("L.R...L.R..")',
    expect='L.RR.LL.RRR',
    views=[
        dict(type='text', fn=_seg, size=24),
        dict(type='string', var='dominoes', label='dominoes（蓝 = R，粉 = L）', cell=70, pointers={'index': 'pink', 'start_pos': 'blue'},
             color=_col, window=('start_pos', 'index'), h=230),
        dict(type='string', var='res', label='res：已经结算好的前缀', cell=70, color=_col, h=230),
    ],
    watch=[('index', 'index', 'pink'), ('start_pos', 'start_pos', 'blue'), ('right_flag', 'right_flag', 'cyan'), 'delta'],
    captions={
        3: '`start_pos`：当前未结算区间的起点，一遇到 L / R 就能结算一段',
        4: '`right_flag`：区间里有没有向右倒的 R 还没等到 L',
        5: '`res` 逐段拼出最终状态',
        'for index, char': '`index = {index}`，`char = {char}`；是点的话什么都不做，继续往后看',
        "if char == 'R'": lambda S, B, r: ("遇到 `R`：它之前的骨牌已经能定下来，和它以及后面的无关" if S.char == 'R' else "不是 `R`，看是不是 `L`"),
        8: lambda S, B, r: (f"`right_flag = {S.right_flag}`：" + ("区间开头有 R，一路向右推" if S.right_flag else "区间开头没有 R")),
        15: lambda S, B, r: (f"`right_flag = {S.right_flag}`：" + ("区间开头有 R，一路向右推" if S.right_flag else "区间开头没有 R")),
        9: '这一段 `{index - start_pos}` 个全被前面的 R 推倒：`res` 加 `{index - start_pos}` 个 `R`，`res = "{res}"`',
        11: '没有 R 推它们、也没有 L：保持竖直 `.` × `{index - start_pos}`，`res = "{res}"`',
        12: 'R 开启新区间：`start_pos = {index}`（R 自己属于新区间）',
        13: '`right_flag = True`：等着后面的 L',
        "elif char == 'L'": lambda S, B, r: ("遇到 `L`：从 `start_pos` 到当前（包含 L）的方向都能定下来" if S.char == 'L' else '是点，不处理'),
        'delta =': '`delta = {index} − {start_pos} = {delta}`，区间共 `{delta + 1}` 个骨牌（含两端）',
        17: '`R...L` 相向倒：先加左半 `{(delta + 1) // 2}` 个 `R`',
        'if delta % 2 == 0': lambda S, B, r: ("`delta` 为偶数 → 区间长度为奇数 → ==正中间的骨牌受力平衡，保持 `.`==" if S.delta % 2 == 0 else "`delta` 为奇数 → 区间长度为偶数，没有中间骨牌"),
        19: '加一个竖直的 `.`，`res = "{res}"`',
        20: '再加右半 `{(delta + 1) // 2}` 个 `L`，`res = "{res}"`',
        21: 'L 已经把这一段结算掉：`right_flag = False`',
        23: '前面没有 R，L 一路向左推：这一段 `{index - start_pos + 1}` 个全变 `L`（含自己），`res = "{res}"`',
        'start_pos = index + 1': '`L` 属于刚结算的区间，新区间从下一个开始：`start_pos = {start_pos}`',
        25: lambda S, B, r: (f"遍历完：`right_flag = {S.right_flag}`，最后一段" + ('前面有 R 在等 L' if S.right_flag else '前面没有 R')),
        26: '遍历完，最后一段前面有 R 却没有 L → 一路向右：加 `{len(dominoes) - start_pos}` 个 `R`，`res = "{res}"`',
        28: '遍历完，最后一段没有 R 推它 → 保持 `.`：加 `{len(dominoes) - start_pos}` 个，`res = "{res}"`',
        'return res': '最终状态 `{res}`',
    },
    cards=dict(
        one_liner='L 和 R 把序列切成互不干涉的区间，逐段结算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`L` 向左推、`R` 向右推、`.` 竖立；两边同时受力则保持不变',
                 '求最终状态',
                 '本视频：`"L.R...L.R.."` → `"L.RR.LL.RRR"`'],
        quote='通过向左或向右倾斜的骨牌，我们可以将整个序列划分成若干个互不干涉的部分分别求解。基于这一点，我们需要维护一个start_pos，表示当前处理部分的起始位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`R` 之前的骨牌已无关后续；`L` 之后的骨牌与它之前无关 → 切段',
              '`right_flag` 记录区间里有没有等待 `L` 的 `R`',
              '遇到 `L` 且有 `R`：左半 R、右半 L，奇数个时中间留 `.`'],
        summary=['时间 `O(n)`，空间 `O(n)`（字符串拼接）',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错：`R` 的区间长度是 `index - start_pos`（不含 R），`L` 是 `index - start_pos + 1`（含 L）',
                 '结尾还要处理最后一段：有 R 就推成 R，否则保持 `.`',
                 '对比灵神：灵神加哨兵按相邻两个非点字符分类；yiduobo 用 `right_flag` 一次遍历拼出答案'],
    ),
)
