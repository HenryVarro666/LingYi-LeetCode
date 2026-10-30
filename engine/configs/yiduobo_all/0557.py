CONFIG = dict(
    num=557, title='反转字符串中的单词 III', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='split 分词 · 逐词反转 · join',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def reverseWords(self, s):

        res = s.split(' ')
        return ' '.join([x[::-1] for x in res])
''',
    call='Solution().reverseWords("Let\'s take LeetCode contest")',
    expect="s'teL ekat edoCteeL tsetnoc",
    views=[
        dict(type='string', var='s', label='原字符串 s（空格也占一格）', cell=32, h=130),
        dict(type='array', var='res', label='res = s.split(\' \')：按空格分出的单词', cell=130, h=190),
        dict(type='text', fn=lambda S: ('逐个反转：' + '  |  '.join(f'`{w}` → ==`{w[::-1]}`==' for w in S['res'])) if 'res' in S else '', size=26),
    ],
    watch=[('res', 'res', 'blue')],
    captions={
        's.split': '按空格分离单词：`res = {res}`，共 `{len(res)}` 个单词',
        'return': '`x[::-1]` 把每个单词原地倒过来，单词之间的顺序不变；再用空格 `join` 合并 → ==`{ret}`==',
    },
    cards=dict(
        one_liner='按空格拆成单词，每个单词倒过来，再拼回去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一个字符串 `s`，反转其中==每个单词==的字符顺序',
                 '空格和单词的初始顺序保持不变',
                 '示例：`"Let\'s take LeetCode contest"` → `"s\'teL ekat edoCteeL tsetnoc"`'],
        quote='比较基础的题目，按空格分离单词，逐个反转后再合并起来就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s.split(\' \')` 得到单词列表，单词顺序就是原来的顺序',
              '列表推导式对每个单词做 `x[::-1]`，只翻转单词内部',
              '`\' \'.join(...)` 用原来的单个空格重新连起来'],
        after=[dict(heading='为什么不会弄乱空格', lines=[
            '`split(\' \')` 按单个空格切，连续空格会产生空串 `\'\'`',
            '空串反转后还是空串，`join` 时空格数量照样还原',
            '所以拼回去的字符串和原串的空格位置完全一致'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：不能直接 `s[::-1]`，那样单词顺序也会被反转',
                 '`split(\' \')` 按单个空格切分，保留的空格数量与原串一致',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '同类：第 541 题反转字符串 II、第 917 题仅仅反转字母'],
    ),
)
