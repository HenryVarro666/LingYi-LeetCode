ENV = [[2, 3], [5, 4], [6, 2], [6, 7], [1, 1], [5, 5]]
SORTED = sorted(ENV, key=lambda d: (d[0], -d[1]))


def _if(S, B, ret):
    res, h = S.res, S.height
    if not res:
        return f'`res` 为空 → 直接放入 {h}'
    if h > res[-1]:
        return f'`{h} > res[-1] = {res[-1]}`：比所有末尾都大 → ==接在后面==，上升子序列变长'
    return f'`{h} ≤ res[-1] = {res[-1]}`：接不上 → ==二分==找第一个 `≥ {h}` 的位置去替换'


def _while(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：区间还没缩成一个点，继续二分'
    return f'`l = r = {S.r}`：找到了第一个 `≥ {S.height}` 的位置'


def _mid_if(S, B, ret):
    m = S.mid
    if S.res[m] < S.height:
        return f'`res[{m}] = {S.res[m]} < {S.height}`：答案在 mid ==右边== → `l = mid + 1`'
    return f'`res[{m}] = {S.res[m]} ≥ {S.height}`：mid 可能就是答案 → `r = mid`'


def _p(name):
    return lambda S: S.get(name) if S.get('_line') in range(12, 20) else None


PL, PR, PM = _p('l'), _p('r'), _p('mid')


def _text(S):
    if 'res' not in S:
        return '按 `(w, -h)` 排序后只取 h：同宽的信封 h 逆序'
    if 'l' in S and S.get('_line') in range(13, 21):
        return f"二分区间 `res[{S['l']}..{S['r']}]`，找第一个 `≥ {S['height']}` 的位置"
    return '`res[k]`：长为 `k+1` 的上升子序列，末尾最小是多少'


CONFIG = dict(
    num=354, title='俄罗斯套娃信封问题', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按 w 排序 · h 上的最长上升子序列',
    tags=['labuladong', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def maxEnvelopes(self, envelopes):

        sorted_envelopes = [x[1] for x in sorted(envelopes, key=lambda d:(d[0], -d[1]))]
        res = []
        for height in sorted_envelopes:
            if not res or height > res[-1]:
                res.append(height)
            else:
                l = 0
                r = len(res) - 1
                while l < r:
                    mid = (l + r) // 2
                    if res[mid] < height:
                        l = mid + 1
                    else:
                        r = mid

                res[r] = height

        return len(res)
''',
    call=f'Solution().maxEnvelopes({ENV!r})',
    expect=4,
    skip=['l = 0', 'r = len(res) - 1'],
    views=[
        dict(type='text', fn=lambda S: '排序后：' + '  '.join(f'[{w},{h}]' for w, h in SORTED), size=26, h=56),
        dict(type='array', var='sorted_envelopes', label='sorted_envelopes（只剩 h）', h=190, cell=80,
             color=lambda S, i, v: 'cyan' if S.get('height') == v and 'res' in S else None),
        dict(type='text', fn=_text, size=26, h=56),
        dict(type='array', var='res', label='res（单调上升）', h=220, cell=80, min_slots=6,
             pointers={PL: 'blue', PR: 'pink', PM: 'yellow'}, pointer_labels={PL: 'l', PR: 'r', PM: 'mid'}),
    ],
    watch=[('height', 'height', 'cyan'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('len(res)', 'len(res)', 'green')],
    captions={
        'sorted_envelopes = [': '按 w 升序；==w 相同按 h 逆序==，避免选到两封同宽信封 → `{sorted_envelopes}`',
        'res = []': '问题转化为 h 上的==最长上升子序列==',
        'for height in': lambda S, B, r: (f'下一个高度 `height = {S.height}`' if B.get('height') != S.get('height') else '全部处理完'),
        'if not res or': _if,
        'res.append(height)': '`res` 末尾加入 {height}，长度 =={len(res)}==',
        'while l < r': _while,
        'mid = (l + r)': '`mid = ({l} + {r}) // 2 = {mid}`',
        'if res[mid] < height': _mid_if,
        'l = mid + 1': '`l` → {l}',
        'r = mid': '`r` → {r}',
        'res[r] = height': '`res[{r}] = {height}`：同样长度，末尾换成更小的 → 后面更容易接',
        'return len(res)': '`res` 的长度就是答案：=={ret}==',
    },
    cards=dict(
        one_liner='先按 w 排序，同宽 h 逆序，问题就变成 h 上的最长上升子序列',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['信封 `[w, h]`：宽和高都==严格更大==才能套进去，不能旋转',
                 '求最多有多少个信封能套成一组',
                 '示例：`[[5,4],[6,4],[6,7],[2,3]]` → `3`',
                 f'本视频：`{ENV}` → `4`'],
        quote='对于w相同的情况是不能选取两个的，因此在排序时可以将w相同的信封==按h逆序排好==，这样一来就可以避免因为h的原因选取到两封相同w信封的情况了。',
        quote_src='—— yiduobo 题解原文',
        idea=['不需要满足原始顺序 → 先按 w 排序，只看 h',
              'h 上求最长上升子序列：`res` 存每个长度的最小末尾',
              '比末尾大就追加，否则手写二分找第一个 `≥ h` 的位置替换'],
        summary=['排序和 LIS 都是 `O(n log n)`',
                 '二分 `res[mid] < height` 时 `l = mid + 1`，否则 `r = mid`：找的是第一个 `≥` 的位置',
                 '易错：同宽若按 h 升序，会选到两封同宽信封',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神直接用 `bisect_left`，yiduobo 手写二分'],
    ),
)
