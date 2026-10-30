import math

CONFIG = dict(
    num=1610, title='可见点的最大数目', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='极角排序 + 环形双指针',
    tags=['滑动窗口与双指针'],
    code='''
class Solution(object):
    def visiblePoints(self, points, angle, location):

        angel_list = []
        overlap = 0
        for x, y in points:
            if x == location[0] and y == location[1]:
                overlap += 1
            else:
                tmp = math.atan2(location[1] - y, location[0] - x)
                angel_list.append(tmp)
                angel_list.append(tmp + 2 * math.pi)
        
        angel_list = sorted(angel_list)
        l = r = 0
        res = 0
        while r < len(angel_list):
            while l < r and angel_list[r] - angel_list[l] > angle * math.pi / 180.0:
                l += 1
            res = max(res, r - l + 1)
            r += 1

        return res + overlap
''',
    setup='import math',
    call='Solution().visiblePoints([[4,0],[4,2],[1,1],[1,5]], 60, [1,1])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"窗口内极角差 `{S['angel_list'][S['r']]-S['angel_list'][S['l']]:.2f}` rad，视野 `{S['angle']*math.pi/180:.2f}` rad；重合点 `{S['overlap']}` 个" if 'r' in S and 'l' in S and 'res' in S and S['r'] < len(S['angel_list']) else '')),
        dict(type='array', var=lambda S: [round(v, 1) for v in S['angel_list']], pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), h=300, label='angel_list（极角，弧度；后半是 +2π 的副本）',
             dim=lambda S, i, v: 'l' in S and 'r' in S and 'res' in S and not (S['l'] <= i <= S['r'])),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('res', 'res', 'green'), 'overlap'],
    captions={
        'overlap += 1': '点和 location 重合：==永远可见==，单独记数 `overlap = {overlap}`',
        'tmp = math.atan2': '以 location 为原点，该点的极角 `{tmp:.2f}` rad',
        'tmp + 2 * math.pi': '再放一份 `+2π` = {tmp + 6.28318:.2f}，把环形拉直，处理跨过 ±π 的窗口',
        'angel_list = sorted': '极角排序：{[round(v, 2) for v in angel_list]}',
        'while l < r': '窗口 `[l, r]` 极角差 `{angel_list[r]-angel_list[l]:.2f}`，视野 `{angle*3.14159/180:.2f}` rad：{"超出视野，左端收缩" if (l < r and angel_list[r]-angel_list[l] > angle*3.14159/180) else "还在视野内"}',
        'l += 1': '最左的点放不进扇形，`l` → {l}',
        'res = max': '扇形内点数 `r - l + 1 = {r-l+1}`，`res = max({B.res}, {r-l+1}) = {res}`',
        'return res': '`res + overlap = {res} + {overlap}` = =={ret}==',
    },
    cards=dict(
        one_liner='极角排序，把环拉直后用滑窗找最多点的扇形',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['站在 `location`，视野是一个角度为 `angle` 的扇形，可任意旋转',
                 '求同时能看见的最多点数；与 location 重合的点永远可见',
                 '示例：`points=[[4,0],[4,2],[1,1],[1,5]]`，`angle=60`，`location=[1,1]` → `3`'],
        quote='以location作为原点建立坐标系，……题目就变成了找出一些点，这些点极角的最大值和最小值之差小于等于angle。实际上这就是一个环形上的区间覆盖问题。',
        quote_src='—— yiduobo 题解',
        idea=['先用 `atan2` 算每个点的极角，重合点另记 `overlap`',
              '环形怎么办？==每个极角再加一份 +2π==，数组拉成两圈',
              '排序后双指针：右端 `r` 前进，极角差超过 angle 就收缩 `l`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：==重合点不能参与 atan2==，要单独 +overlap',
                 '角度要先换成弧度：`angle * pi / 180`',
                 '`tmp` 与 `tmp + 2π` 不会被同一窗口覆盖（angle < 360），不会重复计数'],
    ),
)
