CONFIG = dict(
    num=1217, title='玩筹码', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='奇偶计数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minCostToMoveChips(self, position):

        odd = even = 0
        for p in position:
            if p % 2 == 0:
                even += 1
            else:
                odd += 1
            
        return min(odd, even)
''',
    call='Solution().minCostToMoveChips([2,2,2,3,3])',
    expect=2,
    views=[
        dict(type='array', var='position', label='position（每个筹码所在位置）', h=200,
             color=lambda S, i, v: 'green' if v % 2 == 0 else 'pink'),
        dict(type='text', h=140, size=34, fn=lambda S: f"偶数位置 even = =={S['even']}==，奇数位置 odd = =={S['odd']}==" if 'even' in S else ''),
    ],
    watch=['p', ('even', 'even', 'green'), ('odd', 'odd', 'pink')],
    captions={
        'odd = even = 0': '偶数位置、奇数位置的筹码数都从 0 开始计',
        'for p in position': '扫描筹码位置 `{p}`',
        'if p % 2 == 0': lambda S, B, r: f'位置 `{S.p}` 是{"偶" if S.p % 2 == 0 else "奇"}数：移动 2 格免费，同奇偶的位置可以免费合并',
        'even += 1': '偶数位置的筹码 +1 → `even = {even}`',
        'odd += 1': '奇数位置的筹码 +1 → `odd = {odd}`',
        'return min': '最后合并到一堆：把较少的一边每个筹码移动 1 格（代价 1），花费 `min({odd}, {even})` = =={ret}==',
    },
    cards=dict(
        one_liner='移动 2 格免费：只需数奇偶，取少的一边',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['筹码在若干位置上，移动 2 格代价 0，移动 1 格代价 1',
                 '求把所有筹码移到同一位置的最小代价',
                 '示例：`[2,2,2,3,3]` → `2`'],
        quote='移动两个格子的操作代价为0，那么说明最终我们可以不花任何代价将所有筹码移动到位置0或者位置1上。',
        quote_src='—— yiduobo 题解原文',
        idea=['同奇偶的位置之间随便移动，代价为 0，所以所有偶数位置的筹码可以免费堆到一起，奇数位置同理',
              '最后只剩两堆（偶堆、奇堆），把其中一堆移到另一堆旁边，每个筹码代价 1',
              '代价取较小的一堆：`min(odd, even)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只有一堆筹码时 `min` 自然为 0',
                 '易错：不需要真的模拟移动，只看奇偶性',
                 '原文代码可直接在 Python 3 运行，未做修改'],
    ),
)
