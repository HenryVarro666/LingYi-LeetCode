SETUP = '''
class _Tok(str):
    pass

class _Seq(list):
    def __iter__(self):
        for k in range(len(self)):
            t = _Tok(self[k])
            t.k = k
            yield t

class _Pre(str):
    def split(self, sep=None):
        return _Seq(str.split(self, sep))
'''


def _idx(S):
    return getattr(S.get('char'), 'k', None)


def _toks(S):
    p = S.get('preorder')
    return list(str.split(p, ',')) if p is not None else None


def _slot(S, B, ret):
    c = S['childs']
    return f'当前坑位 `childs = {c}`'


def _info(S):
    c = S.get('childs')
    if c is None:
        return '还没扫描：坑位 `childs` 还不存在（`None`）'
    i = _idx(S)
    tok = S['char'] if i is not None else ''
    if i is None or S['_line'] == 16:
        return f'扫描结束：剩余坑位 `childs = {c}`'
    kind = '空节点 `#`：只消费，不提供' if tok == '#' else f'非空节点 `{tok}`：消费 1 个，提供 2 个'
    return f'读到 `{tok}`（{kind}）→ 坑位 =={c}=='


def _cap_dec(S, B, ret):
    return f'读到 `{S.char}`：它要占掉一个坑位 → `childs = {B.childs} - 1 = {S.childs}`，剩 =={S.childs}== 个坑'


def _cap_neg(S, B, ret):
    if S.childs < 0:
        return f'`childs = {S.childs} < 0`：==没有坑位可占了== → 序列非法'
    return f'`childs = {S.childs} >= 0`：坑位够用，继续'


def _cap_root(S, B, ret):
    return f'第一个节点是根，==不需要占坑==，只设 `childs = 0`'


def _cap_plus(S, B, ret):
    return f'`{S.char}` 是非空节点 → 它自己提供左右两个坑：`childs = {B.childs} + 2 = {S.childs}`，现有 =={S.childs}== 个坑'


def _cap_not(S, B, ret):
    if S.char != '#':
        return f'`{S.char} != \'#\'` → 非空节点，要加坑位'
    return '`#` 是空节点 → 不提供新坑位，坑位只减不增'


def _cap_ret(S, B, ret):
    return f'扫描完：`childs = {S.childs}`，==坑位刚好用完== → `{ret}`' if ret else f'`childs = {S.childs}`，坑位没有刚好用完 → `False`'


CONFIG = dict(
    num=331, title='验证二叉树的前序序列', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='坑位计数',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def isValidSerialization(self, preorder):

        childs = None
        for char in preorder.split(','):
            if childs is not None:
                childs -=1
                if childs < 0:
                    return False
            else:
                childs = 0

            if char != '#':
                childs += 2

        return childs == 0
''',
    setup=SETUP,
    call="Solution().isValidSerialization(_Pre('9,3,4,#,#,1,#,#,2,#,6,#,#'))",
    expect=True,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var=_toks, label='preorder 按逗号切开（蓝 = 正在读的节点）', pointers={'读到': lambda S: _idx(S)},
             cell=64, h=190,
             color=lambda S, i, v: ('blue' if i == _idx(S) else None)),
        dict(type='text', fn=lambda S: ('坑位 ' + '○' * max(0, S['childs']) + f"  （共 {S['childs']} 个）") if S.get('childs') is not None else '', size=30, h=70),
    ],
    watch=[('char', 'char', 'blue'), ('childs', 'childs', 'yellow')],
    captions={
        'childs = None': '`childs` 记录==还空着的坑位数==；`None` 表示还没读到根',
        'for char in': lambda S, B, r: f'读下一个节点 `{S.char}`',
        'if childs is not None': lambda S, B, r: ('已经有坑位记录（读到的不是第一个）→ 这个节点要占一个坑' if S.childs is not None
                                                  else '`childs` 还是 `None`：现在读到的是第一个节点，即根'),
        'childs -=1': _cap_dec,
        'if childs < 0': _cap_neg,
        'return False': '坑位不够，直接判非法 → `False`',
        'childs = 0': _cap_root,
        "if char != '#'": _cap_not,
        'childs += 2': _cap_plus,
        'return childs == 0': _cap_ret,
    },
    cards=dict(
        one_liner='非空节点提供 2 个坑位，每个非根节点占 1 个坑',
        complexity='时间 `O(n)`，空间 `O(1)`（不算切分出的列表）',
        problem=['二叉树前序序列化：非空节点写值，空节点写 `#`，用逗号分隔',
                 '给一个字符串 `preorder`，判断它是否是某棵二叉树合法的前序序列化',
                 '示例：`"9,3,4,#,#,1,#,#,2,#,6,#,#"` → `true`',
                 '本视频用的就是这一例'],
        quote='对于每个非空的节点，其可以提供两个坑位，而除根节点之外的每个节点都需要消费掉一个坑位。',
        quote_src='—— yiduobo 题解原文',
        idea=['不关心数值，只看每个节点是不是 `#`',
              '从左往右扫：根不占坑；之后每个节点先占一个坑，坑不够就非法',
              '非空节点占完坑后再提供 2 个新坑；空节点不提供',
              '全部读完，坑位刚好为 0 才合法'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：==先消费、后提供==。顺序反了，`"#,#"` 这类序列会被误判',
                 '最后必须 `childs == 0`：坑位没填满（`"1,#"`）同样非法',
                 '第一个节点特判：根没有父亲，不占坑',
                 '本视频为了高亮当前读到的字符，在 setup 里给 `split` 包了一层，作者代码未改动'],
    ),
)
