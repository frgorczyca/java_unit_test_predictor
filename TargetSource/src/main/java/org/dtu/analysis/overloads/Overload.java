package org.dtu.analysis.overloads;

public class Overload<T> {
    public Overload() {

    }

    public Overload(int a) {

    }

    public void overloadMethod() {

    }

    public void overloadMethod(int a) {

    }

    public void overloadMethod(double a) {

    }

    public void overloadMethod(boolean a) {

    }

    // legal
    public void overloadMethod(Integer a) {

    }

    public Integer overloadMethod(Integer a, Integer b) {
        return 0;
    }

    // this is actually legal somehow
    public T overloadMethod(T x) {
        return x;
    }

    public static void overloadStatic() {

    }

    public static void overloadStatic(int a) {

    }
}
