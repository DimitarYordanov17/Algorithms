# Selection Sort, Python implementation. @mirokrastev
class SelectionSort:
    def __init__(self, unsorted_ll):
        self.__sorted_ll = []
        self.__unsorted_ll = unsorted_ll
        self.__iterate_over_ll()

    def __get_min_element(self):
            min_num = None

            for num in self.__unsorted_ll:
                if min_num is None or num < min_num:
                    min_num = num
            return min_num

    def __iterate_over_ll(self):
        if not self.__unsorted_ll:
            return
        min_element = self.__get_min_element()
        self.__unsorted_ll.remove(min_element)
        self.__sorted_ll.append(min_element)
        return self.__iterate_over_ll()

    def cleaned(self):
        return self.__sorted_ll


# Driver Code:

if __name__ == '__main__':
    test = SelectionSort([4, 0, -1 , 6, 1, 10, 2])
    print(test.cleaned())