CONFIG = dict(
    num=2293, title='极大极小游戏', difficulty='Easy', category='模拟',
    author='yiduobo', technique='按题意逐轮模拟',
    tags=[],
    code='''
class Solution(object):
    def minMaxGame(self, nums):

        now = nums[:]
        while len(now) > 1:
            next = []
            for index in range(len(now) // 2):
                if index % 2 == 0:
                    next.append(min(now[index * 2], now[index * 2 + 1]))
                else:
                    next.append(max(now[index * 2], now[index * 2 + 1]))
            
            now = next[:]
        
        return now[0]
''',
    call='Solution().minMaxGame([1,3,5,2,4,8,2,2])',
    expect=1,
    views=[
        dict(type='array', var='now', label='now（本轮数组）', cell=90, h=190,
             window=(lambda S: S['index'] * 2 if 'index' in S else None, lambda S: S['index'] * 2 + 1 if 'index' in S else None)),
        dict(type='array', var=lambda S: S.get('next'), label='next（下一轮数组，偶数下标取 min，奇数下标取 max）', cell=90, h=190,
             pointers={'index': 'blue'}),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"下标 `{S['index']}` 是{'偶' if S['index'] % 2 == 0 else '奇'}数 → 取 =={'min' if S['index'] % 2 == 0 else 'max'}== "
                           f"`({S['now'][S['index']*2]}, {S['now'][S['index']*2+1]})`"
                           if 'index' in S and 'now' in S and S['index']*2+1 < len(S['now']) else '')),
    ],
    watch=[('index', 'index', 'blue'), ('len(now)', 'len(now)', 'pink')],
    captions={
        'now = nums[:]': '复制一份 `now = {now}`，后面不改动原数组',
        'while len(now) > 1': lambda S, B, ret: (f'`len(now) = {len(S.now)} > 1`：还要再缩一轮' if len(S.now) > 1 else '`len(now) = 1`：只剩一个数，结束'),
        'next = []': '新一轮：准备空数组 `next`，长度将是 `{len(now) // 2}`',
        'for index in range': lambda S, B, ret: (f'`index = {S.index}`：用 `now[{S.index*2}]` 和 `now[{S.index*2+1}]` 生成 `next[{S.index}]`' if len(S.next) < len(S.now) // 2 else '这一轮的所有位置都处理完了'),
        'if index % 2 == 0': '`index = {index}` 是{"偶" if index % 2 == 0 else "奇"}数 → 取{"最小" if index % 2 == 0 else "最大"}值',
        'next.append(min': '`min({now[index*2]}, {now[index*2+1]})` = =={next[-1]}==，加入 `next`',
        'next.append(max': '`max({now[index*2]}, {now[index*2+1]})` = =={next[-1]}==，加入 `next`',
        'now = next[:]': '本轮结束：`now` 换成 `{now}`，长度减半',
        'return now[0]': '只剩 `{now[0]}`，返回它',
    },
    cards=dict(
        one_liner='每轮长度减半，偶数位取小、奇数位取大',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组长度是 2 的幂；每轮把相邻两数合成一个，长度减半',
                 '新数组偶数下标取 `min`，奇数下标取 `max`，直到只剩一个数',
                 '示例：`[1,3,5,2,4,8,2,2]` → `[1,5,4,2]` → `[1,4]` → `1`'],
        quote='由于题目给出的数组长度较小，同时按照题目描述的过程来看，每一轮都将缩小一半的数据规模，因此可以直接按照题目描述的过程模拟每一轮的操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据规模小，每轮减半，直接照题意模拟',
              '`next[index]` 来自 `now[2*index]` 和 `now[2*index+1]`',
              '`index` 为偶数取 `min`，为奇数取 `max`'],
        summary=['总工作量 n/2 + n/4 + … ≈ n：时间 `O(n)`，空间 `O(n)`',
                 '易错：偶/奇看的是新数组的下标 `index`，不是旧下标',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
