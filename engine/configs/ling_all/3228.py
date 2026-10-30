CONFIG = dict(
    num=3228, title='将 1 移动到末尾的最大操作次数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='车队：先动左边的车',
    tags=['灵神题单', '难度分 1593'],
    code='''
class Solution:
    def maxOperations(self, s: str) -> int:
        ans = cnt1 = 0
        for i, c in enumerate(s):
            if c == '1':
                cnt1 += 1
            elif i > 0 and s[i - 1] == '1':
                ans += cnt1
        return ans
''',
    call='Solution().maxOperations("1001101")',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"左边已有 `{S['cnt1']}` 辆车；累计操作 =={S['ans']}==" if 'cnt1' in S else '')),
        dict(type='string', var='s', pointers={'i': 'blue'}, h=230,
             color=lambda S, i, v: ('green' if v == '1' else None) if 'i' in S and i <= S['i'] else None,
             dim=lambda S, i, v: 'i' in S and i > S['i']),
    ],
    watch=['i', 'c', ('cnt1', 'cnt1', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = cnt1 = 0': '`cnt1`：左边的“车”（1）的数量；`ans`：总操作次数',
        "if c == '1'": lambda S, B, r: (f'`s[{S.i}] = 1`：多一辆车' if S.c == '1' else f'`s[{S.i}] = 0`：是一段空路，看看它左边是不是车'),
        'cnt1 += 1': '`cnt1` → {cnt1}：这辆车排到队伍里',
        'elif i > 0': lambda S, B, r: (f'`s[{S.i-1}] = 1` 紧挨着空位 → 找到一段道路：左边 `{S.cnt1}` 辆车各能操作一次' if S.i > 0 and S.s[S.i-1] == '1' else '左边也是 0（或在开头）：这段路已经算过，不重复算'),
        'ans += cnt1': '==`ans += cnt1`==：`{B.ans} + {cnt1}` = {ans}（先动左边的车，每辆车都多操作一次）',
        'return ans': '最多操作 `{ret}` 次',
    },
    cards=dict(
        one_liner='把 1 当车，先开左边的车，制造“堵车”才能操作最多',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串，可选 `s[i]=1` 且 `s[i+1]=0`，把这个 1 右移直到末尾或碰到另一个 1',
                 '求最多能操作几次',
                 '示例：`"1001101"` → `4`'],
        quote='如果优先操作右边的（能移动的）车，那么这些车都只需操作一次……而如果优先操作左边的（能移动的）车，这会制造大量的「堵车」，每辆车的操作次数会更多。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先动左边的车 → 右边的车一格一格排队，操作次数最大',
              '遇到“1 后接 0”的位置，左边每辆车各操作一次',
              '所以每遇到一段 `10`，答案加上当前 `cnt1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：只在“0 的前一位是 1”时加，连续的 0 只算一次',
                 '答案最大约 `n²/4`，Python 不用担心溢出，C++ 要用 `long long`',
                 '灵神的思考题：构造 `1…10…0` 交替，让答案尽量大'],
    ),
)
