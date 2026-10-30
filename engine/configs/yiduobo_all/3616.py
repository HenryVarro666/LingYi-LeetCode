CONFIG = dict(
    num=3616, title='学生替换人数', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历维护当前最优',
    tags=[],
    code='''
class Solution(object):
    def totalReplacements(self, ranks):
        
        now = ranks[0]
        res = 0
        for r in ranks[1:]:
            if r < now:
                now = r
                res += 1
        
        return res
''',
    call='Solution().totalReplacements([4,6,3,5,2,2,1])',
    expect=3,
    views=[
        dict(type='array', var='ranks', label='ranks（排名越小越好）', cell=84, h=260,
             color=lambda S, i, v: 'green' if 'now' in S and v == S['now'] and i == min(j for j, x in enumerate(S['ranks']) if x == S['now']) else None),
        dict(type='text', fn=lambda S: (f"当前选中排名 `now = {S['now']}`，已替换 ==`{S['res']}`== 次" if 'now' in S and 'res' in S else ''), size=30),
    ],
    watch=[('now', 'now', 'green'), 'r', ('res', 'res', 'orange')],
    captions={
        'now = ranks[0]': '一开始默认选中第一个学生：`now = {now}`',
        'res = 0': '替换次数从 0 开始',
        'for r in ranks': '下一个到达的学生排名 `r = {r}`',
        'if r < now': lambda S, B, ret: (f"`{S.r} < {S.now}` → 排名==严格更好==，要替换" if S.r < S.now else f"`{S.r} < {S.now}` 不成立 → 不比当前更好（相等也不换），保持不变"),
        'now = r': '当前选择换成新学生：`now = {now}`',
        'res += 1': '替换次数加一：`res = {res}`',
        'return': '遍历结束，总共替换 `{ret}` 次',
    },
    cards=dict(
        one_liner='记住当前选中的排名，遇到严格更小的就替换并计数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`ranks[i]` 是第 `i` 个到达学生的排名，数字越小越好',
                 '一开始选中第一个学生；来了==严格更好==的学生就替换',
                 '求替换的总次数。示例：`[4,6,3,5,2,2,1]` → `3`'],
        quote='使用一个变量记录当前选择的学生排名now，然后一趟遍历，若遇到了更好的排名，就将now更新为这个排名，然后将答案加上1即可。',
        quote_src='—— yiduobo 题解',
        idea=['`now` 保存当前选中学生的排名，初值是第一个学生',
              '从第二个开始遍历：`r < now` 才替换，同时 `res += 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：必须==严格==更好才替换，排名相同不算',
                 '第一个学生本来就是选中的，不计入替换次数',
                 '本质是统计「前缀最小值被刷新的次数」'],
    ),
)
