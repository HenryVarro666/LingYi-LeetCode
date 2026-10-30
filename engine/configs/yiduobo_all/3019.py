def _txt(S):
    if 'index' not in S or 'diff' not in S:
        return '相邻字符 ASCII 差为 0 或 32：同一个键'
    d = S['diff']
    return f"`diff = {d}`：" + ('同一个键' if d in (0, 32) else '==差值不是 0 也不是 32，换键==')


CONFIG = dict(
    num=3019, title='按键变更的次数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · ASCII 差值',
    code='''
class Solution(object):
    def countKeyChanges(self, s):
        
        res = 0
        for index in range(1, len(s)):
            diff = abs(ord(s[index]) - ord(s[index - 1]))
            if diff != 0 and diff != 32:
                res += 1
        
        return res
''',
    call="Solution().countKeyChanges('aAbBcCaA')",
    expect=3,
    views=[
        dict(type='string', var='s', label='s（蓝=当前 index，前一个看 index-1）', cell=90, h=200,
             pointers={'index': 'blue'}),
        dict(type='text', fn=_txt, h=100, size=30),
    ],
    watch=['index', 'diff', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录按键变更次数',
        'for index': '看第 `{index}` 个字符和前一个字符 `{s[index-1]!r}` → `{s[index]!r}`',
        'diff =': 'ASCII 差 `|{ord(s[index])} − {ord(s[index-1])}|` = =={diff}==',
        'if diff': '`diff = {diff}`：{"相等或只差 32（大小写）→ 同一个键，不计" if diff in (0, 32) else "既不相等也不差 32 → 换了键"}',
        'res += 1': '换键了：`res` → =={res}==',
        'return res': '一共变更 =={res}== 次',
    },
    cards=dict(
        one_liner='相邻字符 ASCII 差 0 或 32，才是同一个键',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 是用户输入，相邻两次按的不是同一个键就算一次变更',
                 '大小写字母（Shift / Caps Lock）算同一个键',
                 '本视频：`"aAbBcCaA"` → `3`'],
        quote='一趟遍历，检测相邻字符间的ascii码是否相等或者等于32，如果不是，则说明产生了变更，需要将答案加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一个字母的大小写，ASCII 码正好差 32',
              '遍历下标 1 到末尾，算与前一个字符的差的绝对值',
              '差既不是 0 也不是 32 → 换了键，`res += 1`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：从下标 1 开始，第一个字符前面没有按键',
                 '要取绝对值，大小写的先后顺序不定',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神用 `& 31` 位运算；yiduobo 直接比差值'],
    ),
)
