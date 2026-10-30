def _txt(S):
    if 'p' not in S:
        return '先固定 x 方向的异或结果 `p`，y 方向就是 `q = k − p`'
    p, q = S['p'], S['q']
    if 'x' not in S or 'cnt' not in S:
        return f'`p = {p}`，`q = {q}`：每个点 `(x, y)` 要配的搭档是 `(p^x, q^y)`'
    return (f'`p = {p}`，`q = {q}`；点 `({S["x"]}, {S["y"]})` 的搭档 `({p ^ S["x"]}, {q ^ S["y"]})`'
            f' 已出现 =={S["cnt"].get((p ^ S["x"], q ^ S["y"]), 0)}== 次')


CONFIG = dict(
    num=2857, title='统计距离为 k 的点对', difficulty='Medium', category='位运算',
    author='yiduobo', technique='枚举 p + 每轮一遍哈希表',
    tags=['灵神题单·位运算', '难度分 2082'],
    code='''
class Solution(object):
    def countPairs(self, coordinates, k):

        res = 0
        for p in range(k + 1):
            q = k - p
            cnt = {}
            for x, y in coordinates:
                res += cnt.get((p ^ x, q ^ y), 0)
                cnt[(x, y)] = cnt.get((x, y), 0) + 1
        
        return res
''',
    call='Solution().countPairs([[1,2],[4,2],[1,3],[5,2]], 1)',
    expect=2,
    views=[
        dict(type='table', var='coordinates', label='coordinates（每行一个点）', h=210, cell=70),
        dict(type='map', var='cnt', label='cnt（本轮已遍历点的出现次数）', fmt=lambda k, v: f'{k}: {v}', h=190, font=30),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('p', 'p', 'orange'), ('q', 'q', 'cyan'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计满足条件的点对数',
        'for p in range(k + 1)': lambda S, B, r: (f'枚举 x 坐标的异或结果 `p = {S.p}`（异或非负，所以 `p` 只能在 `0..k`）' if 'p' not in B or S.p != B.p
                                                  else '`p` 枚举完毕'),
        'q = k - p': '`q = k − p = {q}`：y 坐标的异或结果必须是 `{q}`',
        'cnt = {}': '每一轮 `p` 都==重新开一张哈希表==，记录已遍历点的次数',
        'for x, y in coordinates': lambda S, B, r: (f'遍历到点 `(x, y) = ({S.x}, {S.y})`' if 'x' not in B or (S.x, S.y, S.p) != (B.x, B.y, B.p) or len(S.cnt) != len(B.cnt) or True and S.cnt != B.cnt
                                                    else '这一轮的点遍历完了'),
        'res += cnt.get': '`(x,y)` 与 `(p^x, q^y)` 异或结果恰为 `(p, q)`：`({p ^ x}, {q ^ y})` 之前出现过 `{cnt.get((p ^ x, q ^ y), 0)}` 次 → `res = {res}`',
        'cnt[(x, y)] =': '检测完再把 `({x}, {y})` 记入哈希表 → 次数 `{cnt[(x, y)]}`，==先检测后加入==避免和自己配对',
        'return res': '所有 `p` 都枚举完，一共 `{res}` 对',
    },
    max_steps=90,
    cards=dict(
        one_liner='k 很小：枚举 x 异或结果 p，y 异或结果就是 k − p',
        complexity='时间 `O(nk)`，空间 `O(n)`',
        problem=['点对距离 = `(x1 xor x2) + (y1 xor y2)`，求 `i < j` 且距离恰为 `k` 的点对数',
                 '示例：`[[1,2],[4,2],[1,3],[5,2]]`，`k=5` → `2`',
                 '本视频：同一组点，`k=1` → `2`（(0,2) 与 (1,3)）'],
        quote='注意到本题中k的规模比较小，而异或的结果必然是非负的，因此在这里就可以从0到k枚举x坐标的异或结果p，通过k - p得到y坐标的异或结果q。',
        quote_src='—— yiduobo 题解原文',
        idea=['点数很多，暴力 `O(n²)` 不行；`k ≤ 100` 才是突破口',
              '外层枚举 `p`，`q = k − p` 随之确定',
              '内层一趟遍历：当前点 `(x, y)` 的搭档必为 `(p^x, q^y)`，查哈希表即可'],
        summary=['时间 `O(nk)`：`k+1` 轮，每轮扫一遍点',
                 '空间 `O(n)`：哈希表每轮重建',
                 '先查询 `(p^x, q^y)`，再记录 `(x, y)`；顺序反了会和自己配对',
                 '和灵神对比：yiduobo 把 `p` 放外层、每轮重置表；灵神把枚举放内层、表只建一次'],
    ),
)
