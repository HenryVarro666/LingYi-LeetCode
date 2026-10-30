CONFIG = dict(
    num=1324, title='竖直打印单词', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按列逐位输出',
    tags=[],
    code='''
class Solution(object):
    def printVertically(self, s):

        words = s.split(' ')
        res = []
        p = 0
        while True:
            flag = False
            tmp = []
            for index in range(len(words) - 1, -1, -1):
                if p < len(words[index]):
                    tmp.append(words[index][p])
                    flag = True
                elif flag:
                    tmp.append(' ')
            
            if len(tmp) == 0:
                break

            res.append(''.join(tmp[::-1]))
            p += 1
        
        return res
''',
    call="Solution().printVertically('A BC D')",
    expect=['ABD', ' C'],
    views=[
        dict(type='array', var='words', pointers={'index': 'blue'}, label='words（index 从最后一个单词往前）', h=160),
        dict(type='array', var='tmp', label='tmp（这一列，倒着收集）', h=160),
        dict(type='array', var='res', label='res（已完成的列）', h=160),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'cyan'), ('flag', 'flag', 'orange')],
    captions={
        'words = s.split': '按空格切开：`{words}`',
        'p = 0': '`p` 是当前打印第几列，从 0 开始',
        'while True': '开始处理第 `{p}` 列',
        'flag = False': '`flag` 记录“是否已遇到有字符的单词”，用来避免末尾空格',
        'tmp = []': '`tmp` 收集这一列',
        'for index in range': '从后往前看单词 `{words[index]}`',
        'if p < len(words[index])': lambda S, B, r: (f"`{S.p} < len('{S.words[S.index]}')` → 这个单词有第 {S.p} 位" if S.p < len(S.words[S.index])
                                                    else f"`{S.p} >= len('{S.words[S.index]}')` → 这个单词已经没字符了"),
        'tmp.append(words[index][p])': "取 `'{words[index]}'[{p}]` = =={words[index][p]}=="
                                       "，并令 `flag = True`：右侧已出现字符",
        'flag = True': '`flag` 为真：往后（更靠左）的短单词要用空格占位',
        'elif flag': lambda S, B, r: ('`flag` 为真：左边还有字符，用空格补位' if S.flag
                                      else '`flag` 为假：右边还没有字符，空格会变成后缀，不补'),
        "tmp.append(' ')": '补一个空格，`tmp = {tmp}`',
        'if len(tmp) == 0': lambda S, B, r: ('`tmp` 为空：所有单词都没有第 {} 位了 → 结束'.format(S.p) if len(S.tmp) == 0
                                             else f'`tmp` 非空：这一列有内容，继续'),
        "res.append(''.join": '`tmp` 是倒着收集的，反转后拼成第 `{p}` 列 =={res[-1]!r}==',
        'p += 1': '换下一列：`p` → {p}',
        'return res': '全部列完成：`{ret}`',
    },
    cards=dict(
        one_liner='按列扫描：从右往左收集，空格只补在中间不留尾巴',
        complexity='时间 `O(总字符数)`，空间 `O(总字符数)`',
        problem=['把句子 `s` 的单词竖着打印：第 `k` 列由每个单词的第 `k` 个字符组成',
                 '单词短了就用空格补位，但每行不能有后缀空格',
                 '示例：`A BC D` → `["ABD", " C"]`'],
        quote='比较基础的题目，按空格分离单词后逐位输出即可。需要注意不能有后缀空格的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 `split(\' \')`，然后逐列处理，`p` 是列号',
              '从最后一个单词往前扫：遇到第一个有字符的单词前，缺字符不补空格',
              '一旦 `flag` 为真，更靠左的缺字符位置才补空格，这样后缀空格自然消失',
              '倒着收集，最后反转成正常顺序'],
        summary=['时间 `O(总字符数)`，空间 `O(总字符数)`',
                 '易错：后缀空格不能留，中间空格要补',
                 '从右往左扫，`flag` 之前的缺位直接跳过，就是去掉后缀空格',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
