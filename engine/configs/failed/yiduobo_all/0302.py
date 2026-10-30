IMG = [list(r) for r in ['0010', '0110', '0100']]


def _bs(S):
    I = S.get('_inner', {})
    return I if 'head' in I and 'delta' in I else None


def _color(S, i, j, v):
    I = _bs(S)
    if I is None:
        return 'green' if v == '1' else None
    horiz = 'bottom' not in S
    k = i if horiz else j
    if 'mid' in I and k == I['mid']:
        return 'yellow'
    if I['head'] <= k <= I['tail']:
        return 'blue' if v != '1' else 'green'
    return None


def _txt(S):
    I = _bs(S)
    if I is None:
        if 'top' in S:
            return f"top={S['top']}" + (f" bottom={S['bottom']}" if 'bottom' in S else '') + (f" left={S['left']}" if 'left' in S else '') + (f" right={S['right']}" if 'right' in S else '')
        return ''
    what = '行' if 'bottom' not in S else '列'
    return f"二分{what}：候选 [{I['head']}, {I['tail']}]" + (f"，试探第 {I['mid']} {what}" if 'mid' in I else '')


CONFIG = dict(
    num=302, title='包含全部黑色像素的最小矩形', difficulty='Hard', category='二分算法',
    author='yiduobo', technique='四次二分求边界',
    tags=['二分算法'],
    code='''
class Solution(object):
    def minArea(self, image, x, y):

        m = len(image)
        n = len(image[0])

        def check_h(i):
            for j in range(n):
                if image[i][j] == '1':
                    return True

            return False

        def check_v(j):
            for i in range(m):
                if image[i][j] == '1':
                    return True

            return False

        def binary_search(head, tail, delta, check):
            while head < tail:
                mid = (head + tail + delta) >> 1
                if check(mid):
                    if delta == 0:
                        tail = mid
                    else:
                        head = mid
                else:
                    if delta == 0:
                        head = mid + 1
                    else:
                        tail = mid - 1

            return head

        top = binary_search(0, x, 0, check_h)
        bottom = binary_search(x, m - 1, 1, check_h)
        left = binary_search(0, y, 0, check_v)
        right = binary_search(y, n - 1, 1, check_v)

        return (bottom - top + 1) * (right - left + 1)
''',
    call=f'Solution().minArea({IMG!r}, 0, 2)',
    expect=6,
    skip=[8, 15],
    max_steps=110,
    views=[
        dict(type='grid', var='image', label='image（绿 = 黑色像素；蓝 = 二分候选范围；黄 = 正在检查的行/列）', cell=110, h=330,
             color=_color),
        dict(type='text', fn=_txt, size=26, h=110),
    ],
    watch=['top', 'bottom', 'left', 'right', ('head', lambda S: S.get('_inner', {}).get('head'), 'blue'),
           ('tail', lambda S: S.get('_inner', {}).get('tail'), 'pink')],
    captions={
        'm = len(image)': '`m = {m}` 行',
        'n = len(image[0])': '`n = {n}` 列',
        'if image[i][j]': lambda S, B, r: (f'`image[{S.i}][{S.j}] = {S.image[S.i][S.j]}`' + (' ==黑色==：这一行有黑色块 → 返回 True' if S.image[S.i][S.j] == '1' else '：白色，看下一个')) if 'i' in S and 'j' in S else '',
        'return True': '找到黑色像素 → 这一行（列）有黑色块',
        'return False': '整行（列）全白 → 没有黑色块',
        'while head < tail': lambda S, B, r: (f'候选区间 `[{S.head}, {S.tail}]` → 继续' if S.head < S.tail else f'区间收敛到 `{S.head}` → 结束'),
        'mid = (head + tail + delta) >> 1': lambda S, B, r: f'`mid = {S.mid}`：{"找最小值，向下取整" if S.delta == 0 else "找最大值，向上取整（+1），避免死循环"}',
        24: lambda S, B, r: f'检查第 `{S.mid}` {"行" if 'bottom' not in S else "列"}有没有黑色块',
        'if delta == 0': lambda S, B, r: ('`delta == 0`：在找最上（最左）边界' if S.delta == 0 else '`delta == 1`：在找最下（最右）边界'),
        26: '有黑块：第 `{mid}` 行（列）可能就是最上（最左）→ `tail = {tail}`',
        31: '没有黑块：最上（最左）一定在后面 → `head = {head}`',
        28: '有黑块：第 `{mid}` 行（列）可能就是最下（最右）→ `head = {head}`',
        33: '没有黑块：最下（最右）一定在前面 → `tail = {tail}`',
        'return head': '边界找到：`{head}`',
        'top = binary_search': '最上侧黑色行 `top = {top}`（已知 `x` 行是黑色，所以在 `[0, x]` 里找）',
        'bottom = binary_search': '最下侧黑色行 `bottom = {bottom}`（在 `[x, m-1]` 里找）',
        'left = binary_search': '最左侧黑色列 `left = {left}`（在 `[0, y]` 里找）',
        'right = binary_search': '最右侧黑色列 `right = {right}`（在 `[y, n-1]` 里找）',
        'return (bottom - top + 1)': '面积 `({bottom} - {top} + 1) × ({right} - {left} + 1)` = =={ret}==',
    },
    cards=dict(
        one_liner='黑色像素连成一块：四个方向各二分一次找边界',
        complexity='时间 `O(m log n + n log m)`，空间 `O(1)`',
        problem=['`image` 是 0/1 字符矩阵，保证只有一块相连的黑色像素（`1`）',
                 '已知其中一个黑色像素 `(x, y)`，求包含所有黑色像素的最小矩形面积',
                 '本视频：`[["0","0","1","0"],["0","1","1","0"],["0","1","0","0"]]`，`(0, 2)` → `6`'],
        quote='若有，那么就可以调整二分的上界为mid，否则需要调整二分的下界为mid + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['黑色块连通 → 每一行（列）有没有黑块，具有==单调性==（以 `(x, y)` 为界）',
              '最上边界：在 `[0, x]` 二分，有黑块就收上界',
              '另三个方向照做，最后面积 = 高 × 宽'],
        summary=['时间 `O(m log n + n log m)`：每次检查扫一整行或一整列',
                 '找最小边界用 `delta = 0`（向下取整，`tail = mid`）；找最大边界用 `delta = 1`（向上取整，`head = mid`）',
                 '`(x, y)` 是黑色，保证了二分的搜索范围',
                 '原文为 Python 2 风格，本题代码无需改动；输入 `image` 用字符矩阵'],
    ),
)
