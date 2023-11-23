package org.dtu.analysis.control;

public class Conditions {

    public static int boolCheck(boolean b) {
        if (b) {
            return 1;
        }
        return 0;
    }

    public static int greaterThanZero(int a) {
        if (a <= 0) {
            a *= -1;
            a += 1;
        }
        return a;
    }

    public static int elseIf(int a) {
        if (a < 0) {
            return -1;
        } else if (a == 0) {
            return 0;
        }
        return 1;
    }
}
