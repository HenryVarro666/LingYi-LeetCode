CONFIG = dict(
    num=780, title='到达终点', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='逆向 + 辗转相除', tags=[],
    code='''
class Solution(object):
    def reachingPoints(self, sx, sy, tx, ty):

        if sx == tx and sy == ty:
            return True
        if tx == ty:
            return False

        if tx < sx:
            return False
        if ty < sy:
            return False

        if tx > ty:
            tx, ty = ty, tx
        if sx > sy:
            sx, sy = sy, sx

        if sx == 0:
            sx, sy = sy, sy
        while tx > sx:
            tx, ty = ty % tx, tx   

        return tx == sx and ty >=sy and (ty - sy) % sx == 0
''',
    call='Solution().reachingPoints(1, 1, 3, 5)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"起点 (==sx={S['sx']}==, ==sy={S['sy']}==)　终点 (==tx={S['tx']}==, ==ty={S['ty']}==)", h=70, size=34),
        dict(type='text', fn=lambda S: f"倒推：(`{S['tx']}`, `{S['ty']}`) 的上一步必是 (`{S['ty'] % S['tx'] if S['tx'] else 0}`, `{S['tx']}`)（ty 对 tx 取模）" if S['tx'] > S['sx'] and S['_line'] else '倒推已停止，只剩一条线上的检查', h=70),
        dict(type='text', fn=lambda S: f"检查：ty − sy = {S['ty'] - S['sy']}，对 sx = {S['sx']} 取余 = {(S['ty'] - S['sy']) % S['sx'] if S['sx'] else '-'}", h=70),
    ],
    watch=['sx', 'sy', ('tx', 'tx', 'blue'), ('ty', 'ty', 'pink')],
    captions={
        'sx == tx and sy == ty': '起点已经等于终点吗？`({sx},{sy})` vs `({tx},{ty})` → 不等，继续',
        'if tx == ty': '`tx == ty` 吗？相等的话它不可能由 (x, y) 变来（x、y 都 > 0 时一边必更小）→ 这里不等，继续',
        'if tx < sx': '终点坐标只会越变越大，`tx < sx` 就不可能 → 不成立，继续',
        'if ty < sy': '同理检查 `ty < sy` → 不成立，继续',
        'tx, ty = ty, tx': '`tx > ty`，交换使 tx 是较小的（变换对称，交换等价）',
        'sx, sy = sy, sx': 'sx 也要是较小的',
        'if sx == 0': '`sx` 不为 0，跳过这个特殊处理',
        'while tx > sx': lambda S, B, r: f'`tx = {S.tx} > sx = {S.sx}`？→ {"成立：继续往回倒推" if S.tx > S.sx else "不成立：倒推结束"}',
        'tx, ty = ty % tx': '(tx, ty) 必由 (ty % tx, tx) 变来（辗转相除）：`({B.tx}, {B.ty})` → `({tx}, {ty})`',
        'return tx == sx': 'tx 已等于 sx，再看 ty：`ty >= sy` 且 `(ty - sy) % sx == 0` → ==`{ret}`==（`({ty} − {sy}) % {sx}` = {(ty - sy) % sx}）',
    },
    cards=dict(
        one_liner='正着走分支太多，倒着走每一步都是唯一的',
        complexity='时间 `O(log max(tx, ty))`，空间 `O(1)`',
        problem=['从 `(x, y)` 一步可到 `(x, x+y)` 或 `(x+y, y)`',
                 '给定起点 `(sx, sy)` 与终点 `(tx, ty)`，能否到达',
                 '示例：`(1,1) → (3,5)` → `true`'],
        quote='如果直接从(sx, sy)开始往外扩展然后检测能否到达(tx, ty)，理论上的复杂度太高，可能到达10^9，于是我们只能想办法从(tx, ty)开始倒推。',
        quote_src='—— yiduobo 题解原文',
        idea=['倒推时较大的数一定是上一步加出来的，上一步唯一',
              '连续倒推相当于对 `(tx, ty)` 做辗转相除：`(tx, ty) ← (ty % tx, tx)`',
              '停在 `tx <= sx` 后：若 `tx == sx`，只需 `ty >= sy` 且差是 `sx` 的倍数'],
        summary=['时间 `O(log)`，空间 `O(1)`',
                 '先排除特殊情形：起点即终点、`tx == ty`、终点小于起点',
                 '交换 x/y 不影响结果，所以统一成 `tx <= ty`、`sx <= sy`',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
