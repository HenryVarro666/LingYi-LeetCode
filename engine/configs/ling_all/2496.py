CONFIG = dict(
    num=2496, title='数组中字符串的最大值', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='isdigit 判断 + max 一行',
    tags=[],
    code='''
class Solution:
    def maximumValue(self, strs: List[str]) -> int:
        return max(int(s) if s.isdigit() else len(s)
                   for s in strs)
''',
    call='Solution().maximumValue(["alic3","bob","3","04","00000"])',
    expect=5,
    views=[
        dict(type='array', var='strs', label='strs（每个字符串的值：纯数字 → 数值；否则 → 长度）', cell=130, h=200,
             color=lambda S, k, v: 'green' if v.isdigit() else 'blue'),
        dict(type='text', size=28, h=240,
             fn=lambda S: '　'.join(f"`{s}` → =={int(s) if s.isdigit() else len(s)}==" for s in S['strs']) if 'strs' in S else ''),
    ],
    watch=[],
    captions={
        'return max': lambda S, B, ret: (
            '逐个算值：' + '；'.join(f"`{s}` " + (f"纯数字，值 {int(s)}" if s.isdigit() else f"含字母，值为长度 {len(s)}") for s in S.strs)
            + f'。最大的是 =={max(int(s) if s.isdigit() else len(s) for s in S.strs)}==，返回'),
    },
    cards=dict(
        one_liner='纯数字取数值，否则取长度，一行 max 搞定',
        complexity='时间 `O(L)`，空间 `O(1)`，`L` 为所有字符串长度之和',
        problem=['字符串的==值==：只含数字 → 十进制数值；否则 → 字符串长度',
                 '返回 `strs` 中所有字符串值的最大值',
                 '示例：`["alic3","bob","3","4","00000"]` → `5`'],
        quote='return max(int(s) if s.isdigit() else len(s) for s in strs)',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['`s.isdigit()` 判断是否纯数字，是就 `int(s)`，否则 `len(s)`',
              '前导零没关系：`int("00000") = 0`、`int("04") = 4`',
              '用生成器表达式把每个字符串的值交给 `max`'],
        after=[dict(heading='拆开看这一行', lines=[
            '`s.isdigit()` 为真 → 走 `int(s)`，为假 → 走 `len(s)`',
            '三元表达式给每个字符串算出一个值，`max` 取其中最大的',
            '`"alic3"` 虽含数字 3，但有字母，所以值是长度 5',
            '`"00000"` 是纯数字，值为 0，不是长度 5'])],
        summary=['时间 `O(L)`，空间 `O(1)`（生成器不建列表）',
                 '易错：`"alic3"` 含字母，值是长度 5，不是 3',
                 '`int("04")` 自动去掉前导零',
                 '题目保证字符串非空，`max` 不会拿到空序列'],
    ),
)
