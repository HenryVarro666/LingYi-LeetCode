CONFIG = dict(
    num=1936, title='新增的最少台阶数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 能走多远走多远',
    tags=[],
    code='''
class Solution(object):
    def addRungs(self, rungs, dist):

        now = 0
        res = 0
        p = 0
        while now < rungs[-1]:
            if rungs[p] - now > dist:
                cnt = (rungs[p] - now) // dist
                if (rungs[p] - now) % dist == 0:
                    cnt -= 1
                res += cnt
                now = now + cnt * dist
            else:
                while p < len(rungs) and rungs[p] - now <= dist:
                    p += 1
                now = rungs[p - 1]
        
        return res
''',
    call='Solution().addRungs([1,3,5,10], 2)',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"当前高度 `now = {S['now']}`，下一级 `rungs[{S['p']}] = {S['rungs'][S['p']]}`，差 ==`{S['rungs'][S['p']] - S['now']}`==，`dist = {S['dist']}`" if 'p' in S and S['p'] < len(S['rungs']) else (f"当前高度 `now = {S['now']}`" if 'now' in S else '')), h=90),
        dict(type='array', var='rungs', pointers={'p': 'blue'}, label='rungs', h=300,
             color=lambda S, i, v: 'green' if 'now' in S and v <= S['now'] else None),
    ],
    watch=[('now', 'now', 'blue'), ('p', 'p', 'pink'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'now = 0': '从地板出发：`now = 0`',
        'p = 0': '`p` 指向下一级要爬的台阶',
        'res = 0': '`res` 累计新增台阶数',
        'while now < rungs[-1]': '`now = {now}`，最后一级 `{rungs[-1]}`：{"还没到顶，继续" if now < rungs[-1] else "到顶了，结束"}',
        'if rungs[p] - now > dist': '差 `{rungs[p]} − {now} = {rungs[p]-now}` {">" if rungs[p]-now > dist else "≤"} `dist = {dist}` → {"够不着，==必须加台阶==" if rungs[p]-now > dist else "能走，不用加台阶"}',
        'cnt = (': '需要的台阶数先取 `差 // dist = {cnt}`',
        '% dist == 0': lambda S, B, r: (f"差 `{S.rungs[S.p]-S.now}` 恰好是 `dist` 的整数倍 → ==最后一步可直接走到 rungs[p]==，要少加一个" if (S.rungs[S.p]-S.now) % S.dist == 0 else f"差 `{S.rungs[S.p]-S.now}` 除不尽 `dist`，向下取整的 `{S.cnt}` 个够用"),
        'cnt -= 1': '少加一个：`cnt = {cnt}`',
        'res += cnt': '新增 `{cnt}` 个台阶：`res` → {res}',
        'now = now + cnt': '新台阶都加在极限距离上，`now` 走到 `{now}`（不是 rungs[p]，尽量走远）',
        'while p < len': lambda S, B, r: (f"`rungs[{S.p}] − {S.now} = {S.rungs[S.p]-S.now}` ≤ `dist` → 这级台阶够得着，`p` 后移" if S.p < len(S.rungs) and S.rungs[S.p]-S.now <= S.dist else "够不着下一级了，停下"),
        'p += 1': '`p` → {p}',
        'now = rungs[p - 1]': '走到够得着的最高一级：`now = rungs[{p-1}] = {now}`',
        'return res': '一共新增 `{res}` 个台阶',
    },
    cards=dict(
        one_liner='能走多远走多远，加台阶也加在最远的位置上',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`rungs` 严格递增，从高度 0 出发，每步最多爬 `dist`，可以在任意整数高度加台阶',
                 '求爬到最后一级最少要加几个台阶',
                 '示例：`rungs = [1,3,5,10]`，`dist = 2` → `2`（加在 7 和 8）'],
        quote='由于题目没有最小移动距离的限制，因此对于每次移动，就应该能走多远就走多远。同样的，如果需要添加新的台阶，那也应该添加在极限距离上。',
        quote_src='—— yiduobo 题解原文',
        idea=['够得着就一路走到能到的最高一级（`p` 往后挪）',
              '够不着就补台阶：数量约 `差 // dist`，恰好整除时少一个',
              '补完 `now` 停在新台阶的最后一个，而不是 `rungs[p]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：差恰好是 `dist` 的倍数时 `cnt` 要减 1',
                 '补台阶后 `now = now + cnt * dist`，不是 `rungs[p]`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
