def _parts(S):
    """按当前 mid 贪心切分，返回每格所属块号（未凑够的尾巴为 -1）。"""
    sw, mid = S['sweetness'], S.get('mid')
    if mid is None:
        return [-2] * len(sw)
    res, s, cur, buf = [], 0, 0, []
    for v in sw:
        s += v
        buf.append(cur)
        if s >= mid:
            res += buf
            buf, s = [], 0
            cur += 1
    return res + [-1] * len(buf)


def _color(S, i, v):
    p = _parts(S)[i]
    if p == -2:
        return None
    if p == -1:
        return 'orange'
    return 'blue' if p % 2 == 0 else 'green'


def _txt(S):
    if 'mid' not in S:
        return f"二分「每块最小甜度」：范围 `[{S['left']}, {S['right']}]`"
    p = _parts(S)
    n = max(p) + 1 if max(p) >= 0 else 0
    return f"目标甜度 `mid = {S['mid']}`：贪心最多切出 ==`{n}`== 块，需要 `k + 1 = {S['k'] + 1}` 块"


CONFIG = dict(
    num=1231, title='分享巧克力', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='二分答案 · 最小值最大',
    tags=[],
    code='''
class Solution(object):
    def maximizeSweetness(self, sweetness, k):

        left = min(sweetness)
        right = sum(sweetness)

        while left < right:
            mid = (left + right + 1) // 2

            cnt = 0
            s = 0
            for v in sweetness:
                s += v
                if s >= mid:
                    cnt += 1
                    s = 0

            if cnt >= k + 1:
                left = mid
            else:
                right = mid - 1
        
        return left
''',
    call='Solution().maximizeSweetness([3,1,4,1,5,9], 2)',
    expect=6,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='sweetness', label='sweetness（蓝/绿 = 贪心切出的块，橙 = 凑不够 mid 的尾巴）', color=_color, h=260),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'), 'cnt', 's'],
    captions={
        'left = min': '每块至少有一格，所以最小甜度至少是 `min = {left}`',
        'right = sum': '上界：整块都给自己，甜度 `sum = {right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left}` < `right = {S.right}`，答案还在区间里 → 继续二分' if S.left < S.right
                                               else f'`left = right = {S.left}`：区间只剩一个数 → 结束'),
        'mid = (': '求最大值，中点要 ==向上取整==：`mid = ({left} + {right} + 1) // 2 = {mid}`，否则 `left = mid` 会死循环',
        'cnt = 0': '检查 `mid = {mid}` 可行吗？从头贪心切块，块数清零',
        's = 0': '当前块的甜度和清零',
        's += v': '把 `{v}` 并入当前块，甜度和 `s` = {s}',
        'if s >= mid': lambda S, B, r: (f'`s = {S.s} ≥ mid = {S.mid}`：这块够甜了 → ==立刻切下==' if S.s >= S.mid
                                        else f'`s = {S.s} < mid = {S.mid}`：还不够，继续往后并'),
        'cnt += 1': '切下一块，`cnt` = {cnt}',
        'if cnt >= k + 1': lambda S, B, r: (f'`cnt = {S.cnt} ≥ k + 1 = {S.k + 1}`：甜度 {S.mid} 做得到（还有余量）→ 往大了试' if S.cnt >= S.k + 1
                                            else f'`cnt = {S.cnt} < k + 1 = {S.k + 1}`：切不出足够块 → {S.mid} 太大了'),
        'left = mid': '可行 → 答案至少是 `{mid}`：`left = mid = {left}`（mid 本身可行，所以保留）',
        'right = mid - 1': '不可行 → `mid` 及更大都不行：`right = mid - 1 = {right}`',
        'return left': '`left == right`，最大的最小甜度是 =={left}==',
    },
    cards=dict(
        one_liner='求最小值最大：二分「每块最小甜度」，贪心判断切得出几块',
        complexity='时间 `O(n log S)`，空间 `O(1)`',
        problem=['一块巧克力由 `sweetness` 数组表示，要切成 `k + 1` 个连续块分给 `k` 位朋友和自己',
                 '自己拿甜度总和最小的那一块，求这一块最大能有多甜',
                 '本视频：`[3,1,4,1,5,9]`，`k = 2` → `6`'],
        quote='之前410题要求的是分割数组的最大值最小，而本题则是最小值最大，在这里只需要注意符号要反过来。相对应的，二分上下界的变化以及二分中点的计算方式也要做出相应的调整。',
        quote_src='—— yiduobo 题解原文',
        idea=['410 题的镜像：`mid` 是「每块至少要有的甜度」，越大越难切出 `k + 1` 块',
              '贪心：甜度和一够 `mid` 就切，切得越多越好；`cnt >= k + 1` 即可行',
              '求最大 → `left = mid`、`right = mid - 1`，中点向上取整'],
        summary=['时间 `O(n log(sum))`，空间 `O(1)`',
                 '==中点必须 +1 向上取整==：否则 `left = mid` 在 `right = left + 1` 时死循环',
                 '`cnt >= k + 1` 而不是 `==`：切多了可以把相邻块合并，甜度只会更大',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '和 410 题对照：最大值最小 ↔ 最小值最大，符号反过来'],
    ),
)
