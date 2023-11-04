package org.dtu.analysis.arrays;

// This might be considered as modification

public class NaiveArrays {

    int a = 11;

    public static int sum_elements(int [] arr) {
        int sum = 0;

        for (int i : arr) {
            sum += i;
        }
        return sum;
    }

    private static int add(int a, int b) {
        return a+b;
    }
    public static int [] sum_two(int [] a, int [] b){

        if (a.length != b.length) {
            return null;
        }

        int [] sum = new int [a.length];

        for (int i = 0; i < sum.length; i++) {
            sum[i] = add(a[i], b[i]);
        }

        return sum;
    }
}
