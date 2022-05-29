"""
Created on 11/18/2021

@author: Olivia Chen
"""

if __name__ == '__main__':
    pass


dicti = {}
dicti['a_'] = [1, 2, 3, 4, 5]
dicti['b__'] = [1, 2, 3, 4]
dicti['a___'] = [1, 2, 3, 4, 5]
dicti = sorted(dicti.items(), key=lambda x: x[0].count('_'), reverse=True)
print(dicti)