CONFIG = dict(
    num=1509, title='三次操作后最大值与最小值的最小差', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='维护最大/最小的四个数',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minDifference(self, nums):

        if len(nums) <= 4:
            return 0

        ma1 = ma2 = ma3 = ma4 = None
        mi1 = mi2 = mi3 = mi4 = None
        
        for num in nums:
            if ma1 is None or num > ma1:
                ma1, ma2, ma3, ma4 = num, ma1, ma2, ma3
            elif ma2 is None or num > ma2:
                ma2, ma3, ma4 = num, ma2, ma3
            elif ma3 is None or num > ma3:
                ma3, ma4 = num, ma3
            elif ma4 is None or num > ma4:
                ma4 = num
            
            if mi1 is None or num < mi1:
                mi1, mi2, mi3, mi4 = num, mi1, mi2, mi3
            elif mi2 is None or num < mi2:
                mi2, mi3, mi4 = num, mi2, mi3
            elif mi3 is None or num < mi3:
                mi3, mi4 = num, mi3
            elif mi4 is None or num < mi4:
                mi4 = num
        
        return min(ma1 - mi4, ma2 - mi3, ma3 - mi2, ma4 - mi1)
''',
    call='Solution().minDifference([6,0,6,1,4,1,9])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=170, label='nums'),
        dict(type='text', h=90, fn=lambda S: ('最大的四个 ==ma1 ≥ ma2 ≥ ma3 ≥ ma4==：' + ' , '.join(str(S.get('ma%d' % i)) for i in (1, 2, 3, 4)))
             if 'ma4' in S else ''),
        dict(type='text', h=90, fn=lambda S: ('最小的四个 ==mi1 ≤ mi2 ≤ mi3 ≤ mi4==：' + ' , '.join(str(S.get('mi%d' % i)) for i in (1, 2, 3, 4)))
             if 'mi4' in S else ''),
    ],
    watch=['num', ('ma', '(ma1, ma2, ma3, ma4)', 'pink'), ('mi', '(mi1, mi2, mi3, mi4)', 'blue')],
    captions={
        'if len(nums) <= 4': '`n = {len(nums)}`：不超过 4 个数时，三次操作足够把所有数改成同一个值 → 差为 0；这里 n > 4，继续',
        'ma1 = ma2': '准备记录最大的四个数 `ma1~ma4`，先置空',
        'mi1 = mi2': '准备记录最小的四个数 `mi1~mi4`，先置空',
        'ma1, ma2, ma3, ma4 = num': '`{num}` 比最大值还大：成为新的 ma1，原来的最大值们各往后挤一位 → ma = ({ma1}, {ma2}, {ma3}, {ma4})',
        'ma2, ma3, ma4 = num': '`{num}` 是第二大：插入 ma2，后面两个往后挤 → ma = ({ma1}, {ma2}, {ma3}, {ma4})',
        'ma3, ma4 = num': '`{num}` 是第三大：插入 ma3 → ma = ({ma1}, {ma2}, {ma3}, {ma4})',
        'ma4 = num': '`{num}` 是第四大：替换 ma4 → ma = ({ma1}, {ma2}, {ma3}, {ma4})',
        'mi1, mi2, mi3, mi4 = num': '`{num}` 比最小值还小：成为新的 mi1，其余往后挤 → mi = ({mi1}, {mi2}, {mi3}, {mi4})',
        'mi2, mi3, mi4 = num': '`{num}` 是第二小：插入 mi2 → mi = ({mi1}, {mi2}, {mi3}, {mi4})',
        'mi3, mi4 = num': '`{num}` 是第三小：插入 mi3 → mi = ({mi1}, {mi2}, {mi3}, {mi4})',
        'mi4 = num': '`{num}` 是第四小：替换 mi4 → mi = ({mi1}, {mi2}, {mi3}, {mi4})',
        'return min': '四种方案：`{ma1}-{mi4}`、`{ma2}-{mi3}`、`{ma3}-{mi2}`、`{ma4}-{mi1}` = `{ma1-mi4}`、`{ma2-mi3}`、`{ma3-mi2}`、`{ma4-mi1}` → 取最小 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='三次操作只会动最大的几个或最小的几个，四种方案取最小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一次操作可把 `nums` 里任意一个数改成任意值，最多操作 3 次',
                 '求操作后 ==最大值 − 最小值== 的最小可能值',
                 '本视频：`[6,0,6,1,4,1,9]` → `4`'],
        quote='数组长度小于等于4时，显然可以将所有数都调整成同样大小，那么此时的答案必然为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['n > 4 时，要缩小极差，只能把最小的调大或把最大的调小',
              '调掉最小的三个 / 两小一大 / 一小两大 / 最大的三个，共 ==4 种==',
              '一趟遍历同时维护最大的四个 `ma1~ma4` 和最小的四个 `mi1~mi4`，答案是 `ma1-mi4`、`ma2-mi3`、`ma3-mi2`、`ma4-mi1` 的最小值'],
        summary=['时间 `O(n)`，空间 `O(1)`：不排序，只维护 8 个变量',
                 '先判 `len(nums) <= 4` 直接返回 0',
                 '插入时必须用 `if / elif` 链，每个数只落在一个位置，后面的往后挤',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比：排序后取 `nums[i] - nums[i+n-4]` 也行，这里是 O(n) 的做法'],
    ),
)
