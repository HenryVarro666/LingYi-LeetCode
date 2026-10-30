G = [[1, 2, 3, 4], [10, 11, 12, 5], [9, 8, 7, 6]]
ARROW = ['→ 向右', '↓ 向下', '← 向左', '↑ 向上']


def _seen(S, i, j, v):
    ans = S.get('ans')
    if ans is not None and v in ans:
        return 'green'
    return None


def _cur(S):
    i, j = S.get('i'), S.get('j')
    if i is None or not (0 <= i < len(S['array']) and 0 <= j < len(S['array'][0])):
        return None, None
    return i, j


def _txt(S):
    if 'di' not in S:
        return '按「右、下、左、上」的顺序，一段一段地走'
    return f'当前方向 =={ARROW[S["di"]]}==　这一段要走 `n = {S["n"]}` 步，走完后 `n, m = m - 1, n`'


CONFIG = dict(
    num='LCR 146', title='螺旋遍历二维数组', difficulty='Easy', category='网格图',
    author='灵茶山艾府', technique='模拟 · 不标记 · 精确控制每段步数',
    tags=[],
    code='''
DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)  # 右下左上

class Solution:
    def spiralArray(self, array: List[List[int]]) -> List[int]:
        if not array:
            return []
        m, n = len(array), len(array[0])
        size = m * n
        ans = []
        i, j, di = 0, -1, 0  # 从 (0, -1) 开始
        while len(ans) < size:
            dx, dy = DIRS[di]
            for _ in range(n):  # 走 n 步（注意 n 会减少）
                i += dx
                j += dy  # 先走一步
                ans.append(array[i][j])  # 再加入答案
            di = (di + 1) % 4  # 右转 90°
            n, m = m - 1, n  # 减少后面的循环次数（步数）
        return ans
''',
    call=f'Solution().spiralArray({G})',
    expect=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    skip=['size = m * n', 'ans = []', 'i += dx', 'j += dy', 'for _ in range(n)'],
    views=[
        dict(type='grid', var='array', label='array（绿 = 已加入答案）', cursors=[(lambda S: _cur(S)[0], lambda S: _cur(S)[1], 'yellow')],
             color=_seen, cell=96, h=330),
        dict(type='text', h=60, size=30, fn=_txt),
        dict(type='array', var='ans', label='ans', h=170, cell=64),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('di', 'di', 'orange'), ('n', 'n'), ('m', 'm')],
    captions={
        'm, n = len(array)': '行数 `m = {m}`，列数 `n = {n}`',
        'i, j, di = 0, -1': '从 `(0, -1)` 出发：先走一步才到 `(0, 0)`，==这样每一步都是「先走再取」==，写法统一',
        'while len(ans) < size': lambda S, B, ret: (f'`len(ans) = {len(S.ans)} < {S.size}`：还没取完，再走一段' if len(S.ans) < S.size
                                                    else f'`len(ans) = {len(S.ans)}` = mn：全部取完'),
        'dx, dy = DIRS[di]': '这一段的方向 `DIRS[{di}]` = `({dx}, {dy})`，{["向右","向下","向左","向上"][di]}，这一段走 `n = {n}` 步',
        'ans.append(array[i][j])': '先走一步到 `({i}, {j})`，再取出 `{array[i][j]}` 加入答案',
        'di = (di + 1) % 4': '这一段走完，==右转 90°==：`di` → {di}（{["向右","向下","向左","向上"][di]}）',
        'n, m = m - 1, n': '==交换并减一==：下一段步数是原来的 `m - 1` = `{n}`；再下一段是原来的 `n` = `{m}`',
        'return ans': '取完，返回 `{ans}`',
    },
    cards=dict(
        one_liner='精确算好每个方向走几步：n、m−1、n−1、m−2……',
        complexity='时间 `O(mn)`，空间 `O(1)`（不计返回值）',
        problem=['给定二维数组，按==顺时针螺旋==顺序返回所有元素',
                 '示例：`[[1,2,3],[8,9,4],[7,6,5]]` → `[1,2,3,4,5,6,7,8,9]`',
                 '本视频：`3×4` 数组 → `[1..12]`'],
        quote='由于走的步数是有规律的，我们可以精确地控制在每个方向上要走多少步，无需判断是否出界、是否重复访问',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['每一段的步数依次是：`n, m-1, n-1, m-2, n-2 ...`',
              '每次只需 `n, m = m - 1, n`，下一轮循环还是走 `n` 步',
              '从 `(0, -1)` 开始，先走一步再取数，不用修改 `array`'],
        summary=['时间 `O(mn)`，空间 `O(1)`；不改动原数组',
                 '易错：起点是 `(0, -1)`，不是 `(0, 0)`；空数组要先判断',
                 '方法一「标记」：访问过的置为 `None`，撞墙或遇到已访问就右转',
                 '同类题：1041 困于环中的机器人、874 模拟行走机器人'],
    ),
)
