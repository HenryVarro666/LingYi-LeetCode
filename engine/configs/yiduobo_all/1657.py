S0, T0 = 'cabbba', 'abbccc'

CONFIG = dict(
    num=1657, title='确定两个字符串是否接近', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='统计次数 · 种类与分布',
    tags=['灵神题单', '贪心与思维', '难度分 1530'],
    code='''
class Solution(object):
    def closeStrings(self, word1, word2):

        cnt_dict1 = {}
        cnt_dict2 = {}

        for char in word1:
            cnt_dict1[char] = cnt_dict1.get(char, 0) + 1
        
        for char in word2:
            cnt_dict2[char] = cnt_dict2.get(char, 0) + 1
        
        if len(cnt_dict1) != len(cnt_dict2):
            return False
        
        for key in cnt_dict1.keys():
            if key not in cnt_dict2:
                return False
        
        if sorted(cnt_dict1.values()) != sorted(cnt_dict2.values()):
            return False
        
        return True
''',
    call=f'Solution().closeStrings("{S0}", "{T0}")',
    expect=True,
    views=[
        dict(type='string', var='word1', label='word1', cell=76),
        dict(type='string', var='word2', label='word2', cell=76),
        dict(type='map', var='cnt_dict1', label='cnt_dict1', fmt=lambda k, v: f'{k} × {v}'),
        dict(type='map', var='cnt_dict2', label='cnt_dict2', fmt=lambda k, v: f'{k} × {v}'),
    ],
    watch=['char', ('key', 'key', 'blue')],
    captions={
        'cnt_dict1 = {}': '`cnt_dict1` 统计 word1 里每种字符的个数',
        'cnt_dict2 = {}': '`cnt_dict2` 统计 word2 里每种字符的个数',
        'for char in word1': '遍历 word1，`char = {char}`',
        'for char in word2': '遍历 word2，`char = {char}`',
        'cnt_dict1[char] =': '`cnt_dict1[{char}]` → `{cnt_dict1[char]}`',
        'cnt_dict2[char] =': '`cnt_dict2[{char}]` → `{cnt_dict2[char]}`',
        'if len(cnt_dict1) != len(cnt_dict2)': '字符==种类数==：`{len(cnt_dict1)}` vs `{len(cnt_dict2)}`，一样才可能接近',
        'for key in cnt_dict1.keys()': '逐个检查 word1 的字符是否也出现在 word2（`key = {key}`）',
        'if key not in cnt_dict2': '`{key}` 在 word2 里 → {"有" if key in cnt_dict2 else "没有"}',
        'if sorted': '各字符次数排序后比较：`{sorted(cnt_dict1.values())}` vs `{sorted(cnt_dict2.values())}`（操作 2 只会==交换次数==，分布不变）',
        'return True': '种类一致、次数分布一致 → 接近，返回 `True`',
    },
    cards=dict(
        one_liner='位置不重要；种类和次数的分布不变，就是接近',
        complexity='时间 `O(n + m)`，空间 `O(1)`（最多 26 个字母）',
        problem=['操作 1 交换任意两个字符，操作 2 把两种字符整体互换',
                 '判断 `word1` 能否变成 `word2`',
                 '示例：`"cabbba"` → `"abbccc"`，答案 `true`'],
        quote='操作一可以任意交换两个字符的位置，就说明无需考虑各个字符的位置，只需要考虑字符的种类以及数量就好了。',
        quote_src='—— yiduobo 题解原文',
        idea=['操作二是两种字符互换 → 出现的==字符种类==不变',
              '互换也不改变各字符出现次数的==分布==',
              '统计两个字符串的次数，对比种类是否一致、次数排序后是否一致'],
        result='种类都是 a、b、c，次数排序后都是 `[1,2,3]` → True ✓',
        summary=['时间 `O(n + m)`，空间 `O(1)`',
                 '易错：只比较次数的分布而不比较字符种类，会把 `abc` 和 `def` 判成接近',
                 '先比种类个数，再比每个字符是否存在，最后比排序后的次数',
                 '对比灵神：灵神用 `set` 和 `Counter(values)` 一行写完，这里手写字典、逐项判断'],
    ),
)
