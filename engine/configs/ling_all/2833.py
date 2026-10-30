CONFIG = dict(
    num=2833, title='距离原点最远的点', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='数 L/R 个数', tags=['难度分 1294'],
    code='''
class Solution:
    def furthestDistanceFromOrigin(self, moves: str) -> int:
        cnt_r = moves.count('R')
        cnt_l = moves.count('L')
        return abs(cnt_r - cnt_l) + len(moves) - cnt_r - cnt_l
''',
    call="Solution().furthestDistanceFromOrigin('_R__LL_')",
    expect=5,
    views=[
        dict(type='string', var='moves', h=200, label='moves',
             color=lambda S, i, v: 'blue' if v == 'R' else 'pink' if v == 'L' else 'yellow'),
        dict(type='text', h=120, size=34, fn=lambda S: (
            f"`R` 有 =={S['cnt_r']}== 个" if 'cnt_r' in S and 'cnt_l' not in S else
            f"`R` {S['cnt_r']} 个，`L` {S['cnt_l']} 个 → 固定部分净位移 =={abs(S['cnt_r']-S['cnt_l'])}==，剩 =={len(S['moves'])-S['cnt_r']-S['cnt_l']}== 个 `_` 全朝同一边" if 'cnt_l' in S else '')),
    ],
    watch=[('n', 'len(moves)'), ('cnt_r', 'cnt_r', 'blue'), ('cnt_l', 'cnt_l', 'pink')],
    captions={
        "count('R')": '先数 `R`：必须向右的步数 `cnt_r = {cnt_r}`',
        "count('L')": '再数 `L`：必须向左的步数 `cnt_l = {cnt_l}`',
        'return': '`|{cnt_r} - {cnt_l}|` + `{len(moves)} - {cnt_r} - {cnt_l}`：固定部分的距离 + 全部 `_` 朝同一方向 = =={ret}==',
    },
    cards=dict(
        one_liner='先只看 L 和 R，剩下的 `_` 全往同一个方向走',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`moves` 由 `L`、`R`、`_` 组成，`L`/`R` 只能左/右走一步，`_` 左右都行',
                 '求走完 n 步后，离原点最远的距离',
                 '示例：`_R__LL_` → `5`'],
        quote='先只看 R 和 L，往右走了 1 步，再往左走 2 步，相当于往左走了 1 步……还剩下 4 个 _，当然是继续往左走啦。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`L`、`R` 的位移固定，净位移是 `|cntR - cntL|`',
              '`_` 个数是 `n - cntR - cntL`，让它们全走在远离原点的方向',
              '两个量加起来就是答案，不用模拟'],
        summary=['时间 `O(n)`（count 扫一遍），空间 `O(1)`',
                 '易错：`_` 的个数要用 `n - cnt_r - cnt_l`，不要重复数',
                 '关键：`_` 全朝较多的那一侧走，距离最大'],
        before=[dict(heading='举例：_R__LL_', lines=['`R` 1 步、`L` 2 步，净向左 1 步，停在 `-1`', '还有 4 个 `_`，继续向左 4 步 → `-5`', '所以距离是 `1 + 4 = 5`，不必真的枚举 2^k 种走法'])],
        after=[dict(heading='为什么贪心成立', lines=['`_` 向两边都行，等价于“方向自选”', '固定位移已定偏左或偏右，`_` 全跟随它就是最远', '若 `cnt_r == cnt_l`，随便选一边，距离就是 `_` 的个数'])],
    ),
)
