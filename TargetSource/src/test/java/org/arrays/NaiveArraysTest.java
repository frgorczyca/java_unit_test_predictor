package org.arrays;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class NaiveArraysTest {

    int [] test_arr = {1,2,3,4,5,6,7,8,9,10};
    @Test
    void find_max() {
        assertEquals(10, NaiveArrays.find_max(test_arr));
    }

    @Test
    void sum_elements() {
        assertEquals(55, NaiveArrays.sum_elements(test_arr));
    }

    @Test
    void sum_two() {
        int [] res = NaiveArrays.sum_two(test_arr, test_arr);

        if (res != null) {
            for (int i=0; i < test_arr.length; i++) {
                assertEquals(test_arr[i]*2, res[i]);
            }
        }
    }
}