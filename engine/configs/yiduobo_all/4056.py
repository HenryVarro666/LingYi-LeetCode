def _txt(S):
    if 'points' not in S:
        return ''
    pts = S['points']
    cur = None
    if 'p' in S and 't' in S:
        cur = pts.index((S['p'], S['t']))
    out = []
    for i, (p, t) in enumerate(pts):
        w = f"{p}{'开' if t == 0 else '闭'}"
        out.append(f'==[{w}]==' if i == cur else w)
    return '事件（位置 + 开/闭）：' + ' '.join(out)


CONFIG = dict(
    num=4056, title='统计相交区间对 I', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='扫描线：起点终点排序 · cnt 记未关闭区间',
    tags=[],
    code='''
class Solution(object):
    def countIntersectingIntervals(self, intervals):
        
        points = []
        for x, y in intervals:
            points.append((x, 0))
            points.append((y, 1))
        
        points.sort()
        cnt = 0
        res = 0
        for p, t in points:
            if t == 0:
                res += cnt
                cnt += 1
            else:
                cnt -= 1
        
        return res
''',
    call='Solution().countIntersectingIntervals([[1, 2], [2, 3], [3, 4]])',
    expect=2,
    views=[
        dict(type='intervals', var='intervals', h=230),
        dict(type='text', fn=_txt, size=30, h=120),
        dict(type='text', fn=lambda S: (f"当前未关闭的区间数 `cnt = {S['cnt']}`，已统计相交对数 `res = {S['res']}`" if 'cnt' in S and 'res' in S else ''),
             size=30, h=100),
    ],
    watch=[('p', 'p', 'blue'), ('t', 't', 'pink'), ('cnt', 'cnt', 'cyan'), ('res', 'res', 'green')],
    captions={
        'points = []': '把每个区间拆成两个事件：起点 `(x, 0)` 和终点 `(y, 1)`',
        'points.append((x, 0))': '区间 `[{x}, {y}]` 的起点事件 `({x}, 0)`',
        'points.append((y, 1))': '区间 `[{x}, {y}]` 的终点事件 `({y}, 1)`',
        'points.sort()': '按位置从小到大排；位置相同时 `0`（起点）排在 `1`（终点）前 → 只共享端点也算相交',
        'cnt = 0': '`cnt` = 目前还没关闭的区间数',
        'res = 0': '`res` 累计相交的区间对数',
        'for p, t in points': lambda S, B, r: (f'扫到位置 `{S.p}` 的{"起点" if S.t == 0 else "终点"}事件'
                                               if 'p' not in B or (B.p, B.t) != (S.p, S.t) or S.get('cnt') != B.get('cnt') else '事件扫完了'),
        'if t == 0': lambda S, B, r: (f'`t = 0`：是起点，新区间开始，先和左边未关闭的区间配对' if S.t == 0
                                      else '`t = 1`：是终点，这个区间关闭了'),
        'res += cnt': '此刻未关闭的 `{cnt}` 个区间都与新区间相交 → `res += {cnt}` = =={res}==',
        'cnt += 1': '新区间成为未关闭区间：`cnt` → {cnt}',
        'cnt -= 1': '区间关闭：`cnt` → {cnt}',
        'return res': '相交的区间对一共 =={ret}== 对',
    },
    cards=dict(
        one_liner='把区间拆成起点、终点事件，扫一遍，起点处数未关闭的区间',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`intervals[i] = [start, end]` 是闭区间，至少有一个公共点就算相交',
                 '只共享一个端点也算相交，数出相交的下标对 `(i, j)`',
                 '示例：`[[1,2],[2,3],[3,4]]` → `2`'],
        quote='对于一个区间[x, y]，其左侧区间如果与之相交，唯一需要满足的条件就是左侧区间的终点大于等于x，换句话说，就是这些区间目前还没有关闭。',
        quote_src='—— yiduobo 题解原文',
        idea=['统计「每个区间左边有多少个与它相交」，不重不漏',
              '起点、终点放进一个列表，位置为第一关键字，起点在前终点在后',
              '遇到起点：`res += cnt`，再 `cnt += 1`；遇到终点：`cnt -= 1`'],
        summary=['时间 `O(n log n)`，瓶颈在排序，空间 `O(n)`',
                 '易错：同一位置起点必须排在终点前，否则只共享端点的区间会被漏数',
                 '遇到起点要先累加 `cnt` 再加 1，否则会把自己算进去',
                 '同样的做法可直接用于第二题（n 到 10^5）；原文代码无需改动'],
    ),
)
