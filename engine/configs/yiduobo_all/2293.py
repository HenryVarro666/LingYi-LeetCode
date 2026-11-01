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
        dict(type='array', var='now', pointers={'index': 'blue'}, label='now', h=200,
             color=lambda S, i, v: 'blue' if 'index' in S and i in (S['index'] * 2, S['index'] * 2 + 1) and S['_line'] in (8, 9, 10, 11) else None),
        dict(type='array', var='next', pointers={'index': 'pink'}, label='next（这一轮的结果）', h=200),
    ],
    watch=['index', ('len(now)', 'len(now)', 'cyan')],
    captions={
        'now = nums': '先复制一份 `now`，后面每轮都在它上面缩小',
        'while len(now) > 1': '`len(now) = {len(now)}`：{"每一轮规模减半，继续" if len(now) > 1 else "只剩一个数，结束"}',
        'next = []': '这一轮的结果放进空列表 `next`',
        'for index': '`index` 从 0 走到 `{len(now)//2 - 1}`，每个位置对应 now 的一对相邻数',
        'if index % 2': '`index = {index}`：{"偶数 → 取较小值" if index % 2 == 0 else "奇数 → 取较大值"}',
        'min(': '`min({now[index*2]}, {now[index*2+1]})` = =={next[-1]}==，追加进 next',
        'max(': '`max({now[index*2]}, {now[index*2+1]})` = =={next[-1]}==，追加进 next',
        'now = next': '一轮结束：`now` 变成 `{now}`，长度 {len(now)}',
        'return now[0]': '只剩一个数 =={now[0]}==，返回',
    },
    cards=dict(
        one_liner='数据规模每轮减半，照题意模拟就行',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组长度是 2 的幂，每轮把相邻两数合成一个：偶数位取小、奇数位取大',
                 '重复直到只剩一个数',
                 '示例：`[1,3,5,2,4,8,2,2]` → `1`'],
        quote='由于题目给出的数组长度较小，同时按照题目描述的过程来看，每一轮都将缩小一半的数据规模，因此可以直接按照题目描述的过程模拟每一轮的操作',
        quote_src='—— yiduobo 题解原文',
        idea=['先拷贝 `nums`，避免改动输入',
              '每轮用 `next` 收集结果，再整体赋回 `now`',
              '规模 n → n/2 → …，总量只有约 2n'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '原文为 Python 2 写法，`len(now) / 2` 已改为整数除法 `//`',
                 '变量名 `next` 会遮住内置函数，但这里不影响结果',
                 '对比灵神：灵神用 `b = [0]*(len(a)//2)` 按下标填；这里用 `append`'],
    ),
)
