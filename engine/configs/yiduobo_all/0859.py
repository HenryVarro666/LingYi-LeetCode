CONFIG = dict(
    num=859, title='亲密字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='差异位置 + 重复字符',
    code='''
class Solution(object):
    def buddyStrings(self, A, B):

        if len(A) != len(B):
            return False

        same_char = False
        char_set = set()
        diff_list = []

        for index in range(len(A)):
            if A[index] != B[index]:
                diff_list.append(index)
            elif A[index] not in char_set:
                char_set.add(A[index])
            else:
                same_char = True

        if not diff_list and same_char:
            return True
        
        if len(diff_list) == 2 and A[diff_list[0]] == B[diff_list[1]] and B[diff_list[0]] == A[diff_list[1]]:
            return True

        return False
''',
    call='Solution().buddyStrings("abcd", "abdc")',
    expect=True,
    views=[
        dict(type='string', var='A', label='A（粉 = 与 B 不同的位置）', cell=90, h=170, pointers={'index': 'blue'},
             color=lambda S, i, v: 'pink' if 'diff_list' in S and i in S['diff_list'] else None),
        dict(type='string', var='B', label='B', cell=90, h=150,
             color=lambda S, i, v: 'pink' if 'diff_list' in S and i in S['diff_list'] else None),
        dict(type='array', var='diff_list', label='diff_list：不同位置的下标', cell=90, h=130),
        dict(type='set', var='char_set', label='char_set：相同位置出现过的字符', fmt=lambda x: f"'{x}'", h=110),
        dict(type='text', size=28, h=80,
             fn=lambda S: f"same_char = =={S['same_char']}==" if 'same_char' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), 'same_char', 'diff_list'],
    captions={
        'len(A) != len(B)': '`len(A) = {len(A)}`，`len(B) = {len(B)}`：{"长度不同，不可能交换成功" if len(A) != len(B) else "长度相同，继续"}',
        'same_char = False': '`same_char`：A、B 完全一致时，要靠重复字符才能交换',
        'if A[index] != B[index]': '`A[{index}] = {A[index]!r}`，`B[{index}] = {B[index]!r}`：{"不同" if A[index] != B[index] else "相同"}',
        'diff_list.append': '位置 `{index}` 不同，记入 `diff_list` → {diff_list}',
        'elif A[index] not in char_set': '`{A[index]!r}` 之前出现过吗？{"没有" if A[index] not in char_set else "出现过，说明有重复字符"}',
        'char_set.add': '第一次见到 `{A[index]!r}`，加入 `char_set`',
        'same_char = True': '重复字符！`same_char = True`：这两个相同字符互换也不变',
        'if not diff_list': '`diff_list = {diff_list}`：{"没有差异且有重复字符 → True" if (not diff_list and same_char) else "不满足情况二"}',
        'if len(diff_list) == 2': lambda S, B, r: (f'`len(diff_list) = {len(S.diff_list)}`：' + ('恰好两处不同，且交叉相等：`A[i] = B[j]`、`A[j] = B[i]` → True' if len(S.diff_list) == 2 and S.A[S.diff_list[0]] == S.B[S.diff_list[1]] and S.B[S.diff_list[0]] == S.A[S.diff_list[1]] else '不满足情况一')),
        'return False': '两种情况都不满足 → False',
    },
    cards=dict(
        one_liner='要么恰好两处不同且交叉相等，要么完全相同且有重复字符',
        complexity='时间 `O(n)`，空间 `O(1)`（字符集有限）',
        problem=['交换 `A` 中两个位置的字符，能否得到 `B`',
                 '必须交换一次（两个下标不同）',
                 '示例：`A = "abcd"`，`B = "abdc"` → `true`'],
        quote='两个串A和B若为亲密字符串，那么其必然满足下面两个条件之一：1、A和B中仅有两个位置的字符不一样，且这两个位置的字符满足A[i] = B[j]、A[j] = B[i]；2、A和B完全一致，且A中有个两相同的字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟扫描：不同的位置记入 `diff_list`',
              '相同位置的字符放入 `char_set`，再次遇到说明有重复字符',
              '扫完后分别检查两种情况'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：完全相同的串必须有重复字符，`"ab"`/`"ab"` 是 False',
                 '长度不同先返回 False',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)
