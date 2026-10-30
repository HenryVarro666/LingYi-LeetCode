CONFIG = dict(
    num=657, title='机器人能否返回原点', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='统计 R/L、U/D 个数',
    code='''
class Solution:
    def judgeCircle(self, moves: str) -> bool:
        return moves.count('R') == moves.count('L') and \\
               moves.count('U') == moves.count('D')
''',
    call='[Solution().judgeCircle(s) for s in ("UD", "LL", "UURDDLLR")]',
    expect=[True, False, True],
    views=[
        dict(type='string', var='moves', label='moves（走法序列）', h=200),
        dict(type='text', size=34, fn=lambda S: (f"`R` {S['moves'].count('R')} 次，`L` {S['moves'].count('L')} 次 → 横坐标 =={S['moves'].count('R') - S['moves'].count('L')}==" if 'moves' in S else '')),
        dict(type='text', size=34, fn=lambda S: (f"`U` {S['moves'].count('U')} 次，`D` {S['moves'].count('D')} 次 → 纵坐标 =={S['moves'].count('U') - S['moves'].count('D')}==" if 'moves' in S else '')),
    ],
    watch=[('R', "moves.count('R')", 'blue'), ('L', "moves.count('L')", 'pink'),
           ('U', "moves.count('U')", 'green'), ('D', "moves.count('D')", 'orange')],
    captions={
        "moves.count('R') == moves.count('L')": lambda S, B, r: (
            f"横坐标 = 右移次数 − 左移次数：`{S.moves.count('R')} − {S.moves.count('L')}` = =={S.moves.count('R') - S.moves.count('L')}=="
            + ('，横向回到 0' if S.moves.count('R') == S.moves.count('L') else '，横向没回来 → 直接 False')),
        "moves.count('U') == moves.count('D')": lambda S, B, r: (
            f"纵坐标 = 上移次数 − 下移次数：`{S.moves.count('U')} − {S.moves.count('D')}` = =={S.moves.count('U') - S.moves.count('D')}==，纵向也回到 0 → 两个条件同时成立"),
    },
    cards=dict(
        one_liner='横纵坐标分别抵消：R 与 L 一样多，U 与 D 一样多',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['机器人从原点 `(0, 0)` 出发，按 `moves` 里的 `R/L/U/D` 逐步移动',
                 '走完后在原点就返回 `true`，否则 `false`',
                 '示例：`"UD"` → `true`，`"LL"` → `false`',
                 '本视频依次判断：`"UD"`、`"LL"`、`"UURDDLLR"`'],
        quote='机器人的横坐标，等于向右移动的次数，减去向左移动的次数。如果 R 的个数等于 L 的个数，那么最终横坐标为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['横坐标只和 `R`、`L` 有关：右移 +1，左移 −1',
              '纵坐标只和 `U`、`D` 有关：上移 +1，下移 −1',
              '两个坐标同时为 0，才回到原点；不需要真的模拟路线'],
        summary=['时间 `O(n)`（`count` 扫四遍），空间 `O(1)`',
                 '易错：只看总步数是偶数不够，`"LR"` 之外如 `"UL"` 也是偶数却回不去',
                 '写法二：`Counter(moves)` 一次统计，再比较 `cnt[R]==cnt[L]`、`cnt[U]==cnt[D]`'],
    ),
)
