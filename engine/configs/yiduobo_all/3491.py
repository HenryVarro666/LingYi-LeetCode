CONFIG = dict(
    num=3491, title='电话号码前缀', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按长度排序 + 暴力 startswith',
    tags=[],
    code='''
class Solution(object):
    def phonePrefix(self, numbers):
        
        numbers.sort(key=lambda d:len(d))
        for index, now in enumerate(numbers):
            for shorter in numbers[:index]:
                if now.startswith(shorter):
                    return False
        
        return True
''',
    call='Solution().phonePrefix(["97", "1234", "12", "5", "123"])',
    expect=False,
    views=[
        dict(type='array', var='numbers', label='numbers（按长度从短到长）', h=230, cell=130,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('pink' if S.get('shorter') == v and i < S.get('index', 0) else 'blue' if i == S.get('index') else None) if 'index' in S else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
        dict(type='text', h=110, size=32,
             fn=lambda S: (f"`{S['now']}` 是否以 `{S['shorter']}` 开头？ ==" + ('是，找到前缀' if S['now'].startswith(S['shorter']) else '否') + '==') if 'shorter' in S and 'now' in S else ''),
    ],
    watch=['index', ('now', 'now', 'blue'), ('shorter', 'shorter', 'pink')],
    captions={
        'numbers.sort': '先按长度从短到长排序：==前缀一定比它所在的号码短==，所以只需要拿「前面更短的」去比：`{numbers}`',
        'for index, now': '取第 `{index}` 个号码 `now = {now}`，它只可能以排在它前面的号码为前缀',
        'for shorter in numbers[:index]': '枚举排在 `now` 前面（更短）的号码：下一个 `shorter`，或已经比完',
        'if now.startswith': lambda S, B, r: (f'`{S.now}` 以 `{S.shorter}` 开头 → ==成立==：`{S.shorter}` 是 `{S.now}` 的前缀' if S.now.startswith(S.shorter) else f'`{S.now}` 不以 `{S.shorter}` 开头 → 不成立，试下一个更短的号码'),
        'return False': '找到了「某号码是另一个号码前缀」→ 返回 ==False==，不用再找',
        'return True': '所有号码都比完了，没有前缀关系 → ==True==',
    },
    cards=dict(
        one_liner='先按长度排序，每个号码只和更短的号码比前缀',
        complexity='时间 `O(n^2 · L)`，空间 `O(1)`（排序除外）',
        problem=['`numbers` 是一组电话号码字符串',
                 '若有号码是另一个号码的前缀，返回 `False`；都不是则返回 `True`',
                 '本视频：`["97","1234","12","5","123"]` → `False`（`12` 是 `1234` 的前缀）'],
        quote='本题的数据规模较小，直接暴力计算也是没问题的。将所有字符串按长度从小到大进行排序，然后一趟遍历……',
        quote_src='—— yiduobo 题解原文',
        idea=['这类前缀题常用 trie 树，但本题数据小，==暴力就够==',
              '前缀不可能比原串长 → 按长度排序后，只看排在前面的号码',
              '对每个 `now`，枚举更短的 `shorter`，用 `startswith` 判断'],
        summary=['时间 `O(n^2 · L)`，空间 `O(1)`（不计排序）',
                 '返回值的含义是「==没有==前缀关系才是 True」，别写反',
                 '数据更大时可换 trie：插入时若路过完整号码、或本号码是别人的前缀，就返回 False',
                 '原文已是 Python 3 可运行写法，未作改动'],
    ),
)
