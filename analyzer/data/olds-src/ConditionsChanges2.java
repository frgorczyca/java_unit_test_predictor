package org.dtu.analysis.controlChanges2;

public class ConditionsChanges2 {

    // Return 2 instead of 1 for true
    // Should only rerun true test
    public static int boolCheck(boolean b) {
        if (b) {
            return 2;
        }
        return 0;
    }

    // Return 1 for all positive numbers
    // Should rerun tests where a is positive
    public static int greaterThanZero(int a) {
        if (a <= 0) {
            a *= -1;
            a += 1;
        } else {
            return 1;
        }
        return a;
    }

    // Return 500 in the else case
    // Should rerun a > 0 tests
    public static int elseIf(int a) {
        if (a < 0) {
            return -1;
        } else if (a == 0) {
            return 0;
        }
        return 500;
    }
}
