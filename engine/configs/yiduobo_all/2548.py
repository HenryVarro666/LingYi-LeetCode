CONFIG = dict(
    num=2548, title='填满背包的最大价格', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按价格重量比贪心',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def maxPrice(self, items, capacity):

        res = 0.0
        for p, w in sorted(items, key=lambda d:d[0] * 1.0 / d[1], reverse=True):
            if w >= capacity:
                res += capacity * 1.0 / w * p
                return res
            
            res += p
            capacity -= w

        return -1.0
''',
    call='Solution().maxPrice([[50,1],[10,8],[20,4]], 6)',
    expect=71.25,
    views=[
        dict(type='text', fn=lambda S: '物品 `[价格, 重量]` 按 价格÷重量 从大到小：' + '，'.join(f"`{p}/{w}`={p/w:g}" for p, w in sorted(S['items'], key=lambda d: d[0]*1.0/d[1], reverse=True)), size=26),
        dict(type='table', label='按性价比排序后的物品', var=lambda S: sorted(S['items'], key=lambda d: d[0]*1.0/d[1], reverse=True), h=200, cell=110,
             rows=['第1名', '第2名', '第3名'], cols=['价格', '重量'],
             color=lambda S, i, j, v: 'yellow' if 'p' in S and [S['p'], S['w']] == sorted(S['items'], key=lambda d: d[0]*1.0/d[1], reverse=True)[i] else None),
        dict(type='text', fn=lambda S: f"背包剩余容量 `capacity` = =={S['capacity']}==，已装价值 `res` = =={S['res']}==" if 'res' in S else '', size=28),
    ],
    watch=['p', 'w', 'capacity', ('res', 'res', 'green')],
    captions={
        'res = 0.0': '`res` 累计装进背包的价值，用小数',
        'for p, w in sorted': '物品可拆分 → ==性价比高的先装==。取出 价格 `{p}`、重量 `{w}`，比值 `{p / w:g}`',
        'if w >= capacity': '重量 `{w}` ≥ 剩余容量 `{capacity}`？{"装不下整件 → 只拆一部分装满" if w >= capacity else "整件装得下"}',
        'res += capacity': '拆一部分：`{capacity} / {w} × {p}` → `res` = =={res}==，背包装满',
        'return res': '背包装满，最大价值 =={res}==',
        'res += p': '整件放入：`res` += `{p}` → {res}',
        'capacity -= w': '容量减去 `{w}`，剩余 `{capacity}`',
        'return -1.0': '所有物品都装进去仍装不满 → 返回 `-1`',
    },
    cards=dict(
        one_liner='物品能拆分，就按价格重量比从大到小装',
        complexity='时间 `O(n log n)`，空间 `O(n)`（排序）',
        problem=['`items[i] = [价格, 重量]`，物品可以==拆成任意比例==，价格按比例缩放',
                 '背包容量 `capacity`，求装满背包的最大总价格；装不满返回 `-1`',
                 '示例：`[[50,1],[10,8],[20,4]]`，`capacity = 6` → `71.25`'],
        quote='由于本体的物品可以随意拆分，因此在这里可以使用贪心法，按价格重量比从大到小进行排序，然后一趟遍历尽量将价格重量比较高的物品加入背包中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['能拆分 → 每单位重量价值越高越先装，不会吃亏',
              '遍历到装不下整件的物品：按剩余容量比例拆开，正好装满',
              '遍历完还没装满，说明总重量不足 → `-1.0`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '比较用 `价格 * 1.0 / 重量`，避免整数除法；拆分价值 `capacity * 1.0 / w * p`',
                 '条件是 `w >= capacity`：恰好等于时也走拆分分支，结果相同',
                 '原文为 Python 2 写法，本题代码无需改动，直接在 Python 3 运行'],
    ),
)
