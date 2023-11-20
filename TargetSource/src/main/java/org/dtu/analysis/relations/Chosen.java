package org.dtu.analysis.relations;

public class Chosen {
    public static int GetA() {
        return 1;
    }

    public static int GetB() {
        return 2;
    }

    public static int GetC() {
        int p = 0;
        for (int i = 0; i < 100000; i++) {
            for(int j = 0; j < 100000; j++ ) {
                p += j % 4;
            }
        }
        return p;
    }

    public static int GetD() {
        return 4;
    }

    public static int GetE() {
        return 5;
    }

    public static int IfElse(boolean get) {
        if (get) {
            return GetA();
        } else {
            return GetB();
        }
    }

    public static int NestedCall() {
        return SumTwo(0, 1) + GetE();
    }

    public static int SumAB() {
        return GetA() + GetB();
    }

    public static int SumAC() {
        return GetA() + GetC();
    }

    public static int SumBD() {
        return GetB() + GetD();
    }

    public static int SumDE() {
        return GetD() + GetE();
    }

    public static int SumEE() {
        return GetE() + GetE();
    }

    public static int SumTwo(int first, int second) {
        int a = GetValue(first);
        int b = GetValue(second);
        return a + b;
    }

    private static int GetValue(int val) {
        return switch (val) {
            case 0 -> GetA();
            case 1 -> GetB();
            case 2 -> GetC();
            case 3 -> GetD();
            case 4 -> GetE();
            default -> -1;
        };
    }
}
