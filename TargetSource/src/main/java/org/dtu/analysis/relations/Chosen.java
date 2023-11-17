package org.dtu.analysis.relations;

public class Chosen {
    public static int GetA() {
        return 1;
    }

    public static int GetB() {
        return 2;
    }

    public static int GetC() {
        return 3;
    }

    public static int GetD() {
        return 4;
    }

    public static int GetE() {
        return 5;
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
