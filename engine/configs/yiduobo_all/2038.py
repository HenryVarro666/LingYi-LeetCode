def _txt(S):
    if 'cnt' not in S:
        return ''
    c = S['cnt']
    return f"`cnt` = A 能删的 − B 能删的 = =={c}=={'（Alice 多）' if c > 0 else ('（Bob 多或相等）' if c <= 0 else '')}"


def _col(S, i, v):
    if 'index' in S and S['index'] - 1 <= i <= S['index'] + 1 and 0 < S['index'] < len(S['colors']) - 1:
        if S['colors'][S['index'] - 1] == S['colors'][S['index']] == S['colors'][S['index'] + 1]:
            return 'green' if i == S['index'] else 'blue'
    return None


CONFIG = dict(
    num=2038, title='如果相邻两个颜色均相同则删除当前颜色', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='互不影响 · 一趟统计三连',
    tags=['灵神题单·数学算法'],
    code='''
class Solution(object):
    def winnerOfGame(self, colors):

        cnt = 0
        for index in range(1, len(colors) - 1):
            if colors[index - 1] == colors[index] == colors[index + 1]:
                if colors[index] == 'A':
                    cnt += 1
                else:
                    cnt -= 1
        
        return cnt > 0
''',
    call='Solution().winnerOfGame("AAAABBBAAB")',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='string', var='colors', label='colors（绿 = 当前可删的颜色，蓝 = 它的左右邻居）', cell=84,
             pointers={'index': 'pink'}, color=_col),
    ],
    watch=[('index', 'index', 'pink'), ('cnt', 'cnt', 'green')],
    captions={
        'cnt = 0': '`cnt` = Alice 能删的次数 − Bob 能删的次数',
        'for index in range': lambda S, B, r: ((f'检查位置 `index = {S.index}`（两端不能删，所以从 `1` 到 `len - 2`）' if S.index == 1 else f'检查位置 `index = {S.index}`') if 'index' not in B or B.index != S.index
                                               else '所有位置都检查完了'),
        'if colors[index - 1] == colors[index] == colors[index + 1]': lambda S, B, r: (
            f'`{S.colors[S.index - 1]}{S.colors[S.index]}{S.colors[S.index + 1]}`：三个颜色相同 → ==这个位置可以被删=='
            if S.colors[S.index - 1] == S.colors[S.index] == S.colors[S.index + 1]
            else f'`{S.colors[S.index - 1]}{S.colors[S.index]}{S.colors[S.index + 1]}`：三个颜色不全相同 → 不能删'),
        "if colors[index] == 'A'": lambda S, B, r: ('是 `A`：Alice 的一次机会' if S.colors[S.index] == 'A' else '是 `B`：Bob 的一次机会'),
        'cnt += 1': 'Alice 多一次：`cnt` → {cnt}',
        'cnt -= 1': 'Bob 多一次：`cnt` → {cnt}',
        'return cnt > 0': '`cnt = {cnt}`：Alice 的次数 {"多于" if cnt > 0 else "不多于"} Bob → ==`{cnt > 0}`==',
    },
    cards=dict(
        one_liner='删一个位置不影响别的位置：各玩各的，比谁能删得多',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`colors` 由 `A`、`B` 组成；Alice 只能删「左右邻居都是 A」的 A，Bob 对 B 同理',
                 'Alice 先手，两端的字符不能删；无法操作的人输',
                 '示例：`"AAABABB"` → `true`；`"AA"` → `false`'],
        quote='删去p并不会给其他任何位置带来影响。有了这个结论，alice和bob实际上就是各玩各的，最终比较的是可删除的A的数量与可删除的B的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['删掉 `p` 后，`p-1` 的右邻居变成 `p+1`，颜色仍然相同 → 其他位置的可删性不变',
              '所以可删位置的数量是固定的：遍历一遍，三连相同的位置里 A 算 `+1`，B 算 `-1`',
              'A 的数量更多，Alice 胜；否则 Bob 胜'],
        result='三连位置：`AAA` 两处（A）、`BBB` 一处（B）→ `cnt = 2 − 1 = 1 > 0` → Alice 赢 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '一个变量 `cnt` 同时记两个人：A 加一，B 减一',
                 '`range(1, len - 1)` 保证两端不会被检查，也不会越界',
                 '`cnt > 0` 是严格大于：相等时 Alice 先手先无路可走，Bob 赢',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，其余未改',
                 '对比灵神：灵神按「段」统计 `l - 2`；yiduobo 逐位置检查三连'],
    ),
)
