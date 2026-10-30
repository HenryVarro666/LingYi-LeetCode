CONFIG = dict(
    num=1153, title='字符串转化', difficulty='Hard', category='字符串',
    author='yiduobo', technique='哈希表记映射 · 看有没有空闲字母',
    tags=['VIP 题'],
    code='''
class Solution(object):
    def canConvert(self, str1, str2):

        mapping = {}
        used = set()
        for char1, char2 in zip(str1, str2):
            if char1 not in mapping:
                mapping[char1] = char2
            elif mapping[char1] != char2:
                return False
            
            used.add(char2)
        
        return str1 == str2 or len(used) < 26
''',
    call='Solution().canConvert("aabcc", "ccdee")',
    expect=True,
    skip=['for char1, char2 in zip'],
    views=[
        dict(type='string', var='str1', label='str1（要变换的）', cell=64, h=120),
        dict(type='string', var='str2', label='str2（目标）', cell=64, h=120),
        dict(type='text', fn=lambda S: f"当前一对：`{S['char1']}` → `{S['char2']}`" if 'char1' in S else '', size=34, h=70),
        dict(type='map', var='mapping', label='mapping：每个字母必须变成的目标字母', h=170),
        dict(type='set', var='used', label='used：出现过的目标字母', h=130),
    ],
    watch=['char1', 'char2', ('len(used)', 'len(used) if "used" in S else 0', 'green')],
    captions={
        'mapping = {}': '`mapping` 记录「某个字母要变成谁」',
        'used = set()': '`used` 记录用过的目标字母：后面要判断==还剩没剩空闲字母==',
        'if char1 not in mapping': lambda S, B, r: (
            f'取一对字符 `{S.char1}` → `{S.char2}`：'
            + (f'`{S.char1}` 还没有规则 → 新建' if S.char1 not in S.mapping else f'`{S.char1}` 已经规定要变成 `{S.mapping[S.char1]}`，检查是否一致')),
        'mapping[char1] = char2': '记下规则：`{char1}` 必须变成 `{char2}`',
        'elif mapping[char1] != char2': lambda S, B, r: (
            f'`{S.char1}` 之前定的目标是 `{S.mapping[S.char1]}`，这次要变成 `{S.char2}`：'
            + ('一致，没有冲突' if S.mapping[S.char1] == S.char2 else '==矛盾==，同一个字母不可能变成两种字母')),
        'return False': '同一个字母要变成两个不同字母 → 一定不行，返回 `False`',
        'used.add(char2)': '目标字母 `{char2}` 记入 `used`，现在用了 `{len(used)}` 个不同的字母',
        'return str1 == str2': lambda S, B, r: (
            f'`used` 有 `{len(S.used)}` 个字母 `< 26` → ==还有空闲字母==，可以当中转，换环也能完成 → `{r}`' if len(S.used) < 26 and S.str1 != S.str2
            else f'两个字符串本来就相等 → `{r}`' if S.str1 == S.str2 else f'26 个字母都被占用，没有空闲字母可当中转 → `{r}`'),
    },
    cards=dict(
        one_liner='无冲突映射 + 至少留一个空闲字母，就一定能转化',
        complexity='时间 `O(n)`，空间 `O(1)`（字母表大小是常数）',
        problem=['两个等长字符串 `str1`、`str2`，每次转换：把 `str1` 中==某个字母的所有出现==统一换成另一个小写字母',
                 '问能否经过若干次转换，把 `str1` 变成 `str2`',
                 '示例：`aabcc` → `ccdee` 返回 `True`；`leetcode` → `codeleet` 返回 `False`',
                 '本视频：`aabcc` → `ccdee`'],
        quote='只要存在空闲的中间字符且没有单个字符变成多个字符的变换，那么就一定可以完成所有的变换。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看冲突：同一个字母要变成两个不同字母，直接 `False`',
              '没有冲突时，变换之间可能有先后依赖，甚至成环（`a→b`、`b→a`）',
              '环可以借一个==空闲字母==当中转解开，所以只要 `used` 不满 26 个就行',
              '`used` 满 26 个时，除非两串相等，否则映射里必有环、却没有中转可用'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：字母集合满 26 个时，`str1 == str2` 要单独判 `True`（什么都不用变）',
                 '原文用图论解释：26 个节点 26 条边必有环，所以满 26 个且不相等就无法转化',
                 '`mapping` 只管一对多冲突；多对一（几个字母变成同一个）是允许的',
                 '代码原样保留（原文是 Python 3 可运行写法），只删去了类型说明文档字符串'],
    ),
)
