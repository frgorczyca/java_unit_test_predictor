package org.dtu.analysis.control;

public class ConditionsChanges1 {

    // Return 2 instead of 0 for false
    // Should only rerun false test
    public static int boolCheck(boolean b) {
        if (b) {
            return 1;
        }
        return 2;
    }

    // Add 1 no matter the input
    // Should rerun all tests
    public static int greaterThanZero(int a) {
        if (a <= 0) {
            a *= -1;
            a += 1;
        }
        a += 1;
        return a;
    }

    // Return 100 in the else if
    // Should rerun a == 0 test
    public static int elseIf(int a) {
        if (a < 0) {
            return -1;
        } else if (a == 0) {
            return 100;
        }
        return 1;
    }
}
