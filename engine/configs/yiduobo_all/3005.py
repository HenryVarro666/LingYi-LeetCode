def _col(S, i, v):
    if 'v' not in S:
        return None
    if v == S['v']:
        return 'blue'
    if 'max_f' in S and S['freq'].get(v) == S['max_f'] and S['max_f'] > 0:
        return 'green'
    return None


def _txt(S):
    if 'v' not in S:
        return '先用 `Counter` 数出每个数的次数，再扫一遍这些频率'
    return f"当前看 `{S['v']}`（出现 {S['f']} 次）；`max_f = {S['max_f']}`，`res = {S['res']}`"


CONFIG = dict(
    num=3005, title='最大频率元素计数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='先统计频率 · 再扫频率求和',
    code='''
class Solution(object):
    def maxFrequencyElements(self, nums):

        freq = Counter(nums)
        res = 0
        max_f = 0
        for v, f in freq.items():
            if f > max_f:
                res = f
                max_f = f
            elif f == max_f:
                res += f
        
        return res
''',
    call='Solution().maxFrequencyElements([1,2,2,3,1,4])',
    expect=4,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', color=_col, h=200),
        dict(type='map', var='freq', h=240, fmt=lambda k, v: f'{k} : {v}'),
    ],
    watch=[('v', 'v', 'blue'), ('f', 'f', 'cyan'), ('max_f', 'max_f', 'yellow'), ('res', 'res', 'green')],
    captions={
        'freq = Counter': '一遍遍历：`Counter` 统计每个数的出现频率',
        'res = 0': '`res` 存最终答案',
        'max_f = 0': '`max_f` 存目前见过的最大频率',
        'for v, f in freq.items': lambda S, B, r: ('所有频率都扫完了' if B.get('v') == S.v and 'v' in B
                                                   else f'再遍历这些频率：数 `{S.v}` 出现 `{S.f}` 次'),
        'if f > max_f': lambda S, B, r: (f'`f = {S.f} > max_f = {S.max_f}`：==更大的频率== → 之前累加的作废'
                                         if S.f > S.max_f else f'`f = {S.f} > max_f = {S.max_f}`？不成立'),
        'res = f': '`res` 重新从 `f` 开始：{res}',
        'max_f = f': '最大频率更新为 `{max_f}`',
        'elif f == max_f': lambda S, B, r: (f'`f = {S.f} == max_f`：==频率并列== → 累加'
                                            if S.f == S.max_f else f'`f = {S.f} < max_f = {S.max_f}`：不是最大频率，跳过'),
        'res += f': '`res += {f}` → {res}',
        'return res': '最大频率元素的总频率：`{res}`',
    },
    cards=dict(
        one_liner='哈希表数频率，再把所有最大频率累加起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找出出现次数最多的元素，返回它们的 ==总出现次数==',
                 '多个元素并列最大时，次数要全部加起来',
                 '本视频：`[1,2,2,3,1,4]` → `4`'],
        quote='一样遍历，使用哈希表统计每个数出现的频率，然后再遍历这些频率，找出其中的最大值，并将所有的最大值累加即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：`Counter(nums)` 得到每个数的频率',
              '第二遍：扫频率，`f > max_f` 就重置，`f == max_f` 就累加',
              '两遍都是线性的，思路直白不容易错'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '第二遍遍历的是哈希表的项，不是原数组',
                 '`res = f` 和 `max_f = f` 要一起更新',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码本身 Python 3 可直接运行',
                 '对比灵神：灵神一遍搞定，边数边维护最大次数'],
    ),
)
