CONFIG = dict(
    num=1518, title='换水问题', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='预留 numExchange 后做除法', tags=[],
    code='''
class Solution(object):
    def numWaterBottles(self, numBottles, numExchange):

        res = numBottles
        if numBottles >= numExchange:
            res += (numBottles - numExchange) // (numExchange - 1) + 1
        
        return res
''',
    call='Solution().numWaterBottles(9, 3)',
    expect=13,
    views=[
        dict(type='text', h=110, size=32,
             fn=lambda S: (f"换一次损失 `numExchange − 1 = {S['numExchange'] - 1}` 个瓶子" if 'numExchange' in S else '')),
        dict(type='text', h=110, size=32,
             fn=lambda S: (f"预留 `numExchange` 瓶，其余 `{S['numBottles'] - S['numExchange']}` 瓶每 `{S['numExchange'] - 1}` 个换一瓶，再加 1" if 'res' in S and S['numBottles'] >= S['numExchange'] else '')),
        dict(type='text', h=110, size=36,
             fn=lambda S: (f"已喝 `res` = ==%d==" % S['res'] if 'res' in S else '')),
    ],
    watch=['numBottles', 'numExchange', ('res', 'res', 'green')],
    captions={
        'res = numBottles': '先把买的 `{numBottles}` 瓶都喝掉：`res = {res}`',
        'if numBottles >=': lambda S, B, r: (f'`{S.numBottles} >= {S.numExchange}`：手上瓶子够换，==可以开始换酒==' if S.numBottles >= S.numExchange
                                             else f'`{S.numBottles} < {S.numExchange}`：一次都换不了，不用算'),
        'res +=': '预留 `{numExchange}` 瓶不动，其余 `{numBottles - numExchange}` 瓶每 `{numExchange - 1}` 个损失换一瓶：`{numBottles - numExchange} // {numExchange - 1} + 1` → `res = {res}`',
        'return res': '最多喝到 `{res}` 瓶',
    },
    cards=dict(
        one_liner='每换一瓶损失 numExchange-1 个瓶子，预留 numExchange 再除',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['用 `numExchange` 个空瓶可兑换 1 瓶水，起初有 `numBottles` 瓶水',
                 '喝完变空瓶，问最多能喝到多少瓶',
                 '示例：`numBottles = 9, numExchange = 3` → `13`'],
        quote='每换一瓶酒都要损失numExchange - 1个瓶子……一种可行的做法是先预留出numExchange瓶酒不动，对于其他瓶子做上面的除法。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次换酒，瓶子少 `numExchange - 1`，直到不够 `numExchange`',
              '直接拿 `numBottles` 去除会出现「赊账」，样例不允许',
              '先留出 `numExchange` 瓶，用剩下的做除法，最后再加换到的那 1 瓶'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：==不能赊账==，要先判断 `numBottles >= numExchange`',
                 '原文 `/` 是 Python 2 整数除法，已改为 `//`',
                 '另一种写法：循环模拟，每次 `numBottles -= numExchange - 1`'],
    ),
)
