package org.dtu.analysis.control;

public class ConditionsChanges3 {

    // No change
    public static int boolCheck(boolean b) {
        if (b) {
            return 1;
        }
        return 0;
    }

    // Use >= instead of <=
    // Should rerun tests where a is not 0
    public static int greaterThanZero(int a) {
        if (a >= 0) {
            a *= -1;
            a += 1;
        }
        return a;
    }

    // Return 1 in if and -1 in else if
    // Should rerun all tests where a != 0
    public static int elseIf(int a) {
        if (a < 0) {
            return 1;
        } else if (a == 0) {
            return 0;
        }
        return -1;
    }
}
