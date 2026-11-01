CONFIG = dict(
    num=2124, title='检查是否所有 A 都在 B 之前', difficulty='Easy', category='字符串',
    author='yiduobo', technique='遍历 + b_flag 标记',
    tags=[],
    code='''
class Solution(object):
    def checkString(self, s):

        b_flag = False
        for char in s:
            if char == 'a' and b_flag:
                return False
            elif char == 'b':
                b_flag = True

        return True
''',
    call='Solution().checkString("aabbab")',
    expect=False,
    views=[
        dict(type='text', size=30, fn=lambda S: (
            f"`b_flag = {S['b_flag']}`：" + ('已经见过 b' if S['b_flag'] else '还没见过 b')) if 'b_flag' in S else ''),
        dict(type='string', var='s', h=300, cell=110,
             color=lambda S, i, v: 'blue' if v == 'a' else 'pink'),
    ],
    watch=[('char', 'char', 'blue'), ('b_flag', 'b_flag', 'pink')],
    captions={
        'b_flag = False': '`b_flag` 记录「到目前为止有没有见过 b」，一开始没有',
        'for char in s': '从左到右看下一个字符 `{char}`',
        "if char == 'a' and b_flag": lambda S, B, r: (
            f"当前是 `a`，而且 `b_flag = True`：==前面已经有 b 了，这个 a 在它后面==" if S.char == 'a' and S.b_flag
            else (f"当前是 `a`，但 `b_flag = False`：前面没有 b，没问题" if S.char == 'a'
                  else "当前是 `b`，不是「a 且见过 b」的情形，往下看")),
        'return False': '有 a 排在 b 后面 → 返回 `False`',
        "elif char == 'b'": lambda S, B, r: ('当前是 `b`，准备记下来' if S.char == 'b' else '当前是 `a`，不是 b，什么也不用记'),
        'b_flag = True': '`b_flag = True`：之后再遇到 a 就说明不合法',
        'return True': '整串扫完没有出问题 → 返回 `True`',
    },
    cards=dict(
        one_liner='扫一遍，见过 b 之后再遇到 a 就失败',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 只含 `a` 和 `b`，问是否每个 `a` 都在每个 `b` 之前',
                 '示例：`"aaabbb"` → `true`，`"abab"` → `false`，`"bbb"` → `true`',
                 '本视频：`"aabbab"` → `false`'],
        quote='使用一个变量b_flag记录当前是否有b出现过，初始化为false，接下来从左向右一趟遍历。若当前字符为a且b_flag为true，那么说明有b出现在当前的a之前，此时直接返回false。',
        quote_src='—— yiduobo 题解原文',
        idea=['用一个布尔变量 `b_flag` 记住「前面有没有 b」',
              '遇到 `b` 就置为真；遇到 `a` 时若 `b_flag` 为真，说明这个 a 前面有 b，直接判错',
              '一趟遍历结束没出问题就是合法'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：要先判断 a 再更新 b_flag；只有 b 的串（`"bbb"`）合法',
                 '原文只删了 Python 2 风格的类型说明（本题原文无需其他改动）',
                 '对比灵神：灵神一行 `"ba" not in s`，这里是显式标记的单趟扫描'],
    ),
)
