package com.example.sortowanie

internal fun bubbleSort(input: List<Int>): List<Int> {
    val result = input.toMutableList()
    for (end in result.lastIndex downTo 1) {
        for (index in 0 until end) {
            if (result[index] > result[index + 1]) {
                val temp = result[index]
                result[index] = result[index + 1]
                result[index + 1] = temp
            }
        }
    }
    return result
}

internal fun quickSort(input: List<Int>): List<Int> = input.sorted()

internal fun insertionSort(input: List<Int>): List<Int> {
    val result = input.toMutableList()
    for (index in 1 until result.size) {
        val key = result[index]
        var position = index - 1
        while (position >= 0 && result[position] > key) {
            result[position + 1] = result[position]
            position--
        }
        result[position + 1] = key
    }
    return result
}

internal fun selectionSort(input: List<Int>): List<Int> {
    val result = input.toMutableList()
    for (index in result.indices) {
        val minimumIndex = (index until result.size).minByOrNull { result[it] } ?: index
        val temp = result[index]
        result[index] = result[minimumIndex]
        result[minimumIndex] = temp
    }
    return result
}