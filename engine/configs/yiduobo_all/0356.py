PTS = [[0, 1], [-1, 0], [2, 1], [1, 2], [3, 0], [1, 0], [1, 2]]


def _pts(S):
    if 'points' not in S:
        return None
    return [f'({x},{y})' for x, y in S['points']]


def _line_txt(S):
    cx = S.get('check_x')
    if 'check_x' in S and cx is not None:
        return f'已确定的对称轴：`x + x\' = {cx}` → 竖直线 x 取 =={cx / 2:g}=='
    return '同一高度 y 上的点，必须关于同一条竖直线对称'


CONFIG = dict(
    num=356, title='直线镜像', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按 y 分组 · 首尾配对求对称轴',
    code='''
class Solution(object):
    def isReflected(self, points):

        points_set = {}
        for x, y in points:
            if y not in points_set:
                points_set[y] = set()

            if x not in points_set[y]:
                points_set[y].add(x)

        def get(x_list):
            x_list.sort()
            n = len(x_list)
            check_pos = x_list[0] + x_list[-1]
            left, right = 0, n - 1
            while left <= right:
                if x_list[left] + x_list[right] != check_pos:
                    return None
                left += 1
                right -= 1
            return check_pos

        check_x = None
        for y in points_set:
            tmp = get(list(points_set[y]))
            if tmp is None:
                return False
            if check_x is None:
                check_x = tmp
            elif check_x != tmp:
                return False

        return True
''',
    call=f'Solution().isReflected({PTS})',
    expect=True,
    views=[
        dict(type='array', var=_pts, label='points（按 y 分组前）', cell=118, h=170, index=False),
        dict(type='map', var='points_set', label='points_set（y → 该高度的 x 集合，自动去重）', fmt=lambda k, v: f'y={k}: {sorted(v)}', h=190, font=30),
        dict(type='array', var='x_list', label='x_list（当前这一层，已排序）', cell=84, pointers={'left': 'blue', 'right': 'pink'},
             window=('left', 'right'), h=190),
        dict(type='text', fn=_line_txt, size=28, h=90),
    ],
    watch=[('y', 'y', 'cyan'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('check_pos', 'check_pos', 'orange'), ('check_x', 'check_x', 'green')],
    skip=['n = len(x_list)', 'def get', 'points_set[y] = set()', 'if y not in points_set', 'if x not in points_set'],
    captions={
        'points_set[y].add(x)': '把点 `({x}, {y})` 按高度 `y = {y}` 归组：`points_set[{y}] = {sorted(points_set[y])}`（集合自动去重）',
        'x_list.sort()': '这一层的 x 排好序：`{x_list}`，对称的点必然头尾配对',
        'check_pos = x_list[0] + x_list[-1]': '最左 + 最右 = `{x_list[0]} + {x_list[-1]}` = =={check_pos}==：若对称，所有配对之和都应等于它（轴在正中，x = {check_pos / 2:g}）',
        'left, right = 0, n - 1': '从两端向中间配对：`left = 0`，`right = {right}`',
        'while left <= right': lambda S, B, r: ('`left = {} <= right = {}`，继续配对'.format(S.left, S.right) if S.left <= S.right
                                                else '`left > right`：这一层全部配对成功'),
        'if x_list[left] + x_list[right] != check_pos': lambda S, B, r: ('`{} + {} = {}` ≠ `{}` → ==这一层不对称==，返回 None'.format(S.x_list[S.left], S.x_list[S.right], S.x_list[S.left] + S.x_list[S.right], S.check_pos)
                                                                          if S.x_list[S.left] + S.x_list[S.right] != S.check_pos
                                                                          else '`{} + {} = {}` == `{}` → 这一对关于轴对称'.format(S.x_list[S.left], S.x_list[S.right], S.x_list[S.left] + S.x_list[S.right], S.check_pos)),
        'return None': '返回 `None`',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}：向中间收拢（奇数个时中间点和自己配对）',
        'return check_pos': '这一层对称，返回它的轴位置 `{ret}`（= 2 × 轴的横坐标）',
        'check_x = None': '`check_x` 记录第一层求出的轴，之后的层都要和它相等',
        'tmp = get(': '第 `y = {y}` 层的轴位置 `tmp = {tmp}`',
        'if tmp is None': lambda S, B, r: ('这一层不对称 → 整体不可能，直接 `False`' if S.tmp is None else '这一层自身对称，继续比较轴'),
        'if check_x is None': lambda S, B, r: ('这是第一层：`check_x = {}` 记下来'.format(S.tmp) if B.check_x is None else '已有 `check_x = {}`，要和这一层比较'.format(B.check_x)),
        'check_x = tmp': '`check_x = {check_x}`',
        'elif check_x != tmp': lambda S, B, r: ('`check_x = {} ≠ tmp = {}`：两层的轴不是同一条 → `False`'.format(S.check_x, S.tmp) if S.check_x != S.tmp
                                                else '`check_x == tmp = {}`：两层轴相同，继续'.format(S.tmp)),
        'return False': '返回 `False`',
        'return True': '每一层都对称、轴还都一样 → `True`',
    },
    cards=dict(
        one_liner='同一高度的点必须以同一条竖线对称：首尾配对，轴都得相同',
        complexity='时间 `O(n log n)`（每层排序），空间 `O(n)`',
        problem=['平面上 `n` 个点，问是否存在一条==竖直线==，使所有点关于它镜像后仍在点集中',
                 '点可能重复（重复点要去重）',
                 '示例：`[[1,1],[-1,1]]` → `true`；`[[1,1],[-1,-1]]` → `false`',
                 '本视频：7 个点（含重复），轴在 `x = 1`'],
        quote='对于出现同一竖直高度的所有点而言，如果这些点关于某竖直的直线对称，那么这条直线必然位于这些点横坐标的正中心。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 `y` 把点分组，每组的 x 去重后排序',
              '首尾两两配对：每对之和都应等于 `x_list[0] + x_list[-1]`，否则这层不对称',
              '每层求出的轴位置（两倍横坐标，免去小数）必须全部一致'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：点可能重复，分组时必须用集合去重',
                 '用「x 之和」代替轴的横坐标，避免出现 `.5` 的浮点比较',
                 '奇数个点时 `left == right`，中间点与自己配对，也要满足和等于 `check_pos`'],
    ),
)
