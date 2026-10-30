CONFIG = dict(
    num=3516, title='找到最近的人', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='比较距离',
    tags=[],
    code='''
class Solution:
    def findClosest(self, x: int, y: int, z: int) -> int:
        a = abs(x - z)
        b = abs(y - z)
        if a == b:
            return 0
        return 1 if a < b else 2
''',
    call='Solution().findClosest(2, 7, 4)',
    expect=1,
    views=[
        dict(type='custom', h=330, draw=lambda cv, S, B, box, T: _draw(cv, S, B, box, T)),
        dict(type='text', size=32, fn=lambda S: f"`a = |x−z|` = =={S['a']}==，`b = |y−z|` = =={S['b']}==" if 'a' in S and 'b' in S else ''),
    ],
    watch=['x', 'y', 'z', ('a', 'a', 'blue'), ('b', 'b', 'pink')],
    captions={
        'a = abs': '速度相同，时间只看距离：第 1 个人 `a = |{x} − {z}|` = =={a}==',
        'b = abs': '第 2 个人 `b = |{y} − {z}|` = =={b}==',
        'if a == b': '`a = {a}`，`b = {b}`：{"相等，同时到达" if a == b else "不相等，继续比较谁更近"}',
        'return 0': '距离相同，同时到达 → 返回 ==0==',
        'return 1 if': '`a {"<" if a < b else ">"} b`（{a} {"<" if a < b else ">"} {b}）→ 距离{"短" if a < b else "长"}的人先到，返回 =={ret}==',
    },
    cards=dict(
        one_liner='速度相同，谁离第三个人近谁先到',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['数轴上三个人：`x`、`y` 在移动，`z` 不动，速度相同',
                 '第 1 人先到返回 1，第 2 人先到返回 2，同时到返回 0',
                 '示例：`x=2, y=7, z=4` → `1`'],
        quote='时间等于距离除以速度，由于两人速度相同，转化成比较两人到第三人的距离。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设 `a = |x−z|`，`b = |y−z|`',
              '`a == b` 返回 0；`a < b` 返回 1；否则返回 2'],
        after=[dict(heading='写法二', lines=['`(a > b) << 1 | (a < b)`：用 bool 自动转 int 把三种情况合成一行',
                                              '`a > b` 得 2，`a < b` 得 1，相等得 0'])],
        before=[dict(heading='为什么只比距离', lines=['到达时间 = 距离 ÷ 速度', '两人速度相同，除数一样', '所以距离小的，时间一定短']),
                dict(heading='距离怎么算', lines=['位置差可能是负数，例如 `x=7, z=4` 差 −3', '距离取绝对值：`|7 − 4| = 3`', 'z 在两人中间时，也一样是绝对值'])],
        summary=['时间、空间都是 `O(1)`',
                 '易错：要取==绝对值==，z 可能在两人之间或同侧',
                 '本视频演示写法一，写法二是位运算压缩版'],
    ),
)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    if 'x' not in S:
        return
    xs = [S['x'], S['y'], S['z']]
    lo, hi = min(xs) - 1, max(xs) + 1
    ax0, ax1 = x0 + 50, x1 - 50
    yy = y0 + (y1 - y0) * 0.55
    sc = (ax1 - ax0) / (hi - lo)
    px = lambda v: ax0 + (v - lo) * sc
    cv.line([(ax0, yy), (ax1, yy)], T['border'], 3)
    for v in range(lo, hi + 1):
        cv.line([(px(v), yy - 6), (px(v), yy + 6)], T['border'], 2)
        cv.text((px(v), yy + 18), v, 18, T['dim'], anchor='mt', mono=True)
    for name, key, c in (('x', 'x', 'blue'), ('y', 'y', 'pink'), ('z', 'z', 'green')):
        X = px(S[key])
        cv.rect((X - 22, yy - 60, X + 22, yy - 20), fill=T[c], r=8)
        cv.text((X, yy - 40), name, 26, T['bg'], anchor='mm', bold=True)
    if 'a' in S:
        cv.arrow((px(S['x']), yy - 80), (px(S['z']), yy - 80), T['blue'], 3)
        cv.text(((px(S['x']) + px(S['z'])) / 2, yy - 108), f"a = {S['a']}", 24, T['blue'], anchor='mm', bold=True)
    if 'b' in S:
        cv.arrow((px(S['y']), yy + 70), (px(S['z']), yy + 70), T['pink'], 3)
        cv.text(((px(S['y']) + px(S['z'])) / 2, yy + 96), f"b = {S['b']}", 24, T['pink'], anchor='mm', bold=True)
