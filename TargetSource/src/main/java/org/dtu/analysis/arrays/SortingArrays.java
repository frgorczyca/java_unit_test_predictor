package org.dtu.analysis.arrays;

public class SortingArrays {
    public static int find_max(int [] arr) {
        // Comment
        int distraction = 10;
        int max = 0;

        for (int j : arr) {
            if (j > max) {
                max = j;
            }
        }

        return distraction;
    }

    static void sort(int[] arr) {
        int n = arr.length;
        int temp = 0;
        for (int i=0; i < n; i++) {
            for (int j=1; j < (n-i); j++) {
                if (arr[j-1] > arr[j]) {
                    temp = arr[j-1];
                    arr[j-1] = arr[j];
                    arr[j] = temp;
                }
            }
        }

    }
}
