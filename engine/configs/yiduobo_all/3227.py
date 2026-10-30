V = 'aeiou'


def _cur(S):
    ch = S.get('char')
    s = S['s']
    if ch is None or ch not in s:
        return None
    return s.index(ch)


def _col(S, i, v):
    cur = _cur(S)
    if cur is None:
        return 'green' if v in V else None
    if i == cur:
        return 'green' if v in V else 'blue'
    return None


def _dim(S, i, v):
    cur = _cur(S)
    return cur is not None and i < cur


def _top(S):
    s = S['s']
    cnt = sum(c in V for c in s)
    return f'`s` 里共有 `cnt = {cnt}` 个元音；`cnt` 为奇数 → 小红整串删光；`cnt` 为偶数且 > 0 → 留下 1 个元音；`cnt` = 0 → 小红输'


def _bot(S):
    ch = S.get('char')
    if ch is None:
        return '从左到右找元音：找到一个就说明 `cnt ≥ 1`'
    if ch in V:
        return f'`{ch}` 是元音 → ==小红必胜== → 直接返回 `True`'
    return f'`{ch}` 不是元音，继续往右找'


CONFIG = dict(
    num=3227, title='字符串元音游戏', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='元音个数奇偶讨论 · 找到元音即返回',
    tags=['灵神题单·数学算法', '难度分 1452'],
    code='''
class Solution(object):
    def doesAliceWin(self, s):

        vowel_set = set(['a', 'e', 'i', 'o', 'u'])
        for char in s:
            if char in vowel_set:
                return True
        
        return False
''',
    call='Solution().doesAliceWin("crowd")',
    expect=True,
    views=[
        dict(type='string', var='s', color=_col, dim=_dim, label='s：逐个字符检查是否为元音', h=230),
        dict(type='set', var='vowel_set', fmt=lambda x: str(x), h=130),
        dict(type='text', fn=_top, size=24, h=130),
        dict(type='text', fn=_bot, size=28, h=100),
    ],
    watch=['char'],
    captions={
        'vowel_set = set': '`vowel_set` 放进 5 个元音字母，判断 `char in vowel_set` 是 `O(1)`',
        'for char in s': '取出 `s` 的下一个字符 `char = {char}`',
        'if char in vowel_set': '`{char}` 在 `vowel_set` 里吗？{"是元音，找到了" if char in vowel_set else "不是元音，继续"}',
        'return True': '有元音，`cnt ≥ 1`：奇数个小红一次删光，偶数个小红留下 1 个，小明删不掉 → 小红必胜，返回 `True`',
        'return False': '一个元音都没有，小红第一步就没法删 → 小明必胜，返回 `False`',
    },
    cards=dict(
        one_liner='只看元音个数 cnt：只要有元音，小红就必胜',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['小红先手删含奇数个元音的子串，小明删含偶数个元音的子串，无法删的人输',
                 '两人都最优，问小红能否获胜',
                 '本视频：`crowd` → `True`'],
        quote='若字符串中存在元音字符，则小红必胜，否则小明必胜。',
        quote_src='—— yiduobo 题解原文',
        idea=['设元音个数为 `cnt`。`cnt` 为奇数：小红第一轮整串删完，必胜',
              '`cnt` 为 0：小红一开始就无法删除，小明必胜',
              '`cnt` 为正偶数：小红删掉含 `cnt−1` 个元音的子串，只剩 1 个元音；小明删不掉它，小红再整串删光'],
        summary=['时间 `O(n)`，空间 `O(1)`；遇到第一个元音就可以提前返回',
                 '不需要真的数 `cnt`，也不用模拟删除过程',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神用 `any` 一行写法，yiduobo 用集合逐字符判断，思路相同'],
    ),
)
