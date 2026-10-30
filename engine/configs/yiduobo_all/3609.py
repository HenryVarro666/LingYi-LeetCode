def _pt(S):
    return [S['tx'], S['ty']] if 'tx' in S and 'ty' in S else None


def _st(S):
    return [S['sx'], S['sy']] if 'sx' in S and 'sy' in S else None


def _txt(S):
    if 'tx' not in S:
        return ''
    tx, ty, sx, sy = S['tx'], S['ty'], S['sx'], S['sy']
    if 7 <= S['_line'] <= 30 and sx == 0:
        return f'上一步是 `(0, {S["ty"] if S["_line"] < 9 else ty})` 翻倍而来：ty 一路 ÷2，要还原到 `sy = {sy}`，当前 `ty = {ty}`'
    if 7 <= S['_line'] <= 30 and sy == 0:
        return f'上一步是 `({tx}, 0)` 翻倍而来：tx 一路 ÷2，要还原到 `sx = {sx}`，当前 `tx = {tx}`'
    if tx == sx and ty == sy:
        return f'`({tx}, {ty})` 就是起点 `({sx}, {sy})`，倒推完成，共 `{S["res"]}` 步'
    if tx == ty:
        return f'`tx == ty = {tx}`：上一步必有一维是 0，剩下一维一路翻倍而来'
    return f'倒推中：`({tx}, {ty})` → 起点 `({sx}, {sy})`，已倒退 `{S["res"]}` 步'


CONFIG = dict(
    num=3609, title='到达目标点的最小移动次数', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='倒推 · 分 tx>ty / tx<ty / 相等三种',
    tags=['灵神题单·贪心与思维', '难度分 2419'],
    code='''
class Solution(object):
    def minMoves(self, sx, sy, tx, ty):
        
        res = 0
        while tx >= sx and ty >= sy and (tx != sx or ty != sy):
            if tx == ty:
                res += 1
                if sx == 0:
                    while ty > sy:
                        res += 1
                        if ty % 2 != 0:
                            return -1
                        ty //= 2

                    if ty != sy:
                        return -1

                elif sy == 0:
                    while tx > sx:
                        res += 1
                        if tx % 2 != 0:
                            return -1
                        tx //= 2

                    if tx != sx:
                        return -1
                else:
                    return -1
            
                return res
            
            elif tx > ty:
                if ty * 2 < tx:
                    if tx % 2 != 0:
                        return -1
                    tx //= 2
                else:
                    tx -= ty
                
                res += 1
            
            else:
                if tx * 2 < ty:
                    if ty % 2 != 0:
                        return -1
                    ty //= 2
                else:
                    ty -= tx
                
                res += 1
        
        if tx == sx and ty == sy:
            return res
        return -1
''',
    call='Solution().minMoves(0, 1, 8, 4)',
    expect=4,
    views=[
        dict(type='array', var=_pt, label='当前点 (tx, ty)：从终点倒推', cell=110, h=210, index=False,
             color=lambda S, i, v: 'green' if S.get('tx') == S.get('sx') and S.get('ty') == S.get('sy') else ('blue' if i == 0 else 'pink')),
        dict(type='array', var=_st, label='起点 (sx, sy)', cell=110, h=210, index=False),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=[('res', 'res', 'green'), ('tx', 'tx', 'blue'), ('ty', 'ty', 'pink'), ('sx', 'sx'), ('sy', 'sy')],
    captions={
        4: '`res` 记倒推的步数。从 `(tx, ty)` 往回走，每步上一个位置能确定',
        5: lambda S, B, r: (f'`({S.tx}, {S.ty})` 还没到起点且没越过它，继续倒推' if (S.tx >= S.sx and S.ty >= S.sy and (S.tx != S.sx or S.ty != S.sy))
                            else ('倒推结束：到了起点或已越过起点' )),
        6: lambda S, B, r: (f'`tx == ty == {S.tx}`：上一步必然有一维是 0' if S.tx == S.ty else
                            (f'`tx = {S.tx} > ty = {S.ty}`：较大的 tx 是某个数加出来的' if S.tx > S.ty else f'`tx = {S.tx} < ty = {S.ty}`：较大的 ty 是某个数加出来的')),
        7: '先算进从 `(0, ty)` 或 `(tx, 0)` 到 `(tx, ty)` 的那一步：`res` = {res}',
        8: lambda S, B, r: ('`sx == 0`：起点 x 是 0，所以上一步是 `(0, ty)`，ty 一路翻倍而来' if S.sx == 0 else f'`sx = {S.sx}` 非 0，看 sy 是否为 0'),
        9: lambda S, B, r: (f'`ty = {S.ty} > sy = {S.sy}`：还没减到起点的 y，继续往回除以 2' if S.ty > S.sy else f'`ty = {S.ty} <= sy`：不用再除了'),
        10: '往回一步（`(0, ty)` 由 `(0, ty/2)` 翻倍得来），`res` = {res}',
        11: lambda S, B, r: (f'`ty = {S.ty}` 是奇数，不可能由翻倍得来 → -1' if S.ty % 2 != 0 else f'`ty = {S.ty}` 是偶数，可以减半'),
        13: '`ty` 减半为 =={ty}==',
        15: lambda S, B, r: (f'`ty = {S.ty} != sy = {S.sy}`：除不到起点 → -1' if S.ty != S.sy else f'`ty == sy = {S.sy}`：刚好除到起点'),
        18: lambda S, B, r: ('`sy == 0`：起点 y 是 0，上一步是 `(tx, 0)`，tx 一路翻倍而来' if S.sy == 0 else '`sx` 和 `sy` 都非 0，`(tx, tx)` 不可能 → -1'),
        30: '倒推完成，共 `{res}` 步',
        32: lambda S, B, r: f'`tx = {S.tx} > ty = {S.ty}`：上一步 tx 加过某个数',
        33: lambda S, B, r: (f'`ty*2 = {S.ty * 2} < tx = {S.tx}`：翻倍而来（那时 tx 较大，加的是它自己）' if S.ty * 2 < S.tx
                             else f'`ty*2 = {S.ty * 2} >= tx = {S.tx}`：上一步 tx 加的是 ty'),
        34: lambda S, B, r: (f'`tx = {S.tx}` 是奇数 → 不可能 -1' if S.tx % 2 != 0 else f'`tx = {S.tx}` 是偶数，可以减半'),
        36: '撤销翻倍：`tx` = =={tx}==',
        38: '撤销加 ty：`tx -= ty` → =={tx}==',
        40: '倒退一步，`res` = {res}',
        43: lambda S, B, r: (f'`tx*2 = {S.tx * 2} < ty = {S.ty}`：翻倍而来' if S.tx * 2 < S.ty else f'`tx*2 = {S.tx * 2} >= ty = {S.ty}`：上一步 ty 加的是 tx'),
        44: lambda S, B, r: (f'`ty = {S.ty}` 是奇数 → -1' if S.ty % 2 != 0 else f'`ty = {S.ty}` 是偶数，可以减半'),
        46: '撤销翻倍：`ty` = =={ty}==',
        48: '撤销加 tx：`ty -= tx` → =={ty}==',
        50: '倒退一步，`res` = {res}',
        52: lambda S, B, r: ('到达起点' if S.tx == S.sx and S.ty == S.sy else '没能到达起点'),
        53: '答案 `{res}`',
        54: '到不了起点，返回 -1',
    },
    cards=dict(
        one_liner='从终点倒推：较大数要么是翻倍来的，要么是加了较小数',
        complexity='时间 `O(log(tx+ty))`，空间 `O(1)`',
        problem=['在 `(x, y)` 令 `m = max(x, y)`，可走到 `(x+m, y)` 或 `(x, y+m)`',
                 '求从 `(sx, sy)` 到 `(tx, ty)` 的最少步数，到不了返回 -1',
                 '本视频：`(0,1) → (8,4)`，答案 `4`'],
        quote='直接从(sx, sy)开始计算后续的行动可能性非常多，在这里不妨看看能否从(tx, ty)倒推回去。',
        quote_src='—— yiduobo 题解原文',
        idea=['`tx != ty` 时：较大值 `ma` 上一轮是 `ma // 2`（`mi * 2 < ma`，要偶数）或 `ma - mi`',
              '`tx == ty` 时：上一轮必有一维是 0，由 `sx == 0` 还是 `sy == 0` 决定哪一维',
              '另一维不断除以 2 直到 `sy`（或 `sx`），遇奇数返回 -1，最后再加 1 步'],
        summary=['时间 `O(log(tx+ty))`，空间 `O(1)`',
                 '`tx == ty` 时单独处理：`sx` 和 `sy` 都非 0 一定不行',
                 '`while` 条件包含 `tx >= sx and ty >= sy`：走过头直接退出并返回 -1',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神靠交换 x、y 把两种情形合并；yiduobo 分 tx>ty / tx<ty 各写一份'],
    ),
)
