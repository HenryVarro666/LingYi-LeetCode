CONFIG = dict(
    num=2038, title='如果相邻两个颜色均相同则删除当前颜色', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='博弈拆解 · 各删各的',
    tags=['数学算法', '难度分 1468'],
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
    call='Solution().winnerOfGame("AAABAAABBBB")',
    expect=False,
    views=[
        dict(type='string', var='colors', h=240, pointers={'index': 'blue'},
             color=lambda S, i, v: ('green' if v == 'A' else 'pink') if ('index' in S and i == S['index'] and 0 < i < len(S['colors']) - 1 and S['colors'][i-1] == v == S['colors'][i+1] and S['_line'] >= 8) else None),
        dict(type='text', size=34, fn=lambda S: (f"可删 A 比可删 B 多 ==`{S['cnt']}`== 个" if S.get('cnt', 0) > 0 else f"可删 A 与可删 B 之差 ==`{S['cnt']}`==" ) if 'cnt' in S else ''),
    ],
    watch=['index', ('cnt', 'cnt（A 可删数 − B 可删数）', 'orange')],
    captions={
        'cnt = 0': '`cnt` = 可删的 A 的个数 − 可删的 B 的个数',
        'for index in range': lambda S, B, r: ('遍历完毕，循环结束' if B.get('index') == S['index'] else f'只看中间位置（两端不能删）：`index = {S["index"]}`'),
        'if colors[index - 1] == colors[index] == colors[index + 1]': '`{colors[index-1]}{colors[index]}{colors[index+1]}` 三个相邻颜色：{"全相同，中间这个能删" if colors[index-1] == colors[index] == colors[index+1] else "不全相同，删不了"}',
        "if colors[index] == 'A'": '能删的是 `{colors[index]}`：{"归 Alice" if colors[index] == "A" else "归 Bob"}',
        'cnt += 1': 'Alice 多一次机会：`cnt` → =={cnt}==',
        'cnt -= 1': 'Bob 多一次机会：`cnt` → =={cnt}==',
        'return cnt > 0': '各玩各的，Alice 的机会要严格多于 Bob 才赢：`{cnt} > 0` → =={ret}==',
    },
    cards=dict(
        one_liner='删掉一个，不影响其他位置能不能删，两人各玩各的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['Alice 只能删两边都是 A 的 A，Bob 只能删两边都是 B 的 B，Alice 先手',
                 '不能操作的人输，两人最优策略下 Alice 是否获胜',
                 '本视频：`AAABAAABBBB` → `false`'],
        quote='删去p并不会给其他任何位置带来影响。有了这个结论，alice和bob实际上就是各玩各的，最终比较的是可删除的A的数量与可删除的B的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['删 p 后，p−1 的右邻、p+1 的左邻颜色都没变（三者同色）',
              '所以每个位置能否删除，从头到尾不变',
              '数一数可删的 A 和 B，A 多则 Alice 胜'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '==Alice 先手，必须严格多==：A 与 B 相等时 Alice 先无路可走，输',
                 '循环只取 `1..n-2`，两端不能删',
                 '一段连续 `l` 个同色可删 `l−2` 个，与逐点计数等价'],
    ),
)
