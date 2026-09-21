class sortowanie:
    def __init__(self):
        self.data = []

    def get_data(self):
        return self.data

    def generate_data(self, min, max, size):
        import random
        return [random.randint(min, max) for _ in range(size)]

    def add(self, item):
        self.data.append(item)

    def clear(self): 
        self.data = [] 

    # 1 bubble sort
    def bubble_sort(self, data=None):
        if data is not None:
            self.data = data

        n = len(self.data)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.data[j] > self.data[j+1]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]

        return self.data
    # 2 quick sort
    def quick_sort(self, data=None):
        if data is not None:
            self.data = data

        if len(self.data) <= 1:
            return self.data
        else:
            pivot = self.data[0]
            less_than_pivot = [x for x in self.data[1:] if x <= pivot]
            greater_than_pivot = [x for x in self.data[1:] if x > pivot]
            return self.quick_sort(less_than_pivot) + [pivot] + self.quick_sort(greater_than_pivot)

    # 3 insertion sort
    def insertion_sort(self, data=None):
        if data is not None:
            self.data = data

        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and key < self.data[j]:
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key

        return self.data
    # 4 selection sort

    def selection_sort(self, data=None):
        if data is not None:
            self.data = data

        for i in range(len(self.data)):
            min_idx = i
            for j in range(i + 1, len(self.data)):
                if self.data[j] < self.data[min_idx]:
                    min_idx = j
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]

        return self.data



#test_array = [2343244,3424324234324, 434273984623749963249324,4324234324]

#print ("Original array:", test_array)
#print ("Sorted array(bubblesort):", sortowanie().bubble_sort(test_array))
#print ("Sorted array(quicksort):", sortowanie().quick_sort(test_array))
#print ("Sorted array(insertionsort):", sortowanie().insertion_sort(test_array))
#print ("Sorted array(selectionsort):", sortowanie().selection_sort(test_array))