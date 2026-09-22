package com.example.sortowanie

import org.junit.Assert.assertEquals
import org.junit.Test

class SortAlgorithmsTest {
    private val input = listOf(5, -1, 5, 0, -10, 3, 0)
    private val expected = listOf(-10, -1, 0, 0, 3, 5, 5)

    @Test
    fun every_algorithm_sorts_the_same_values() {
        val algorithms = listOf(::bubbleSort, ::quickSort, ::insertionSort, ::selectionSort)

        algorithms.forEach { algorithm ->
            assertEquals(expected, algorithm(input))
        }
    }

    @Test
    fun algorithms_do_not_mutate_the_input() {
        val original = input.toList()

        bubbleSort(input)
        quickSort(input)
        insertionSort(input)
        selectionSort(input)

        assertEquals(original, input)
    }
}