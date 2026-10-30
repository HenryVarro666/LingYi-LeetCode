def _opp(ch):
    return '0' if ch == '1' else '1'


def _exit(S):
    return bool(S['_inner'].get('_exit'))


def _lr(S):
    """当前下标 i 的左边 / 右边各有多少个「和 s[i] 不同」的字符"""
    s, i = S['s'], S['i']
    o = _opp(s[i])
    return o, s[:i].count(o), s[i + 1:].count(o)


def _info(S):
    if 'i' not in S or _exit(S):
        return '合法的三栋只有两种：`010`（中间是 1）和 `101`（中间是 0）→ ==枚举中间那一栋=='
    ch, i = S['s'][S['i']], S['i']
    o, L, R = _lr(S)
    return f"中间 `s[{i}] = '{ch}'`：左边的 `'{o}'` 有 =={L}== 个，右边的 `'{o}'` 有 =={R}== 个 → {L} × {R} = =={L * R}=="


def _color(S, k, v):
    if 'i' not in S or _exit(S):
        return None
    o, _, _ = _lr(S)
    i = S['i']
    if k == i:
        return 'orange'
    if S['s'][k] == o:
        return 'green' if k < i else 'blue'
    return None


def _dim(S, k, v):
    if 'i' not in S or _exit(S):
        return False
    return k != S['i'] and S['s'][k] != _opp(S['s'][S['i']])


def _contrib(S):
    s = S['s']
    if 'i' not in S:
        return [None] * len(s)
    done = S['i'] + 1 if (S['_line'] in (7, 10, 11, 12) or _exit(S)) else S['i']
    out = []
    for k in range(len(s)):
        if k >= done:
            out.append(None)
            continue
        ch = s[k]
        o = _opp(ch)
        out.append(s[:k].count(o) * s[k + 1:].count(o))
    return out


def _for(S, B, ret):
    if 'i' in B and B.i == S.i:
        S['_inner']['_exit'] = True
        return '所有字符都当过「中间那栋」了，循环结束'
    return f"枚举下一个当==中间那栋==的位置：`s[{S.i}] = '{S.ch}'`"


def _if(S, B, ret):
    if S.ch == '1':
        return '`ch == \'1\'` 成立 → 它是 `010` 的中间，要数==左边和右边的 0=='
    return '`ch == \'1\'` 不成立 → 它是 0，是 `101` 的中间，要数==左边和右边的 1=='


CONFIG = dict(
    num=2222, title='选择建筑的方案数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='枚举中间 · 前后缀计数（Go 原文转写）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1657'],
    code='''
class Solution:
    def numberOfWays(self, s: str) -> int:
        tot0 = s.count("0")
        ans, c0 = 0, 0
        for i, ch in enumerate(s):
            if ch == '1':
                ans += c0 * (tot0 - c0)  # 对每个 1，统计左边 0 的个数和右边 0 的个数
            else:
                c1 = i - c0
                ans += c1 * (len(s) - tot0 - c1)  # 对每个 0，统计左边 1 的个数和右边 1 的个数
                c0 += 1
        return ans
''',
    call='Solution().numberOfWays("001101")',
    expect=6,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='string', var='s', label='s（橙 = 中间那栋，绿 = 左边的对立字符，蓝 = 右边的）', cell=100,
             pointers={'i': 'pink'}, color=_color, dim=_dim, h=210),
        dict(type='array', var=_contrib, label='每个位置当中间那栋时的方案数（辅助观察，代码里没有这个数组）', cell=100,
             color=lambda S, k, v: 'orange' if v else None, h=170),
    ],
    watch=[('i', 'i', 'pink'), 'ch', ('c0', 'c0', 'green'), 'c1', 'tot0', ('ans', 'ans', 'orange')],
    captions={
        'tot0 = s.count': '先数一遍：全串有 `tot0 = {tot0}` 个 0，所以 1 有 `len(s) − tot0 = {len(s) - tot0}` 个',
        'ans, c0 = 0, 0': '`ans` 累计方案数；`c0` 是==已经扫过的 0 的个数==，也就是当前位置左边 0 的个数',
        'for i, ch': _for,
        'if ch ==': _if,
        'ans += c0 *': '`010`：左边 0 有 `c0 = {c0}` 个，右边 0 有 `tot0 − c0 = {tot0 - c0}` 个 → 加 `{c0} × {tot0 - c0}`，`ans = {ans}`',
        'c1 = i - c0': '下标 `i = {i}` 前面共 `i` 个字符，其中 `c0 = {c0}` 个是 0，其余都是 1 → ==左边 1 有 `c1 = {c1}` 个==',
        'ans += c1 *': '`101`：左边 1 有 `c1 = {c1}` 个，右边 1 有 `{len(s) - tot0} − {c1} = {len(s) - tot0 - c1}` 个 → 加 `{c1} × {len(s) - tot0 - c1}`，`ans = {ans}`',
        'c0 += 1': '这个 0 扫过去了，对后面的字符来说它在左边：`c0` → {c0}',
        'return ans': '每个位置当过中间那栋了，累计得到 `ans = {ret}`',
    },
    cards=dict(
        one_liner='枚举中间那栋：左边对立字符数 × 右边对立字符数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 的每个字符是 `0`（办公楼）或 `1`（餐厅），要选 3 栋建筑',
                 '选出来的相邻两栋==类型不能相同==，即子序列只能是 `010` 或 `101`',
                 '返回有效方案数',
                 '本视频：`s = "001101"` → `6`'],
        quote='根据题意，只有两种情况：010：对每个 1，统计左边 0 的个数和右边 0 的个数；101：对每个 0，统计左边 1 的个数和右边 1 的个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法的三栋只有 `010` 和 `101` → ==枚举中间那一栋==',
              '中间是 1：左边挑一个 0、右边挑一个 0，方案数 = 两边 0 的个数相乘',
              '一边扫一边维护 `c0`；右边的个数用总数减去左边的得到，不用再扫一遍'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`for i, ch := range s` → `enumerate(s)`，`int64(ans)` 直接 `return ans`）',
                 '时间 `O(n)`，空间 `O(1)`：只维护 `tot0`、`c0`、`c1`',
                 '易错：`c1 = i − c0`，当前字符还没算进 `c0`；`c0 += 1` 要放在算完 `ans` 之后',
                 '右边 0 的个数 = `tot0 − c0`；右边 1 的个数 = `len(s) − tot0 − c1`',
                 '同一思路也可看成状态机 DP：状态 `0、1、01、10`，每次转移加一位'],
    ),
)
