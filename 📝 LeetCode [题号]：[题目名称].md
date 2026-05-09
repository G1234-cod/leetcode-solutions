# 📝 LeetCode [题号]：[题目名称]

- **题目链接**: [填入力扣题目网址]
- **刷题日期**: YYYY-MM-DD
- **模块分类**: [例如：01. 哈希 (Hash)]

## 一. 大白话思路
*(面试逐字稿：假装对面坐着面试官，用最接地气的话把解法讲清楚。)*
- **解法思路**：[例如：这题绝对不能用两个 for 循环暴力穷举。直接搞个字典（哈希表）边存边查。遍历到一个数时，去字典里查“能跟它凑成目标的另一半”在不在。在的话直接返回，不在就把自己存进去，等下一个数来找。]

## 二. 核心代码实现
*(要求：关键逻辑必须带上中文注释，变量命名必须符合业务规范。推荐优先使用 Python 以培养 AI 开发手感。)*

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 创建一个字典，用来存 元素值:对应索引
        num_map = {} 
        for i, num in enumerate(nums):
            complement = target - num
            # 如果另一半已经在字典里了，直接返回
            if complement in num_map:
                return [num_map[complement], i]
            # 否则把自己存进去
            num_map[num] = i
            
        return []
```

## 三. 复杂度分析



## 四.易错点



## 五.举一反三