package org.arrays;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SortingArraysTest {

    int [] test_arr = {5,10,6,4,1,3,7,8,9,2};
    @Test
    void find_max() {
        assertEquals(10, SortingArrays.find_max(test_arr));
    }

    @Test
    void sort() {
        SortingArrays.sort(test_arr);
        assertEquals(1, test_arr[0]);
        assertEquals(10, test_arr[test_arr.length-1]);
    }
}