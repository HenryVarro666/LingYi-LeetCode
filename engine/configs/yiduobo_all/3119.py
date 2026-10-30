CONFIG = dict(
    num=3119, title='最大数量的可修复坑洼', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='统计连续段 + 长段优先',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def maxPotholes(self, road, budget):

        cnt = []
        p = 0
        while p < len(road):
            while p < len(road) and road[p] == '.':
                p += 1
            
            if p == len(road):
                break
            
            q = p
            while q < len(road) and road[q] == 'x':
                q += 1
            
            cnt.append(q - p)
            p = q
        
        cnt.sort(reverse=True)
        res = 0
        for v in cnt:
            if budget > v + 1:
                res += v
                budget -= v + 1
            else:
                res += budget - 1
                break
        
        return res
''',
    call="Solution().maxPotholes('xxx.xx.xxxx', 8)",
    expect=6,
    views=[
        dict(type='string', var='road', pointers={'p': 'blue', 'q': 'pink'}, h=170),
        dict(type='array', var='cnt', label='cnt（每段连续 x 的长度）', h=170, cell=90),
        dict(type='text', fn=lambda S: (f"修复一段长 `{S['v']}` 的坑，花费 `{S['v']}+1` = =={S['v']+1}==，剩余预算 `{S['budget']}`" if 'v' in S else '先统计每段连续 `x` 的长度'), size=26),
    ],
    watch=['p', 'q', 'budget', ('res', 'res', 'green')],
    captions={
        "road[p] == '.'": '`road[{p}]` 是 `.`，不用修，`p` 右移',
        'p += 1': '`p` → {p}',
        'if p == len(road)': '`p = {p}`，{"走到末尾，没有更多坑洼 → 结束统计" if p == len(road) else "遇到 x，一段坑洼开始"}',
        'q = p': '从 `p = {p}` 起往右找这一段 `x` 的终点',
        "road[q] == 'x'": '`road[{q}]` 还是 `x` → 这段继续延伸，`q` 右移',
        'q += 1': '`q` → {q}',
        'cnt.append': '这一段长度 `{q} - {p}` = =={q - p}==，记入 `cnt` = {cnt}',
        'p = q': '跳到这一段末尾继续找下一段：`p = {p}`',
        'cnt.sort': '长段优先：修 `n` 个连续 x 花 `n+1`，==越长越划算==（平均每个 `1+1/n`）。排序后 `cnt` = {cnt}',
        'for v in cnt': '取最长的未修段 `v = {v}`，剩余预算 `{budget}`',
        'if budget > v + 1': '预算 `{budget}` {">" if budget > v + 1 else "≤"} 整段花费 `{v + 1}` → {"够修完整段" if budget > v + 1 else "不够修完整段，只能修一部分"}',
        'res += v': '整段修完：`res` += `{v}` → =={res}==',
        'budget -= v + 1': '预算扣掉 `{v} + 1`，剩 `{budget}`',
        'res += budget - 1': '预算不够整段：花 `1` 做“开销”，剩下 `{budget} - 1` 个坑能修 → `res` = =={res}==',
        'return res': '最多修复 =={res}== 个坑洼',
    },
    cards=dict(
        one_liner='连续的坑一次修更省，先修最长的段',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`road` 由 `x`（坑）和 `.` 组成；修复连续 `n` 个坑的代价为 `n + 1`',
                 '总预算 `budget`，求最多能修复多少个坑',
                 '示例：`road = "xxx.xx.xxxx"`，`budget = 8` → `6`'],
        quote='对于长度为n的\'x\'，修复单个\'x\'的评价代价为1 + 1 / n，换言之，n越大，评价的修改代价就越小，也就是说在这里应该先尽量修复较长的连续\'x\'。',
        quote_src='—— yiduobo 题解原文',
        idea=['先一趟遍历，把每段连续 `x` 的长度存进 `cnt`',
              '长度越大平均代价越低 → 从大到小排序后逐段修',
              '预算不够整段时，修这段的一部分：额外的 1 是固定开销，能修 `budget - 1` 个'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '整段条件是 `budget > v + 1`（严格大于）；相等时走 else，`budget - 1` 与整段结果一致，都正确',
                 '预算为 0 或 1 时 `budget - 1` 可能为负或 0，本题数据下按原文写法仍成立',
                 '原文为 Python 2 写法，本题代码无需改动'],
    ),
)
