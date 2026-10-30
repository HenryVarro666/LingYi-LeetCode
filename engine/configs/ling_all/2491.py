CONFIG = dict(
    num=2491, title='划分技能点相等的团队', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 最小配最大',
    tags=[],
    code='''
class Solution:
    def dividePlayers(self, skill: List[int]) -> int:
        skill.sort()
        ans, s = 0, skill[0] + skill[-1]
        for i in range(len(skill) // 2):
            x, y = skill[i], skill[-1 - i]
            if x + y != s: return -1
            ans += x * y
        return ans
''',
    call='Solution().dividePlayers([3,2,5,1,3,4])',
    expect=22,
    views=[
        dict(type='array', var='skill', label='skill（排序后：蓝 = 当前最小，粉 = 当前最大）', cell=90, h=230,
             pointers={'i': 'blue', 'len(skill) - 1 - i': 'pink'},
             pointer_labels={'i': 'x', 'len(skill) - 1 - i': 'y'},
             color=lambda S, k, v: (('blue' if k == S['i'] else 'pink' if k == len(S['skill']) - 1 - S['i'] else
                                     'green' if k < S['i'] or k > len(S['skill']) - 1 - S['i'] else None)
                                    if 'i' in S else None)),
        dict(type='text', size=28, h=70,
             fn=lambda S: (f"每队目标和 `s = {S['s']}`" + (f"　已累计化学反应 =={S['ans']}==" if 'ans' in S else '')) if 's' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('s', 's', 'orange'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'skill.sort()': '先排序：最小的在左，最大的在右 → `{skill}`',
        'ans, s = 0, skill[0] + skill[-1]': '最小的必须配最大的，所以每队的和 `s = {skill[0]} + {skill[-1]} = {s}`',
        'for i in range': lambda S, B, ret: (f'第 `{S.i}` 对：从两端往中间配' if S.get('i') is not None and (B.get('i') != S.i or 'i' not in B)
                                               else '所有队伍都配完了'),
        'x, y = skill': '最小的剩余数 `x = {x}`，最大的剩余数 `y = {y}`',
        'if x + y != s': lambda S, B, ret: (f'`{S.x} + {S.y} = {S.x + S.y}` ≠ `{S.s}` → ==凑不出相等的和==，返回 -1'
                                            if S.x + S.y != S.s else f'`{S.x} + {S.y} = {S.s}` 等于目标和，这一队成立'),
        'ans += x * y': '化学反应 `{x} × {y} = {x*y}`，`ans` → =={ans}==',
        'return ans': '每对都等于 `{s}`，返回 =={ans}==',
        'return -1': '有一对和不等于 `{s}`，返回 -1',
    },
    cards=dict(
        one_liner='排序后最小配最大，逐对检查和是否一致',
        complexity='时间 `O(n log n)`，空间 `O(1)`（忽略排序栈）',
        problem=['偶数个玩家分成 `n/2` 个二人队，每队技能点之和==相等==',
                 '队的化学反应 = 两人技能点的乘积，求总和；做不到返回 `-1`',
                 '示例：`[3,2,5,1,3,4]` → 三队和都为 6 → `22`'],
        quote='如果最小的不和最大的匹配，那么最大的和一个比最小数更大的数匹配，就会导致技能点之和不相等。因此最小的一定和最大的匹配。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['反证：最大数若不配最小数，就配到更大的数，和必然比最小数那队更大',
              '所以排序后首尾配对，和 `s = skill[0] + skill[-1]` 就被确定了',
              '往中间逐对检查和是否等于 `s`，同时累加乘积'],
        summary=['时间 `O(n log n)`，主要是排序；空间 `O(1)`',
                 '易错：循环只走一半 `len(skill) // 2`，否则每队会算两次',
                 '发现某队和不等于 `s` 就立刻返回 `-1`',
                 '另一种写法（方法二）：哈希表计数，`O(n)`，最后答案要除以 2'],
    ),
)
