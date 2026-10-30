CONFIG = dict(
    num=1528, title='重新排列字符串', difficulty='Easy', category='字符串',
    author='yiduobo', technique='按下标直接放置', tags=[],
    code='''
class Solution(object):
    def restoreString(self, s, indices):

        res = [''] * len(s)
        for index, pos in enumerate(indices):
            res[pos] = s[index]
        
        return ''.join(res)
''',
    call="Solution().restoreString('codeleet', [4,5,6,7,0,2,1,3])",
    expect='leetcode',
    views=[
        dict(type='string', var='s', h=150, label='s', pointers={'index': 'blue'}),
        dict(type='array', var='indices', h=170, label='indices（s[i] 要放到的位置）', pointers={'index': 'blue'}),
        dict(type='array', var='res', h=200, label='res', pointers={'pos': 'pink'},
             color=lambda S, i, v: 'green' if v != '' else None),
    ],
    watch=['index', 'pos', ('res', "''.join(res)", 'green')],
    captions={
        'res = [': '准备 `res`：长度 `{len(s)}` 的空槽，等着往里放字符',
        'for index, pos': '第 `{index}` 个字符 `s[{index}] = {s[index]}`，目标位置 `indices[{index}] = {pos}`',
        'res[pos] = s[index]': '把 `{s[index]}` 放进 `res[{pos}]`：==按 indices 直接定位，不用排序==',
        'return': '槽都填满了，拼起来得 `{ret}`',
    },
    cards=dict(
        one_liner='第 i 个字符该去 indices[i]，直接放过去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给字符串 `s` 和等长整数数组 `indices`',
                 '重新排列后，`s` 的第 `i` 个字符要落到位置 `indices[i]`',
                 '示例：`s = "codeleet"`，`indices = [4,5,6,7,0,2,1,3]` → `"leetcode"`'],
        quote='比较基础的题目，按题目意思根据indices重新排布s然后输出即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先开一个等长的空数组 `res`',
              '`enumerate(indices)` 同时拿到下标和目标位置',
              '一次循环把每个字符放到位，最后 `join`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：==方向别搞反==，是 `res[indices[i]] = s[i]`，不是 `res[i] = s[indices[i]]`',
                 '`indices` 是 `0..n-1` 的排列，不会冲突也不会漏位',
                 '原文为 Python 2 写法，在 Python 3 下无需改动'],
    ),
)
