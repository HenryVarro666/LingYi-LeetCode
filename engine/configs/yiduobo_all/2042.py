def _tok(S):
    return S['s'].split(' ') if 's' in S else None


def _col(S, i, v):
    if 'word' not in S:
        return None
    toks = _tok(S)
    cur = toks.index(S['word'])
    if i == cur:
        return 'blue'
    if i < cur and v[0].isdigit():
        return 'green'
    return None


def _top(S):
    if 'word' not in S:
        return '把句子按单个空格切成 token'
    last = S.get('last')
    return f"上一个数字 `last = {last}`" if last is not None else '还没遇到数字，`last = None`'


CONFIG = dict(
    num=2042, title='检查句子中的数字是否递增', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按空格切分 + 记录上一个数字',
    code='''
class Solution(object):
    def areNumbersAscending(self, s):

        last = None
        for word in s.split(' '):
            if word[0] < '0' or word[0] > '9':
                continue
            
            now = int(word)
            
            if last is not None and last >= now:
                return False
            last = now
        
        return True
''',
    call='Solution().areNumbersAscending("at 7 51 pm low 50 s")',
    expect=False,
    views=[
        dict(type='text', fn=_top, size=28, h=60),
        dict(type='array', var=_tok, label='token（蓝 = 当前，绿 = 已处理的数字）', cell=100, color=_col,
             pointers={"s.split(' ').index(word)": 'blue'}, pointer_labels={"s.split(' ').index(word)": 'word'}, h=300),
    ],
    watch=[('word', 'word', 'blue'), ('now', 'now', 'cyan'), ('last', 'last', 'orange')],
    captions={
        'last = None': '`last` 记上一个数字，还没遇到数字所以是 `None`',
        'for word in': '按单个空格切开，逐个看 token：`word = "{word}"`',
        'if word[0] <': lambda S, B, ret: (f"只看首字符 `'{S.word[0]}'`：不是数字 → 这是单词，跳过" if (S.word[0] < '0' or S.word[0] > '9')
                                           else f"只看首字符 `'{S.word[0]}'`：是数字 → ==整个 token 都是数字=="),
        'continue': '单词不用管，看下一个 token',
        'now = int(word)': '转成整数：`now = {now}`',
        'if last is not None': lambda S, B, ret: ('第一个数字，前面没有数字可比，直接记下' if S.last is None
                                                  else (f'`last = {S.last} >= now = {S.now}` → ==不是严格递增==' if S.last >= S.now
                                                        else f'`last = {S.last} < now = {S.now}` → 仍然递增')),
        'return False': '出现 `last >= now`（相等也不行）→ 返回 `False`',
        'last = now': '`last` 更新为 `{last}`，下一个数字要比它大',
        'return True': '全部数字都严格递增 → `True`',
    },
    cards=dict(
        one_liner='split 后只看首字符：是数字就和上一个数字比大小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['句子由单词和不含前导零的正整数 token 组成，空格分隔',
                 '检查句子里的数字是否==从左到右严格递增==',
                 '本视频：`"at 7 51 pm low 50 s"` → `false`（51 之后是 50）'],
        quote='由于单个token要么全是字符，要么是数字，那么检测token的首字符就可以判断当前的token是不是数字。如果是，将其转化后判断其是否大于等于上一个数字即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目保证 token 间只有单个空格，直接 `split(\' \')`',
              'token 要么全字母要么全数字 → 看首字符 `word[0]` 就够了',
              '数字用 `last` 记着上一个，`last >= now` 立刻返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：要求严格递增，相等也是 `False`，所以判断用 `>=`',
                 '易错：`last` 初值用 `None`，第一个数字不比较',
                 '原文为 Python 2 写法，本题代码无需改动'],
    ),
)
