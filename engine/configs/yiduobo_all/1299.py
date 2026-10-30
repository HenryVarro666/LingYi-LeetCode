def _text(S):
    if 'max_num' not in S:
        return '`res[i] = max(res[i+1], arr[i])` 的递推，从后往前扫'
    return f'`max_num = {S["max_num"]}`：已扫过部分（当前元素右侧）的最大值'


def _cur(S):
    if 'num' not in S:
        return None
    a = S['arr']
    for i in range(len(a) - 1, -1, -1):
        if a[i] == S['num']:
            return i
    return None


CONFIG = dict(
    num=1299, title='将每个元素替换为右侧最大元素', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='从后往前递推',
    code='''
class Solution(object):
    def replaceElements(self, arr):

        res = []
        max_num = -1
        for num in arr[::-1]:
            res.append(max_num)
            max_num = max(max_num, num)
        
        return res[::-1]
''',
    call='Solution().replaceElements([17, 18, 5, 4, 6, 1])',
    expect=[18, 6, 6, 6, 1, -1],
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var='arr', label='arr', h=230,
             color=lambda S, i, v: 'blue' if i == _cur(S) else None,
             dim=lambda S, i, v: _cur(S) is not None and i > _cur(S)),
        dict(type='array', var='res', label='res（从后往前追加，最后翻转）', h=230),
    ],
    watch=['num', ('max_num', 'max_num', 'orange')],
    captions={
        'res = []': '`res` 按从后往前的顺序收集答案',
        'max_num = -1': '`max_num = -1`：最后一个元素右边没有数，答案就是 `-1`',
        'for num in arr[::-1]': lambda S, B, r: ('已倒着取完所有元素' if ('num' in B and B.num == S.num and len(S.res) == len(S.arr)) else f'倒着取 `num = {S.num}`'),
        'res.append': '这个位置的答案是 ==右侧最大== `max_num = {max_num}` → 追加到 `res`',
        'max_num = max': '把 `{num}` 并入：`max_num = max({B.max_num}, {num}) = {max_num}`，留给更左边的位置用',
        'return res[::-1]': '`res` 是倒着存的，翻转回来：`{ret}`',
    },
    cards=dict(
        one_liner='res[i] = max(res[i+1], arr[i])：从后往前递推',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把每个元素换成它右边的最大值，最后一个换成 `-1`',
                 '示例：`[17,18,5,4,6,1]` → `[18,6,6,6,1,-1]`'],
        quote='res[i] = max(res[i + 1], arr[i])，于是可以从后向前一趟扫描，根据上面的式子逐个计算当前位置的res即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['列出第 `i` 位和第 `i+1` 位答案的式子',
              '和第 `i+1` 位的式子对比，只差一个 `arr[i]`',
              '所以倒着扫，用 `max_num` 滚动保存已扫部分的最大值'],
        summary=['时间 `O(n)`，空间 `O(n)`（新建了 `res`）',
                 '先 `append(max_num)` 再更新 `max_num`：答案不能包含自己',
                 '`res` 是倒着存的，返回前要 `[::-1]` 翻转',
                 '对比灵神：灵神原地覆盖 `arr`，空间 `O(1)`'],
    ),
)
