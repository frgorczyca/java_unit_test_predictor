package org.dtu.analysis.overloads;

import static org.junit.jupiter.api.Assertions.*;

class OverloadTest {


    void test() {
        Overload.overloadStatic();
        Overload.overloadStatic(0);
        Overload<Double> overload = new Overload<>();
        overload.overloadMethod();
        overload.overloadMethod(0);
        overload.overloadMethod(Integer.valueOf(0));
        overload.overloadMethod(0.0);
        Overload<Integer> overload1 = new Overload<>();
        //overload1.overloadMethod(Integer.valueOf(1)); // we cannot actually call this lol
    }
}