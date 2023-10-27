package org.dtu.analysis.control;

public class Loops {

    public static int stopAtPoint(int a) {
        int b = 0;
        for (int i = 0; i < a; i++) {
            if (i > 5) {
                break;
            }
            b += 1;
        }
        return b;
    }

    public static int innerLoop(int a) {
        int c = 0;
        for (int i = 0; i < a; i++) {
            for (int j = 9; j < a; j++) {
                c += 1;
            }
        }
        return c;
    }
}
