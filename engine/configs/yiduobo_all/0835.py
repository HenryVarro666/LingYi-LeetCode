A0 = [[1, 1, 0], [0, 1, 0], [0, 1, 0]]
B0 = [[0, 0, 0], [0, 1, 1], [0, 0, 1]]


def _g1(S, i, j, v):
    if S['_line'] >= 12 and (i, j) == (S.get('x1'), S.get('y1')) and v == 1 and S['_line'] >= 12:
        return 'orange'
    return 'blue' if v == 1 else None


def _g2(S, i, j, v):
    if (i, j) == (S.get('x2'), S.get('y2')) and S['_line'] >= 12 and v == 1:
        return 'pink'
    return 'blue' if v == 1 else None


CONFIG = dict(
    num=835, title='图像重叠', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='统计平移向量出现次数',
    tags=['卷积'],
    code='''
class Solution(object):
    def largestOverlap(self, img1, img2):

        m = len(img1)

        pos1_set = set()
        for x1 in range(m):
            for y1 in range(m):
                if img1[x1][y1] == 1:
                    pos1_set.add((x1, y1))

        pos2_set = set()
        move_dict = {}
        for x2 in range(m):
            for y2 in range(m):
                if img2[x2][y2] == 1:
                    for x1, y1 in pos1_set:
                        delta_x = x1 - x2
                        delta_y = y1 - y2
                        move_dict[(delta_x, delta_y)] = move_dict.get((delta_x, delta_y), 0) + 1
        
        if not move_dict:
            return 0
        return max(move_dict.values())
''',
    call=f'Solution().largestOverlap({A0}, {B0})',
    expect=3,
    views=[
        dict(type='grid', var='img1', label='img1（橙 = 正在配对的 1）', h=170, cell=56,
             color=_g1, cursors=[]),
        dict(type='grid', var='img2', label='img2（粉 = 正在配对的 1）', h=170, cell=56,
             color=_g2, cursors=[]),
        dict(type='map', var='move_dict', label='move_dict：平移向量 (dx, dy) → 能对上的 1 的个数', h=230,
             fmt=lambda k, v: f'{k} → {v}'),
    ],
    watch=[('x2,y2', lambda S: (S.get('x2'), S.get('y2')) if 'y2' in S else None, 'pink'),
           ('x1,y1', lambda S: (S.get('x1'), S.get('y1')) if 'y1' in S else None, 'orange'),
           ('delta', lambda S: (S.get('delta_x'), S.get('delta_y')) if 'delta_y' in S else None, 'yellow')],
    skip=['m = len', 'pos1_set = set', 'pos2_set = set', 'move_dict = {}', 'for x1 in range', 'for y1 in range',
          'for x2 in range', 'for y2 in range', 'if img1[x1]', 'for x1, y1 in pos1_set', 'if img2[x2][y2]', 'if not move_dict', 'delta_x =', 'delta_y ='],
    max_steps=60,
    captions={
        'pos1_set.add': '`img1[{x1}][{y1}]` 是 1 → 记下这个 1 的位置 `({x1}, {y1})`，现有 `{len(pos1_set)}` 个',
        'if img2[x2][y2]': '`img2[{x2}][{y2}] == 1` → 只有 1 才参与配对',
        'move_dict[(delta_x': lambda S, B, r: (f"把 img2 的 `({S.x2},{S.y2})` 移到 img1 的 `({S.x1},{S.y1})` 上，需要平移 `({S.delta_x}, {S.delta_y})`；"
                                             f"这个向量已有 `{S.move_dict[(S.delta_x, S.delta_y)] - 1}` 对，现在 =={S.move_dict[(S.delta_x, S.delta_y)]}== 对"),
        'return max': '出现次数最多的平移向量，就是能同时重叠最多个 1 的平移 → 答案 =={max(move_dict.values())}==',
    },
    cards=dict(
        one_liner='不枚举平移，改成枚举「一对 1」，给它们的平移向量计数',
        complexity='时间 `O(k1·k2)`（1 的个数之积，最坏 `O(n^4)`），空间 `O(k1·k2)`',
        problem=['两个 `n×n` 的 0/1 图像，可平移其中一个（不旋转）',
                 '重叠 = 同一位置都是 1 的个数，求最大值',
                 '本视频：`img1=[[1,1,0],[0,1,0],[0,1,0]]`，`img2=[[0,0,0],[0,1,1],[0,0,1]]` → `3`'],
        quote='我在这里采用的是枚举B中每个值为1的点经过什么样的操作可以重叠到A中值为1的点，然后统计这些操作出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`img2` 的某个 1 移到 `img1` 的某个 1 上，需要平移 `(x1-x2, y1-y2)`',
              '同一个平移向量出现 `k` 次 = 有 `k` 对 1 同时对上 = 重叠 `k`',
              '出现次数最多的向量就是答案；没有 1 时返回 `0`'],
        summary=['时间 `O(k1·k2)`，`k` 是各图里 1 的个数；空间同阶',
                 '`move_dict` 为空（某图全 0）时 `max` 会报错，要先判断返回 0',
                 '`pos2_set` 在原代码里没有用到，可忽略',
                 '对比灵神：他枚举 `(2n-1)^2` 个平移再数重叠；这里反过来，枚举 1 的配对来投票'],
    ),
)
