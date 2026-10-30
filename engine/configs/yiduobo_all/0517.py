def _cur(S):
    m, v = S.get('machines'), S.get('now')
    if v is None or v not in m:
        return None
    return m.index(v)


def _txt(S):
    if 'tot' not in S or 'left_rest' not in S:
        return ''
    n = len(S['machines'])
    return f"目标：每台 `{S['tot']}` 件　｜　左侧净流入 left_rest = ==`{S['left_rest']}`==（负数 = 左边缺货）　｜　最少操作数 res = =={S['res']}=="


def _fmt_color(S, i, v):
    c = _cur(S)
    if c is None or 'tot' not in S:
        return None
    if i == c:
        return 'blue'
    return None


CONFIG = dict(
    num=517, title='超级洗衣机', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='只看超载的洗衣机',
    code='''
class Solution(object):
    def findMinMoves(self, machines):

        n = len(machines)
        tot = sum(machines)

        if tot % n != 0:
            return -1

        tot //= n
        left_rest = 0
        res = 0
        for now in machines:
            if now == tot:
                continue
            elif now < tot:
                left_rest += now - tot
            else:
                now_rest = now - tot
                if left_rest < 0:
                    if now_rest + left_rest >= 0:
                        res = max(now_rest, res)
                    else:
                        res = max(-left_rest, res)
                else:
                    res = max(left_rest + now_rest, res)
                left_rest += now_rest

        return res
''',
    call='Solution().findMinMoves([0,1,4,7])',
    expect=5,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='machines', label='machines（每台洗衣机的衣服数）', color=_fmt_color, h=240,
             dim=lambda S, i, v: _cur(S) is not None and 'tot' in S and v <= S['tot'] and i != _cur(S)),
        dict(type='text', fn=lambda S: (f"当前这台 `now = {S['now']}`，目标 `{S['tot']}`，" + ('==超载==，要往外送' if S['now'] > S['tot'] else '不超载 → 不用管它，只记账' if S['now'] < S['tot'] else '刚好 → 跳过')) if 'now' in S and 'tot' in S else '', size=26, h=60),
    ],
    watch=[('tot(目标)', 'tot', 'cyan'), ('left_rest', 'left_rest', 'blue'), ('now_rest', 'now_rest', 'orange'), ('res', 'res', 'green')],
    captions={
        'tot % n': '总数 `{tot}` 除以 `{n}` 台：{"能整除，继续" if tot % n == 0 else "不能整除 → 永远分不平"}',
        'tot //= n': '每台洗衣机最终应有 `avg = {tot}` 件（后面一直把 tot 当 avg 用）',
        'for now': '{"所有洗衣机都看完了，循环结束" if B.get("now") == now else "看下一台洗衣机：`now = " + str(now) + "`"}',
        'if now == tot': '`now = {now}`，目标 `{tot}` → {"相等：进出一样多，操作数被上游抵消，跳过" if now == tot else "不相等，继续判断"}',
        'elif now < tot': '`{now} < {tot}`：{"缺衣服的台不用管，只记账" if now < tot else "多了，要往外分"}',
        'left_rest += now - tot': '缺货：`left_rest += {now} - {tot}` → =={left_rest}==（左侧累计缺 `{-left_rest}` 件）',
        'now_rest = now - tot': '超载：这台至少要送出 `now_rest = {now} - {tot} =` =={now_rest}== 次',
        'if left_rest < 0': '`left_rest = {left_rest}`：{"左边缺货，这台还得往左补" if left_rest < 0 else "左边有富余送过来"}',
        'if now_rest + left_rest >= 0': '`{now_rest} + ({left_rest}) = {now_rest + left_rest}` → {"够补左边，左右同时送，只需 now_rest 次" if now_rest + left_rest >= 0 else "不够补左边，瓶颈在左边缺口 -left_rest"}',
        'res = max(now_rest, res)': '同时向两侧送：操作数 `now_rest = {now_rest}` → `res = max({now_rest}, {B.res})` = =={res}==',
        'res = max(-left_rest, res)': '右边也得先来货再往左送，瓶颈是左边缺口：`res = max({-left_rest}, {B.res})` = =={res}==',
        'res = max(left_rest + now_rest': '左边送来 `{left_rest}` 件，自己又要送出 `{now_rest}` 件，都经过这台：`res = max({left_rest + now_rest}, {B.res})` = =={res}==',
        'left_rest += now_rest': '更新左侧账：`left_rest += {now_rest}` → =={left_rest}==',
        'return res': '最少需要 `{res}` 次操作',
    },
    cards=dict(
        one_liner='只有超载的洗衣机会拖慢进度，答案是它们操作数的最大值',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一排洗衣机，每次可选若干台，各自往相邻洗衣机送 1 件衣服（同时进行算一步）',
                 '求让每台衣服数相等的最少步数，不可能返回 `-1`',
                 '示例：`[0,1,4,7]` → `5`（总数 12，平均 3）'],
        quote='当前衣服数量k小于等于目标数量avg时，都可以不予考虑。接下来就只需要考虑当前衣服数量k大于avg时的操作了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先求 `avg`；衣服总数不能被台数整除 → `-1`',
              '`k <= avg` 的台：它的操作会被上游的操作覆盖，只记账 `left_rest`',
              '`k > avg` 的台：至少送出 `rest = k - avg` 次；若左侧缺货 `-left_rest`，瓶颈取 `max(rest, -left_rest)`；左侧有余则 `left_rest + rest`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`left_rest` 为负表示左边缺货，要先分三种情况再更新答案',
                 '最后别忘了 `left_rest += now_rest`，否则下一台账不对',
                 '原文为 Python 2 写法，整数除法 `tot /= n` 已改为 `tot //= n`'],
    ),
)
