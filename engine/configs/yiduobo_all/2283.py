CONFIG = dict(
    num=2283, title='判断一个数的数字计数是否等于数位的值', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · 两趟遍历', tags=[],
    code='''
class Solution(object):
    def digitCount(self, num):

        cnt_dict = {}
        for char in num:
            cnt_dict[int(char)] = cnt_dict.get(int(char), 0) + 1
        
        for index, char in enumerate(num):
            if cnt_dict.get(index, 0) != int(char):
                return False
        
        return True
''',
    call='Solution().digitCount("1210")',
    expect=True,
    views=[
        dict(type='string', var='num', pointers={'index': 'blue'}, h=200, label='num'),
        dict(type='map', var='cnt_dict', h=260, label='cnt_dict：数字 → 出现次数'),
    ],
    watch=['char', ('index', 'index', 'blue')],
    captions={
        'cnt_dict = {}': '用字典记录每个数字出现的次数',
        'cnt_dict[int(char)] =': '数字 `{char}` 出现次数 +1 → `cnt_dict[{char}] = {cnt_dict[int(char)]}`',
        'if cnt_dict.get(index, 0)': lambda S, B, r: (f'数字 `{S.index}` 出现 `{S.cnt_dict.get(S.index, 0)}` 次，要求 `{S.char}` 次 → 相等，通过' if S.cnt_dict.get(S.index, 0) == int(S.char) else f'数字 `{S.index}` 出现 `{S.cnt_dict.get(S.index, 0)}` 次，要求 `{S.char}` 次 → 不等'),
        'return False': '有一位对不上 → `False`',
        'return True': '每一位都对得上 → `True`',
    },
    cards=dict(
        one_liner='长度很短，一趟统计、一趟核对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `num` 的第 `i` 位要等于「数字 `i` 在 `num` 里出现的次数」',
                 '每一位都满足返回 `True`，否则 `False`',
                 '示例：`"1210"` → `True`'],
        quote='由于题目给出的数的长度很短，因此可以直接一趟遍历，统计每种数字出现的次数，然后再一趟遍历，判断每一位下标对应的数字出现的次数是否恰好等于这位下标对应的数。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：用字典统计每种数字出现次数',
              '第二趟：`enumerate` 同时拿到下标和字符',
              '没出现过的数字用 `get(index, 0)` 当作 0 次'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：字典里没有的数字要当 0，用 `get(index, 0)`，否则 `KeyError`',
                 '字符要转 `int` 再比较，不能直接拿字符和次数比',
                 '原文本身可在 Python 3 直接运行，未做修改'],
    ),
)
