# https: // repl.it / repls / DullImpressionableBits
import json
import unittest

input0 = [{"name": "John"}, {"name": 2}, {"name": "Joe"}, {"name": {"name": "nobody"}}, {"name": {"name": "34"}},
          {"name": {"name": 43}}, {"name": "43"}, {"name": "a43"}, {"name": "christos"}, {"name": "393"}]

output0 = [{"name": 2}, {"name": "393"}, {"name": "43"}, {"name": "Joe"}, {"name": "John"}, {"name": "a43"},
           {"name": "christos"}, {"name": {"name": 43}}, {"name": {"name": "34"}}, {"name": {"name": "nobody"}}]

input1 = [{"name": "Christos"}, {"name": "looks"}, {"name": "like"}, {"name": {"name": "French"}},
          {"name": {"name": "Montana"}}, {"name": {"name": 2019}}, {"name": "20 \n 19"}, {"name": "whitespace"},
          {"name": " "}, {"name": "_"}]

input2 = [{"name": "Christos"}, {"name": "looks"}, {"name": "like"}, {"name": {"name": "French"}},
          {"name": {"name": "Montana"}}, {"name": {"name": 2019}}, {"name": "20 \n 19"}, {"name": "whitespace"},
          {"name": " "}, {"name": "_"}]

input3 = [{"name": " Travis"}, {"name": "Scott"}, {"name": "Ast"}, {"name": {"name": "ro"}},
          {"name": {"name": "world"}}, {"name": {"name": 2019}}, {"name": "20 \n 19"}, {"name": "whitespace"},
          {"name": " "}, {"name": "_"}]

input4 = [{"name": "chri"}, {"name": "7tos"}, {"name": "23"}, {"name": {"name": 23}}, {"name": {"name": 23}},
          {"name": {"name": "2019"}}, {"name": "json"}, {"name": "jason"}, {"name": " j7son"}, {"name": "arnold"}]

input5 = [{"name": "terminator"}, {"name": "says"}, {"name": "i"}, {"name": {"name": ""}}, {"name": "am"},
          {"name": {"name": "back"}}, {"name": " i need"}, {"name": " one 1"}, {"name": " last"},
          {"name": "  t  h  i ng !"}]


def dict_value(d):
    for k, v in d.items():
        if isinstance(v, dict):
            return (dict_value(v))
        else:
            return v


# def dict_depth(dic, level=1):
#     str_dic = str(dic)
#     counter = 0
#     for i in str_dic:
#         if i == "{":
#             counter += 1
#     return (counter)

#https://stackoverflow.com/questions/9538875/recursive-depth-of-python-dictionary
def dict_depth(d, depth=0):
    if not isinstance(d, dict) or not d:
        return depth
    return max(dict_depth(v, depth+1) for k, v in d.items())


def bubble_sort(nums):
    # inverse sorting
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            if dict_depth(nums[i]) > dict_depth(nums[i + 1]):
                # Swap the elements
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                # Set the flag to True so we'll loop again
                swapped = True
            elif dict_depth(nums[i]) == dict_depth(nums[i + 1]):
                # need to check case if same type
                if (type(dict_value(nums[i])) == type(dict_value(nums[i + 1]))):
                    if (dict_value(nums[i]) > dict_value(nums[i + 1])):
                        nums[i], nums[i + 1] = nums[i + 1], nums[i]
                        swapped = True
                # need to check case if different types
                if (isinstance((dict_value(nums[i])), str) == True & isinstance((dict_value(nums[i + 1])),
                                                                                int) == True):
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    swapped = True
                    # swapped = True
    return nums

# inspired by https://repl.it/repls/AncientWorrisomePerl

def sort(arr):
    object_array = []
    str_array = []
    num_array = []
    return_array = []
    for x in range(0, len(arr)):
        if (isinstance((arr[x]), dict) == True):
            object_array.append(arr[x])
        elif (isinstance((arr[x]), str) == True):
            str_array.append(arr[x])
        elif (isinstance((arr[x]), int) == True or isinstance((arr[x]), float) == True):
            num_array.append(arr[x])
    if (len(num_array) > 0):
        return_array = return_array + (sorted(num_array))
    if (len(str_array) > 0):
        return_array = return_array + (sorted(str_array))
    if (len(object_array) > 0):
        return_array = return_array + (bubble_sort(object_array))
    return return_array


# if __name__ == '__main__':

    # #sort()
    # print(su(team9))

#     unittest.main()














