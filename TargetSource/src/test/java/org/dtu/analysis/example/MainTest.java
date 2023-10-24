package org.dtu.analysis.example;

import org.dtu.analysis.example.Main;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class MainTest {

    @Test
    void addSimple() {
        assertEquals(3, Main.add(1, 2));
    }

    @Test
    void addMinus() {
        assertEquals(-10, Main.add(10, -20));
    }
}