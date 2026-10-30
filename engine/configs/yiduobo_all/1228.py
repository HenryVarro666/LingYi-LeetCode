ARR = [5, 7, 11, 13]


CONFIG = dict(
    num=1228, title='等差数列中缺失的数字', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='等差数列求和 − 实际和',
    tags=[],
    code='''
class Solution(object):
    def missingNumber(self, arr):

        return (arr[0] + arr[-1]) * (len(arr) + 1) // 2 - sum(arr)
''',
    call=f'Solution().missingNumber({ARR})',
    expect=9,
    views=[
        dict(type='array', var='arr', label='arr（缺了一个数，但首尾都在）', cell=100, h=220,
             color=lambda S, i, v: 'green' if i in (0, len(S['arr']) - 1) else None),
        dict(type='text', size=34, h=110, fn=lambda S: f"完整数列有 `{len(S['arr']) + 1}` 项：`({S['arr'][0]} + {S['arr'][-1]}) × {len(S['arr']) + 1} // 2` = =={(S['arr'][0] + S['arr'][-1]) * (len(S['arr']) + 1) // 2}=="),
        dict(type='text', size=34, h=110, fn=lambda S: f"实际只有 `{sum(S['arr'])}`，差值 =={(S['arr'][0] + S['arr'][-1]) * (len(S['arr']) + 1) // 2 - sum(S['arr'])}== 就是缺的数"),
    ],
    watch=[],
    captions={
        'return': '完整数列和 `({arr[0]} + {arr[-1]}) × {len(arr) + 1} // 2 = {(arr[0] + arr[-1]) * (len(arr) + 1) // 2}`，减去实际和 `{sum(arr)}`，缺失的数是 ==`{ret}`==',
    },
    cards=dict(
        after=[dict(heading='为什么差值就是缺的数', lines=['完整数列：`5, 7, 9, 11, 13`，共 `5` 项，和 `45`',
                                                      '现有 `[5,7,11,13]` 的和是 `36`',
                                                      '`45 − 36 = 9`：少掉的恰好就是缺的那一项',
                                                      '不用找公差，也不用排序或二分',
                                                      '代码只有一行，思路全在公式里']),],
        one_liner='补全后的等差数列和减去现有和，差值就是缺的数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一个等差数列恰好被删掉一个数，且删掉的不是首尾',
                 '给出剩下的数组 `arr`，找出缺失的数',
                 '示例：`[5,7,11,13]` → `9`'],
        quote='如果没有缺失数字，那么arr中各个数字的总和s就可以通过等差数列求和公式得到。只需使用s减去当前arr的和，就得到缺失的数值了。',
        quote_src='—— yiduobo 题解原文',
        idea=['首尾没缺，所以完整数列有 `len(arr) + 1` 项',
              '等差数列求和：`(首 + 尾) × 项数 / 2`',
              '减去 `sum(arr)`，剩下的就是缺的那一项'],
        summary=['时间 `O(n)`（`sum` 遍历），空间 `O(1)`',
                 '项数是 `len(arr) + 1`，不是 `len(arr)`',
                 '原文为 Python 2 写法，整数除法 `/ 2` 已改为 `// 2`（乘积必为偶数，结果是整数）'],
    ),
)
