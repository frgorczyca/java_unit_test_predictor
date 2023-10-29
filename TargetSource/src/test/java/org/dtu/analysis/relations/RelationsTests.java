package org.dtu.analysis.relations;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class RelationsTests {

    @Test
    void BasicClass_SetsAndReturnsId () {
        Basic b = new Basic();

        int id = 4;
        b.SetId(id);

        assertEquals(b.GetId(), id);
    }

    @Test
    void Offspring_SetsAndReturnsOffsetId () {
        int offset = 7;

        Offspring o = new Offspring(offset);

        int id = 5;
        o.SetId(id);

        assertEquals(o.GetOffsetId(),id + offset);
    }

    @Test
    void Composed_ReturnsIdSum() {
        Basic b = new Basic();

        int basicId = 4;
        b.SetId(basicId);

        int offset = 7;

        Offspring o = new Offspring(offset);

        int offspringId = 5;
        o.SetId(offspringId);

        Composed c = new Composed(b, o);

        assertEquals(c.GetIdSum(), basicId+offspringId+offset);
    }

    @Test
    void Composed_ReturnsLabel() {
        Basic b = new Basic();
        Offspring o = new Offspring(1);
        Composed c = new Composed(b, o);

        assertEquals(c.GetLabel(), BaseMapping.L1.label);
    }

    @Test
    void Overrider_ReturnsLabel() {
        Basic b = new Basic();
        Offspring o = new Offspring(1);

        Overrider ov = new Overrider(b, o);

        assertEquals(ov.GetLabel(), BaseMapping.L3.label);
    }

    @Test
    void Invoker_InvokeBasic_SetsCorrectValues() {
        Basic b = new Basic();

        int basicId = 4;
        b.SetId(basicId);

        Invoker inv = new Invoker();
        inv.InvokeBasic(b);
        assertEquals(inv.number, basicId);
    }

    @Test
    void Invoker_InvokeOffspring_SetsCorrectValues() {
        int offset = 7;

        Offspring o = new Offspring(offset);

        int id = 5;
        o.SetId(id);

        Invoker inv = new Invoker();
        inv.InvokeOffspring(o);
        assertEquals(inv.number, id+offset);
    }

    @Test
    void Invoker_InvokeComposed_SetsCorrectValues() {
        Basic b = new Basic();

        int basicId = 10;
        b.SetId(basicId);

        int offset = 33;

        Offspring o = new Offspring(offset);

        int offspringId = 0;
        o.SetId(offspringId);

        Composed c = new Composed(b, o);

        Invoker inv = new Invoker();
        inv.InvokeComposed(c);
        assertEquals(inv.number, basicId+offspringId+offset);
        assertEquals(inv.label, BaseMapping.L1.label);
    }

    @Test
    void Invoker_InvokeOverrider_SetsCorrectValues() {
        Basic b = new Basic();

        int basicId = 70;
        b.SetId(basicId);

        int offset = 44;

        Offspring o = new Offspring(offset);

        int offspringId = 0;
        o.SetId(offspringId);

        Overrider ov = new Overrider(b, o);

        Invoker inv = new Invoker();
        inv.InvokeOverrider(ov);
        assertEquals(inv.number, basicId+offspringId+offset);
        assertEquals(inv.label, BaseMapping.L3.label);
    }

}
