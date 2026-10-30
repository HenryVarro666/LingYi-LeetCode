def _txt(S):
    if 'last_x' not in S:
        return '山 = 等腰直角三角形：峰 `(x, y)` 的底边是 ==[x−y, x+y]=='
    if 'x' not in S or S['last_x'] is None:
        return '还没有「当前最外层的山」'
    return f"当前外层山底边 `[{S['last_x']}, {S['last_y']}]`，正在看 `[{S['x']}, {S['y']}]`，还剩 `res = {S['res']}` 座"


CONFIG = dict(
    num=2345, title='寻找可见山的数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='转成区间 · 排序后找被包含的',
    code='''
class Solution(object):
    def visibleMountains(self, peaks):

        intervals = []
        for x, y in peaks:
            intervals.append([x - y, x + y])
        
        last_x, last_y = None, None
        check_same = False
        res = len(peaks)
        for x, y in sorted(intervals, key=lambda d:(d[0], -d[1])):
            if last_x is None:
                last_x, last_y = x, y
            else:
                if not check_same and last_x == x and last_y == y:
                    check_same = True
                    res -= 1

                if last_x <= x and y <= last_y:
                    res -= 1
                else:
                    last_x, last_y = x, y
                    check_same = False
                
        return res
''',
    call='Solution().visibleMountains([[2,2],[6,3],[6,3],[9,1]])',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=28, h=90),
        dict(type='intervals', var='intervals', h=330),
        dict(type='array', var='peaks', label='peaks（峰的坐标 [x, y]）', h=150, cell=130, fmt=lambda v: str(v)),
    ],
    watch=['x', 'y', ('last_x', 'last_x', 'blue'), ('last_y', 'last_y', 'blue'), 'check_same', ('res', 'res', 'green')],
    captions={
        'for x, y in peaks': '取峰 `({x}, {y})`',
        'intervals.append': '峰 `({x}, {y})` 的底边：`[{x} − {y}, {x} + {y}]` = `{intervals[-1]}`',
        'last_x, last_y = None': '`last` 记录目前「最外层」那座山的底边',
        9: '`check_same` 标记：这座山的完全重叠副本，是否已经多扣过一次',
        'res = len': '先假设全部 `{res}` 座山都可见，后面遇到被盖住的再减',
        'for x, y in sorted': lambda S, B, r: f'按左端点升序、左端相同时右端降序，取下一个区间 `[{S.x}, {S.y}]`',
        'if last_x is None': lambda S, B, r: ('`last_x` 还是 None：还没有最外层的山' if S.last_x is None else '已有最外层的山，和它比较'),
        22: lambda S, B, r: f'`last` 更新为 `[{S.last_x}, {S.last_y}]`：这座山没被前面的盖住，成为新的最外层',
        'if not check_same': lambda S, B, r: ('与 `last` 完全相同 → 两座重叠的山都不可见：先 `res` 减 1（另一座下面的包含判断再减 1）' if (not S.check_same and S.last_x == S.x and S.last_y == S.y) else '不是「首次遇到的完全重叠」，不用额外处理'),
        13: '第一个区间直接成为 `last`：`[{last_x}, {last_y}]`',
        17: '重叠的两座山都不可见：这是多扣的那一座，`res` → =={res}==',
        'check_same = True': '记下已处理重叠，同一座山的第三份重复不再多扣',
        20: lambda S, B, r: f'这座山不可见，`res` 减 1 → =={S.res}==',
        'if last_x <= x': lambda S, B, r: (f'`{S.last_x} <= {S.x}` 且 `{S.y} <= {S.last_y}`：底边被 `last` 完全包含 → 山顶被盖住' if (S.last_x <= S.x and S.y <= S.last_y) else f'`[{S.x}, {S.y}]` 伸出了 `last` 的右端 → 没被盖住'),
        23: '换了新的最外层山，重置 `check_same`',
        'return res': '可见的山一共 `{res}` 座',
    },
    cards=dict(
        one_liner='山是等腰直角三角形，山顶被盖住 = 底边被别的底边包含',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每座山是等腰直角三角形，峰在 `(x, y)`，底在 x 轴上',
                 '一座山的山顶==被另一座山盖住==（含边界），就不可见',
                 '返回可见山的数量；两座完全一样的山，==两座都不可见==',
                 '本视频：`[[2,2],[6,3],[6,3],[9,1]]` → `2`'],
        quote='一座山的顶峰被另一座山覆盖等价于其底边被另一座山的底边完全包含，于是问题就转化成了给出若干区间，求没有被其他区间完全包围的区间。',
        quote_src='—— yiduobo 题解原文',
        idea=['峰 `(x, y)` → 底边区间 `[x−y, x+y]`，几何问题变成区间包含',
              '按左端升序、左端相同时右端降序排序，外层的区间排在前面',
              '一趟扫描：和当前最外层区间比较，被包含就减一座，否则它成为新的最外层',
              '重复的区间要特判：用 `check_same` 保证两座重叠的山都被扣掉'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错点：两座完全重叠的山==都不可见==，所以第一次碰到重复时要多扣一座',
                 '排序键 `(左端, -右端)` 保证左端相同时大区间先出现',
                 '原文为 Python 2 风格，在 Python 3 下无需改动'],
    ),
)
