N, K0 = 25, 15
ORDER = sorted(range(1, N + 1), key=str)          # 字典序 = 十叉树的先序遍历
RANK = {v: i + 1 for i, v in enumerate(ORDER)}


def _in_sub(u, v):
    return str(u).startswith(str(v))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'n = {N} 的十叉树（先序遍历 = 字典序，从左到右摆放）', 24, T['muted'], bold=True)
    sp = (x1 - x0 - 60) / N
    rad = min(17, sp * 0.45)

    def X(v):
        return x0 + 30 + (RANK[v] - 0.5) * sp

    def Y(v):
        return y0 + 150 if v < 10 else y0 + 250

    rx, ry = (x0 + x1) / 2, y0 + 62
    line = S.get('_line', 0)
    res = S.get('res')
    k = S.get('k')
    visited = K0 - k if isinstance(k, int) else 0
    counting = res is not None and 'cnt' in S and line in (6, 7, 8, 9, 10, 14)
    tmp = S.get('tmp')
    fresh = counting and isinstance(tmp, int) and tmp % res == 0 and str(tmp // res).strip('0') == '1'  # tmp 属于本轮
    layer = None
    if fresh and line in (9, 10) and tmp <= N:
        layer = (S['tmp'], min(S['next'], N + 1) - 1)
    for v in range(1, N + 1):
        px, py = (rx, ry) if v < 10 else (X(v // 10), Y(v // 10))
        cv.line([(px, py + (12 if v < 10 else rad)), (X(v), Y(v) - rad)], T['border'], 2)
    cv.d.ellipse((rx - 22, ry - 22, rx + 22, ry + 22), fill=T['panel2'], outline=T['border'], width=2)
    cv.text((rx, ry), '根', 20, T['muted'], anchor='mm', bold=True)
    if counting:
        sub = [u for u in range(1, N + 1) if _in_sub(u, res)]
        a, b = min(RANK[u] for u in sub), max(RANK[u] for u in sub)
        top = Y(res) - rad - 10
        cv.rect((x0 + 30 + (a - 1) * sp + 2, top, x0 + 30 + b * sp - 2, y0 + 282), fill=T['cyan'], alpha=26, r=12)
        cv.rect((x0 + 30 + (a - 1) * sp + 2, top, x0 + 30 + b * sp - 2, y0 + 282), outline=T['cyan'], width=2, r=12)
        cv.text((x0 + 30 + (a - 1) * sp + 6, top - 14), f"以 {res} 为根的子树：已数 cnt = {S['cnt']}", 20, T['cyan'],
                anchor='lm', bold=True)
    for v in range(1, N + 1):
        r = RANK[v]
        fill, tc, oc, ow = T['panel2'], T['text'], T['border'], 2
        if r <= visited:
            fill = (30, 70, 45)
        if fresh and _in_sub(v, res) and v < tmp and not (layer and layer[0] <= v):
            oc, ow = T['cyan'], 4  # 已经数过的层
        if v == res:
            fill, tc = T['blue'], T['bg']
        if layer and layer[0] <= v <= layer[1]:
            oc, ow = T['orange'], 4
        cv.d.ellipse((X(v) - rad, Y(v) - rad, X(v) + rad, Y(v) + rad), fill=fill, outline=oc, width=ow)
        cv.text((X(v), Y(v)), v, 17 if v >= 10 else 20, tc, anchor='mm', bold=True)
    yr = y0 + 300
    for v in ORDER:
        r = RANK[v]
        c = T['pink'] if r == K0 else (T['green'] if r <= visited else T['dim'])
        cv.text((X(v), yr + 2), r, 16, c, anchor='mt', mono=True, bold=r == K0)
    cv.text((x0 + 18, yr + 28), '↑ 先序第几个', 18, T['dim'])
    cv.text((X(ORDER[K0 - 1]), yr + 26), f'第 {K0} 个 = 答案', 18, T['pink'], anchor='mt', bold=True)
    cv.text((x1 - 20, yr + 28), '橙 = 正在数的这一层', 19, T['orange'], anchor='ra')


def _text(S):
    if 'res' not in S:
        return f'找 `[1, {N}]` 的字典序第 `{K0}` 小 = 十叉树先序遍历的第 `{K0}` 个节点'
    if 'cnt' in S and S['_line'] in (6, 7, 8, 9, 10):
        if 'tmp' in S and S['tmp'] <= N and S['_line'] in (9, 10) and S['tmp'] % S['res'] == 0:
            return f"这一层：`[{S['tmp']}, min({S['next']}, n + 1) − 1]`，共 `{min(S['next'], N + 1) - S['tmp']}` 个"
        return f"逐层填充，数以 `{S['res']}` 为根的子树有多少个节点"
    return f"已排除 `{K0 - S['k']}` 个节点，还要找第 `k = {S['k']}` 个（从 `res = {S['res']}` 往后数）"


def _if_cap(S, B, ret):
    if S.k >= S.cnt:
        return f'`k = {S.k} ≥ cnt = {S.cnt}`：第 k 个节点==不在==以 `{S.res}` 为根的子树中'
    return f'`k = {S.k} < cnt = {S.cnt}`：要找的节点==就在==以 `{S.res}` 为根的子树中'


CONFIG = dict(
    num=440, title='字典序的第K小数字', difficulty='Hard', category='数学',
    author='yiduobo', technique='十叉树先序遍历 · 逐层统计子树大小',
    tags=['热题173'],
    code='''
class Solution(object):
    def findKthNumber(self, n, k):
        res = 1
        k -= 1
        while k > 0:
            cnt = 0
            tmp = res
            next = res + 1
            while tmp <= n:
                cnt += min(next, n + 1) - tmp
                tmp *= 10
                next *= 10
            print(tmp, next, cnt)
            if k >= cnt:
                k -= cnt
                res += 1
            else:
                k -= 1
                res *= 10

        return res
''',
    call=f'Solution().findKthNumber({N}, {K0})',
    expect=22,
    skip=['print(tmp, next, cnt)', 'tmp *= 10', 'next *= 10'],
    views=[
        dict(type='custom', draw=_draw, h=360),
        dict(type='text', fn=_text, size=25, h=56),
    ],
    watch=[('res', 'res', 'blue'), ('k', 'k', 'pink'), ('cnt', 'cnt', 'cyan'), ('tmp', 'tmp', 'orange'), ('next', 'next')],
    captions={
        'res = 1': '从根节点的第一个儿子 `1` 开始，`res` 是当前迭代到的节点',
        'k -= 1': lambda S, B, r: (f'节点 `1` 已经算一个：`k` → `{S.k}`' if S._line == 4 else
                                   f'排除节点 `{B.res}` 自己：`k - 1` → `{S.k}`'),
        'while k > 0': lambda S, B, r: (f'`k = {S.k} > 0`：继续迭代' if S.k > 0 else
                                        '`k = 0`：此时迭代到的根节点就是答案'),
        'cnt = 0': '`cnt`：以 `res` 为根的子树一共有多少个节点',
        'tmp = res': '`tmp` 从 `res = {res}` 这一层开始',
        'next = res + 1': '`next = res + 1 = {next}`：这一层的节点在 `[tmp, next)` 里',
        'while tmp <= n': lambda S, B, r: (f'`tmp = {S.tmp} ≤ n`：整棵树可以扩展到这一层' if S.tmp <= S.n else
                                           f'`tmp = {S.tmp} > n`：没有这一层了，子树共 `cnt = {S.cnt}` 个节点'),
        'cnt += min(next, n + 1) - tmp': '这一层 `min({B.next}, n + 1) - {B.tmp}` 个 → `cnt = {cnt}`；`tmp`、`next` 各乘 10 进入下一层',
        'if k >= cnt': _if_cap,
        'k -= cnt': '`k - cnt` → `{k}`：==排除了以 {B.res} 为根的树中的所有节点==',
        'res += 1': '按同样的方式计算以 `{res}` 为根的子树',
        'res *= 10': '去以 `{res}` 为根的子树里继续找',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='能提前知道子树有多少节点，就能判断第 k 个在不在子树里',
        complexity='时间 `O(log² n)`（每层最多 10 个兄弟），空间 `O(1)`',
        problem=['给定整数 `n` 和 `k`，返回 `[1, n]` 中==字典序==第 `k` 小的数字',
                 '示例：`n = 13, k = 2` → `10`（`[1,10,11,12,13,2,3,…,9]`）',
                 '`1 <= k <= n <= 10⁹`：模拟先序遍历 `O(k)` 太慢'],
        quote='一个自然的想法就是==如果能提前得知以当前节点为根的子树中有多少个节点==，那么就可以高效地判断第k个节点是否位于当前子树中了。',
        quote_src='—— yiduobo 题解',
        idea=['看成十叉树：先序遍历找第 k 个节点；模拟是 `O(k)`，效率捉急',
              '逐层填充：`tmp × 10 ≤ n` 就能扩展到下一层，每层在 `[tmp, next)` 里',
              '`cnt ≤ k` → 不在子树中，`k -= cnt`，`res + 1`；否则 `k -= 1`，`res × 10`'],
        result='第 15 小是 `22` ✓',
        summary=['时间 `O(log² n)`：下钻 `O(log n)` 层，每层至多 10 个兄弟、每个逐层统计 `O(log n)`',
                 '`k` 表示还要往后数几个：先 `k -= 1` 排除起点 `1`',
                 '最后一层用 `min(next, n + 1)` 截断，别数出超过 n 的数',
                 '对比灵神：同样的十叉树思路；灵神把满层写成 `(pow10 - 1) // 9`，子树大小 `O(1)`',
                 '原文为 Python 2：调试输出 `print tmp, next, cnt` 改成 `print(...)`，动画中跳过该行'],
    ),
)
