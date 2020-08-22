# Insertion Sort using recursion, Python implementation. @mirokrastev
class InsertionSort:
    def __init__(self, unsorted_ll):
        self.__sorted_ll = unsorted_ll[:1]
        self.__unsorted_ll = unsorted_ll[1:]
        self.__iterate_over_ll()

    def __check_conditions(self, inx):
        if inx <= 0:
            return

        element = self.__sorted_ll[inx]
        if self.__sorted_ll[inx-1] > element:
            self.__sorted_ll[inx-1], self.__sorted_ll[inx] = self.__sorted_ll[inx], self.__sorted_ll[inx-1]
            return self.__check_conditions(inx-1)

    def __iterate_over_ll(self):
        for el in range(len(self.__unsorted_ll)):
            self.__sorted_ll.append(self.__unsorted_ll[el])
            self.__check_conditions(el+1)

    def cleaned(self):
        return self.__sorted_ll


# Driver Code:

if __name__ == '__main__':
    test = InsertionSort([4, 0, -1 , 6, 1, 10, 2])
    print(test.cleaned())