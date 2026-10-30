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
    if 'dis_x' in S:
        cv.arrow((px(S['x']), yy - 80), (px(S['z']), yy - 80), T['blue'], 3)
        cv.text(((px(S['x']) + px(S['z'])) / 2, yy - 108), f"dis_x = {S['dis_x']}", 24, T['blue'], anchor='mm', bold=True)
    if 'dis_y' in S:
        cv.arrow((px(S['y']), yy + 70), (px(S['z']), yy + 70), T['pink'], 3)
        cv.text(((px(S['y']) + px(S['z'])) / 2, yy + 96), f"dis_y = {S['dis_y']}", 24, T['pink'], anchor='mm', bold=True)


CONFIG = dict(
    num=3516, title='找到最近的人', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='两个绝对值比大小',
    tags=[],
    code='''
class Solution(object):
    def findClosest(self, x, y, z):
        
        dis_x = abs(x - z)
        dis_y = abs(y - z)
        if dis_x < dis_y:
            return 1
        if dis_x > dis_y:
            return 2
        return 0
''',
    call='Solution().findClosest(2, 5, 6)',
    expect=2,
    views=[
        dict(type='custom', h=330, draw=_draw),
        dict(type='text', size=32, fn=lambda S: f"`dis_x` = =={S['dis_x']}==，`dis_y` = =={S['dis_y']}==" if 'dis_x' in S and 'dis_y' in S else ''),
    ],
    watch=['x', 'y', 'z', ('dis_x', 'dis_x', 'blue'), ('dis_y', 'dis_y', 'pink')],
    captions={
        'dis_x = abs': '第一个人到 z 的距离：`|{x} − {z}|` = =={dis_x}==',
        'dis_y = abs': '第二个人到 z 的距离：`|{y} − {z}|` = =={dis_y}==',
        'if dis_x < dis_y': '`{dis_x} < {dis_y}`？{"是，x 更近，第一个人先到" if dis_x < dis_y else "否，x 不比 y 近"}',
        'return 1': '`dis_x` 更小 → 第一个人先到，返回 ==1==',
        'if dis_x > dis_y': '`{dis_x} > {dis_y}`？{"是，y 更近，第二个人先到" if dis_x > dis_y else "否，两个距离相等"}',
        'return 2': '`dis_y` 更小 → 第二个人先到，返回 ==2==',
        'return 0': '两个距离相等，同时到达，返回 ==0==',
    },
    cards=dict(
        one_liner='分别算 x、y 到 z 的距离，谁小谁先到',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`x`、`y` 是两个人的位置，`z` 是不动的第三个人',
                 '两人同速向 `z` 移动，问谁先到：1、2 或同时到 0',
                 '本视频：`x=2, y=5, z=6` → `2`'],
        quote='题目实际上就是需要判断x和y哪个与z的距离更近，因此只需分别计算x和y与z的差的绝对值就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['速度相同，路程短的先到',
              '路程就是位置差的绝对值',
              '三种情况：小于返回 1，大于返回 2，否则 0'],
        before=[dict(heading='三种结果', lines=['`dis_x < dis_y`：第一个人先到，返回 1', '`dis_x > dis_y`：第二个人先到，返回 2', '两者相等：同时到达，返回 0'])],
        after=[dict(heading='另外两个示例', lines=['`x=2, y=7, z=4`：距离 2 和 3，返回 1', '`x=1, y=5, z=3`：距离 2 和 2，返回 0'])],
        summary=['时间、空间都是 `O(1)`',
                 '别忘了取绝对值：z 可以在 x、y 的任何一侧',
                 '原文为 Python 2 写法，仅有类型说明注释，代码无需修改'],
    ),
)
